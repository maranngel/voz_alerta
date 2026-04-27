from django.shortcuts import render
from django.http import JsonResponse
from .models import EmergencySignal

def dashboard(request):
    recent_signals = EmergencySignal.objects.all().order_by('-timestamp')[:10]
    return render(request, 'emergency/dashboard.html', {'recent_signals': recent_signals})

def trigger_signal(request):
    if request.method == 'POST':
        level = request.POST.get('level')
        if level in ['GREEN', 'YELLOW', 'RED']:
            signal = EmergencySignal.objects.create(level=level)
            return JsonResponse({
                'status': 'success',
                'level': signal.level,
                'timestamp': signal.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
    return JsonResponse({'status': 'error'}, status=400)
