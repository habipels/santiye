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
 path('update/sitebloglist/', views.blog_duzenle_api, name='blog_duzenle_api'),
 path('del/sitebloglist/', views.blog_sil_api, name='blog_sil_api'),
 #######
  path('constructionsite/<int:id>/', views.santiye_kalemleri_api, name='santiye_kalemleri_api'),
 #######
 path('create/constructionsite/', views.santiyeye_kalem_ekle_api, name='santiyeye_kalem_ekle_api'),
 path('update/constructionsite/<int:id>/', views.santiye_kalemleri_duzenle_api, name='santiye_kalemleri_duzenle_api'),
 path('del/constructionsite/<int:id>/', views.kalem_sil_api, name='kalem_sil_api'),
 #######
 path('siteblogconstruction/', views.santiye_kalem_ve_blog_api, name='santiye_kalem_ve_blog_api'),
 path('progresstracking/<int:id>/', views.blogtan_kaleme_ilerleme_takibi_api, name='blogtan_kaleme_ilerleme_takibi_api'),
]
#
