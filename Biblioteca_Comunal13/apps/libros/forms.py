from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'editorial', 'categoria', 'fecha_publicacion', 'cantidad']
        widgets = {
            'fecha_publicacion': forms.DateInput(attrs={'type': 'date'}),
        }

class FiltroLibroForm(forms.Form):
    q = forms.CharField(label='Buscar', required=False)
    titulo = forms.CharField(label='Título', required=False)
    autor = forms.CharField(label='Autor', required=False)
    editorial = forms.CharField(label='Editorial', required=False)
    categoria = forms.CharField(label='Categoría', required=False)
