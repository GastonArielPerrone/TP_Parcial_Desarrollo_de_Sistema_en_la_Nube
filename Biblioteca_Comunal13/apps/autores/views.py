from django.shortcuts import render, redirect, get_object_or_404
from apps.autores.models import Autor
from .forms import AutorForm, FiltroAutorForm
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.
def lista_autores(request):
    filtro_form = FiltroAutorForm(request.GET or None)
    autores = Autor.objects.all()

    if filtro_form.is_valid():
        query = filtro_form.cleaned_data.get("q")
        nombre = filtro_form.cleaned_data.get("nombre")
        nacionalidad = filtro_form.cleaned_data.get("nacionalidad")

        if query:
            q_obj = Q(nombre__icontains=query)
            if query.isdigit():
                q_obj |= Q(id=int(query))
            autores = autores.filter(q_obj)

        if nombre:
            autores = autores.filter(nombre__icontains=nombre)

        if nacionalidad:
            autores = autores.filter(nacionalidad=nacionalidad)

    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_autores')
    else:
        form = AutorForm()
    return render(request, 'autores.html', {'form': form, 'autores': autores, 'filtro_form': filtro_form})

def editar_autor_modal(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    if request.method == 'POST':
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = AutorForm(instance=autor)
        html = render_to_string('editar_modal.html', {
            'form': form,
            'object': autor,
            'model_name': 'Autor'
        }, request=request)
        return JsonResponse({'html': html})