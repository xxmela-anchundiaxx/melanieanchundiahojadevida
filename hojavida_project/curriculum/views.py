from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, FileResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
from reportlab.lib import colors
from .models import DatosPersonales
from django.conf import settings
import os
from PIL import Image as PILImage
from io import BytesIO
import mimetypes

def hoja_vida(request, idperfil=1):
    perfil = get_object_or_404(
        DatosPersonales,
        idperfil=idperfil,
        perfilactivo=1
    )

    context = {
        'perfil': perfil
    }

    return render(request, 'hoja_vida_completa.html', context)

def descargar_pdf(request, idperfil=1):
    """Descargar la hoja de vida en formato PDF"""
    perfil = get_object_or_404(
        DatosPersonales,
        idperfil=idperfil,
        perfilactivo=1
    )

    # Crear respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Hoja_Vida_{perfil.nombres}_{perfil.apellidos}.pdf"'

    # Crear documento PDF
    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=6,
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        spaceAfter=12,
        alignment=1
    )

    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.whitesmoke,
        backColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        leftIndent=6,
        rightIndent=6,
        topPadding=6,
        bottomPadding=6
    )

    # Incluir imagen de perfil en PDF si existe
    if getattr(perfil, 'foto_perfil') and perfil.foto_perfil.name:
        ruta_imagen = os.path.join(settings.MEDIA_ROOT, perfil.foto_perfil.name)
        if os.path.exists(ruta_imagen):
            try:
                # Redimensionar imagen para PDF si es muy grande
                img = PILImage.open(ruta_imagen)
                if img.width > 400 or img.height > 400:
                    img.thumbnail((400, 400), PILImage.Resampling.LANCZOS)
                    img_bytes = BytesIO()
                    img.save(img_bytes, format='PNG')
                    img_bytes.seek(0)
                    rl_img = RLImage(img_bytes, width=1.5*inch, height=1.5*inch)
                else:
                    rl_img = RLImage(ruta_imagen, width=1.5*inch, height=1.5*inch)
                rl_img.hAlign = 'CENTER'
                story.append(rl_img)
                story.append(Spacer(1, 0.1*inch))
            except Exception as e:
                print(f"Error cargando imagen: {e}")
                # Si falla, continuar sin ella
                pass

    # Encabezado (texto)
    story.append(Paragraph(f"{perfil.nombres} {perfil.apellidos}", title_style))
    story.append(Paragraph(perfil.descripcionperfil or "Mi Perfil Profesional", subtitle_style))
    story.append(Spacer(1, 0.2*inch))

    # Información Personal
    info_data = [
        [f"<b>Cédula:</b> {perfil.numerocedula}", f"<b>Estado Civil:</b> {perfil.estadocivil or 'N/A'}"],
        [f"<b>Nacionalidad:</b> {perfil.nacionalidad or 'N/A'}", f"<b>Teléfono:</b> {perfil.telefonofijo or 'N/A'}"],
        [f"<b>Lugar de Nacimiento:</b> {perfil.lugarnacimiento or 'N/A'}", f"<b>Dirección:</b> {perfil.direcciondomiciliaria or 'N/A'}"],
        [f"<b>Fecha de Nacimiento:</b> {perfil.fechanacimiento.strftime('%d/%m/%Y') if perfil.fechanacimiento else 'N/A'}", f"<b>Sexo:</b> {'Mujer' if perfil.sexo == 'M' else 'Hombre'}"],
    ]
    
    info_table = Table(info_data, colWidths=[3.25*inch, 3.25*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))

    # EXPERIENCIA LABORAL
    if perfil.mostrar_experiencia and perfil.experiencias.exists():
        story.append(Paragraph("EXPERIENCIA LABORAL", section_style))
        for exp in perfil.experiencias.filter(activarparaqueseveaenfront=True):
            exp_text = f"<b>{exp.cargodesempenado}</b> - {exp.nombrempresa}"
            story.append(Paragraph(exp_text, styles['Heading3']))
            if exp.descripcionfunciones:
                story.append(Paragraph(exp.descripcionfunciones, styles['BodyText']))
            story.append(Spacer(1, 0.1*inch))

    # CURSOS
    if perfil.mostrar_cursos and perfil.cursos.exists():
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("CURSOS Y CAPACITACIONES", section_style))
        for curso in perfil.cursos.filter(activarparaqueseveaenfront=True):
            curso_text = f"<b>{curso.nombrecurso}</b> - {curso.entidadpatrocinadora}"
            story.append(Paragraph(curso_text, styles['Heading3']))
            if curso.descripcioncurso:
                story.append(Paragraph(curso.descripcioncurso, styles['BodyText']))
            story.append(Spacer(1, 0.1*inch))

    # RECONOCIMIENTOS
    if perfil.mostrar_reconocimientos and perfil.reconocimientos.exists():
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("RECONOCIMIENTOS Y PREMIOS", section_style))
        for rec in perfil.reconocimientos.filter(activarparaqueseveaenfront=True):
            rec_text = f"<b>{rec.descripcionreconocimiento}</b> - {rec.tiporeconocimiento}"
            story.append(Paragraph(rec_text, styles['Heading3']))
            if rec.entidadpatrocinadora:
                story.append(Paragraph(f"Otorgado por: {rec.entidadpatrocinadora}", styles['BodyText']))
            story.append(Spacer(1, 0.1*inch))

    # PRODUCTOS ACADÉMICOS
    if perfil.mostrar_productos_academicos and perfil.productos_academicos.exists():
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("PRODUCTOS ACADÉMICOS", section_style))
        for prod in perfil.productos_academicos.filter(activarparaqueseveaenfront=True):
            prod_text = f"<b>{prod.nombrerecurso}</b> - {prod.clasificador}"
            story.append(Paragraph(prod_text, styles['Heading3']))
            if prod.descripcion:
                story.append(Paragraph(prod.descripcion, styles['BodyText']))
            story.append(Spacer(1, 0.1*inch))

    # PRODUCTOS LABORALES
    if perfil.mostrar_productos_laborales and perfil.productos_laborales.exists():
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("PRODUCTOS LABORALES", section_style))
        for prod in perfil.productos_laborales.filter(activarparaqueseveaenfront=True):
            prod_text = f"<b>{prod.nombreproducto}</b>"
            story.append(Paragraph(prod_text, styles['Heading3']))
            if prod.descripcion:
                story.append(Paragraph(prod.descripcion, styles['BodyText']))
            story.append(Spacer(1, 0.1*inch))

    # Construir PDF
    doc.build(story)
    return response

