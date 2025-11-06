from apps.empleados.views import lista_empleados, index
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('lista/', lista_empleados, name='lista_empleados'),
    path('register/', views.register, name='register'),
    path('', index, name='index'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]