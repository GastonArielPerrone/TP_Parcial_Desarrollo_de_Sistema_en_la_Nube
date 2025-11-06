from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False, db_column='nombre_categoria')

    def __str__(self):
        return self.nombre