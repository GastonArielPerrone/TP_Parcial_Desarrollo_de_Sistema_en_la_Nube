from django import forms
from .models import Autor

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'nacionalidad']

class FiltroAutorForm(forms.Form):
    q = forms.CharField(label='Búsqueda global', required=False)
    nombre = forms.CharField(label='Nombre', required=False)
    nacionalidad = forms.ChoiceField(label='Nacionalidad', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Obtener todas las nacionalidades distintas de la base de datos
        nacionalidades = Autor.objects.values_list('nacionalidad', flat=True).distinct()

        # Armar las opciones del select (primero una vacía)
        opciones = [('', 'Todas las nacionalidades')] + [(n, n) for n in nacionalidades if n]
        self.fields['nacionalidad'].choices = opciones