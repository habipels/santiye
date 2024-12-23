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
    path("dairedetayi/<int:id>", views.crm_dairedetayi, name="crm_dairedetayi"),
    path("daire_ekle", views.daire_ekle, name="daire_ekle"),
    path("daire_evrak_ekle", views.daire_evrak_ekle, name="daire_evrak_ekle"),
    path("daireyonetimi", views.crm_daireyonetimi, name="crm_daireyonetimi"),
    path("dokumanlar", views.crm_evr, name="crm_evr"),
    path("dokumanyonetimi", views.crm_evrak_dokuman, name="crm_evrak_dokuman"),
    path("musteridetayi/<int:id>", views.crm_musteri_detayi, name="crm_musteri_detayi"),
    path("get_bloglar", views.get_bloglar, name="get_bloglar"),
    path("get_katlar", views.get_katlar, name="get_katlar"),
    path("get_daireler", views.get_daireler, name="get_daireler"),
    path("get_talep", views.get_talep, name="get_talep"),
    path("get_daire_evraklari", views.get_daire_evraklari, name="get_daire_evraklari"),
    
    path("musteriyonetimi", views.musteri_sayfasi, name="musteri_sayfasi"),
    path("musteri_ekle", views.musteri_ekleme, name="musteri_ekleme"),
    path("musteri_silme", views.musteri_silme, name="musteri_silme"),
    path("musteri_duzenleme", views.musteri_duzenleme, name="musteri_duzenleme"),
    path("daire_musteriye_ata", views.daire_musteriye_ata, name="daire_musteriye_ata"),
    path("talep_veya_sikayet_olustur_musteri_detayi", views.talep_veya_sikayet_olustur_musteri_detayi, name="talep_veya_sikayet_olustur_musteri_detayi"),
    path("talep_veya_sikayet_duzenle_musteri_detayi", views.talep_veya_sikayet_duzenle_musteri_detayi, name="talep_veya_sikayet_duzenle_musteri_detayi"),
    path("musterinotu", views.museri_notu_ekle, name="museri_notu_ekle"),
    path("duzenle", views.daire_musteriye_duzenle, name="daire_musteriye_duzenle"),
    path("sil", views.daire_musteriye_sil, name="daire_musteriye_sil"),
    path("baglama_onayla", views.daire_musteriye_onayla, name="daire_musteriye_onayla"),
    path("musteri_bilgisi_views/", views.musteri_bilgisi_views, name="musteri_bilgisi_views"),
    path("crm_teklif_olustur_gonder", views.crm_teklif_olustur_gonder, name="crm_teklif_olustur_gonder"),
    path("teklif_silme", views.teklif_silme, name="teklif_silme"),
    path("teklif_duzenleme/<int:id>", views.teklif_duzenleme, name="teklif_duzenleme"),
    path("crm_teklif_duzenle_gonder", views.crm_teklif_duzenle_gonder, name="crm_teklif_duzenle_gonder"),
    path("musteri_notu_sil", views.musteri_notu_sil, name="musteri_notu_sil"),
    path("musteri_notu_duzenle", views.musteri_notu_duzenle, name="musteri_notu_duzenle"),

#

    path("taleplervesikayetler", views.crm_talepler_sikayetler, name="crm_talepler_sikayetler"),
    path("talepsikayetolustur", views.talep_veya_sikayet_olustur, name="talep_veya_sikayet_olustur"),
    path("taleplervesikayetlerduzenle", views.talep_veya_sikayet_duzenle, name="talep_veya_sikayet_duzenle"),
    path("taleplervesikayetlersil", views.talep_veya_sikayet_sil, name="talep_veya_sikayet_sil"),

    path("teklifolustur", views.crm_teklif_olustur, name="crm_teklif_olustur"),
    path("teklifyonetimi", views.crm_teklif_yonetimi, name="crm_teklif_yonetimi"),
]
#
