from django import forms
from .models import Editorial

class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = '__all__'

class FiltroEditorialForm(forms.Form):
    q = forms.CharField(label='Buscar', required=False)
    nombre = forms.CharField(label='Nombre', required=False)
    pais = forms.CharField(label='País', required=False)
