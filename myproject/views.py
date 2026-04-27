from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>¡Hola! El proyecto de Django está funcionando correctamente.</h1>")
