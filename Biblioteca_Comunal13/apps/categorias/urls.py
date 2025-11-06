from apps.categorias.views import lista_categorias
from django.urls import path

urlpatterns = [
    path('lista/', lista_categorias, name='lista_categorias')
]