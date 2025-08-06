# your_project_name/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import users.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djang_website.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                users.routing.websocket_urlpatterns
            )
        )
    ),
})

"""
import os
import django

# Django ayarlarını yükleyin
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djang_website.settings')
django.setup()  # Django ayarlarını yükleyin

# Gerekli modülleri içe aktarın
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator  # WebSocket için güvenlik kontrolü
from django.urls import path
import users.routing  # Kullanıcıların routing dosyasını doğru bir şekilde içe aktarın

# Uygulama yapılandırması
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP istekleri için ASGI uygulamasını kullanın
    "websocket": AllowedHostsOriginValidator(  # WebSocket bağlantıları için güvenlik kontrolü
        AuthMiddlewareStack(  # Kullanıcı doğrulama işlemi yapılacak
            URLRouter(
                users.routing.websocket_urlpatterns  # WebSocket URL'lerini kullanıcı routing dosyasından alıyoruz
            )
        )
    ),
})
CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [('127.0.0.1', 6379)],  # Redis bağlantısı
            },
        },
    }
"""