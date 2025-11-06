from django.urls import path
from apps.prestamos.views import lista_prestamos, devolver_prestamo

urlpatterns = [
    path('lista/', lista_prestamos, name='lista_prestamos'),
    path('devolver/<int:prestamo_id>/', devolver_prestamo, name='devolver_prestamo'),
]
