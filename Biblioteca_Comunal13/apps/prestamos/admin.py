from django.contrib import admin

from apps.prestamos.models import Prestamo

# Register your models here.
@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "titulo_libro",
        "nombre_usuario",
        "nombre",
        "fecha_prestamo",
        "hora_prestamo",
        "fecha_devolucion",
        "hora_devolucion",
        "estado",
        "created_at",
        "updated_at",
    )
    list_filter = ("estado", "fecha_prestamo", "fecha_devolucion")
    search_fields = (
        "titulo_libro__titulo",       # ajustá según el campo real de Libro
        "nombre_usuario__nombre",     # ajustá según el campo real de Usuario
        "nombre_empleado__nombre",    # ajustá según el campo real de Empleado
    )