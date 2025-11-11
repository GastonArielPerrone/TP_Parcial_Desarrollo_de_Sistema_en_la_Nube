from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
from .forms import RegistrationForm, FiltroEmpleadoForm
from apps.empleados.models import Empleado, EmpleadoManager
from typing import cast
from django.db.models import Q
from django.db import IntegrityError
import logging

# Para LDAP
from ldap3 import Server, Connection, ALL, NTLM, core

logger = logging.getLogger(__name__)

# -------------------------
# LOGIN (INDEX)
# -------------------------
def index(request):
    if request.method == "POST":
        dni = request.POST.get('dni')
        password = request.POST.get('password')

        if not dni or not password:
            messages.error(request, "Debes ingresar DNI y contraseña.")
            return render(request, 'index.html', {})

        # Parámetros del servidor LDAP
        LDAP_HOST = getattr(settings, "LDAP_HOST", "192.168.56.101")
        LDAP_DOMAIN = getattr(settings, "LDAP_DOMAIN", "IFTS")
        ldap_user = f"{LDAP_DOMAIN}\\{dni}"

        try:
            # Conectamos al servidor LDAP
            server = Server(LDAP_HOST, get_info=ALL)
            conn = Connection(
                server,
                user=ldap_user,
                password=password,
                authentication=NTLM,
                auto_bind=True
            )

            if conn.bound:
                # Si la conexión es exitosa, creamos o actualizamos el empleado local
                try:
                    empleado, created = Empleado.objects.get_or_create(
                        dni=dni,
                        defaults={
                            'nombre': '',
                            'apellido': '',
                            'email': '',
                            'is_staff': False,
                            'is_active': True,
                        }
                    )
                    empleado.is_active = True
                    empleado.set_unusable_password()
                    empleado.save()

                except IntegrityError as ie:
                    logger.exception("Error al crear/actualizar empleado: %s", ie)
                    messages.error(request, "Error interno al crear el usuario local.")
                    conn.unbind()
                    return render(request, 'index.html', {'error': 'Error interno al crear usuario local'})

                # Autenticamos en Django
                empleado.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, empleado)
                conn.unbind()

                # Redirección post-login
                next_url = request.GET.get('next') or request.POST.get('next') or 'lista_usuarios'
                return redirect(next_url)

            else:
                messages.error(request, "Error al autenticar en Active Directory.")

        except core.exceptions.LDAPBindError as e:
            logger.warning("Credenciales AD inválidas para %s: %s", dni, e)
            messages.error(request, "❌ Credenciales inválidas o usuario deshabilitado en Active Directory.")

        except core.exceptions.LDAPSocketOpenError as e:
            logger.error("No se puede conectar al servidor LDAP: %s", e)
            messages.error(request, "⚠️ No se puede conectar al servidor de Active Directory.")

        except Exception as e:
            logger.exception("Error LDAP inesperado para %s: %s", dni, e)
            messages.error(request, "⚠️ Error inesperado de conexión con Active Directory.")

        return render(request, 'index.html', {})

    # Si es GET, mostramos el formulario vacío
    return render(request, 'index.html', {})


# -------------------------
# REGISTRO DE USUARIOS
# -------------------------
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                cast(EmpleadoManager, Empleado.objects).create_user(
                    dni=data['dni'],
                    password=data['password'],
                    nombre=data.get('nombre', ''),
                    apellido=data.get('apellido', ''),
                    email=data.get('email', ''),
                    telefono=data.get('telefono', ''),
                    cargo=data.get('cargo', ''),
                    is_staff=data.get('is_staff', False),
                    is_active=data.get('is_active', True),
                    fecha_contratacion=data.get('fecha_contratacion', None)
                )
            except Exception as e:
                return render(
                    request,
                    "register.html",
                    {"form": form, "error": f"Error al crear el usuario: {e}"}
                )
            return redirect('index')
        else:
            return render(request, "register.html", {"form": form})
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})


# -------------------------
# LISTA DE EMPLEADOS
# -------------------------
def lista_empleados(request):
    filtro_form = FiltroEmpleadoForm(request.GET or None)
    empleados = Empleado.objects.all()

    if filtro_form.is_valid():
        query = filtro_form.cleaned_data.get("q")
        dni = filtro_form.cleaned_data.get("dni")
        nombre = filtro_form.cleaned_data.get("nombre")
        apellido = filtro_form.cleaned_data.get("apellido")

        if query:
            q_obj = Q(dni__icontains=query) | Q(nombre__icontains=query) | Q(apellido__icontains=query)
            empleados = empleados.filter(q_obj)

        if dni:
            empleados = empleados.filter(dni__icontains=dni)
        if nombre:
            empleados = empleados.filter(nombre__icontains=nombre)
        if apellido:
            empleados = empleados.filter(apellido__icontains=apellido)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                cast(EmpleadoManager, Empleado.objects).create_user(
                    dni=data['dni'],
                    password=data['password'],
                    nombre=data.get('nombre', ''),
                    apellido=data.get('apellido', ''),
                    email=data.get('email', ''),
                    telefono=data.get('telefono', ''),
                    cargo=data.get('cargo', ''),
                    is_staff=data.get('is_staff', False),
                    is_active=data.get('is_active', True),
                    fecha_contratacion=data.get('fecha_contratacion', None)
                )
            except Exception as e:
                return render(
                    request,
                    "empleados.html",
                    {"form": form, "error": f"Error al crear el usuario: {e}"}
                )
            return redirect('lista_empleados')
    else:
        form = RegistrationForm()

    return render(
        request,
        'empleados.html',
        {'form': form, 'empleados': empleados, 'filtro_form': filtro_form}
    )
