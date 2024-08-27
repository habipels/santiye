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
 path('saveprogresstracking/', views.ilerleme_kaydet_api, name='ilerleme_kaydet_api'),
 ##
 path('projectpage/', views.projeler_sayfasi_api, name='projeler_sayfasi_api'),
 #######
 path('create/projectpage/', views.proje_ekle_api, name='proje_ekle_api'),
 path('update/projectpage/', views.proje_duzenle_bilgi_api, name='proje_duzenle_bilgi_api'),
 path('del/projectpage/', views.proje_silme_api, name='proje_silme_api'),
 #######
  ##
 path('subcontractors/', views.taseron_sayfasi_api, name='taseron_sayfasi_api'),
 #######
 path('create/subcontractors/', views.taseron_ekle_api, name='taseron_ekle_api'),
 path('update/subcontractors/', views.taseron_duzelt_api, name='taseron_duzelt_api'),
 path('del/subcontractors/', views.taseron_silme_api, name='taseron_silme_api'),
 #######
   ##
 path('contracts/', views.sozlesmeler_sayfasi_api, name='sozlesmeler_sayfasi_api'),
 #######
 path('create/contracts/', views.sozlesme_ekle_api, name='sozlesme_ekle_api'),
 path('update/contracts/', views.sozlesme_duzenle_api, name='sozlesme_duzenle_api'),
 path('del/contracts/', views.sozlesme_silme_api, name='sozlesme_silme_api'),
 #######
 path('progresspayment/', views.hakedis_sayfasi_api, name='hakedis_sayfasi_api'),
 #######
 #path('create/contracts/', views.sozlesme_ekle_api, name='sozlesme_ekle_api'),
 #path('update/contracts/', views.sozlesme_duzenle_api, name='sozlesme_duzenle_api'),
 #path('del/contracts/', views.sozlesme_silme_api, name='sozlesme_silme_api'),
 #######
]
#
