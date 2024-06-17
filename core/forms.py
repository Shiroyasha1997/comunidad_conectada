from django import forms
from .models import SolicitudInscripcion, CustomUser
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.forms import DateInput

class IngresarForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nombre de Usuario", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Contraseña")

class DateInput(forms.DateInput):
    input_type = 'date'

from datetime import datetime, timedelta

class RegistroForm(forms.ModelForm):
    class Meta:
        model = SolicitudInscripcion
        fields = ['username', 'first_name', 'last_name', 'email', 'run', 'direccion', 'telefono', 'fecha_nacimiento']
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'run': 'RUN',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'fecha_nacimiento': 'Fecha de Nacimiento',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
            'run': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'fecha_nacimiento': DateInput(attrs={'class': 'form-control', 'required': 'required'}),
        }
        error_messages = {
            'username': {
                'unique': 'Este nombre de usuario ya está en uso. Por favor, elige otro.',
            },
            'run': {
                'unique': 'Este RUN ya está registrado. Por favor, ingresa otro.',
            },
            'fecha_nacimiento': {
                'min_age': 'Debes tener al menos 14 años para registrarte.',
            }
        }

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        edad_minima = datetime.now().date() - timedelta(days=14*365)  # Calcular fecha hace 14 años
        if fecha_nacimiento > edad_minima:
            raise forms.ValidationError(self.Meta.error_messages['fecha_nacimiento']['min_age'])
        return fecha_nacimiento

from django.contrib.auth.forms import UserChangeForm

class PerfilForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        disable_email = kwargs.pop('disable_email', False)
        disable_username = kwargs.pop('disable_username', False)  # Nuevo parámetro para deshabilitar username
        super().__init__(*args, **kwargs)
        
        if 'password' in self.fields:
            self.fields.pop('password')
        for field in self.fields:
            self.fields[field].required = True

        if disable_email:
            self.fields['email'].widget.attrs['readonly'] = True
        
        if disable_username:
            self.fields['username'].widget.attrs['readonly'] = True  # Deshabilitar el campo de username

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'run', 'direccion', 'telefono']
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'run': 'RUN',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'run': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'username': {
                'unique': 'Este nombre de usuario ya está en uso. Por favor, elige otro.',
            },
            'run': {
                'unique': 'Este RUN ya está en uso. Por favor, ingresa otro.',
            }
        }

    def clean_password(self):
        return self.initial.get('password')

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Contraseña Actual",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label="Confirmar Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

from .models import Publicacion
from django.core.validators import MaxLengthValidator

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['tipo', 'titulo', 'detalle', 'imagen']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '60'}),
            'detalle': forms.Textarea(attrs={'class': 'form-control', 'maxlength': '350'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super(PublicacionForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].required = True
        self.fields['titulo'].required = True
        self.fields['detalle'].required = True
        self.fields['imagen'].required = False
        self.fields['titulo'].validators.append(MaxLengthValidator(60))
        self.fields['detalle'].validators.append(MaxLengthValidator(350))


from django import forms
from django.core.validators import MaxLengthValidator
from .models import Proyecto, Postulacion

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'presupuesto', 'cupos', 'disponible']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'maxlength': '500'}),
            'presupuesto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cupos': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProyectoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        self.fields['descripcion'].required = True
        self.fields['presupuesto'].required = True
        self.fields['cupos'].required = True
        self.fields['nombre'].validators.append(MaxLengthValidator(100))
        self.fields['descripcion'].validators.append(MaxLengthValidator(500))


class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ['detalle']
        widgets = {
            'detalle': forms.Textarea(attrs={'class': 'form-control', 'maxlength': '500'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostulacionForm, self).__init__(*args, **kwargs)
        self.fields['detalle'].required = True
        self.fields['detalle'].validators.append(MaxLengthValidator(500))

from django import forms
from .models import Espacio, Reserva

class EspacioForm(forms.ModelForm):
    class Meta:
        model = Espacio
        fields = ['nombre', 'descripcion', 'dias_disponibles', 'horario_inicio', 'horario_fin']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'dias_disponibles': forms.TextInput(attrs={'class': 'form-control'}),
            'horario_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'horario_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['hora_reserva', 'dia_reserva', 'espacio']
        widgets = {
            'hora_reserva': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'dia_reserva': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'espacio': forms.Select(attrs={'class': 'form-control'}),
        }