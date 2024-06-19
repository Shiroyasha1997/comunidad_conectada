import random, string, uuid, os
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils import timezone
from django.utils.timezone import now
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import residente_required, directivo_required

CustomUser = get_user_model()

#-------------------------------------------------------------------------------------------------------------------
#PAGINA DE INICIO
#-------------------------------------------------------------------------------------------------------------------

def inicio(request):
    es_admin = request.user.is_staff
    es_directivo = request.user.groups.filter(name='Directivo').exists()
    es_residente = request.user.groups.filter(name='Residente').exists()

    # Obtener publicaciones por categoría
    noticias = Publicacion.objects.filter(tipo='noticia').order_by('-fecha_creacion')
    eventos = Publicacion.objects.filter(tipo='evento').order_by('-fecha_creacion')
    anuncios = Publicacion.objects.filter(tipo='anuncio').order_by('-fecha_creacion')

    return render(request, 'inicio.html', {
        'es_admin': es_admin,
        'es_directivo': es_directivo,
        'es_residente': es_residente,
        'noticias': noticias,
        'eventos': eventos,
        'anuncios': anuncios,
    })

#-------------------------------------------------------------------------------------------------------------------
#AUTENTICACION
#-------------------------------------------------------------------------------------------------------------------
from .forms import CustomPasswordChangeForm, IngresarForm, RegistroForm, PerfilForm
from .models import SolicitudInscripcion, CustomUser

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')  # Redirige al inicio después de cerrar sesión

def ingresar(request):
    if request.method == 'POST':
        form = IngresarForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_staff:
                        return redirect('inicio')
                    elif user.groups.filter(name='Directivo').exists():
                        return redirect('inicio')
                    elif user.groups.filter(name='Residente').exists():
                        return redirect('inicio')
                    else:
                        messages.error(request, "No tienes permiso para acceder a esta área.")
                else:
                    messages.error(request, "Esta cuenta está inactiva. Contacta al administrador.")
            else:
                if not CustomUser.objects.filter(username=username).exists():
                    messages.error(request, "El nombre de usuario no existe.", extra_tags='ingresar_error')  # Agregar la etiqueta 'ingresar_error'
                else:
                    messages.error(request, "Contraseña incorrecta.", extra_tags='ingresar_error')  # Agregar la etiqueta 'ingresar_error'
    else:
        form = IngresarForm()
    
    return render(request, 'ingresar.html', {'form': form})

