from django import forms
from apps.prestamos.models import Prestamo

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = [
            'titulo_libro',
            'nombre_usuario',
            'nombre',
        ]

class FiltroPrestamoForm(forms.Form):
    q = forms.CharField(label='Buscar', required=False)
    libro = forms.CharField(label='Libro', required=False)
    usuario = forms.CharField(label='Usuario', required=False)
    estado = forms.CharField(label='Estado', required=False)