def perfil(request):
    perfil = get_object_or_404(DatosPersonales, perfilactivo=1)
    context = {'perfil': perfil}
    return render(request, 'perfil.html', context)

def experiencia(request):
    perfil = get_object_or_404(DatosPersonales, perfilactivo=1)
    context = {'perfil': perfil}
    return render(request, 'experiencia.html', context)

def cursos(request):
    perfil = get_object_or_404(DatosPersonales, perfilactivo=1)
    context = {'perfil': perfil}
    return render(request, 'cursos.html', context)

def productos_academicos(request):
    perfil = get_object_or_404(DatosPersonales, perfilactivo=1)
    context = {'perfil': perfil}
    return render(request, 'productos_academicos.html', context)

def productos_laborales(request):
    perfil = get_object_or_404(DatosPersonales, perfilactivo=1)
    context = {'perfil': perfil}
    return render(request, 'productos_laborales.html', context)

def reconocimientos(request):
    perfil = get_object_or_404(DatosPersonales, perfilactivo=1)
    context = {'perfil': perfil}
    return render(request, 'reconocimientos.html', context)

def venta_garage(request):
    perfil = get_object_or_404(DatosPersonales, perfilactivo=1)
    context = {'perfil': perfil}
    return render(request, 'venta_garage.html', context)

def servir_foto(request, filename):
    """Sirve fotos de perfil directamente"""
    # Construir ruta segura
    ruta_foto = os.path.join(settings.MEDIA_ROOT, 'fotos_perfil', filename)
    
    # Validar que el archivo existe y está en la carpeta correcta
    base_dir = os.path.join(settings.MEDIA_ROOT, 'fotos_perfil')
    ruta_real = os.path.realpath(ruta_foto)
    base_real = os.path.realpath(base_dir)
    
    if not ruta_real.startswith(base_real) or not os.path.exists(ruta_real):
        return HttpResponse("No encontrado", status=404)
    
    # Servir archivo
    try:
        mime_type, _ = mimetypes.guess_type(ruta_real)
        with open(ruta_real, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mime_type or 'image/jpeg')
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(ruta_foto)}"'
            response['Cache-Control'] = 'public, max-age=3600'
            return response
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)

def servir_imagen(request, carpeta, filename):
    """Sirve imágenes de cualquier carpeta (fotos_perfil, ventas_garage, certificados/*, etc)"""
    # Solo permitir carpetas específicas por seguridad
    # Permitir rutas con subcarpetas como certificados/experiencia
    carpetas_permitidas = [
        'fotos_perfil', 
        'ventas_garage',
        'certificados/experiencia',
        'certificados/cursos',
        'certificados/reconocimientos'
    ]
    
    if carpeta not in carpetas_permitidas:
        return HttpResponse("Acceso denegado", status=403)
    
    # Construir ruta segura
    ruta_imagen = os.path.join(settings.MEDIA_ROOT, carpeta, filename)
    
    # Validar que el archivo está en la carpeta correcta (evitar path traversal)
    base_dir = os.path.join(settings.MEDIA_ROOT, carpeta)
    ruta_real = os.path.realpath(ruta_imagen)
    base_real = os.path.realpath(base_dir)
    
    if not ruta_real.startswith(base_real) or not os.path.exists(ruta_real):
        return HttpResponse("No encontrado", status=404)
    
    # Servir archivo
    try:
        mime_type, _ = mimetypes.guess_type(ruta_real)
        # Para PDFs y documentos, permitir inline o descargar según el tipo
        with open(ruta_real, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mime_type or 'application/octet-stream')
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(ruta_imagen)}"'
            response['Cache-Control'] = 'public, max-age=3600'
            return response
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)