@login_required
def perfil(request):
    user = request.user
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=user)
        if form.is_valid():
            username = form.cleaned_data['username']
            if CustomUser.objects.filter(username=username).exclude(id=user.id).exists():
                form.add_error('username', 'El nombre de usuario ya está en uso. Por favor, elige otro.')
                messages.error(request, 'El nombre de usuario ya está en uso. Por favor, elige otro.', extra_tags='perfil')
                return render(request, 'perfil.html', {'form': form, 'password_form': CustomPasswordChangeForm(user)})

            run = form.cleaned_data['run']
            if SolicitudInscripcion.objects.filter(run=run).exists():
                form.add_error('run', 'El RUN ya está registrado. Por favor, ingresa otro.')
                messages.error(request, 'El RUN ya está registrado. Por favor, ingresa otro.', extra_tags='perfil')
                return render(request, 'perfil.html', {'form': form, 'password_form': CustomPasswordChangeForm(user)})

            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado!', extra_tags='perfil')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.', extra_tags='perfil')
    else:
        if user.groups.filter(name='Directivo').exists():
            form = PerfilForm(instance=user, disable_email=True, disable_username=True)  # Pasar disable_username=True
        else:
            form = PerfilForm(instance=user)

    password_form = CustomPasswordChangeForm(user)
    return render(request, 'perfil.html', {'form': form, 'password_form': password_form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '¡Tu contraseña ha sido actualizada!', extra_tags='perfil')
            return redirect('perfil')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error, extra_tags='password_error')
            return redirect('perfil')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            user.delete()
            logout(request)
            messages.success(request, '¡Tu cuenta ha sido eliminada exitosamente!')
            return redirect('inicio')
        else:
            messages.error(request, 'La contraseña ingresada no es correcta. Por favor, intenta nuevamente.')
            return redirect('perfil')
    return redirect('perfil')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            run = form.cleaned_data['run']
            fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
            
            # Validación de nombre de usuario único en los usuarios registrados
            if CustomUser.objects.filter(username=username).exists():
                form.add_error('username', 'El nombre de usuario ya está en uso. Por favor, elige otro.')
                return render(request, 'registro.html', {'form': form})

            # Validación de nombre de usuario único en las solicitudes de inscripción
            if SolicitudInscripcion.objects.filter(username=username).exists():
                form.add_error('username', 'El nombre de usuario ya está en uso. Por favor, elige otro.')
                return render(request, 'registro.html', {'form': form})

            # Validación de RUN único en los usuarios registrados
            if CustomUser.objects.filter(run=run).exists():
                form.add_error('run', 'El RUN ya está registrado. Por favor, ingresa otro.')
                return render(request, 'registro.html', {'form': form})

            # Validación de RUN único en las solicitudes de inscripción
            if SolicitudInscripcion.objects.filter(run=run).exists():
                form.add_error('run', 'El RUN ya está registrado. Por favor, ingresa otro.')
                return render(request, 'registro.html', {'form': form})

            # Validación de edad mínima (14 años)
            edad_minima = datetime.now().date() - timedelta(days=14*365)  # Calcular fecha hace 14 años
            if fecha_nacimiento > edad_minima:
                form.add_error('fecha_nacimiento', 'Debes tener al menos 14 años para registrarte.')
                return render(request, 'registro.html', {'form': form})

            # Si todas las validaciones pasan, guarda el formulario
            solicitud = form.save(commit=False)
            solicitud.save()

            messages.success(request, 'Tu solicitud de registro ha sido enviada. Espera la aprobación del directivo.', extra_tags='registro')
            return redirect('registro')  # Redirigir a la página de registro nuevamente
        else:
            messages.error(request, 'Hubo un error al procesar tu solicitud. Por favor, inténtalo de nuevo.', extra_tags='registro')
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form})

@login_required
@directivo_required
def solicitudes(request):
    if request.user.groups.filter(name='Directivo').exists():
        solicitudes = SolicitudInscripcion.objects.all()
        return render(request, 'solicitudes.html', {'solicitudes': solicitudes})
    else:
        return redirect('inicio')  # Redirigir a la página de inicio si el usuario no es un directivo

@login_required
@directivo_required
def aprobar_solicitud(request, solicitud_id):
    if request.user.groups.filter(name='Directivo').exists():
        solicitud = SolicitudInscripcion.objects.get(id=solicitud_id)
        solicitud.estado = 'aceptada'
        solicitud.fecha_aprobacion = timezone.now()
        
        # Obtener el nombre del directivo
        nombre_directivo = request.user.get_full_name()

        # Generar una contraseña aleatoria
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        # Enviar la contraseña por correo electrónico
        subject = 'Bienvenido a nuestra comunidad'
        message = f'Hola {solicitud.first_name}, tu solicitud ha sido aprobada.\n\nUsuario: {solicitud.username}\nContraseña: {password}.\nATTE: {nombre_directivo}'
        from_email = 'comunidad_conectada@outlook.com'  # Ingresa tu dirección de correo
        to_email = [solicitud.email]
        send_mail(subject, message, from_email, to_email)

        # Guardar la contraseña generada en el modelo de SolicitudInscripcion
        solicitud.password = make_password(password)
        solicitud.save()

        # Crear el usuario con los datos de la solicitud
        nuevo_usuario = CustomUser.objects.create_user(
            username=solicitud.username,
            first_name=solicitud.first_name,
            last_name=solicitud.last_name,
            email=solicitud.email,
            run=solicitud.run,
            direccion=solicitud.direccion,
            telefono=solicitud.telefono,
            fecha_nacimiento=solicitud.fecha_nacimiento,
            password=password
        )

        # Asignar al usuario al grupo Residente
        grupo_residente = Group.objects.get(name='Residente')
        nuevo_usuario.groups.add(grupo_residente)

        # Eliminar la solicitud aprobada de la base de datos
        solicitud.delete()

        messages.success(request, "La solicitud ha sido aprobada. Se ha enviado un correo electrónico con los detalles de inicio de sesión.", extra_tags='solicitudes')
        return redirect('solicitudes')
    else:
        messages.error(request, "No tienes permisos para aprobar esta solicitud.", extra_tags='solicitudes')
        return redirect('solicitudes')

