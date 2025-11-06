from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class FiltroCategoriaForm(forms.Form):
    q = forms.CharField(label='Buscar', required=False)
    nombre = forms.CharField(label='Nombre', required=False)
