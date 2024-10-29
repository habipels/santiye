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
    path('deladdemployee/',views.personeller_sil,name = "personeller_sil"),
    path('setaddemployee/',views.personelleri_düzenle,name = "personelleri_düzenle"),
    path('detailemployee/<int:id>/',views.personel_bilgisi_axaj,name = "personel_bilgisi_axaj"),
    path('buyemployee/',views.personeller_odenmeye_maaslar,name = "personeller_odenmeye_maaslar"),
    path('payroll/<str:tarih>/<int:id>/',views.bodro,name = "bodro"),
    #
    path('givesalaryoradvance/',views.calisan_odemeleri_kaydet,name = "calisan_odemeleri_kaydet"),
    # POzisyon Sayfası
    path('position/',views.personeller_kategori_sayfalari,name = "personeller_kategori_sayfalari"),
    path('addposition/',views.personeller_kategori_ekle,name = "personeller_kategori_ekle"),
    path('delposition/',views.personeller_kategori_sil,name = "personeller_kategori_sil"),
    path('setposition/',views.personelleri_kategori_düzenle,name = "personelleri_kategori_düzenle"),
    # DEpartman Sayfası
    path('department/',views.personeller_depertman_sayfalari,name = "personeller_depertman_sayfalari"),
    path('adddepartment/',views.personeller_departman_ekle,name = "personeller_departman_ekle"),
    path('deldepartment/',views.personeller_departman_sil,name = "personeller_departman_sil"),
    path('setdepartment/',views.personelleri_departman_düzenle,name = "personelleri_departman_düzenle"),
    #personel
    path('tally/',views.personeller_puantaj_sayfasi,name = "personeller_puantaj_sayfasi"),
    path('savetally/',views.save_attendance,name = "save_attendance"),
    path('taketally/',views.calismalari_cek,name = "calismalari_cek"),

    path('havadurumu/',views.weather_view,name = "weather_view"),
    path('users/', views.user_list, name='user_list'),
    path('user/<int:user_id>/', views.user_chat, name='user_chat'),
    path('create_group/', views.create_group, name='create_group'),
    path('group/<int:group_id>/', views.group_chat, name='group_chat'),
    path('groups/', views.group_list, name='group_list'),  # Grup listeleme URL'si
    path('denemechat/', views.chat_view, name='chat_view'),
#
#
]
#lock_screen