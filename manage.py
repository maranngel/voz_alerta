#!/usr/bin/env python
"""Django's command-line utility for administrative tasks.

Este archivo se utiliza para ejecutar comandos como:
- python manage.py runserver
- python manage.py migrate
- python manage.py createsuperuser
"""
import os
import sys


def main():
    """Configura el entorno y ejecuta el comando recibido."""
    # Define de forma predeterminada el módulo de settings de Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Ejecuta el comando recibido desde la línea de comandos
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
