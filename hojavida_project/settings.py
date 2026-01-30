# Shim settings to make `hojavida_project.settings` importable when Render
# runs with a different working directory or prefixes the package name.
# This simply re-exports the real settings from the inner package.
from .hojavida_project.settings import *  # noqa
