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

        # ✅ STATİK / MEDIA / ADMIN BYPASS
        if (
            request.path.startswith('/static/') or
            request.path.startswith('/media/') or
            request.path.startswith('/uploads/') or
            request.path.startswith('/admin/')
        ):
            return self.get_response(request)

        if not self.status_url:
            return self.get_response(request)

        try:
            response = requests.get(self.status_url, timeout=3)
            data = response.json()
            durum = str(data.get("status", "")).lower()

            if durum != "aktif":
                return JsonResponse({
                    "success": False,
                    "detail": data.get(
                        "hata_mesajı",
                        "Sistem şu anda pasif."
                    )
                }, status=503)

        except Exception:
            return JsonResponse({
                "success": False,
                "detail": "Durum kontrol edilemedi."
            }, status=503)

        return self.get_response(request)
