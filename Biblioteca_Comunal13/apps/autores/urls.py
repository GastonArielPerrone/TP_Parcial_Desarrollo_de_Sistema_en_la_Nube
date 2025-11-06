from apps.autores.views import lista_autores, editar_autor_modal
from django.urls import path

urlpatterns = [
    path('lista/', lista_autores, name='lista_autores'),
    path('editar/<int:autor_id>/modal/', editar_autor_modal, name='editar_autor_modal'),
]