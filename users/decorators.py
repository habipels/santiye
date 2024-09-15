from django.shortcuts import redirect

def user_not_authenticated(function=None, redirect_url='/'):
    """
    Decorator for views that checks that the user is NOT logged in, redirecting
    to the homepage if necessary by default.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
                
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator

from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps

def lock_screen_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            # Eğer request objesinde 'user' özelliği yoksa veya oturum açık değilse
            return view_func(request, *args, **kwargs)

        lock_status = request.user.lockscreenstatus
        if lock_status.is_locked:
            # Lock screen aktifse, unlock ekranına yönlendir
            if request.path_info != reverse('users:unlock'):
                return redirect('users:unlock')

        return view_func(request, *args, **kwargs)

    return _wrapped_view