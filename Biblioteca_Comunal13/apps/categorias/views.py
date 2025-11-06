from django.shortcuts import render, redirect, get_object_or_404
from apps.categorias.models import Categoria
from .forms import CategoriaForm, FiltroCategoriaForm
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.
def lista_categorias(request):
    filtro_form = FiltroCategoriaForm(request.GET or None)
    categorias = Categoria.objects.all()

    if filtro_form.is_valid():
        query = filtro_form.cleaned_data.get("q")
        nombre = filtro_form.cleaned_data.get("nombre")

        if query:
            q_obj = Q(nombre__icontains=query)
            if query.isdigit():
                q_obj |= Q(id=int(query))
            categorias = categorias.filter(q_obj)

        if nombre:
            categorias = categorias.filter(nombre__icontains=nombre)

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()

    return render(request, 'categorias.html', {'form': form, 'categorias': categorias, 'filtro_form': filtro_form})

def editar_categoria_modal(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CategoriaForm(instance=categoria)
        html = render_to_string('editar_modal.html', {
            'form': form,
            'object': categoria,
            'model_name': 'Categoría'
        }, request=request)
        return JsonResponse({'html': html})