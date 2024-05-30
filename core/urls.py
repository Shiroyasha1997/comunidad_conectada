from django.urls import path
from .views import inicio, ingresar, registro, perfil, change_password, cerrar_sesion
from .views import solicitudes, aprobar_solicitud, rechazar_solicitud
from .views import certificados, generar_certificado_pdf
from .views import iniciar_pago, procesar_pago, pago_exitoso

urlpatterns = [
    path('', inicio, name='inicio'),

    # AUTENTICACION
    path('ingresar/', ingresar, name='ingresar'),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('registro/', registro, name='registro'),
    path('solicitudes/', solicitudes, name='solicitudes'),
    path('solicitud/<int:solicitud_id>/aprobar/', aprobar_solicitud, name='aprobar_solicitud'),
    path('solicitud/<int:solicitud_id>/rechazar/', rechazar_solicitud, name='rechazar_solicitud'),
    path('perfil/', perfil, name='perfil'),
    path('change-password/', change_password, name='change_password'),

    # CERTIFICADOS
    path('generar_certificado_pdf/', generar_certificado_pdf, name='generar_certificado_pdf'),
    path('certificados/', certificados, name='certificados'),


    # API DE PAGOS
    path('iniciar_pago/', iniciar_pago, name='iniciar_pago'),
    path('procesar_pago/', procesar_pago, name='procesar_pago'),
    path('pago_exitoso/', pago_exitoso, name='pago_exitoso'),
]
