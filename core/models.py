from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Campos adicionales
    cargo = models.CharField(max_length=100, blank=True, null=True)
    run = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

class SolicitudInscripcion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]
    
    username = models.CharField(max_length=100)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    run = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    fecha_rechazo = models.DateTimeField(null=True, blank=True)
    notas = models.TextField(null=True, blank=True)

from django.contrib.auth import get_user_model
User = get_user_model()

class Certificado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    detalle = models.CharField(max_length=100)
    pdf_certificado = models.FileField(upload_to='certificados/')

    def __str__(self):
        return f'Certificado para {self.usuario.username}'

class Publicacion(models.Model):
    TIPO_CHOICES = [
        ('noticia', 'Noticia'),
        ('evento', 'Evento'),
        ('anuncio', 'Anuncio'),
    ]
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=255)
    detalle = models.TextField()
    imagen = models.ImageField(upload_to='publicaciones/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

#-------------------------------------------------------------------------------------------------------------------
#PROYECTOS
#-------------------------------------------------------------------------------------------------------------------
from django.conf import settings

class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cupos = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Postulacion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='postulaciones')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    detalle = models.TextField()
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f'{self.usuario.username} - {self.proyecto.nombre}'

#-------------------------------------------------------------------------------------------------------------------
#RESERVAS
#-------------------------------------------------------------------------------------------------------------------
class Espacio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    dias_disponibles = models.CharField(max_length=200)
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hora_reserva = models.TimeField()
    dia_reserva = models.DateField()
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)

    def __str__(self):
        return f'Reserva de {self.usuario.get_full_name()} en {self.espacio.nombre} el {self.dia_reserva} a las {self.hora_reserva}'
