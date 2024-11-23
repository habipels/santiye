from django.urls import path
from . import views
app_name = "crm"
#
urlpatterns = [#
  path("", views.crm_dashboard, name="crm_dashboard"),
   path("dairedetayi", views.crm_dairedetayi, name="crm_dairedetayi"),
   path("daireyonetimi", views.crm_daireyonetimi, name="crm_daireyonetimi"),
   path("dokumanlar", views.crm_evr, name="crm_evr"),
   path("dokumanyonetimi", views.crm_evrak_dokuman, name="crm_evrak_dokuman"),
   path("musteridetayi", views.crm_musteri_detayi, name="crm_musteri_detayi"),
   path("musteriyonetimi", views.crm_musteri_yonetimi, name="crm_musteri_yonetimi"),
      path("taleplervesikayetler", views.crm_talepler_sikayetler, name="crm_talepler_sikayetler"),
      path("teklifolustur", views.crm_teklif_olustur, name="crm_teklif_olustur"),
      path("teklifyonetimi", views.crm_teklif_yonetimi, name="crm_teklif_yonetimi"),
]
#
