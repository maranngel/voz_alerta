from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class EmergencySignal(models.Model):
    LEVEL_CHOICES = [
        ('GREEN', 'Código Verde - Bajo'),
        ('YELLOW', 'Código Amarillo - Intermedio'),
        ('RED', 'Código Rojo - Alto'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    patient_name = models.CharField(max_length=100, blank=True, null=True)
    patient_age = models.IntegerField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.level} - {self.patient_name or 'Sin nombre'} by {self.user.username if self.user else 'Anon'}"
