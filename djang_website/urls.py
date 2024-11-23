"""django_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import handler404
urlpatterns = [
    path("", include('main.urls', namespace='main')),
    path("accounting/", include('muhasebe.urls', namespace='muhasebe')),
    path('admin/', admin.site.urls),
    path('users/',include("users.urls", namespace='users')),
    path('crm/',include("crm.urls", namespace='crm')),
    path('biadago/api/',include("api.urls", namespace='api')),
    path('', include('pwa.urls')),  # PWA URL - Tolga

]


urlpatterns += i18n_patterns (
    path("", include('main.urls', namespace='main')),
    path('users/',include("users.urls", namespace='users')),
    path('crm/',include("crm.urls", namespace='crm')),
    path("accounting/", include('muhasebe.urls', namespace='muhasebe')),
    
)
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "main.views.page_not_found_view"
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