@login_required
@directivo_required
def rechazar_solicitud(request, solicitud_id):
    if request.user.groups.filter(name='Directivo').exists():
        solicitud = SolicitudInscripcion.objects.get(id=solicitud_id)
        solicitud.estado = 'rechazada'
        solicitud.fecha_rechazo = timezone.now()
        solicitud.save()
        
        # Obtener el nombre del directivo
        nombre_directivo = request.user.get_full_name()

        # Enviar un correo electrónico informando sobre el rechazo
        subject = 'Solicitud de registro rechazada'
        message = f'Hola {solicitud.first_name}, lamentamos informarte que tu solicitud de registro ha sido rechazada.\nATTE: {nombre_directivo}'
        from_email = 'comunidad_conectada@outlook.com'  # Ingresa tu dirección de correo
        to_email = [solicitud.email]
        send_mail(subject, message, from_email, to_email)

        # Eliminar la solicitud rechazada de la base de datos
        solicitud.delete()

        messages.success(request, "La solicitud ha sido rechazada. Se ha enviado un correo electrónico al solicitante.", extra_tags='solicitudes')
        return redirect('solicitudes')
    else:
        messages.error(request, "No tienes permisos para rechazar esta solicitud.", extra_tags='solicitudes')
        return redirect('solicitudes')


#-------------------------------------------------------------------------------------------------------------------
#CERTIFICADOS
#-------------------------------------------------------------------------------------------------------------------
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from .models import Certificado

@login_required
@residente_required
def certificados(request):
    certificados_usuario = Certificado.objects.filter(usuario=request.user)
    return render(request, 'certificados.html', {'certificados_usuario': certificados_usuario})

