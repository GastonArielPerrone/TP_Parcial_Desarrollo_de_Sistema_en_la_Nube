from apps.libros.views import lista_libros
from django.urls import path

urlpatterns = [
    path('stock/', lista_libros,name='lista_libros')
]