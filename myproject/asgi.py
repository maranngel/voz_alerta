"""
ASGI config for myproject project.

Este archivo se utiliza cuando el servidor ejecuta el proyecto usando un servidor compatible con ASGI.
Expone la variable ``application`` que Django usa para iniciar la aplicación.
"""

import os

from django.core.asgi import get_asgi_application

# Establece el módulo de configuración si no está definido en el entorno.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Objeto de aplicación ASGI que el servidor utilizará.
application = get_asgi_application()
