# Importamos el módulo forms de Django para crear formularios web fácilmente
from django import forms
# Importamos el modelo User por defecto de Django
from django.contrib.auth.models import User
# Importamos UserCreationForm, un formulario incorporado de Django diseñado específicamente para el registro con contraseñas seguras
from django.contrib.auth.forms import UserCreationForm
# Importamos nuestro modelo Profile personalizado
from .models import Profile


# Formulario de registro que hereda de UserCreationForm para aprovechar su validación de contraseñas
class UserRegisterForm(UserCreationForm):
    """
    Formulario para registrar nuevos usuarios en la plataforma.
    Añadimos campos extras que no vienen por defecto en el UserCreationForm.
    """
    # Campo booleano para definir si el usuario debe ser administrador. required=False para que no sea obligatorio
    is_admin = forms.BooleanField(required=False, label="Registrar como Administrador")
    # Hacemos que el campo email sea obligatorio en el registro
    email = forms.EmailField(required=True)

    class Meta:
        # Vinculamos este formulario al modelo User
        model = User
        # Definimos los campos que se mostrarán en el formulario de registro (la contraseña se añade sola por UserCreationForm)
        fields = ['username', 'email', 'is_admin']


# Formulario para actualizar la información básica del usuario (Nombre, Apellido, Email)
class UserUpdateForm(forms.ModelForm):
    """
    Formulario para actualizar datos básicos del usuario una vez que ya tiene cuenta.
    Hereda de ModelForm, lo que genera automáticamente los campos basados en el modelo.
    """
    # Sobrescribimos email para asegurarnos de que el usuario siempre mantenga un email válido
    email = forms.EmailField()

    class Meta:
        model = User
        # Solo permitimos actualizar el nombre, apellido y correo
        fields = ['first_name', 'last_name', 'email']


# Formulario para actualizar la información extendida (Profile)
class ProfileUpdateForm(forms.ModelForm):
    """
    Formulario para actualizar campos adicionales del perfil (Cédula y Contacto de emergencia).
    Se usa en conjunto con UserUpdateForm en la misma vista de perfil.
    """
    class Meta:
        model = Profile
        # Campos de nuestro modelo Profile personalizado que permitiremos editar
        fields = ['id_number', 'emergency_contact']
