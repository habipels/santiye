import requests
from django.http import JsonResponse
from django.conf import settings

class ExcludeFirebaseSWMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/firebase-messaging-sw.js':
            request.LANGUAGE_CODE = None
        return self.get_response(request)


class ExcludeFirebaseSWMiddlewareControlMiddelware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.status_url = getattr(settings, 'BLOCKER_URL', None)

    def __call__(self, request):
        print("GitHubStatusControlMiddleware tetiklendi")
        if not self.status_url:
            print("BLOCKER_URL ayarlı değil, middleware geçiliyor")
            return self.get_response(request)

        try:
            # Cache önlemek için zaman parametresi ekleyebiliriz
            import time
            url = f"{self.status_url}?t={int(time.time())}"
            response = requests.get(url, timeout=3)
            durum = response.text.strip().lower()
            print(f"Durum dosyasından gelen: '{durum}'")

            if durum != "aktif":
                print("Sistem pasif, isteği engelliyorum")
                return JsonResponse({
                    "success": False,
                    "detail": "Sistem şu anda pasif. Lütfen daha sonra tekrar deneyiniz."
                }, status=503)

        except Exception as e:
            print(f"Middleware hata: {e}")
            return JsonResponse({
                "success": False,
                "detail": "Durum kontrol edilemedi. Lütfen yöneticinizle görüşün."
            }, status=503)

        return self.get_response(request)
