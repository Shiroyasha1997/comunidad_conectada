from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from functools import wraps

def residente_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.groups.filter(name='Residente').exists():
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def directivo_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.groups.filter(name='Directivo').exists():
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
