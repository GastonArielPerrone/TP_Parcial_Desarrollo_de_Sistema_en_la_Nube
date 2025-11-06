from django.contrib import admin

from apps.editoriales.models import Editorial

@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    # usa los nombres exactos de los campos de tu modelo
    list_display = (
        'id',
        'nombre',
        'pais',
        'calle',
        'numero_calle',
        'tipo_ubicacion',  # columna calculada (ver método abajo)
        'piso',
        'departamento',
        'created_at',
        'updated_at',
    )

    search_fields = ('nombre', 'pais', 'calle')
    list_filter = ('pais', 'casa', 'edificio', 'created_at')

    # columna calculada que combina casa/edificio y muestra algo legible
    def tipo_ubicacion(self, obj):
        partes = []
        if getattr(obj, 'casa', False):
            partes.append('Casa')
        if getattr(obj, 'edificio', False):
            partes.append('Edificio')
        if not partes:
            partes.append('—')
        return " / ".join(partes)
    tipo_ubicacion.short_description = 'Tipo de ubicación'
    tipo_ubicacion.admin_order_field = 'casa'  # opcional: ordena por este campo