@login_required
@residente_required
def descargar_certificado(request):
    # Obtener el último certificado del usuario
    certificado = Certificado.objects.filter(usuario=request.user).order_by('-fecha_compra').first()
    
    if not certificado or not certificado.pdf_certificado:
        return HttpResponse("No se encontró un certificado disponible para descargar.", status=404)

    # Preparar la respuesta con el archivo PDF
    response = HttpResponse(certificado.pdf_certificado.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_residencia_{uuid.uuid4().hex[:6]}.pdf"'
    return response

def guardar_certificado(request):
    # Obtener el usuario actual
    user = request.user

    # Crear un certificado para el usuario
    certificado = Certificado(usuario=user, detalle="Certificado de Residencia")

    # Generar el PDF del certificado
    certificado_pdf = generar_certificado_pdf(certificado)

    # Asignar el PDF generado al campo pdf_certificado del certificado
    nombre_archivo = f'certificado_residencia_{uuid.uuid4().hex[:6]}.pdf'
    certificado.pdf_certificado.save(nombre_archivo, ContentFile(certificado_pdf.getvalue()))

    # Guardar el certificado en la base de datos
    certificado.save()

def generar_certificado_pdf(certificado):
    buffer = BytesIO()

    # Crear el PDF del certificado
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Definir estilos
    titulo_style = styles["Heading1"]
    titulo_style.alignment = 1
    contenido_style = styles["BodyText"]
    contenido_style.fontSize = 12
    contenido_style.leading = 14

    # Contenido del PDF
    contenido = []

    # Título del certificado
    contenido.append(Paragraph("Certificado de Residencia", titulo_style))
    contenido.append(Spacer(1, 12))

    # Nombre del usuario
    nombre_usuario = certificado.usuario.get_full_name()
    contenido.append(Paragraph(f"Nombre: {nombre_usuario}", contenido_style))
    contenido.append(Spacer(1, 12))

    # Dirección del usuario (suponiendo que tienes este dato en el perfil del usuario)
    direccion_usuario = certificado.usuario.direccion  # Ajusta esto según tu modelo
    contenido.append(Paragraph(f"Dirección: {direccion_usuario}", contenido_style))
    contenido.append(Spacer(1, 12))

    # Declaración oficial
    declaracion_text = (
        "Este certificado de residencia es emitido para acreditar que el "
        "señor(a) {nombre} reside en la dirección {direccion}, en la comuna de Santiago, "
        "Chile. Este documento tiene validez oficial y ha sido emitido conforme a las leyes y "
        "regulaciones vigentes en el país."
    ).format(nombre=nombre_usuario, direccion=direccion_usuario)
    contenido.append(Paragraph(declaracion_text, contenido_style))
    contenido.append(Spacer(1, 12))

    # Firma
    contenido.append(Paragraph("Firma:", contenido_style))
    contenido.append(Spacer(1, 48))
    contenido.append(Paragraph("__________________________", contenido_style))
    contenido.append(Paragraph("Firma Autorizada", contenido_style))
    contenido.append(Spacer(1, 12))

    # Construir el documento
    doc.build(contenido)

    # Devolver el contenido del PDF generado
    buffer.seek(0)
    return buffer

#-------------------------------------------------------------------------------------------------------------------
#API DE PAGO WEBPAY
#-------------------------------------------------------------------------------------------------------------------
from django.urls import reverse
from .webpay_config import webpay_options, generar_buy_order
from transbank.webpay.webpay_plus.transaction import Transaction

@login_required
@residente_required
def iniciar_pago(request):
    if request.method == 'POST':
        buy_order = generar_buy_order()
        if len(buy_order) > 26:
            return HttpResponse("Error: 'buy_order' es demasiado largo.")
        
        session_id = request.session.session_key
        amount = 1000  # Monto del pago en pesos chilenos
        return_url = request.build_absolute_uri(reverse('procesar_pago'))

        try:
            tx = Transaction(webpay_options)
            response = tx.create(buy_order, session_id, amount, return_url)
        except Exception as e:
            return redirect(reverse('iniciar_pago') + '?error=1')

        return redirect(f"{response['url']}?token_ws={response['token']}")
    
    return render(request, 'iniciar_pago.html')

from django.core.files.base import ContentFile
from io import BytesIO

@login_required
def procesar_pago(request):
    token = request.GET.get('token_ws')
    try:
        # Confirmar y obtener el resultado de la transacción
        tx = Transaction(webpay_options)
        response = tx.commit(token)
    except Exception as e:
        # Si hay un error, redirigir de nuevo a la página iniciar_pago.html con un parámetro de error
        return redirect(reverse('iniciar_pago') + '?error=1')
    
    status = response.get('status')
    if status == 'AUTHORIZED':
        # Si el pago es autorizado, procesar la compra del certificado
        guardar_certificado(request)

        # Redirigir a la página de éxito
        return redirect(reverse('pago_exitoso'))
    elif status == 'REJECTED':
        # Si el pago es rechazado, redirigir a la página de rechazo o iniciar_pago.html con un parámetro de error
        return redirect(reverse('iniciar_pago') + '?error=1')
    elif status == 'NULLIFIED':
        # Si el pago es anulado, redirigir a la página de anulación o iniciar_pago.html con un parámetro de error
        return redirect(reverse('iniciar_pago') + '?error=1')
    else:
        # Otros estados posibles de la transacción
        return redirect(reverse('iniciar_pago') + '?error=1')

@login_required
@residente_required
def pago_exitoso(request):
    return render(request, 'pago_exitoso.html', {
        'options': ['Ver certificado', 'Descargar certificado', 'Enviar al correo']
    })

#-------------------------------------------------------------------------------------------------------------------
#PUBLICACIONES
#-------------------------------------------------------------------------------------------------------------------
from .forms import PublicacionForm
from .models import Publicacion

def publicaciones(request):
    # Obtener todas las publicaciones
    publicaciones = Publicacion.objects.all()

    # Si se envía un formulario para crear una nueva publicación
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Agregar mensaje de éxito con el tag 'publicaciones'
            messages.success(request, 'Publicación creada con éxito', extra_tags='publicaciones')
            return redirect('publicaciones')
        else:
            # Agregar mensaje de error con el tag 'publicaciones' si el formulario no es válido
            messages.error(request, 'No se pudo crear la publicación. Por favor, corrige los errores.', extra_tags='publicaciones')
    else:
        # Si es una solicitud GET o no se envió un formulario válido
        form = PublicacionForm()

    return render(request, 'publicaciones.html', {'publicaciones': publicaciones, 'form': form})

@login_required
@directivo_required
def editar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publicación editada con éxito', extra_tags='publicaciones')
            return redirect('publicaciones')
    else:
        form = PublicacionForm(instance=publicacion)
    
    publicaciones = Publicacion.objects.all()
    return render(request, 'publicaciones.html', {'publicaciones': publicaciones, 'form': form, 'edit_publicacion_id': publicacion.id})

@login_required
@directivo_required
def eliminar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, pk=publicacion_id)

    if request.method == 'POST' and 'delete_publicacion' in request.POST:
        # Eliminar la imagen asociada
        if publicacion.imagen:
            imagen_path = publicacion.imagen.path
            if os.path.exists(imagen_path):
                os.remove(imagen_path)

        # Eliminar la publicación
        publicacion.delete()

        # Agregar un mensaje de éxito con el tag 'publicaciones'
        messages.success(request, 'La publicación se eliminó correctamente.', extra_tags='publicaciones')
    else:
        # Agregar un mensaje de error con el tag 'publicaciones'
        messages.error(request, 'Se produjo un error al intentar eliminar la publicación.', extra_tags='publicaciones')

    # Redirigir a la página de publicaciones
    return redirect('publicaciones')


