from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class EmpleadoManager(BaseUserManager):
    def create_user(self, dni, password=None, **extra_fields):
        if not dni:
            raise ValueError("El DNI debe ser proporcionado")
        dni = str(dni).strip()
        user = self.model(dni=dni, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(dni, password, **extra_fields)


class Empleado(AbstractBaseUser, PermissionsMixin):
    dni = models.CharField('DNI', max_length=20, unique=True)
    nombre = models.CharField('Nombre', max_length=150, blank=True)
    apellido = models.CharField('Apellido', max_length=150, blank=True)
    email = models.EmailField('Email', blank=True)
    telefono = models.CharField('Teléfono', max_length=20, blank=True)
    cargo = models.CharField('Cargo', max_length=100, blank=True)
    fecha_contratacion = models.DateField('Fecha de contratación', blank=True, null=True)
    is_staff = models.BooleanField('Staff')
    is_active = models.BooleanField('Activo')
    date_joined = models.DateTimeField('Fecha de alta', default=timezone.now)

    objects = EmpleadoManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return f"{self.apellido} {self.nombre}"
