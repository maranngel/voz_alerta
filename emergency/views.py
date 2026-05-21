# Importamos funciones útiles para renderizar plantillas (render) y redirigir usuarios (redirect)
from django.shortcuts import render, redirect
# Importamos JsonResponse para enviar respuestas en formato JSON, fundamental para peticiones AJAX
from django.http import JsonResponse
# Importamos la función logout para cerrar la sesión del usuario actual
from django.contrib.auth import logout
# Importamos un decorador que asegura que solo usuarios logueados puedan acceder a ciertas vistas
from django.contrib.auth.decorators import login_required
# Importamos la vista basada en clases LoginView, que maneja el inicio de sesión por defecto de Django
from django.contrib.auth.views import LoginView
# Importamos el framework de mensajes de Django, útil para mostrar alertas flash temporales
from django.contrib import messages
# Importamos el modelo EmergencySignal de esta aplicación para interactuar con la base de datos
from .models import EmergencySignal
# Importamos los formularios definidos en forms.py para manejar el registro y actualización
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm


# Vista para el registro de nuevos usuarios
def register_view(request):
    """
    Muestra y procesa el formulario de registro de usuarios.
    Maneja tanto la petición GET (mostrar formulario vacío) como la POST (procesar datos).
    """
    # Verificamos si el método de la solicitud HTTP es POST (envío de datos)
    if request.method == 'POST':
        # Instanciamos el formulario con los datos enviados por el usuario
        form = UserRegisterForm(request.POST)
        # Verificamos si los datos ingresados cumplen con las validaciones del formulario
        if form.is_valid():
            # Creamos el objeto del usuario sin guardarlo todavía en la base de datos (commit=False)
            user = form.save(commit=False)
            
            # Comprobamos si en el formulario se marcó la casilla 'is_admin'
            # Si el usuario marca la casilla de administrador, se habilitan permisos especiales.
            if form.cleaned_data.get('is_admin'):
                # Le otorgamos permisos de staff y superusuario al nuevo registro
                user.is_staff = True
                user.is_superuser = True
                
            # Ahora sí guardamos el usuario de forma definitiva en la base de datos
            user.save()
            # Obtenemos el nombre de usuario de los datos ya limpiados
            username = form.cleaned_data.get('username')
            # Generamos un mensaje de éxito que se mostrará en la siguiente vista (login)
            messages.success(request, f'¡Cuenta creada para {username}! Ya puedes iniciar sesión.')
            # Redirigimos al usuario a la página de inicio de sesión
            return redirect('login')
    else:
        # Si no es POST (es GET), instanciamos un formulario vacío para mostrárselo al usuario
        form = UserRegisterForm()

    # Renderizamos la plantilla HTML de registro pasándole el formulario como contexto
    return render(request, 'emergency/register.html', {'form': form})


# El decorador @login_required impide que usuarios no autenticados vean esta página
@login_required
def dashboard(request):
    """
    Genera la vista principal (Centro de Comando) con las señales recientes y estadísticas.
    """
    # Comprobamos si el usuario actual tiene permisos de administrador (is_staff)
    if request.user.is_staff:
        # Si es admin, obtenemos las 20 señales más recientes de todos los usuarios
        recent_signals = EmergencySignal.objects.all().order_by('-timestamp')[:20]
    else:
        # Usuarios normales solo pueden ver sus propias señales. Filtramos por el usuario actual (request.user)
        recent_signals = EmergencySignal.objects.filter(user=request.user).order_by('-timestamp')[:10]
    
    # Preparamos un diccionario con el conteo de cada tipo de señal, que usaremos para pintar la gráfica en JS
    stats = {
        'GREEN': EmergencySignal.objects.filter(level='GREEN').count(),
        'YELLOW': EmergencySignal.objects.filter(level='YELLOW').count(),
        'RED': EmergencySignal.objects.filter(level='RED').count(),
    }
    
    # Renderizamos el HTML del dashboard y le pasamos las señales recientes y estadísticas
    return render(request, 'emergency/dashboard.html', {
        'recent_signals': recent_signals,
        'stats': stats
    })