#-------------------------------------------------------------------------------------------------------------------
#PROYECTOS
#-------------------------------------------------------------------------------------------------------------------
from .models import Proyecto, Postulacion
from .forms import ProyectoForm, PostulacionForm

@login_required
@residente_required
def proyectos_postular(request):
    proyectos = Proyecto.objects.filter(disponible=True).order_by('-fecha_creacion')
    postulaciones_usuario = Postulacion.objects.filter(usuario=request.user)
    proyectos_postulados = postulaciones_usuario.values_list('proyecto_id', flat=True)

    if request.method == 'POST':
        proyecto_id = request.POST.get('proyecto_id')
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
        form = PostulacionForm(request.POST)
        if form.is_valid():
            postulacion = form.save(commit=False)
            postulacion.usuario = request.user
            postulacion.proyecto = proyecto
            postulacion.save()
            
            # Reducir el número de cupos disponibles
            proyecto.cupos -= 1
            if proyecto.cupos <= 0:
                proyecto.disponible = False
            proyecto.save()

            messages.success(request, 'Te has postulado al proyecto con éxito.', extra_tags='proyectos')
            return redirect('proyectos_postular')
        else:
            messages.error(request, 'Hubo un error con tu postulación.', extra_tags='proyectos')
    else:
        form = PostulacionForm()

    return render(request, 'proyectos_postular.html', {
        'proyectos': proyectos,
        'form': form,
        'proyectos_postulados': proyectos_postulados
    })

@login_required
def proyectos(request):
    proyectos = Proyecto.objects.all()
    form = ProyectoForm()  # Se crea una instancia del formulario ProyectoForm
    return render(request, 'proyectos.html', {'proyectos': proyectos, 'form': form})  # Se pasa 'form' al contexto

@login_required
@directivo_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto creado con éxito', extra_tags='proyectos')
            return redirect('proyectos')
    else:
        form = ProyectoForm()
    return render(request, 'proyectos.html', {'proyectos': Proyecto.objects.all(), 'form': form})

@login_required
@directivo_required
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto editado con éxito', extra_tags='proyectos')
            return redirect('proyectos')
    else:
        form = ProyectoForm(instance=proyecto)
    
    proyectos = Proyecto.objects.all()  # Obtener todos los proyectos
    return render(request, 'proyectos.html', {'proyectos': proyectos, 'form': form, 'edit_proyecto_id': proyecto.id})

