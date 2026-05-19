from django.http import HttpResponse


def index(request):
    """Vista simple que sirve para comprobar que el proyecto está funcionando."""
    return HttpResponse("<h1>¡Hola! El proyecto de Django está funcionando correctamente.</h1>")
