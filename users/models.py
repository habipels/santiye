from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
from io import BytesIO
from simple_history.models import HistoricalRecords
from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords
# Create your models here.
class CustomUser(AbstractUser):

    STATUS = (
        ('sirket', 'sirket'),
        ('sirketcalisani', 'sirketcalisani'),
        ('moderator', 'moderator'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='sirket')
    description = models.TextField("Açıklama", max_length=600, default='', blank=True)
    kullanicilar_db = models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    kullanici_silme_bilgisi = models.BooleanField(default= False)
    image  = models.FileField(upload_to='profile/',verbose_name="Profile",blank=True,null=True,)
    background_image  = models.FileField(upload_to='background/',verbose_name="background",blank=True,null=True,)
    telefon_numarasi =  models.CharField(max_length= 20 , verbose_name="Telefon Numarası ",blank=True,null = True)
    gorevi = models.CharField(max_length = 250 ,verbose_name="Görevi",blank = True,null = True)
    adrrsi = models.TextField("Adres", max_length=600, default='', blank=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)


    def __str__(self):
        return self.username
class faturalardaki_gelir_gider_etiketi_ozel(models.Model):
    kullanici = models.ForeignKey(CustomUser, on_delete = models.SET_NULL,blank  =True,null = True,verbose_name="Kullanıcı Bilgisi")
    gelir_etiketi = models.CharField(max_length=10,verbose_name  ="Gelir Etiketi",blank = True,null=True)
    gider_etiketi = models.CharField(max_length=10,verbose_name  ="Gider Etiketi",blank = True,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class LockScreenStatus(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_locked = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class personel_dosyalari(models.Model):
    kullanici = models.ForeignKey(CustomUser, on_delete = models.SET_NULL,blank  =True,null = True,verbose_name="Kullanıcı Bilgisi")
    dosyalari  = models.FileField(verbose_name="Kullanıcı Dosyası",upload_to='kullanici_dosyasi/',blank=True,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class personel_izinleri(models.Model):
    #bu izinler kime ait
    isim = models.CharField(max_length = 250 ,verbose_name="Görevi",blank = True,null = True)
    izinlerin_sahibi_kullanici = models.ForeignKey(CustomUser, on_delete = models.SET_NULL,blank  =True,null = True,verbose_name="Kullanıcı Bilgisi")
    #kasada virman yapma özelliği
    kasa_virman_olusturma_izni = models.BooleanField(default= False,verbose_name="Kasa Virman Yapma İzni")
    kasa_virman_gorme_izni = models.BooleanField(default= False,verbose_name="Kasa Virman Yapma İzni")
    #kasada işlem yapma özelliği
    kasa_gosterme_izni = models.BooleanField(default = False,verbose_name = "Kasa Oluştuma İzni")
    kasa_olusturma_izni = models.BooleanField(default = False,verbose_name = "Kasa Oluştuma İzni")
    kasa_guncelleme_izni = models.BooleanField(default = False,verbose_name = "Kasa Oluştuma İzni")
    Kasa_silme_izni = models.BooleanField(default = False,verbose_name = "Cari Silme İzni")
    #cari hesaplarda işlem yapmöa özelliği
    cari_gosterme_izni = models.BooleanField(default = False,verbose_name = "Kasa Oluştuma İzni")
    cari_guncelleme_izni = models.BooleanField(default = False,verbose_name = "Cari Silme İzni")
    cari_olusturma = models.BooleanField(default= False,verbose_name="Cari Oluşturma İzni")
    cari_silme_izni = models.BooleanField(default = False,verbose_name = "Cari Silme İzni")
    #gelir gider kategori ve etiket  oluşturma silme düzenlme işlemi
    gelir_etiketi_olusturma = models.BooleanField(default = False,verbose_name = "Gelir Etiketi Oluştuma İzni")
    gelir_etiketi_silme = models.BooleanField(default = False,verbose_name = "Gelir Etiketi Silme İzni ")
    gelir_etiketi_guncelleme = models.BooleanField(default = False,verbose_name = "Gelir Etiketi Oluştuma İzni")
    gelir_etiketi_gorme = models.BooleanField(default = False,verbose_name = "Gelir Etiketi Silme İzni ")
    gider_etiketi_olusturma = models.BooleanField(default = False,verbose_name = "Gider Etiketi Oluştuma İzni")
    gider_etiketi_silme = models.BooleanField(default = False,verbose_name = "Gider Etiketi Silme İzni ")
    gider_etiketi_guncelleme = models.BooleanField(default = False,verbose_name = "Gider Etiketi Oluştuma İzni")
    gider_etiketi_gorme = models.BooleanField(default = False,verbose_name = "Gider Etiketi Silme İzni ")
    gider_kategorisi_olusturma = models.BooleanField(default = False,verbose_name = "Gider Kategorisi Oluştuma İzni")
    gider_kategorisi_silme = models.BooleanField(default = False,verbose_name = "Gider Kategorisi Silme İzni ")
    gider_kategorisi_guncelleme = models.BooleanField(default = False,verbose_name = "Gider Kategorisi Oluştuma İzni")
    gider_kategorisi_gorme = models.BooleanField(default = False,verbose_name = "Gider Kategorisi Silme İzni ")
    gelir_kategorisi_olusturma = models.BooleanField(default = False,verbose_name = "Gelir Kategorisi Oluştuma İzni")
    gelir_kategorisi_silme = models.BooleanField(default = False,verbose_name = "Gelir Kategorisi Silme İzni ")
    gelir_kategorisi_gorme = models.BooleanField(default = False,verbose_name = "Gelir Kategorisi Oluştuma İzni")
    gelir_kategorisi_guncelleme = models.BooleanField(default = False,verbose_name = "Gelir Kategorisi Silme İzni ")
    #ürün oluşturma silme özelliği
    urun_olusturma = models.BooleanField(default = False,verbose_name = "Ürün Oluştuma İzni")
    urun_silme = models.BooleanField(default = False,verbose_name = "Ürün Silme İzni ")
    urun_guncelleme = models.BooleanField(default = False,verbose_name = "Ürün Oluştuma İzni")
    urun_gorme = models.BooleanField(default = False,verbose_name = "Ürün Silme İzni ")
    # gelir gider faturası oluştuma silme ve düzenleme özelliği
    gelir_faturasi_kesme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Kesme İzni ")
    gelir_faturasi_silme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Silme İzni ")
    gelir_faturasi_duzenleme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Düzenleme İzni ")
    gelir_faturasi_gorme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Kesme İzni ")
    gider_faturasi_kesme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Kesme İzni ")
    gider_faturasi_silme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Silme İzni ")
    gider_faturasi_duzenleme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Düzenleme İzni ")
    gider_faturasi_gorme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Silme İzni ")
    #gelir gider makbuz işlemleri
    gider_faturasi_makbuz_kesme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Makbuz Kesme İzni ")
    gider_faturasi_makbuz_silme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Makbuz Silme İzni ")
    gider_faturasi_makbuz_duzenleme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Makbuz Düzenleme İzni ")
    gider_faturasi_makbuz_gorme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Makbuz Silme İzni ")
    
    gelir_faturasi_makbuz_kesme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Makbuz Kesme İzni ")
    gelir_faturasi_makbuz_silme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Makbuz Silme İzni ")
    gelir_faturasi_makbuz_duzenleme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Makbuz Düzenleme İzni ")
    gelir_faturasi_makbuz_gorme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Makbuz Düzenleme İzni ")
    #şantiye proje oluştuma özelliği
    proje_tipi_olusturma = models.BooleanField(default = False,verbose_name = "Proje Tipi Oluştuma  İzni")
    proje_tipi_silme = models.BooleanField(default = False,verbose_name = "Proje Tipi Silme İzni ")
    proje_tipi_gorme = models.BooleanField(default = False,verbose_name = "Proje Tipi Oluştuma  İzni")
    proje_tipi_duzenleme = models.BooleanField(default = False,verbose_name = "Proje Tipi Silme İzni ")
    #Şantiye Oluştuma
    santiye_olusturma = models.BooleanField(default = False,verbose_name = "Şantiye Oluşturma İzni")
    santiye_silme = models.BooleanField(default = False,verbose_name = "Şantiye Silme İzni ")
    santiye_gorme = models.BooleanField(default = False,verbose_name = "Şantiye Oluşturma İzni")
    santiye_duzenleme = models.BooleanField(default = False,verbose_name = "Şantiye Silme İzni ")
    #Şantiye Kategorileri
    santiye_kategoriler_olusturma = models.BooleanField(default = False,verbose_name = "Şantiye Kategorileri Oluşturma İzni")
    santiye_kategoriler_silme = models.BooleanField(default = False,verbose_name = "Şantiye Kategorileri Silme İzni ")
    santiye_kategoriler_gorme = models.BooleanField(default = False,verbose_name = "Şantiye Kategorileri Oluşturma İzni")
    santiye_kategoriler_duzenleme = models.BooleanField(default = False,verbose_name = "Şantiye Kategorileri Silme İzni ")
    #Sözleşmeler Kategorileri
    sozlesmeler_olusturma = models.BooleanField(default = False,verbose_name = "Sözleşmeler Oluşturma İzni")
    sozlesmeler_silme = models.BooleanField(default = False,verbose_name = "Sözleşmeler Silme İzni ")
    sozlesmeler_gorme = models.BooleanField(default = False,verbose_name = "Sözleşmeler Oluşturma İzni")
    sozlesmeler_duzenleme = models.BooleanField(default = False,verbose_name = "Sözleşmeler Silme İzni ")
    #Hakedişler Kategorileri
    hakedisler_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    hakedisler_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    hakedisler_gorme = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    hakedisler_duzenleme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    #Taşeronlar Kategorileri
    taseronlar_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    taseronlar_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    taseronlar_gorme = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    taseronlar_duzenleme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    #İlerleme Takibi Kategorileri
    ilerleme_takibi_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    ilerleme_takibi_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    ilerleme_takibi_gorme = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    ilerleme_takibi_duzenleme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    #İş Planı Kategorileri
    is_plani_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    is_plani_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    is_plani_gorme = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    is_plani_duzenleme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    #Yapacaklar Kategorileri
    yapilacaklar_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    yapilacaklar_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    yapilacaklar_gorme = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    yapilacaklar_duzenleme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    #Dosya Yöneticisi Kategorileri
    dosya_yoneticisi_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    dosya_yoneticisi_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    dosya_yoneticisi_gorme = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    dosya_yoneticisi_duzenleme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    #Projeler Kategorileri
    projeler_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    projeler_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    projeler_gorme = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    projeler_duzenleme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    #Personeller Kategorileri
    personeller_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    personeller_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    personeller_gorme = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    personeller_duzenleme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    #Dashboard Kategorileri
    dashboard_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    dashboard_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    dashboard_gorme = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    dashboard_duzenleme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    #Gelir Özeti Kategorileri
    gelir_ozeti_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    gelir_ozeti_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    gelir_ozeti_gorme = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    gelir_ozeti_duzenleme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    #Gider Özeti Kategorileri
    gider_ozeti_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    gider_ozeti_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    gider_ozeti_gorme = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    gider_ozeti_duzenleme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    #hesap Ekstra Kategorileri
    hesap_ekstra_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    hesap_ekstra_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    hesap_ekstra_gorme = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    hesap_ekstra_duzenleme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    #virman Raporu Kategorileri
    virman_raporu_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    virman_raporu_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    virman_raporu_gorme = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    virman_raporu_duzenleme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class bagli_kullanicilar(models.Model):
    #bu izinler kime ait
    izinler = models.ForeignKey(personel_izinleri, on_delete = models.CASCADE,blank  =True,null = True,verbose_name="Kullanıcı Bilgisi")
    kullanicilar = models.ForeignKey(CustomUser, on_delete = models.CASCADE,blank  =True,null = True,verbose_name="Kullanıcı Bilgisi")

from datetime import datetime
from simple_history.models import HistoricalRecords
class calisanlar(models.Model):
    calisan_kime_ait = models.ForeignKey(CustomUser,verbose_name="Çalışan Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    isim = models.CharField(max_length=200,null=True,verbose_name="İsim",blank = True)
    soyisim = models.CharField(max_length=200,null=True,verbose_name="Soyisim",blank = True)
    maas = models.FloatField(verbose_name="Maaş",default=0,blank=True,null=True)
    puantaj = models.FloatField(verbose_name="Puantaj",default=0,blank=True,null=True)
    aciklama = models.TextField(verbose_name="Gelir Açıklaması",blank=True,null=True)
    ulkeye_gelis_tarihi = models.DateTimeField(null=True,verbose_name="Ülkeye Geliş Tarihi",blank = True)
    İse_baslama_tarihi = models.DateTimeField(null=True,verbose_name="İşe Başlama Tarihi",blank = True)
    silinme_bilgisi = models.BooleanField(default=False)
    durum = models.BooleanField(default=False) #False Maaşlı , True İse Puantaja Ait 
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class calisanlar_kategorisi(models.Model):
    kategori_kime_ait = models.ForeignKey(CustomUser,verbose_name="Çalışan Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    kategori_isimi = models.CharField(max_length= 200 ,verbose_name="Çalışan Kategori İsmi")
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class calisanlar_kategorisi_baglama(models.Model):
    #models.ForeignKey(CustomUser,verbose_name="Çalışan Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    kategori = models.CharField(max_length= 200 ,verbose_name="Çalışan Kategori İsmi")
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

