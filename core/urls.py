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

    # PUBLICACIONES
    path('publicaciones/', views.publicaciones, name='publicaciones'),
    path('eliminar_publicacion/<int:publicacion_id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('editar_publicacion/<int:publicacion_id>/', views.editar_publicacion, name='editar_publicacion'),

    # PROYECTOS
    path('proyectos_postular/', views.proyectos_postular, name='proyectos_postular'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('editar_proyecto/<int:proyecto_id>/', views.editar_proyecto, name='editar_proyecto'),
    path('eliminar_proyecto/<int:proyecto_id>/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('cambiar_estado_postulacion/<int:id>/', views.cambiar_estado_postulacion, name='cambiar_estado_postulacion'),

    #RESERVA
    path('reservas/', views.reservas, name='reservas'),
    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    path('cargar_eventos/', views.cargar_eventos, name='cargar_eventos'),
    path('eliminar_reserva/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),

    path('gestionar_espacios/', views.gestionar_espacios, name='gestionar_espacios'),
    path('editar_espacio/', views.editar_espacio, name='editar_espacio'),
    path('eliminar_espacio/<int:espacio_id>/', views.eliminar_espacio, name='eliminar_espacio'),

]
