from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
from io import BytesIO
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


    def __str__(self):
        return self.username

class LockScreenStatus(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_locked = models.BooleanField(default=False)
class personel_dosyalari(models.Model):
    kullanici = models.ForeignKey(CustomUser, on_delete = models.SET_NULL,blank  =True,null = True,verbose_name="Kullanıcı Bilgisi")
    dosyalari  = models.FileField(verbose_name="Kullanıcı Dosyası",upload_to='kullanici_dosyasi/',blank=True,null=True)
class personel_izinleri(models.Model):
    #bu izinler kime ait
    izinlerin_sahibi_kullanici = models.ForeignKey(CustomUser, on_delete = models.SET_NULL,blank  =True,null = True,verbose_name="Kullanıcı Bilgisi")
    #kasada virman yapma özelliği
    kasa_virman_izni = models.BooleanField(default= False,verbose_name="Kasa Virman Yapma İzni")
    #kasada işlem yapma özelliği
    kasa_olusturma_izni = models.BooleanField(default = False,verbose_name = "Kasa Oluştuma İzni")
    Kasa_silme_izni = models.BooleanField(default = False,verbose_name = "Cari Silme İzni")
    #cari hesaplarda işlem yapmöa özelliği
    cari_olusturma = models.BooleanField(default= False,verbose_name="Cari Oluşturma İzni")
    cari_silme_izni = models.BooleanField(default = False,verbose_name = "Cari Silme İzni")
    #gelir gider kategori ve etiket  oluşturma silme düzenlme işlemi
    gelir_etiketi_olusturma = models.BooleanField(default = False,verbose_name = "Gelir Etiketi Oluştuma İzni")
    gelir_etiketi_silme = models.BooleanField(default = False,verbose_name = "Gelir Etiketi Silme İzni ")
    gider_etiketi_olusturma = models.BooleanField(default = False,verbose_name = "Gider Etiketi Oluştuma İzni")
    gider_etiketi_silme = models.BooleanField(default = False,verbose_name = "Gider Etiketi Silme İzni ")
    gider_kategorisi_olusturma = models.BooleanField(default = False,verbose_name = "Gider Kategorisi Oluştuma İzni")
    gider_kategorisi_silme = models.BooleanField(default = False,verbose_name = "Gider Kategorisi Silme İzni ")
    gelir_kategorisi_olusturma = models.BooleanField(default = False,verbose_name = "Gelir Kategorisi Oluştuma İzni")
    gelir_kategorisi_silme = models.BooleanField(default = False,verbose_name = "Gelir Kategorisi Silme İzni ")
    #ürün oluşturma silme özelliği
    urun_olusturma = models.BooleanField(default = False,verbose_name = "Ürün Oluştuma İzni")
    urun_silme = models.BooleanField(default = False,verbose_name = "Ürün Silme İzni ")
    # gelir gider faturası oluştuma silme ve düzenleme özelliği
    gelir_faturasi_kesme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Kesme İzni ")
    gelir_faturasi_silme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Silme İzni ")
    gelir_faturasi_duzenleme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Düzenleme İzni ")
    gider_faturasi_kesme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Kesme İzni ")
    gider_faturasi_silme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Silme İzni ")
    gider_faturasi_duzenleme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Düzenleme İzni ")
    #gelir gider makbuz işlemleri
    gider_faturasi_makbuz_kesme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Makbuz Kesme İzni ")
    gider_faturasi_makbuz_silme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Makbuz Silme İzni ")
    gider_faturasi_makbuz_duzenleme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Makbuz Düzenleme İzni ")
    gelir_faturasi_makbuz_kesme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Makbuz Kesme İzni ")
    gelir_faturasi_makbuz_silme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Makbuz Silme İzni ")
    gelir_faturasi_makbuz_duzenleme_izni = models.BooleanField(default = False,verbose_name = "Geli Faturası Makbuz Düzenleme İzni ")
    #şantiye proje oluştuma özelliği
    proje_tipi_olusturma = models.BooleanField(default = False,verbose_name = "Proje Tipi Oluştuma  İzni")
    proje_tipi_silme = models.BooleanField(default = False,verbose_name = "Proje Tipi Silme İzni ")
    #Şantiye Oluştuma
    santiye_olusturma = models.BooleanField(default = False,verbose_name = "Şantiye Oluşturma İzni")
    santiye_silme = models.BooleanField(default = False,verbose_name = "Şantiye Silme İzni ")
    #Şantiye Kategorileri
    santiye_kategoriler_olusturma = models.BooleanField(default = False,verbose_name = "Şantiye Kategorileri Oluşturma İzni")
    santiye_kategoriler_silme = models.BooleanField(default = False,verbose_name = "Şantiye Kategorileri Silme İzni ")
    #Sözleşmeler Kategorileri
    sozlesmeler_olusturma = models.BooleanField(default = False,verbose_name = "Sözleşmeler Oluşturma İzni")
    sozlesmeler_silme = models.BooleanField(default = False,verbose_name = "Sözleşmeler Silme İzni ")
    #Hakedişler Kategorileri
    hakedisler_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    hakedisler_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")

