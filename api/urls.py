from django.urls import path
from . import views
app_name = "api"
urlpatterns = [#
 path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
 path('dashboard/', views.homepage_api, name='homepage-api'),
 path('projecttype/', views.proje_tipi_api, name='proje_tipi_api'),
 #######
 path('create/projecttype/', views.proje_ekleme_api, name='proje_ekleme_api'),
 path('del/projecttype/', views.proje_adi_sil, name='proje_adi_sil'),
 path('update/projecttype/', views.proje_duzenle, name='proje_duzenle'),
 #######
]
#