@login_required
@directivo_required
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST' and 'delete_proyecto' in request.POST:
        proyecto.delete()
        messages.success(request, 'El proyecto se eliminó correctamente.', extra_tags='proyectos')
    else:
        messages.error(request, 'Se produjo un error al intentar eliminar el proyecto.', extra_tags='proyectos')
    return redirect('proyectos')

@login_required
@directivo_required
def cambiar_estado_postulacion(request, id):
    postulacion = get_object_or_404(Postulacion, id=id)
    proyecto = postulacion.proyecto
    if request.method == 'POST':
        estado = request.POST.get('estado')
        if estado == 'rechazado':
            # Eliminar la postulación
            postulacion.delete()
            
            # Incrementar el número de cupos disponibles
            proyecto.cupos += 1
            if proyecto.cupos > 0:
                proyecto.disponible = True
            proyecto.save()
            
            messages.success(request, 'Postulación rechazada y eliminada con éxito', extra_tags='proyectos')
        else:
            postulacion.estado = estado
            postulacion.save()
            messages.success(request, f'Postulación {estado} con éxito', extra_tags='proyectos')
    return redirect('proyectos')

#-------------------------------------------------------------------------------------------------------------------
#RESERVAS
#-------------------------------------------------------------------------------------------------------------------
from .models import Reserva, Espacio
from .forms import ReservaForm, EspacioForm

@login_required
@directivo_required
def gestionar_espacios(request):
    if request.method == 'POST':
        form = EspacioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Espacio creado exitosamente.')
            return redirect('gestionar_espacios')
    else:
        form = EspacioForm()

    espacios = Espacio.objects.all()
    return render(request, 'gestionar_espacios.html', {'form': form, 'espacios': espacios})

