from django.contrib import admin
from apps.autores.models import Autor

# Register your models here.
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "nacionalidad")
    search_fields = ("nombre", "nacionalidad")
    list_filter = ("nacionalidad",)