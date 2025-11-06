from django.shortcuts import render, redirect
from apps.editoriales.models import Editorial
from .forms import EditorialForm, FiltroEditorialForm
from django.db.models import Q

# Create your views here.
def lista_editoriales(request):
    filtro_form = FiltroEditorialForm(request.GET or None)
    editoriales = Editorial.objects.all()

    if filtro_form.is_valid():
        query = filtro_form.cleaned_data.get("q")
        nombre = filtro_form.cleaned_data.get("nombre")
        pais = filtro_form.cleaned_data.get("pais")

        if query:
            q_obj = Q(nombre__icontains=query) | Q(pais__icontains=query)
            if query.isdigit():
                q_obj |= Q(id=int(query))
            editoriales = editoriales.filter(q_obj)

        if nombre:
            editoriales = editoriales.filter(nombre__icontains=nombre)

        if pais:
            editoriales = editoriales.filter(pais__icontains=pais)

    if request.method == 'POST':
        form = EditorialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_editoriales')
    else:
        form = EditorialForm()

    return render(request, 'editoriales.html', {'form': form, 'editoriales': editoriales, 'filtro_form': filtro_form})