from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Empleado

@admin.register(Empleado)
class EmpleadoAdmin(UserAdmin):
    model = Empleado
    list_display = ('dni', 'apellido', 'nombre', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('dni', 'apellido', 'nombre', 'email')
    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('dni', 'password')}),
        ('Datos personales', {'fields': ('nombre', 'apellido', 'email')}),
        ('Permisos', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Fechas', {'fields': ('date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('dni', 'nombre', 'apellido', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )