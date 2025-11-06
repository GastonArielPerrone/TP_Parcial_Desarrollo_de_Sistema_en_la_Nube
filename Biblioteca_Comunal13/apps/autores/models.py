from django.db import models


class Autor(models.Model):
    # nombre en el modelo: 'nombre' pero conservamos la columna antigua para compatibilidad
    nombre = models.CharField(max_length=100, null=False, blank=False, db_column='nombre_autor')
    nacionalidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre