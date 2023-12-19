from django.urls import path
from . import views
app_name = "accounting"
urlpatterns = [
    path("till", views.kasa_viev, name="kasa"),
    path("addtill", views.kasa_ekle, name="kasa_ekle"),
    path("deltill", views.kasa_sil, name="kasa_sil"),
    path("settill", views.kasa_duzenle, name="kasa_duzenle"),
]
#