from django.db import models
from apps.empleados.models import Empleado
from apps.libros.models import Libro
from apps.usuarios.models import Usuario



class Prestamo(models.Model):
    titulo_libro = models.ForeignKey(Libro, on_delete=models.CASCADE, null=False, blank=False, db_column='libro_id')
    nombre_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False, blank=False, db_column='usuario_id')
    nombre = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=False, blank=False, db_column='empleado_id')
    fecha_prestamo = models.DateField(auto_now_add=True)
    hora_prestamo = models.TimeField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    hora_devolucion = models.TimeField(null=True, blank=True)
    estado = models.CharField(max_length=10, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
