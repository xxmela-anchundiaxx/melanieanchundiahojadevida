from django.contrib import admin
from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimientos,
    CursosRealizados,
    ProductosAcademicos,
    ProductosLaborales,
    VentaGarage,
)


@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'numerocedula', 'nacionalidad', 'perfilactivo')
    search_fields = ('nombres', 'apellidos', 'numerocedula')
    list_filter = ('nacionalidad', 'estadocivil', 'sexo', 'perfilactivo')
    readonly_fields = ('numerocedula',)  # Solo cédula protegida
    fieldsets = (
        ('Información Personal', {
            'fields': ('descripcionperfil', 'nombres', 'apellidos', 'foto_perfil', 'numerocedula', 'sexo', 'nacionalidad', 'lugarnacimiento', 'fechanacimiento')
        }),
        ('Contacto', {
            'fields': ('telefonofijo', 'telefonoconvencional', 'direcciondomiciliaria', 'direcciontrabajo', 'sitioweb')
        }),
        ('Estado Civil y Documentos', {
            'fields': ('estadocivil', 'licenciaconducir')
        }),
        ('Visibilidad en Frontend', {
            'fields': ('mostrar_experiencia', 'mostrar_reconocimientos', 'mostrar_cursos', 'mostrar_productos_academicos', 'mostrar_productos_laborales', 'mostrar_venta_garage')
        }),
        ('Impresión en PDF', {
            'fields': ('imprimir_experiencia', 'imprimir_reconocimientos', 'imprimir_cursos', 'imprimir_productos_academicos', 'imprimir_productos_laborales', 'imprimir_venta_garage')
        }),
        ('Estado del Perfil', {
            'fields': ('perfilactivo',)
        }),
    )


@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'fechafingestion', 'activarparaqueseveaenfront')
    search_fields = ('cargodesempenado', 'nombrempresa')
    list_filter = ('fechainiciogestion', 'activarparaqueseveaenfront')
    fieldsets = (
        ('Información General', {
            'fields': ('idperfilconqueestaactivo', 'cargodesempenado', 'nombrempresa', 'lugarempresa')
        }),
        ('Fechas', {
            'fields': ('fechainiciogestion', 'fechafingestion')
        }),
        ('Contacto Empresa', {
            'fields': ('emailempresa', 'sitiowebempresa', 'nombrecontactoempresarial', 'telefonocontactoempresarial')
        }),
        ('Descripción y Archivos', {
            'fields': ('descripcionfunciones', 'rutacertificado')
        }),
        ('Visibilidad', {
            'fields': ('activarparaqueseveaenfront',)
        }),
    )


@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    list_display = ('descripcionreconocimiento', 'tiporeconocimiento', 'fechareconocimiento', 'activarparaqueseveaenfront')
    search_fields = ('descripcionreconocimiento', 'entidadpatrocinadora')
    list_filter = ('tiporeconocimiento', 'fechareconocimiento', 'activarparaqueseveaenfront')
    fieldsets = (
        ('Información General', {
            'fields': ('idperfilconqueestaactivo', 'descripcionreconocimiento', 'tiporeconocimiento')
        }),
        ('Detalles', {
            'fields': ('fechareconocimiento', 'entidadpatrocinadora')
        }),
        ('Contacto', {
            'fields': ('nombrecontactoauspicia', 'telefonocontactoauspicia')
        }),
        ('Archivos', {
            'fields': ('rutacertificado',)
        }),
        ('Visibilidad', {
            'fields': ('activarparaqueseveaenfront',)
        }),
    )


@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    list_display = ('nombrecurso', 'entidadpatrocinadora', 'fechainicio', 'fechafin', 'totalhoras', 'activarparaqueseveaenfront')
    search_fields = ('nombrecurso', 'entidadpatrocinadora')
    list_filter = ('fechainicio', 'entidadpatrocinadora', 'activarparaqueseveaenfront')
    fieldsets = (
        ('Información General', {
            'fields': ('idperfilconqueestaactivo', 'nombrecurso', 'entidadpatrocinadora')
        }),
        ('Fechas y Duración', {
            'fields': ('fechainicio', 'fechafin', 'totalhoras')
        }),
        ('Descripción', {
            'fields': ('descripcioncurso',)
        }),
        ('Contacto', {
            'fields': ('nombrecontactoauspicia', 'telefonocontactoauspicia', 'emailempresapatrocinadora')
        }),
        ('Archivos', {
            'fields': ('rutacertificado',)
        }),
        ('Visibilidad', {
            'fields': ('activarparaqueseveaenfront',)
        }),
    )


@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador', 'fecha_registro', 'activarparaqueseveaenfront')
    search_fields = ('nombrerecurso', 'clasificador')
    list_filter = ('clasificador', 'fecha_registro', 'activarparaqueseveaenfront')
    fieldsets = (
        ('Información General', {
            'fields': ('idperfilconqueestaactivo', 'nombrerecurso', 'clasificador')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'fecha_registro')
        }),
        ('Enlaces y Archivos', {
            'fields': ('link', 'archivo')
        }),
        ('Visibilidad', {
            'fields': ('activarparaqueseveaenfront',)
        }),
    )


@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'fechaproducto', 'activarparaqueseveaenfront')
    search_fields = ('nombreproducto',)
    list_filter = ('fechaproducto', 'activarparaqueseveaenfront')
    fieldsets = (
        ('Información General', {
            'fields': ('idperfilconqueestaactivo', 'nombreproducto', 'fechaproducto')
        }),
        ('Descripción', {
            'fields': ('descripcion',)
        }),
        ('Enlaces y Archivos', {
            'fields': ('link', 'archivo')
        }),
        ('Visibilidad', {
            'fields': ('activarparaqueseveaenfront',)
        }),
    )


@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'estadoproducto', 'valordelbien', 'fecha_publicacion', 'activarparaqueseveaenfront')
    search_fields = ('nombreproducto',)
    list_filter = ('estadoproducto', 'fecha_publicacion', 'activarparaqueseveaenfront')
    readonly_fields = ('fecha_publicacion',)
    fieldsets = (
        ('Información del Producto', {
            'fields': ('idperfilconqueestaactivo', 'nombreproducto', 'estadoproducto', 'valordelbien')
        }),
        ('Descripción e Imagen', {
            'fields': ('descripcion', 'imagen_producto')
        }),
        ('Fechas', {
            'fields': ('fecha_publicacion',)
        }),
        ('Visibilidad', {
            'fields': ('activarparaqueseveaenfront',)
        }),
    )

