
from . import views
from django.urls import path

urlpatterns = [
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('editar/<int:usuario_id>/modal/', views.editar_usuario_modal, name='editar_usuario_modal'),
]
