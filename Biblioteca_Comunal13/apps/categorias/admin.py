from django.contrib import admin
from apps.categorias.models import Categoria

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)
    list_filter = ("nombre",)