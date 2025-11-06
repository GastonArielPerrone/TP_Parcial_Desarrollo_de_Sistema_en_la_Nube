from django.contrib import admin

from apps.usuarios.models import Usuario

# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre_usuario",
        "dni",
        "telefono",
        "calle",
        "numero_calle",
        "casa",
        "edificio",
        "piso",
        "departamento_numero_casa",
        "created_at",
        "updated_at",
    )
    search_fields = ("nombre_usuario", "dni", "telefono", "calle")
    list_filter = ("casa", "edificio", "created_at")