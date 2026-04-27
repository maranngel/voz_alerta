from django.db import models

class EmergencySignal(models.Model):
    LEVEL_CHOICES = [
        ('GREEN', 'Código Verde - Bajo'),
        ('YELLOW', 'Código Amarillo - Intermedio'),
        ('RED', 'Código Rojo - Alto'),
    ]
    
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.level} at {self.timestamp}"
