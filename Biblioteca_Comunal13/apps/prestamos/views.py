from django.shortcuts import render, redirect, get_object_or_404
from apps.prestamos.models import Prestamo
from apps.prestamos.forms import PrestamoForm, FiltroPrestamoForm
from apps.libros.models import Libro
from django.utils import timezone
from django.db.models import Q

def lista_prestamos(request):
    filtro_form = FiltroPrestamoForm(request.GET or None)
    prestamos = Prestamo.objects.all()

    if filtro_form.is_valid():
        query = filtro_form.cleaned_data.get("q")
        libro = filtro_form.cleaned_data.get("libro")
        usuario = filtro_form.cleaned_data.get("usuario")
        estado = filtro_form.cleaned_data.get("estado")

        if query:
            q_obj = Q(titulo_libro__titulo__icontains=query) | Q(nombre_usuario__nombre_usuario__icontains=query) | Q(estado__icontains=query)
            prestamos = prestamos.filter(q_obj)

        if libro:
            prestamos = prestamos.filter(titulo_libro__titulo__icontains=libro)

        if usuario:
            prestamos = prestamos.filter(nombre_usuario__nombre_usuario__icontains=usuario)

        if estado:
            prestamos = prestamos.filter(estado__icontains=estado)

    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)
            libro_obj = prestamo.titulo_libro
            if libro_obj.cantidad > 0:
                libro_obj.cantidad -= 1
                libro_obj.save()
                prestamo.save()
                return redirect('lista_prestamos')
            else:
                form.add_error('titulo_libro', 'Libro no está disponible. ☹️')
    else:
        form = PrestamoForm()
    
    return render(request, 'prestamos.html', {'prestamos': prestamos, 'form': form, 'filtro_form': filtro_form})

def devolver_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    if request.method == 'POST':
        if not prestamo.fecha_devolucion:
            prestamo.fecha_devolucion = timezone.now().date()
            prestamo.hora_devolucion = timezone.now().time()
            prestamo.estado = 'devuelto'
            prestamo.save()

            libro = prestamo.titulo_libro
            libro.cantidad += 1
            libro.save()
    return redirect('lista_prestamos')