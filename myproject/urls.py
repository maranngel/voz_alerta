"""
URL configuration for myproject project.

Este archivo es el "enrutador principal" o "raíz" del proyecto Django. 
Define a qué aplicación se delega cada petición web dependiendo de la URL visitada.
"""
# Importamos el módulo de administración nativo de Django
from django.contrib import admin
# Importamos 'path' para definir rutas simples y 'include' para delegar rutas a otras aplicaciones
from django.urls import path, include

urlpatterns = [
    # Ruta 'admin/': Apunta al panel de administración autogenerado de Django.
    # Permite gestionar usuarios, grupos y nuestros modelos (si los registramos).
    path('admin/', admin.site.urls),
    
    # Ruta vacía '': Actúa como la ruta principal de la web (el index o homepage).
    # Usamos 'include' para decir: "Cualquier petición a la raíz o a las rutas dentro de 'emergency', 
    # pásaselas al archivo urls.py de la aplicación 'emergency' para que las resuelva".
    path('', include('emergency.urls')),
]
