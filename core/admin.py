from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, SolicitudInscripcion, Certificado, Publicacion, Proyecto, Postulacion, Reserva, Espacio, Actividad, Agendar

CustomUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = '__all__'

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = '__all__'

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'cargo', 'run', 'direccion', 'telefono', 'fecha_nacimiento', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('cargo', 'run', 'direccion', 'telefono', 'fecha_nacimiento')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SolicitudInscripcion)
admin.site.register(Certificado)

class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'fecha_creacion')
    search_fields = ('titulo', 'detalle')
    list_filter = ('tipo', 'fecha_creacion')

admin.site.register(Publicacion, PublicacionAdmin)
admin.site.register(Proyecto)
admin.site.register(Postulacion)
admin.site.register(Reserva)
admin.site.register(Espacio)

admin.site.register(Actividad)
admin.site.register(Agendar)