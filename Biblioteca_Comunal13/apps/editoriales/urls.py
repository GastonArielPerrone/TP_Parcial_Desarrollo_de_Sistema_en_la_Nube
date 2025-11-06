from apps.editoriales.views import lista_editoriales
from django.urls import path

urlpatterns = [
    path('lista/',lista_editoriales,name='lista_editoriales')
]