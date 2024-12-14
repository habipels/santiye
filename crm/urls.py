from django.urls import path
from . import views
from django.views.static import serve
from django.urls import re_path, path
from django.conf import settings  # settings.py'den BASE_DIR'i al
import os
from . import views
app_name = "crm"
#
# Dil kodu eklenmeyen yol
urlpatterns = [
#
    path("", views.crm_dashboard, name="crm_dashboard"),#
    path("dairedetayi", views.crm_dairedetayi, name="crm_dairedetayi"),
    path("daire_ekle", views.daire_ekle, name="daire_ekle"),
    path("daireyonetimi", views.crm_daireyonetimi, name="crm_daireyonetimi"),
    path("dokumanlar", views.crm_evr, name="crm_evr"),
    path("dokumanyonetimi", views.crm_evrak_dokuman, name="crm_evrak_dokuman"),
    path("musteridetayi/<int:id>", views.crm_musteri_detayi, name="crm_musteri_detayi"),
    path("get_bloglar", views.get_bloglar, name="get_bloglar"),
    path("get_katlar", views.get_katlar, name="get_katlar"),
    path("get_daireler", views.get_daireler, name="get_daireler"),
    
    path("musteriyonetimi", views.musteri_sayfasi, name="musteri_sayfasi"),
    path("musteri_ekle", views.musteri_ekleme, name="musteri_ekleme"),
    path("musteri_silme", views.musteri_silme, name="musteri_silme"),
    path("musteri_duzenleme", views.musteri_duzenleme, name="musteri_duzenleme"),
    path("daire_musteriye_ata", views.daire_musteriye_ata, name="daire_musteriye_ata"),
    
    path("taleplervesikayetler", views.crm_talepler_sikayetler, name="crm_talepler_sikayetler"),
    path("talepsikayetolustur", views.talep_veya_sikayet_olustur, name="talep_veya_sikayet_olustur"),
    
    path("teklifolustur", views.crm_teklif_olustur, name="crm_teklif_olustur"),
    path("teklifyonetimi", views.crm_teklif_yonetimi, name="crm_teklif_yonetimi"),
]
#
