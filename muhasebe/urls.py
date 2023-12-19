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
]
#