"""
WSGI config for myproject project.

Este archivo se utiliza cuando el proyecto se despliega con un servidor compatible con WSGI.
Expone la variable ``application`` que el servidor web debe invocar.
"""

import os

from django.core.wsgi import get_wsgi_application

# Establece el módulo de configuración si no está definido en el entorno.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Objeto de aplicación WSGI que el servidor web utilizará.
application = get_wsgi_application()
