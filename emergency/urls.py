# Importamos la función path, necesaria para definir cada una de las rutas
from django.urls import path
# Importamos el módulo de vistas (views.py) que contiene las funciones que responden a cada ruta
from . import views

# Lista urlpatterns donde se definen las rutas (URLs) disponibles en la aplicación 'emergency'
urlpatterns = [
    # Ruta principal (''). Cuando el usuario entre a la raíz de la app, se ejecutará views.dashboard.
    # Le asignamos el nombre 'dashboard' para poder referenciar esta URL en las plantillas HTML fácilmente.
    path('', views.dashboard, name='dashboard'),
    
    # Ruta para recibir peticiones AJAX que disparan una señal. 
    # Esta ruta no muestra una página HTML, sino que procesa datos y devuelve JSON.
    path('trigger/', views.trigger_signal, name='trigger_signal'),
    
    # Ruta para el registro de nuevos usuarios en la plataforma.
    path('register/', views.register_view, name='register'),
    
    # Ruta de inicio de sesión. Aquí usamos una vista basada en clases provista por Django,
    # y la convertimos en una vista normal usando el método .as_view().
    path('login/', views.CustomLoginView.as_view(), name='login'),
    
    # Ruta para cerrar la sesión activa.
    path('logout/', views.logout_view, name='logout'),
    
    # Ruta para que el usuario pueda ver y editar su perfil personal.
    path('profile/', views.profile_view, name='profile'),
]
