from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    """Formulario para registrar nuevos usuarios en la plataforma."""
    is_admin = forms.BooleanField(required=False, label="Registrar como Administrador")
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'is_admin']


class UserUpdateForm(forms.ModelForm):
    """Formulario para actualizar datos básicos del usuario."""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """Formulario para actualizar campos adicionales del perfil."""
    class Meta:
        model = Profile
        fields = ['id_number', 'emergency_contact']
