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
 path('siteprojectlist/', views.santiye_projesi_liste, name='santiye_projesi_liste'),
#######
 path('create/siteprojectlist/', views.santiye_ekleme_api, name='santiye_ekleme_api'),
 path('del/siteprojectlist/', views.santiye_projesi_sil_api, name='santiye_projesi_sil_api'),
 path('update/siteprojectlist/', views.santiye_projesi_duzenle_api, name='santiye_projesi_duzenle_api'),
 #######
 path('sitebloglist/<int:id>/', views.santiye_projesi_bloklar_ekle_api, name='santiye_projesi_bloklar_ekle_api'),
 #######
 path('create/sitebloglist/', views.blog_ekle_api, name='blog_ekle_api'),
 #path('del/siteprojectlist/', views.santiye_projesi_sil_api, name='santiye_projesi_sil_api'),
 #path('update/siteprojectlist/', views.santiye_projesi_duzenle_api, name='santiye_projesi_duzenle_api'),
 #######
]
#
