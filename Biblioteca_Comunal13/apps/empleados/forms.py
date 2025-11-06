from django import forms
from apps.empleados.models import Empleado


class RegistrationForm(forms.Form):
    dni = forms.CharField(max_length=20, label="DNI")
    nombre = forms.CharField(max_length=150, required=False, label="Nombre")
    apellido = forms.CharField(max_length=150, label="Apellido")
    email = forms.EmailField(required=False, label="E-mail")
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono")
    cargo = forms.CharField(max_length=100, label="Cargo")
    is_staff = forms.BooleanField(required=False, initial=False, label="Staff Administrativo")
    is_active = forms.BooleanField(required=False, initial=False, label="Empleado Activo")
    fecha_contratacion = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de contratación")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni:
            dni = str(dni).strip()
            if Empleado.objects.filter(dni=dni).exists():
                raise forms.ValidationError("Ya existe un empleado con ese DNI")
        return dni

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirm = cleaned.get('confirm_password')
        if password and confirm and password != confirm:
            self.add_error('confirm_password', 'Las contraseñas no coinciden')
        return cleaned

class FiltroEmpleadoForm(forms.Form):
    q = forms.CharField(label='Buscar', required=False)
    dni = forms.CharField(label='DNI', required=False)
    nombre = forms.CharField(label='Nombre', required=False)
    apellido = forms.CharField(label='Apellido', required=False)
