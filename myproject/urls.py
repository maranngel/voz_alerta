"""
URL configuration for myproject project.

Este archivo define las rutas principales del proyecto. En este caso:
- `admin/` apunta al panel de administración de Django.
- la ruta raíz `''` incluye las URLs de la aplicación emergency.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('emergency.urls')),
]
