from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .models import Usuario
from .forms import UsuarioForm, RegistrationForm, FiltroUsuarioForm
from django.db.models import Q

@login_required
def lista_usuarios(request):
    filtro_form = FiltroUsuarioForm(request.GET or None)
    usuarios = Usuario.objects.all()

    if filtro_form.is_valid():
        query = filtro_form.cleaned_data.get("q")
        nombre_usuario = filtro_form.cleaned_data.get("nombre_usuario")
        dni = filtro_form.cleaned_data.get("dni")

        if query:
            q_obj = Q(nombre_usuario__icontains=query) | Q(dni__icontains=query)
            usuarios = usuarios.filter(q_obj)

        if nombre_usuario:
            usuarios = usuarios.filter(nombre_usuario__icontains=nombre_usuario)

        if dni:
            usuarios = usuarios.filter(dni__icontains=dni)

    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            Usuario.objects.create(
                nombre_usuario=form.cleaned_data['nombre_usuario'],
                dni=form.cleaned_data['dni'],
                telefono=form.cleaned_data['telefono'],
                calle=form.cleaned_data['calle'],
                numero_calle=form.cleaned_data['numero_calle'],
                casa=form.cleaned_data['casa'],
                edificio=form.cleaned_data['edificio'],
                piso=form.cleaned_data['piso'],
                departamento_numero_casa=form.cleaned_data['departamento_numero_casa']
            )
            return redirect('lista_usuarios')

    return render(request, 'usuarios.html', {
        'usuarios': usuarios,
        'form': form,
        'filtro_form': filtro_form
    })

@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return render(request, 'usuarios.html', {'usuarios': Usuario.objects.all()})
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required
def editar_usuario_modal(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UsuarioForm(instance=usuario)
        html = render_to_string('editar_modal_form.html', {
            'form': form,
            'usuario': usuario
        }, request=request)
        return HttpResponse(html)

@login_required
def register_usuario(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Crear el usuario manualmente
            Usuario.objects.create(
                nombre_usuario=form.cleaned_data['nombre_usuario'],
                dni=form.cleaned_data['dni'],
                telefono=form.cleaned_data['telefono'],
                calle=form.cleaned_data['calle'],
                numero_calle=form.cleaned_data['numero_calle'],
                casa=form.cleaned_data['casa'],
                edificio=form.cleaned_data['edificio'],
                piso=form.cleaned_data['piso'],
                departamento_numero_casa=form.cleaned_data['departamento_numero_casa']
            )
            return redirect('lista_usuarios')
    else:
        form = RegistrationForm()
    return render(request, 'usuarios.html', {'form': form})