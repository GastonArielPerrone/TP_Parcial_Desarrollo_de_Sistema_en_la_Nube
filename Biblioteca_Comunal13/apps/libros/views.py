# apps/libros/views.py
from django.shortcuts import render, redirect
from django.contrib import admin
from .models import Libro
from .forms import LibroForm, FiltroLibroForm
from django.db.models import Q

admin.register(Libro)
def lista_libros(request):
    filtro_form = FiltroLibroForm(request.GET or None)
    libros = Libro.objects.all()

    if filtro_form.is_valid():
        query = filtro_form.cleaned_data.get("q")
        titulo = filtro_form.cleaned_data.get("titulo")
        autor = filtro_form.cleaned_data.get("autor")
        editorial = filtro_form.cleaned_data.get("editorial")
        categoria = filtro_form.cleaned_data.get("categoria")

        if query:
            q_obj = Q(titulo__icontains=query) | Q(autor__nombre__icontains=query) | Q(editorial__nombre__icontains=query) | Q(categoria__nombre__icontains=query)
            libros = libros.filter(q_obj)

        if titulo:
            libros = libros.filter(titulo__icontains=titulo)

        if autor:
            libros = libros.filter(autor__nombre__icontains=autor)

        if editorial:
            libros = libros.filter(editorial__nombre__icontains=editorial)

        if categoria:
            libros = libros.filter(categoria__nombre__icontains=categoria)

    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_libros')
    else:
        form = LibroForm()

    return render(request, 'libros.html', {'form': form, 'libros': libros, 'filtro_form': filtro_form})
