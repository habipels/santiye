from django.contrib import admin
from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('register/',views.register,name = "register"),
    path('login/',views.loginUser,name = "login"),
    path('logout/',views.logoutUser,name = "logout"),
    path('profile/',views.profil_bilgisi,name = "profil_bilgisi"),
    #kullanici işlemleri
    path('myusers/',views.kullanicilarim,name = "kullanicilarim"),
    #kullanici işlemleri

]
#