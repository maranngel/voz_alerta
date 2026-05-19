from django.urls import path
from . import views

urlpatterns = [
    # Ruta principal que muestra el dashboard de señales.
    path('', views.dashboard, name='dashboard'),
    # Ruta para recibir peticiones AJAX que disparan una señal.
    path('trigger/', views.trigger_signal, name='trigger_signal'),
    # Registro de nuevos usuarios.
    path('register/', views.register_view, name='register'),
    # Inicio de sesión con vista basada en clases.
    path('login/', views.CustomLoginView.as_view(), name='login'),
    # Cierre de sesión.
    path('logout/', views.logout_view, name='logout'),
    # Vista de perfil de usuario.
    path('profile/', views.profile_view, name='profile'),
]
