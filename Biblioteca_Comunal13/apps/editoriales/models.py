from django.db import models


class Editorial(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False, db_column='nombre_editorial')
    pais = models.CharField(max_length=50, db_column='pais_editorial')
    calle = models.CharField(max_length=100, db_column='calle_editorial', null=True, blank=True)
    numero_calle = models.IntegerField(db_column='numero_calle_editorial', null=True, blank=True)
    casa = models.BooleanField(default=False, db_column='casa_editorial')
    edificio = models.BooleanField(default=False, db_column='edificio_editorial')
    piso = models.CharField(max_length=10, db_column='piso_editorial', null=True, blank=True)
    departamento = models.CharField(max_length=10, db_column='departamento_numero_casa_editorial', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
        