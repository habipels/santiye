from django.urls import path
from . import views
app_name = "main"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    #şantiye işlemelri
    path("addingsite", views.santiye_ekle, name="santiye_ekle"),
    path("sitesettings", views.santiye_listele, name="santiye_listele"),
    path("delsite", views.santiye_sil, name="santiye_sil"),
    path("editsite", views.santiye_duzelt, name="santiye_duzelt"),
    #şantiye işlemelri
    #dil ayarları
    path("langsettings", views.dil_ayari_listele, name="dil_ayari_listele"),
    path("addlang", views.dil_ekle, name="dil_ekle"),
    path("setlang", views.dil_duzelt, name="dil_duzelt"),
    path("dellang", views.dil_sil, name="dil_sil"),
    #dil ayarları
    #proje tip işlemelri
    path("projectstype", views.proje_tipi_, name="proje_tipi_"),
    path("addprojectstype", views.proje_ekle, name="proje_ekle"),
    path("delprojectstype", views.proje_Adi_sil, name="proje_Adi_sil"),
    path("setprojecttype", views.proje_duzenle, name="proje_duzenle"),
    #proje tip işlemelri
    #şantiye proje işlemleri
    path("siteprojects", views.santiye_projesi_ekle_, name="santiye_projesi_ekle_"),
    path("addsite", views.santiye_ekleme_sahibi, name="santiye_ekleme_sahibi"),
    path("addsitesuperadmin/<int:id>", views.santiye_ekleme_super_admin, name="santiye_ekleme_super_admin"),
    path("delsiteproject", views.santiye_projesi_sil, name="santiye_projesi_sil"),
    path("setsiteprojetc", views.santiye_projesi_duzenle, name="santiye_projesi_duzenle"),
    #şantiye proje işlemleri
    path("yetkisiz", views.yetkisiz, name="yetkisiz"),
    #şantiye Kalemleri
    path("buldingsite/<int:id>", views.santtiye_kalemleri, name="santtiye_kalemleri"),
    path("addbuldingsite", views.santiyeye_kalem_ekle, name="santiyeye_kalem_ekle"),
    path("addbuldingsiteadmin/<int:id>", views.santiye_kalem_ekle_admin, name="santiye_kalem_ekle_admin"),
    path("editsite", views.santiye_duzelt, name="santiye_duzelt"),
    #şantiye Kalemleri

]
#