from django.contrib import admin
from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('register/',views.register,name = "register"),
    path('login/',views.loginUser,name = "login"),
    path('unlock/', views.lock_screen, name='unlock'),
    path('logout/',views.logoutUser,name = "logout"),
    path('profile/',views.profil_bilgisi,name = "profil_bilgisi"),
    path('yonlendir/',views.yonlendir,name = "yonlendir"),
    path('profileedit/',views.profile_edit_kismi,name = "profile_edit_kismi"),
    path('chengepaswrd/',views.parola_degistime,name = "parola_degistime"),
    #kullanici işlemleri
    path('myusers/',views.kullanicilarim,name = "kullanicilarim"),
    path('addmyusers/',views.kullanici_ekleme,name = "kullanici_ekleme"),
    path('delmyusers/',views.kullanici_silme,name = "kullanici_silme"),
    path('setmyusers/',views.kullanici_bilgileri_duzenle,name = "kullanici_bilgileri_duzenle"),
    #kullanici işlemleri
    #personel
    path('employee/',views.personeller_sayfasi,name = "personeller_sayfasi"),
    path('addemployee/',views.personeller_ekle,name = "personeller_ekle"),
    path('detailemployee/<int:id>/',views.personel_bilgisi_axaj,name = "personel_bilgisi_axaj"),
    # POzisyon Sayfası
    path('position/',views.personeller_kategori_sayfalari,name = "personeller_kategori_sayfalari"),
    path('addposition/',views.personeller_kategori_ekle,name = "personeller_kategori_ekle"),
    path('delposition/',views.personeller_kategori_sil,name = "personeller_kategori_sil"),
    path('setposition/',views.personelleri_kategori_düzenle,name = "personelleri_kategori_düzenle"),
    #personel
#
#
]
#lock_screen