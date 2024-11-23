from django.urls import path
from . import views
app_name = "crm"
#
urlpatterns = [#
  path("", views.crm_dashboard, name="crm_dashboard"),
   path("crmdairedetayi", views.crm_dairedetayi, name="crm_dairedetayi"),
   path("crm_daireyonetimi", views.crm_daireyonetimi, name="crm_daireyonetimi"),
   path("crm_evr", views.crm_evr, name="crm_evr"),
   path("crm_evrak_dokuman", views.crm_evrak_dokuman, name="crm_evrak_dokuman"),
   path("crm_musteri_detayi", views.crm_musteri_detayi, name="crm_musteri_detayi"),
   path("crm_musteri_yonetimi", views.crm_musteri_yonetimi, name="crm_musteri_yonetimi"),
      path("crm_talepler_sikayetler", views.crm_talepler_sikayetler, name="crm_talepler_sikayetler"),
      path("crm_teklif_olustur", views.crm_teklif_olustur, name="crm_teklif_olustur"),
      path("crm_teklif_yonetimi", views.crm_teklif_yonetimi, name="crm_teklif_yonetimi"),
]
#
