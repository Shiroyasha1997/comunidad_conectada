import random
import string
from django.http import HttpResponse
from django.utils import timezone
from django.utils.timezone import now
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm, IngresarForm, RegistroForm, PerfilForm
from .models import SolicitudInscripcion, CustomUser, Certificado

CustomUser = get_user_model()

#-------------------------------------------------------------------------------------------------------------------
#PAGINA DE INICIO
#-------------------------------------------------------------------------------------------------------------------
def inicio(request):
    es_admin = request.user.is_staff
    es_directivo = request.user.groups.filter(name='Directivo').exists()
    es_residente = request.user.groups.filter(name='Residente').exists()
    return render(request, 'inicio.html', {'es_admin': es_admin, 'es_directivo': es_directivo, 'es_residente': es_residente})


#-------------------------------------------------------------------------------------------------------------------
#AUTENTICACION
#-------------------------------------------------------------------------------------------------------------------
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')  # Redirige al inicio después de cerrar sesión

def ingresar(request):
    if request.method == 'POST':
        form = IngresarForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Intentar autenticar al usuario
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Si el usuario es administrador de Django, redirigir al panel de administración
                if user.is_staff:
                    login(request, user)
                    return redirect('inicio')  # Redirigir al panel de administración de Django

                # Si el usuario no es administrador, verificar los grupos
                elif user.groups.filter(name='Directivo').exists():
                    login(request, user)
                    return redirect('inicio')  # Redirigir a la página de inicio de Directivos

                elif user.groups.filter(name='Residente').exists():
                    login(request, user)
                    return redirect('inicio')  # Redirigir a la página de inicio de Residentes

            # Si la autenticación falla, mostrar un mensaje de error
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else:
        form = IngresarForm()
    return render(request, 'ingresar.html', {'form': form})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.save()

            messages.success(request, 'Tu solicitud de registro ha sido enviada. Espera la aprobación del directivo.')
            return redirect('inicio')
        else:
            messages.error(request, 'Hubo un error al procesar tu solicitud. Por favor, inténtalo de nuevo.')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def solicitudes(request):
    if request.user.groups.filter(name='Directivo').exists():
        solicitudes = SolicitudInscripcion.objects.all()
        return render(request, 'solicitudes.html', {'solicitudes': solicitudes})
    else:
        return redirect('inicio')  # Redirigir a la página de inicio si el usuario no es un directivo

@login_required
def aprobar_solicitud(request, solicitud_id):
    if request.user.groups.filter(name='Directivo').exists():
        solicitud = SolicitudInscripcion.objects.get(id=solicitud_id)
        solicitud.estado = 'aceptada'
        solicitud.fecha_aprobacion = timezone.now()

        # Generar una contraseña aleatoria
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        # Enviar la contraseña por correo electrónico
        subject = 'Bienvenido a nuestra comunidad'
        message = f'Hola {solicitud.first_name}, tu solicitud ha sido aprobada.\n\nUsuario: {solicitud.username}\nContraseña: {password}'
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

        messages.success(request, "La solicitud ha sido aprobada. Se ha enviado un correo electrónico con los detalles de inicio de sesión.")
        return redirect('solicitudes')
    else:
        messages.error(request, "No tienes permisos para aprobar esta solicitud.")
        return redirect('inicio')

@login_required
def rechazar_solicitud(request, solicitud_id):
    if request.user.groups.filter(name='Directivo').exists():
        solicitud = SolicitudInscripcion.objects.get(id=solicitud_id)
        solicitud.estado = 'rechazada'
        solicitud.fecha_rechazo = timezone.now()
        solicitud.save()

        # Enviar un correo electrónico informando sobre el rechazo
        subject = 'Solicitud de registro rechazada'
        message = f'Hola {solicitud.first_name}, lamentamos informarte que tu solicitud de registro ha sido rechazada.'
        from_email = 'comunidad_conectada@outlook.com'  # Ingresa tu dirección de correo
        to_email = [solicitud.email]
        send_mail(subject, message, from_email, to_email)

        # Eliminar la solicitud rechazada de la base de datos
        solicitud.delete()

        messages.success(request, "La solicitud ha sido rechazada. Se ha enviado un correo electrónico al solicitante.")
        return redirect('solicitudes')
    else:
        messages.error(request, "No tienes permisos para rechazar esta solicitud.")
        return redirect('inicio')

@login_required
def perfil(request):
    user = request.user
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado!')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
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
            update_session_auth_hash(request, user)  # Importante para mantener al usuario autenticado
            messages.success(request, '¡Tu contraseña ha sido actualizada!')
            return redirect('perfil')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error, extra_tags='password_error')
            return redirect('perfil')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


#-------------------------------------------------------------------------------------------------------------------
#CERTIFICADOS
#-------------------------------------------------------------------------------------------------------------------
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

@login_required
def certificados(request):
    certificados_usuario = Certificado.objects.filter(usuario=request.user)
    return render(request, 'certificados.html', {'certificados_usuario': certificados_usuario})

@login_required
def descargar_certificado(request, certificado_id):
    certificado = Certificado.objects.get(id=certificado_id, usuario=request.user)
    response = generar_certificado_pdf(certificado)
    response['Content-Disposition'] = 'attachment; filename="certificado_residencia.pdf"'
    return response

def guardar_certificado(request):
    # Obtener el usuario actual
    user = request.user

    # Crear un certificado para el usuario
    certificado = Certificado(usuario=user, detalle="Certificado de Residencia")

    # Generar el PDF del certificado
    certificado_pdf = generar_certificado_pdf(certificado)


    import uuid
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

    # Firma y sello (opcional)
    contenido.append(Paragraph("Firma:", contenido_style))
    contenido.append(Spacer(1, 48))
    contenido.append(Paragraph("__________________________", contenido_style))
    contenido.append(Paragraph("Firma Autorizada", contenido_style))
    contenido.append(Spacer(1, 12))

    contenido.append(Paragraph("Sello:", contenido_style))
    contenido.append(Spacer(1, 48))
    contenido.append(Paragraph("__________________________", contenido_style))
    contenido.append(Paragraph("Sello Oficial", contenido_style))

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
def pago_exitoso(request):
    return render(request, 'pago_exitoso.html', {
        'options': ['Ver certificado', 'Descargar certificado', 'Enviar al correo']
    })