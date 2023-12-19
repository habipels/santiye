from django.urls import path
from . import views
app_name = "accounting"
urlpatterns = [
    #kasa işlemleri
    path("till", views.kasa_viev, name="kasa"),
    path("addtill", views.kasa_ekle, name="kasa_ekle"),
    path("deltill", views.kasa_sil, name="kasa_sil"),
    path("settill", views.kasa_duzenle, name="kasa_duzenle"),
    #kasa işlemleri
    #gelir kategorileri
    path("incomecategory", views.gelir_kategorisi_tipleri, name="gelir_kategorisi_tipleri"),
    path("addcomecategory", views.gelir_kategorisi_ekleme, name="gelir_kategorisi_ekleme"),
    path("delcomecategory", views.gelir_kategoisi_sil, name="gelir_kategoisi_sil"),
    path("setcomecategory", views.gelir_kategorisi_duzenle, name="gelir_kategorisi_duzenle"),
    #gelir kategorileri
    #gider kategorileri
    path("inwcategory", views.gider_kategorisi_tipleri, name="gider_kategorisi_tipleri"),
    path("addwcategory", views.gider_kategorisi_ekleme, name="gider_kategorisi_ekleme"),
    path("delwcategory", views.gider_kategoisi_sil, name="gider_kategoisi_sil"),
    path("setwcategory", views.gider_kategorisi_duzenle, name="gider_kategorisi_duzenle"),
    #gider kategorileri
    #cari işlemleri
    path("current", views.cari_viev, name="cari"),
    path("addcurrent", views.cari_ekle, name="cari_ekle"),
    path("delcurrent", views.cari_sil, name="cari_sil"),
    path("setcurrent", views.cari_duzenle, name="cari_duzenle"),
    #cari işlemleri
    #gelir etiket işlemleri
    path("incometag", views.gelir_etiketi_tipleri, name="gelir_etiketi_tipleri"),
    path("addincometag", views.gelir_etiketi_ekleme, name="gelir_etiketi_ekleme"),
    path("delincometag", views.gelir_etiketi_sil, name="gelir_etiketi_sil"),
    path("setincometag", views.gelir_etiketi_duzenle, name="gelir_etiketi_duzenle"),
    #gelir etiket işlemleri
    #gider etiketleri
    path("expensetag", views.gider_etiketi_tipleri, name="gider_etiketi_tipleri"),
    path("addexpensetag", views.gider_etiketi_ekleme, name="gider_etiketi_ekleme"),
    path("delexpensetag", views.gider_etiketi_sil, name="gider_etiketi_sil"),
    path("setexpensetag", views.gider_etiketi_duzenle, name="gider_etiketi_duzenle"),
    #gider etiketleri
]
#
#