# Otra vista protegida: solo usuarios registrados pueden emitir alertas
@login_required
def trigger_signal(request):
    """
    Crea una nueva señal de emergencia a partir de peticiones AJAX (POST).
    Este endpoint se comunica directamente con JavaScript, no devuelve HTML, sino JSON.
    """
    # Verificamos que se esté enviando información a través de POST
    if request.method == 'POST':
        # Extraemos cada uno de los parámetros recibidos por la petición AJAX
        level = request.POST.get('level')
        description = request.POST.get('description', '')
        patient_name = request.POST.get('patient_name', '')
        patient_age = request.POST.get('patient_age', None)
        
        # Validamos que el nivel recibido esté dentro de nuestras opciones permitidas
        if level in ['GREEN', 'YELLOW', 'RED']:
            # Creamos y guardamos un nuevo registro de alerta en la base de datos
            signal = EmergencySignal.objects.create(
                user=request.user,  # Asignamos la alerta al usuario actual
                level=level,
                description=description,
                patient_name=patient_name,
                patient_age=patient_age if patient_age else None
            )
            
            # Imprimimos un mensaje en consola para depuración o auditoría en el backend
            print(f"\n[ALERTA DISPARADA] Paciente: {patient_name} | Nivel: {level}")
            
            # Devolvemos un JSON indicando éxito y devolviendo los datos de la alerta recién creada
            # para que el frontend (Javascript) actualice la UI sin recargar la página.
            return JsonResponse({
                'status': 'success',
                'level': signal.level,
                'description': signal.description,
                'patient_name': signal.patient_name,
                'user': request.user.get_full_name() or request.user.username,
                'timestamp': signal.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })

    # Si la petición no es POST o el nivel de alerta no es válido, retornamos un JSON con error
    return JsonResponse({'status': 'error'}, status=400)


# Vista para editar el perfil
@login_required
def profile_view(request):
    """
    Permite al usuario actualizar datos de su perfil y de su cuenta base de Django.
    Maneja dos formularios a la vez: uno para User y otro para Profile.
    """
    if request.method == 'POST':
        # Instanciamos los formularios de User y Profile rellenándolos con los datos recibidos (request.POST)
        # y vinculándolos a los datos existentes (instance=request.user) para sobreescribirlos.
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        # Verificamos que ambos formularios sean válidos
        if u_form.is_valid() and p_form.is_valid():
            # Guardamos los cambios de ambos modelos en la base de datos
            u_form.save()
            p_form.save()
            # Añadimos un mensaje flotante de éxito
            messages.success(request, f'¡Tu perfil ha sido actualizado!')
            # Redirigimos al usuario a la misma página (Post/Redirect/Get pattern)
            return redirect('profile')
    else:
        # Si la petición es GET, pre-rellenamos los formularios con los datos actuales del usuario
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Creamos un contexto con ambos formularios para enviarlos a la plantilla
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    # Renderizamos la página del perfil de usuario
    return render(request, 'emergency/profile.html', context)


# Usamos una clase en vez de una función para el Login, heredando del LoginView de Django
class CustomLoginView(LoginView):
    """
    Vista de inicio de sesión personalizada que usa la plantilla definida.
    LoginView ya contiene toda la lógica de autenticación segura.
    """
    # Indicamos la ruta exacta a nuestra plantilla HTML para el formulario de login
    template_name = 'emergency/login.html'
    # Si un usuario que ya ha iniciado sesión intenta ir al Login, lo redirigimos automáticamente (al dashboard)
    redirect_authenticated_user = True


# Vista muy simple para cerrar la sesión actual
def logout_view(request):
    """
    Cierra sesión eliminando las cookies y datos de sesión temporales,
    y luego redirige al usuario a la página de inicio de sesión.
    """
    logout(request)
    return redirect('login')
