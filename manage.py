#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

manage.py es el script principal de entrada para cualquier proyecto de Django.
Este archivo se utiliza en la terminal para ejecutar comandos clave del ciclo de desarrollo y despliegue:
- `python manage.py runserver`: Levanta el servidor local de desarrollo.
- `python manage.py makemigrations`: Prepara los cambios en los modelos para la base de datos.
- `python manage.py migrate`: Aplica los cambios de la base de datos.
- `python manage.py createsuperuser`: Crea un administrador maestro.
"""
import os
import sys

def main():
    """Configura el entorno y ejecuta el comando recibido por consola."""
    
    # 1. Configurar el Entorno
    # Le decimos a Django dónde encontrar la configuración principal (settings.py).
    # 'myproject.settings' es el módulo por defecto.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    
    try:
        # 2. Importar la función ejecutora de Django
        # Django intercepta los comandos del sistema operativo y los traduce a acciones internas.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si Django no está instalado o el entorno virtual no está activado, lanzamos un error descriptivo.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        
    # 3. Ejecutar el comando
    # Pasa los argumentos de la línea de comandos (sys.argv) a la herramienta de Django.
    execute_from_command_line(sys.argv)


# Punto de entrada de Python:
# Si este archivo se ejecuta directamente (no se importa desde otro lado), llama a la función main()
if __name__ == '__main__':
    main()