@login_required
@directivo_required
def editar_espacio(request):
    if request.method == 'POST':
        espacio_id = request.POST['espacio_id']
        espacio = get_object_or_404(Espacio, id=espacio_id)
        form = EspacioForm(request.POST, instance=espacio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Espacio editado exitosamente.')
            return redirect('gestionar_espacios')

@login_required
@directivo_required
def eliminar_espacio(request, espacio_id):
    espacio = get_object_or_404(Espacio, id=espacio_id)
    espacio.delete()
    messages.success(request, 'Espacio eliminado exitosamente.')
    return redirect('gestionar_espacios')

@login_required
@residente_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user

            # Obtiene la fecha de la reserva
            dia_reserva = reserva.dia_reserva

            # Obtiene todas las reservas del usuario en la misma fecha
            reservas_del_dia = Reserva.objects.filter(usuario=request.user, dia_reserva=dia_reserva)

            # Verifica si el usuario ya tiene 2 reservas en el mismo día
            if reservas_del_dia.count() >= 2:
                messages.error(request, 'No puede realizar más de 2 reservas en un día.')
                return redirect('reservas')
            else:
                reserva.save()
                messages.success(request, 'Reserva creada exitosamente.')
                return redirect('reservas')
    else:
        form = ReservaForm()
    return render(request, 'reservas.html', {'form': form})

@login_required
def reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    reservas_con_espacio = []

    for reserva in reservas:
        espacio = Espacio.objects.get(id=reserva.espacio_id)
        reservas_con_espacio.append({
            'reserva': reserva,
            'espacio_nombre': espacio.nombre
        })

    espacios = Espacio.objects.all()
    return render(request, 'reservas.html', {
        'reservas_con_espacio': reservas_con_espacio,
        'espacios': espacios
    })

@login_required
@residente_required
def eliminar_reserva(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    if reserva:
        reserva.delete()
        messages.success(request, 'Reserva eliminada exitosamente.')
    return redirect('reservas')

@login_required
@residente_required
def cargar_eventos(request):
    espacio_id = request.GET.get('espacio_id')
    dia = request.GET.get('dia')
    eventos = []
    horas_reservadas = []
    if espacio_id:
        reservas = Reserva.objects.filter(espacio_id=espacio_id)
        for reserva in reservas:
            hora_inicio = reserva.hora_reserva
            hora_fin = (datetime.combine(datetime.today(), hora_inicio) + timedelta(hours=1)).time()
            eventos.append({
                'title': f'{hora_inicio.strftime("%H:%M")}',
                'start': f"{reserva.dia_reserva}T{hora_inicio.strftime('%H:%M')}",
                'id': reserva.id,
            })
            if dia and reserva.dia_reserva.isoformat() == dia:
                horas_reservadas.append(hora_inicio.strftime('%H:%M'))

    return JsonResponse({'eventos': eventos, 'horas_reservadas': horas_reservadas})


#-------------------------------------------------------------------------------------------------------------------
#ACTIVIDADES
#-------------------------------------------------------------------------------------------------------------------
from .models import Actividad, Agendar
from .forms import ActividadForm, AgendarForm

@login_required
@residente_required
def actividades_agendar(request):
    actividades = Actividad.objects.filter(disponible=True).order_by('-fecha_creacion')
    actividades_agendadas = Agendar.objects.filter(usuario=request.user).values_list('actividad_id', flat=True)

    if request.method == 'POST':
        actividad_id = request.POST.get('actividad_id')
        actividad = get_object_or_404(Actividad, id=actividad_id)
        
        # Verificar si el usuario ya tiene agendada esta actividad
        if actividad.id in actividades_agendadas:
            messages.error(request, 'Ya has agendado esta actividad.', extra_tags='actividades')
            return redirect('actividades_agendar')

        # Crear el agendamiento
        agendar = Agendar.objects.create(
            usuario=request.user,
            actividad=actividad,
            estado='pendiente'  # Establecer el estado inicial, puede ser pendiente, aprobada, etc.
        )

        # Reducir el número de cupos disponibles
        actividad.cupos -= 1
        if actividad.cupos <= 0:
            actividad.disponible = False
        actividad.save()

        messages.success(request, 'Has agendado la actividad con éxito.', extra_tags='actividades')
        return redirect('actividades_agendar')

    return render(request, 'actividades_agendar.html', {
        'actividades': actividades,
        'actividades_agendadas': actividades_agendadas
    })

@login_required
def actividades(request):
    actividades = Actividad.objects.all()
    form = ActividadForm()  # Se crea una instancia del formulario ActividadForm
    return render(request, 'actividades.html', {'actividades': actividades, 'form': form})  # Se pasa 'form' al contexto

@login_required
@directivo_required
def crear_actividad(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actividad creada con éxito', extra_tags='actividades')
            return redirect('actividades')
    else:
        form = ActividadForm()
    return render(request, 'actividades.html', {'actividades': Actividad.objects.all(), 'form': form})

@login_required
@directivo_required
def editar_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    if request.method == 'POST':
        form = ActividadForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actividad editada con éxito', extra_tags='actividades')
            return redirect('actividades')
    else:
        form = ActividadForm(instance=actividad)
    
    actividades = Actividad.objects.all()  # Obtener todas las actividades
    return render(request, 'actividades.html', {'actividades': actividades, 'form': form, 'edit_actividad_id': actividad.id})

@login_required
@directivo_required
def eliminar_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    if request.method == 'POST' and 'delete_actividad' in request.POST:
        actividad.delete()
        messages.success(request, 'La actividad se eliminó correctamente.', extra_tags='actividades')
    else:
        messages.error(request, 'Se produjo un error al intentar eliminar la actividad.', extra_tags='actividades')
    return redirect('actividades')

@login_required
@directivo_required
def cambiar_estado_agendar(request, id):
    agendar = get_object_or_404(Agendar, id=id)
    actividad = agendar.actividad
    if request.method == 'POST':
        estado = request.POST.get('estado')
        if estado == 'rechazado':
            # Eliminar la agenda
            agendar.delete()

            # Incrementar el número de cupos disponibles
            actividad.cupos += 1
            if actividad.cupos > 0:
                actividad.disponible = True
            actividad.save()

            messages.success(request, 'Se cambió el estado del agendamiento a Rechazado', extra_tags='actividades')
        else:
            agendar.estado = estado
            agendar.save()
            messages.success(request, f'Agenda {estado} con éxito', extra_tags='actividades')

    return redirect('actividades')
