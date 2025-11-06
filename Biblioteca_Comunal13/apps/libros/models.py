from django.db import models
from apps.autores.models import Autor
from apps.editoriales.models import Editorial
from apps.categorias.models import Categoria

class Libro(models.Model):
    titulo = models.CharField(max_length=200, null=False, blank=False, db_column='titulo_libro')
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, null=False, blank=False, db_column='nombre_autor')
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE, null=False, blank=False, db_column='nombre_editorial')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=False, blank=False, db_column='nombre_categoria')
    fecha_publicacion = models.DateField()
    cantidad = models.IntegerField(null=False, blank=False)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.titulo