from django.db import models
from django.db import models

from simple_history.models import HistoricalRecords
from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords
from users.models import CustomUser
# Create your models here.
# Create your models here.
from PIL import Image
from io import BytesIO
class sayfa_logosu(models.Model):
    image  = models.ImageField(upload_to='logo/',verbose_name="Sayfaya Logo Dark",blank = True,null=True)
    dark_image  = models.ImageField(upload_to='logo/',verbose_name="Sayfaya Logo Light",blank = True,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class faturalardaki_gelir_gider_etiketi(models.Model):
    kime_ait = models.ForeignKey(CustomUser, verbose_name="Proje Ait Olduğu", blank=True, null=True, on_delete=models.SET_NULL)
    gelir_etiketi = models.CharField(max_length=10,verbose_name  ="Gelir Etiketi",blank = True,null=True)
    gider_etiketi = models.CharField(max_length=10,verbose_name  ="Gider Etiketi",blank = True,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class sayfa_iconu(models.Model):
    sayfa_icon = models.FileField(upload_to='logo/',verbose_name="Sayfaya ikon ekleyin")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class site_adi(models.Model):
    site_adi_genel = models.CharField(max_length=200,verbose_name="Google Nasıl Görünecek")
    site_adi_sekme_tr= models.CharField(max_length=200,verbose_name="Sekmede Görünme Türkçe")
    footer = models.CharField(max_length=200,verbose_name="Footer")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
    def __str__(self):
        return self.site_adi_genel

class numara(models.Model):
    sirket_numarasi_gosterilecek_metin = models.CharField(max_length=20,verbose_name="Telefon Sitede Nasıl görünecek" )
    sirket_numarasi = models.CharField(max_length=20,verbose_name="Aranacak Numara Başında + olmadan ülke kodu ile Yazabilirisniz")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
    def __str__(self):
        return self.sirket_numarasi_gosterilecek_metin

class adres(models.Model):
    sirket_adresi_tr = models.CharField(max_length=200,verbose_name="Şirket Adresi Türkçe")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
    def __str__(self):
        return self.sirket_adresi_tr
class gomulu_adres(models.Model):
    sirket_adresi_tr = models.CharField(max_length=1000,verbose_name="Şirket Adresi Türkçe")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
    def __str__(self):
        return self.sirket_adresi_tr
class email_adres(models.Model):
    sirket_email_adresi = models.EmailField(max_length=200,verbose_name="Şirket Email Adresi")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
    def __str__(self):
        return self.sirket_email_adresi

class sosyalmedyaInsgr(models.Model):
    link = models.CharField(max_length=400,verbose_name="Şirket İnstagram Linki")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class sosyalmedyalinkd(models.Model):
    link = models.CharField(max_length=400,verbose_name="Şirket Linkedin Linki")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class sosyalmedyaFace(models.Model):
    link = models.CharField(max_length=400,verbose_name="Şirket Facebook Linki")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class sosyalmedyayoutube(models.Model):
    link = models.CharField(max_length=400,verbose_name="Şirket Youtube Linki")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class sosyalmedyatw(models.Model):
    link = models.CharField(max_length=400,verbose_name="Şirket TW Linki")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class seo_ayarlari(models.Model):
    site_seo_kelimeleri_tr =models.TextField(max_length=400,verbose_name="Seo Kelmeleri Türkçe")
    site_seo_metni_tr = models.TextField(max_length=400,verbose_name="Seo Metni Türkçe")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class banner(models.Model):
    banner_basligi_tr =models.CharField(max_length=400,verbose_name="Banner Başliği Türkçe")
    banner_aciklama_tr = models.TextField(max_length=400,verbose_name="Banner Aciklama Türkçe")
    banner_sira = models.IntegerField(verbose_name="Banner Gösterme Sırası")
    banner_gosterme = models.BooleanField(verbose_name="Banner Gösterilsin mi ? ")
    banner_link = models.CharField(max_length=400,verbose_name="Bannera Link Brakmak İstiyorsanız link Ekleyin",null=True,blank=True)
    image  = models.ImageField(upload_to='banner/',blank = True,null = True,verbose_name="Sayfaya Banner Ekleyin")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
    def save(self, *args, **kwargs):
        super(banner, self).save(*args, **kwargs)
        if self.image:
            with Image.open(self.image.path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                width, height = img.size
                if width > 800:
                    new_width = 800
                    new_height = int((new_width / width) * height)
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)
                    buffer = BytesIO()
                    img.save(buffer, format='JPEG', quality=60)
                    self.image.save(self.image.name, content=buffer, save=False)
                    super(banner, self).save(*args, **kwargs)


class dil_ayarla(models.Model):
    dil_adi = models.CharField(max_length= 200,verbose_name="Dil Adı",blank = True,null=True)
    dil_kisaltması = models.CharField(max_length=5,verbose_name="Dİl Kısaltması",blank=True,null = True)
    dil_bayragi_icon = models.FileField(upload_to='bayrak/',verbose_name="Dil Bayrağı")
    dil_aktiflik_durumu = models.BooleanField(default = False,verbose_name="Dİl Aktiflik Durumu")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)


#sistem görüntü ayarları
class layout(models.Model):
    isim  = models.CharField(max_length = 500,verbose_name ="Görünüş isimleri")
    data_layout = models.CharField(max_length = 500 ,verbose_name="Görünüş Anahtarı")
    aktiflik = models.BooleanField(default = False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class layout_uzunlugu(models.Model):
    isim  = models.CharField(max_length = 500,verbose_name ="Görünüş isimleri")
    data_layout_width = models.CharField(max_length = 500 ,verbose_name="Görünüş Anahtarı")
    aktiflik = models.BooleanField(default = False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class color_sheme(models.Model):
    isim  = models.CharField(max_length = 500,verbose_name ="Görünüş isimleri")
    data_bs_theme = models.CharField(max_length = 500 ,verbose_name="Görünüş Anahtarı")
    aktiflik = models.BooleanField(default = False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class side_bar_gorunum(models.Model):
    isim  = models.CharField(max_length = 500,verbose_name ="Görünüş isimleri")
    data_sidebar_visibility = models.CharField(max_length = 500 ,verbose_name="Görünüş Anahtarı")
    aktiflik = models.BooleanField(default = False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class layout_pozisyonu(models.Model):
    isim  = models.CharField(max_length = 500,verbose_name ="Görünüş isimleri")
    data_layout_position = models.CharField(max_length = 500 ,verbose_name="Görünüş Anahtarı")
    aktiflik = models.BooleanField(default = False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class topbar_color(models.Model):
    isim  = models.CharField(max_length = 500,verbose_name ="Görünüş isimleri")
    data_topbar = models.CharField(max_length = 500 ,verbose_name="Görünüş Anahtarı")
    aktiflik = models.BooleanField(default = False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class sidebar_boyutu(models.Model):
    isim  = models.CharField(max_length = 500,verbose_name ="Görünüş isimleri")
    data_sidebar_size = models.CharField(max_length = 500 ,verbose_name="Görünüş Anahtarı")
    aktiflik = models.BooleanField(default = False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class layout_sitili(models.Model):
    isim  = models.CharField(max_length = 500,verbose_name ="Görünüş isimleri")
    data_layout_style = models.CharField(max_length = 500 ,verbose_name="Görünüş Anahtarı")
    aktiflik = models.BooleanField(default = False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class sidebar_rengi(models.Model):
    isim  = models.CharField(max_length = 500,verbose_name ="Görünüş isimleri")
    data_sidebar = models.CharField(max_length = 500 ,verbose_name="Görünüş Anahtarı")
    aktiflik = models.BooleanField(default = False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

from django.utils.crypto import get_random_string
import hashlib

class ApiKey(models.Model):
    key = models.CharField(max_length=40, unique=True,blank = True,null = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()

        return super(ApiKey, self).save(*args, **kwargs)

    def generate_key(self):
        return get_random_string(length=40)
