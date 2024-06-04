from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    # AUTENTICACION
    path('ingresar/', views.ingresar, name='ingresar'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('registro/', views.registro, name='registro'),
    path('solicitudes/', views.solicitudes, name='solicitudes'),
    path('solicitud/<int:solicitud_id>/aprobar/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('solicitud/<int:solicitud_id>/rechazar/', views.rechazar_solicitud, name='rechazar_solicitud'),
    path('perfil/', views.perfil, name='perfil'),
    path('change-password/', views.change_password, name='change_password'),

    # CERTIFICADOS
    path('certificados/', views.certificados, name='certificados'),
    path('generar_certificado_pdf/', views.generar_certificado_pdf, name='generar_certificado_pdf'),
    path('guardar_certificado/',views.guardar_certificado, name='guardar_certificado'),
    path('descargar_certificado/', views.descargar_certificado, name='descargar_certificado'),

    # API DE PAGOS
    path('iniciar_pago/', views.iniciar_pago, name='iniciar_pago'),
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),
]
