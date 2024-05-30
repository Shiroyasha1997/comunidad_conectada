from django import forms
from .models import SolicitudInscripcion, CustomUser
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.forms import DateInput

class IngresarForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nombre de Usuario", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Contraseña")

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
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'run': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': DateInput(attrs={'class': 'form-control'}),
        }

class PerfilForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
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
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'run': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': DateInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if 'password' in self.fields:
                self.fields.pop('password')  # Remover el campo de contraseña

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
