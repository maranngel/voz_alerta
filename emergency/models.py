# Importamos el módulo base de modelos de Django que nos permite definir las estructuras de la base de datos
from django.db import models
# Importamos el modelo User por defecto de Django, que maneja la autenticación y los datos básicos del usuario
from django.contrib.auth.models import User
# Importamos post_save, que es una señal de Django que se emite automáticamente después de guardar un modelo
from django.db.models.signals import post_save
# Importamos receiver, un decorador para conectar funciones a señales específicas (como post_save)
from django.dispatch import receiver


# Definición del modelo Profile (Perfil) que extiende la información del usuario estándar de Django
class Profile(models.Model):
    """
    Perfil extendido asociado a cada usuario.
    Se utiliza una relación OneToOne para vincular un único perfil a un único usuario (1 a 1).
    Esto es útil para almacenar datos adicionales que no vienen por defecto en el modelo User.
    """
    # Relación uno a uno con el modelo User. Si el usuario se elimina, su perfil también se elimina (CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Campo para almacenar el número de identificación del usuario. Puede estar en blanco o nulo en la BD
    id_number = models.CharField(max_length=20, blank=True, null=True)
    # Campo para un contacto de emergencia (nombre, teléfono, etc.) del propio usuario
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        # Método mágico que define cómo se representa el objeto como cadena (ej. en el panel de admin)
        return f"Perfil de {self.user.username}"


# Función receptora que "escucha" la señal post_save emitida por el modelo User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crea automáticamente un objeto Profile (perfil) cada vez que se registra y crea un nuevo usuario en la BD.
    - sender: Es el modelo que envía la señal (User).
    - instance: Es la instancia específica del usuario que acaba de ser guardada.
    - created: Un valor booleano (True/False) que indica si se acaba de crear un registro nuevo.
    """
    if created:
        # Si el usuario es nuevo, creamos su perfil correspondiente vinculándolo a la instancia
        Profile.objects.create(user=instance)


# Otra función receptora para guardar el perfil cada vez que se modifique o actualice el usuario
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Garantiza que cualquier actualización en el modelo User también guarde los cambios en su perfil asociado.
    """
    # Llama al método save() del perfil vinculado al usuario
    instance.profile.save()


# Definición del modelo EmergencySignal que registra todas las alertas generadas
class EmergencySignal(models.Model):
    """
    Registro de cada señal de emergencia generada en el sistema.
    Representa las alertas que disparan los usuarios desde el dashboard frontal.
    """
    # Tupla de tuplas que define las opciones fijas (choices) para el nivel de la alerta. 
    # El primer elemento es el valor en BD y el segundo es la etiqueta legible.
    LEVEL_CHOICES = [
        ('GREEN', 'Código Verde - Bajo'),
        ('YELLOW', 'Código Amarillo - Intermedio'),
        ('RED', 'Código Rojo - Alto'),
    ]
    
    # Clave foránea que relaciona la alerta con el usuario que la emitió. Si el usuario se borra, sus alertas también.
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Campo de texto corto que almacena el nivel de la alerta (GREEN, YELLOW, RED)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    # Fecha y hora exacta en la que se generó la alerta. auto_now_add=True rellena este campo automáticamente.
    timestamp = models.DateTimeField(auto_now_add=True)
    # Descripción detallada de la situación, puede estar vacío
    description = models.TextField(blank=True, null=True)
    # Nombre del paciente afectado, puede estar vacío
    patient_name = models.CharField(max_length=100, blank=True, null=True)
    # Edad del paciente en un campo entero (Integer), puede estar vacío
    patient_age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        # Representación en texto de la alerta indicando su nivel, paciente y quién la emitió
        return f"{self.level} - {self.patient_name or 'Sin nombre'} by {self.user.username if self.user else 'Anon'}"
