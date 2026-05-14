from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import EmergencySignal, Profile
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Si marcó la casilla de admin, le damos permisos
            if form.cleaned_data.get('is_admin'):
                user.is_staff = True
                user.is_superuser = True
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'emergency/register.html', {'form': form})

@login_required
def dashboard(request):
    # Si es admin, ve todo. Si es usuario, ve solo lo suyo.
    if request.user.is_staff:
        recent_signals = EmergencySignal.objects.all().order_by('-timestamp')[:20]
    else:
        recent_signals = EmergencySignal.objects.filter(user=request.user).order_by('-timestamp')[:10]
    
    stats = {
        'GREEN': EmergencySignal.objects.filter(level='GREEN').count(),
        'YELLOW': EmergencySignal.objects.filter(level='YELLOW').count(),
        'RED': EmergencySignal.objects.filter(level='RED').count(),
    }
    
    return render(request, 'emergency/dashboard.html', {
        'recent_signals': recent_signals,
        'stats': stats
    })

@login_required
def trigger_signal(request):
    if request.method == 'POST':
        level = request.POST.get('level')
        description = request.POST.get('description', '')
        patient_name = request.POST.get('patient_name', '')
        patient_age = request.POST.get('patient_age', None)
        
        if level in ['GREEN', 'YELLOW', 'RED']:
            signal = EmergencySignal.objects.create(
                user=request.user, 
                level=level, 
                description=description,
                patient_name=patient_name,
                patient_age=patient_age if patient_age else None
            )
            
            print(f"\n[ALERTA DISPARADA] Paciente: {patient_name} | Nivel: {level}")
            
            return JsonResponse({
                'status': 'success',
                'level': signal.level,
                'description': signal.description,
                'patient_name': signal.patient_name,
                'user': request.user.get_full_name() or request.user.username,
                'timestamp': signal.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'¡Tu perfil ha sido actualizado!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'emergency/profile.html', context)

class CustomLoginView(LoginView):
    template_name = 'emergency/login.html'
    redirect_authenticated_user = True

def logout_view(request):
    logout(request)
    return redirect('login')
