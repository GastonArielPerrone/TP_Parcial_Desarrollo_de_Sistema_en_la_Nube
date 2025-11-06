from django.db import models

class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=100, null=False, blank=False)
    dni = models.CharField(max_length=15, unique=True, null=False, blank=False)
    telefono = models.CharField(max_length=20)
    calle = models.CharField(max_length=100)
    numero_calle = models.IntegerField()
    casa = models.BooleanField(default=False)
    edificio = models.BooleanField(default=False)
    piso = models.CharField(max_length=10, null=True, blank=True)
    departamento_numero_casa = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre_usuario}"