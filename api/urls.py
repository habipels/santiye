from django.urls import path 
from . import views
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Pastebin API')
app_name = "api"

from rest_framework_swagger.views import get_swagger_view
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Dokümantasyonu",
        default_version='v1',
        description="API Dokümantasyonu",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
#schema_view = get_swagger_view(title='API Dokümantasyonu')
urlpatterns = [#deneme
 # Diğer URL'leriniz... kullanicilari
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
 path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
 path('dashboard/', views.homepage_api, name='homepage-api'),
 path('projecttype/', views.proje_tipi_api, name='proje_tipi_api'),
 path('users/', views.kullanicilari, name='kullanicilari'),
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
 path('create/progresspayment/', views.hakedis_ekle_api, name='hakedis_ekle_api'),
 path('update/progresspayment/', views.hakedis_duzenle_api, name='hakedis_duzenle_api'),
 path('del/progresspayment/', views.hakedis_silme_api, name='hakedis_silme_api'),
 #######
 #######
 path('myfiles/', views.depolama_sistemim, name='depolama_sistemim'),
 #######
 path('create/myfiles/', views.klasor_olustur, name='klasor_olustur'),
 path('update/myfiles/', views.klasor_yeniden_adlandir_api, name='klasor_yeniden_adlandir_api'),
 path('del/myfiles/', views.klasor_sil_api, name='klasor_sil_api'),
 #######
  #######
 path('inmyfiles/<int:id>/', views.klasore_gir_api, name='klasore_gir_api'),
 #######
  #######
 #path('files/', views.dosya_ekle_api, name='dosya_ekle_api'),
 #######
 path('create/files/', views.dosya_ekle_api, name='dosya_ekle_api'),
 path('del/files/', views.dosya_sil_api, name='dosya_sil_api'),
 path('safe/files/', views.dosya_geri_getir_api, name='dosya_geri_getir_api'),
 #######
#######
 path('doc/files/', views.dokumanlar_api, name='dokumanlar_api'),
 path('media/files/', views.media_dosyalari_api, name='media_dosyalari_api'),
 path('time/files/', views.zamana_dosyalari_api, name='zamana_dosyalari_api'),
 path('statusdel/files/', views.silinen_dosyalari_api, name='silinen_dosyalari_api'),
 #######
 #/thingstodo
  #######
 path('thingstodo/', views.yapilacaklar_api, name='yapilacaklar_api'),
 path('statusthingstodo/', views.yapilacaklar_durum_bilgisi, name='yapilacaklar_durum_bilgisi'),
 #######
 path('create/thingstodo/', views.yapilacalar_ekle_api, name='yapilacalar_ekle_api'),

 path('del/thingstodo/', views.yapilacalar_sil, name='yapilacalar_sil'),
 path('statusset/thingstodo/', views.yapilacak_durumu_yenileme, name='yapilacak_durumu_yenileme'),
 path('update/thingstodo/', views.yapilacalar_duzenle_api, name='yapilacalar_duzenle_api'),
 #######
   #######
 path('todo/', views.yapilacaklar_timeline_api, name='yapilacaklar_timeline_api'),
 #######
 path('create/todo/', views.yapilacalar_time_line_ekle_api, name='yapilacalar_time_line_ekle_api'),
 path('del/todo/', views.yapilacalar_time_line_sil_api, name='yapilacalar_time_line_sil_api'),
 path('update/todo/', views.yapilacaklar_time_line_duzenle_api, name='yapilacaklar_time_line_duzenle_api'),
 #######
    path('report/<int:id>', views.santiye_raporu_api, name='santiye_raporu_api'),
    path('layer/', views.api_katman_sayfasi, name="api_katman_sayfasi"),
    path('create/layer/', views.api_katman_ekle, name="api_katman_ekle"),
    path('del/layer/', views.api_katman_sil, name="api_katman_sil"),
    path('set/layer/', views.api_katman_duzenle, name="api_katman_duzenle"),

    path('weather', views.hava_durumu_api, name='hava_durumu_api'),

]#
#
