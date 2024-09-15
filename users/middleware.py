from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import LockScreenStatus

class LockScreenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Middleware çalıştı!")

        if not hasattr(request, 'user') or not request.user.is_authenticated:
            print("bitti")
            # Eğer request objesinde 'user' özelliği yoksa veya oturum açık değilse
            return self.get_response(request)

        lock_status = get_object_or_404(LockScreenStatus, user=request.user)

        if lock_status.is_locked and not self.is_unlock_url(request.path_info):
            print("kilitli")
            return redirect('users:unlock')

        response = self.get_response(request)
        return response

    def is_unlock_url(self, url):
        # Burada unlock URL'si kontrolü yapılmalı
        unlock_url = reverse('users:unlock')
        if url == reverse('users:unlock'):

            return url == unlock_url
        elif url == reverse('users:logout'):
            return url == reverse('users:logout')
    def is_logout_url(self, url):
        # Burada unlock URL'si kontrolü yapılmalı
        unlock_url = reverse('users:logout')
        return url == unlock_url