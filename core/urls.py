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

    # Vista para mostrar todos los proyectos y crear nuevos
    path('proyectos_postular/', views.proyectos_postular, name='proyectos_postular'),

    # Vista para mostrar todos los proyectos y crear nuevos
    path('proyectos/', views.proyectos, name='proyectos'),
    
    # Vista para procesar la creación de un nuevo proyecto
    path('crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    
    # Vista para editar un proyecto existente
    path('editar_proyecto/<int:proyecto_id>/', views.editar_proyecto, name='editar_proyecto'),

    # Vista para eliminar un proyecto existente
    path('eliminar_proyecto/<int:proyecto_id>/', views.eliminar_proyecto, name='eliminar_proyecto'),
    
    # Vista para cambiar el estado de una postulación
    path('cambiar_estado_postulacion/<int:id>/', views.cambiar_estado_postulacion, name='cambiar_estado_postulacion'),

]
