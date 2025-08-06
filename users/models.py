from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
from io import BytesIO
from simple_history.models import HistoricalRecords
from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords
from django.utils import timezone
#from muhasebe.models import Gider_Bilgisi
# Create your models here.
class CustomUser(AbstractUser):

    STATUS = (
        ('sirket', 'sirket'),
        ('sirketcalisani', 'sirketcalisani'),
        ('moderator', 'moderator'),
    )
    plat = (('web', 'Web'),
        ('android', 'Android'),
        ('ios', 'iOS'),)

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='sirket')
    description = models.TextField("Açıklama", max_length=600, default='', blank=True)
    kullanicilar_db = models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    kullanici_silme_bilgisi = models.BooleanField(default= False)
    image  = models.FileField(upload_to='profile/',verbose_name="Profile",blank=True,null=True,)
    background_image  = models.FileField(upload_to='background/',verbose_name="background",blank=True,null=True,)
    telefon_numarasi =  models.CharField(max_length= 20 , verbose_name="Telefon Numarası ",blank=True,null = True)
    imza_sifresi = models.CharField(null= True,blank=True ,max_length=400, verbose_name = "Onaylama Şifresi")
    gorevi = models.CharField(max_length = 250 ,verbose_name="Görevi",blank = True,null = True)
    adrrsi = models.TextField("Adres", max_length=600, default='', blank=True)
    online  = models.BooleanField(default=False)
    token = models.CharField(max_length=255, unique=False, blank=True, null=True, verbose_name="Token")
    platform = models.CharField(max_length=10,choices=plat, default='web', verbose_name="Platform")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
    kullanici_tercih_dili = models.CharField(max_length=10,verbose_name="Kullanıcı Tercih Dili",default="en")
    last_seen = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

    def update_last_seen(self):
        self.last_seen = timezone.now()
        self.save()

    def is_online(self):
        now = timezone.now()
        return now - self.last_seen < timezone.timedelta(minutes=5)

class DeviceToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='device_tokens')
    token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=20, default='web')  # iOS, Android, web vs.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.platform} - {self.token[:10]}..."
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
    #kasada işlem yapma özelliği
    kasa_detay_izni = models.BooleanField(default = False)
    cari_detay_izni = models.BooleanField(default = False)
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
    #Muhasabe Ayarları
    muhasabe_ayarlari_gorme = models.BooleanField(default = False)
    muhasabe_ayarlari_guncelleme = models.BooleanField(default = False)
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
    #Şantiye Blogları
    blog_olusturma = models.BooleanField(default = False)
    blog_silme = models.BooleanField(default = False)
    blog_gorme = models.BooleanField(default = False)
    blog_duzenleme = models.BooleanField(default = False)
    #Şantiye Kalemleri
    kalemleri_olusturma = models.BooleanField(default = False)
    kalemleri_silme = models.BooleanField(default = False)
    kalemleri_gorme = models.BooleanField(default = False)
    kalemleri_duzenleme = models.BooleanField(default = False)
    #Şantiye raporu
    santiye_raporu_olusturma = models.BooleanField(default = False)
    santiye_raporu_silme = models.BooleanField(default = False)
    santiye_raporu_gorme = models.BooleanField(default = False)
    santiye_raporu_duzenleme = models.BooleanField(default = False)
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
    #Üst Yüklenici Kategorileri
    ust_yuklenici_olusturma = models.BooleanField(default = False)
    ust_yuklenici_silme = models.BooleanField(default = False)
    ust_yuklenici_gorme = models.BooleanField(default = False)
    ust_yuklenici_duzenleme = models.BooleanField(default = False)
    #
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
    projeler_olusturma = models.BooleanField(default = False)
    projeler_silme = models.BooleanField(default = False)
    projeler_gorme = models.BooleanField(default = False)
    projeler_duzenleme = models.BooleanField(default = False)
    #Personeller Kategorileri back end olarak yapılmadı
    personeller_olusturma = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    personeller_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    personeller_gorme = models.BooleanField(default = False,verbose_name = "Hakedişler Oluşturma İzni")
    personeller_duzenleme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    #Dashboard Kategorileri
    dashboard_olusturma = models.BooleanField(default = True,verbose_name = "Hakedişler Oluşturma İzni")
    dashboard_silme = models.BooleanField(default = False,verbose_name = "Hakedişler Silme İzni ")
    dashboard_gorme = models.BooleanField(default = True,verbose_name = "Hakedişler Oluşturma İzni")
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
    #stok back end olarak bağlanmmadı
    satin_alma_talebi_olusturma = models.BooleanField(default = False)
    satin_alma_talebi_silme = models.BooleanField(default = False)
    satin_alma_talebi_gorme = models.BooleanField(default = False)
    satin_alma_talebi_duzenleme = models.BooleanField(default = False)
    #stok back end olarak bağlanmmadı
    satin_alma_talebi_onaylama_olusturma = models.BooleanField(default = False)
    satin_alma_talebi_onaylama_silme = models.BooleanField(default = False)
    satin_alma_talebi_onaylama_gorme = models.BooleanField(default = False)
    satin_alma_talebi_onaylama_duzenleme = models.BooleanField(default = False)
    stok_olusturma = models.BooleanField(default = False)
    stok_talebi_onaylama_silme = models.BooleanField(default = False)
    stok_talebi_onaylama_gorme = models.BooleanField(default = False)
    stok_talebi_onaylama_duzenleme = models.BooleanField(default = False)
    zimmet_olusturma = models.BooleanField(default = False)
    zimmet_silme = models.BooleanField(default = False)
    zimmet_gorme = models.BooleanField(default = False)
    #puantaj durum
    personeller_puantaj_olusturma = models.BooleanField(default = False)
    personeller_puantaj_silme = models.BooleanField(default = False)
    personeller_puantaj_gorme = models.BooleanField(default = False)
    personeller_puantaj_duzenleme = models.BooleanField(default = False)
    #personel maaş ödeme
    personeller_odeme_olusturma = models.BooleanField(default = False)
    personeller_odeme_silme = models.BooleanField(default = False)
    personeller_odeme_gorme = models.BooleanField(default = False)
    personeller_odeme_duzenleme = models.BooleanField(default = False)
    #personel maaş ödeme
    katman_olusturma = models.BooleanField(default = False)
    katman_silme = models.BooleanField(default = False)
    katman_gorme = models.BooleanField(default = False)
    katman_duzenleme = models.BooleanField(default = False)

    #gant
    gant_olusturma = models.BooleanField(default = False)
    gant_gorme = models.BooleanField(default = False)
    gant_duzenleme = models.BooleanField(default = False)
    gant_silme = models.BooleanField(default = False)
    #genel Rapor
    genel_rapor_olusturma = models.BooleanField(default = False)
    genel_rapor_gorme = models.BooleanField(default = False)
    genel_rapor_duzenleme = models.BooleanField(default = False)
    genel_rapor_silme = models.BooleanField(default = False)
    genel_rapor_onaylama = models.BooleanField(default = False)
    #musteri Kısmı
    musteri_olusturma = models.BooleanField(default=False)
    musteri_gorme = models.BooleanField(default=False)
    musteri_duzenleme = models.BooleanField(default=False)
    musteri_silme = models.BooleanField(default=False)
    # CRM permissions
    crm_musteri_olusturma = models.BooleanField(default=False, verbose_name="CRM Müşteri Oluşturma İzni")
    crm_musteri_silme = models.BooleanField(default=False, verbose_name="CRM Müşteri Silme İzni")
    crm_musteri_gorme = models.BooleanField(default=False, verbose_name="CRM Müşteri Görme İzni")
    crm_musteri_duzenleme = models.BooleanField(default=False, verbose_name="CRM Müşteri Düzenleme İzni")
    
    crm_talep_olusturma = models.BooleanField(default=False, verbose_name="CRM Talep Oluşturma İzni")
    crm_talep_silme = models.BooleanField(default=False, verbose_name="CRM Talep Silme İzni")
    crm_talep_gorme = models.BooleanField(default=False, verbose_name="CRM Talep Görme İzni")
    crm_talep_duzenleme = models.BooleanField(default=False, verbose_name="CRM Talep Düzenleme İzni")
    
    crm_teklif_olusturma = models.BooleanField(default=False, verbose_name="CRM Teklif Oluşturma İzni")
    crm_teklif_silme = models.BooleanField(default=False, verbose_name="CRM Teklif Silme İzni")
    crm_teklif_gorme = models.BooleanField(default=False, verbose_name="CRM Teklif Görme İzni")
    crm_teklif_duzenleme = models.BooleanField(default=False, verbose_name="CRM Teklif Düzenleme İzni")
    
    crm_daire_olusturma = models.BooleanField(default=False, verbose_name="CRM Daire Oluşturma İzni")
    crm_daire_silme = models.BooleanField(default=False, verbose_name="CRM Daire Silme İzni")
    crm_daire_gorme = models.BooleanField(default=False, verbose_name="CRM Daire Görme İzni")
    crm_daire_duzenleme = models.BooleanField(default=False, verbose_name="CRM Daire Düzenleme İzni")
    
    crm_evrak_olusturma = models.BooleanField(default=False, verbose_name="CRM Evrak Oluşturma İzni")
    crm_evrak_silme = models.BooleanField(default=False, verbose_name="CRM Evrak Silme İzni")
    crm_evrak_gorme = models.BooleanField(default=False, verbose_name="CRM Evrak Görme İzni")
    crm_evrak_duzenleme = models.BooleanField(default=False, verbose_name="CRM Evrak Düzenleme İzni")
    santiye_kontrol =  models.BooleanField(default=True, verbose_name="Santiye Kontrol")
    rapor_olusturucu_gorme = models.BooleanField(default=False, verbose_name="Rapor Oluşturucu Görme İzni")
    rapor_olusturucu_olusturma = models.BooleanField(default=False, verbose_name="Rapor Oluşturucu Oluşturma İzni")
    
    rfi_olusturma = models.BooleanField(default=False, verbose_name="RFI Oluşturma İzni")
    rfi_gorme = models.BooleanField(default=False, verbose_name="RFI Görme İzni")
    rfi_duzenleme = models.BooleanField(default=False, verbose_name="RFI Düzenleme İzni")
    rfi_silme = models.BooleanField(default=False, verbose_name="RFI Silme İzni")
    
    rfi_listesi_olusturma = models.BooleanField(default=False, verbose_name="RFI Listesi Oluşturma İzni")
    rfi_listesi_gorme = models.BooleanField(default=False, verbose_name="RFI Listesi Görme İzni")
    rfi_listesi_duzenleme = models.BooleanField(default=False, verbose_name="RFI Listesi Düzenleme İzni")
    rfi_listesi_silme = models.BooleanField(default=False, verbose_name="RFI Listesi Silme İzni")

    rfi_listesi_onaylama_olustur = models.BooleanField(default=False, verbose_name="RFI Listesi Onaylama İzni")
    rfi_listesi_onaylama_gorme = models.BooleanField(default=False, verbose_name="RFI Listesi Onaylama Görme İzni")
    rfi_listesi_onaylama_silme = models.BooleanField(default=False, verbose_name="RFI Listesi Onaylama Silme İzni")

    #rapor_olusturucu_silme = models.BooleanField(default=False, verbose_name="Rapor Oluşturucu Silme İzni")
    #rapor_olusturucu_duzenleme = models.BooleanField(default=False, verbose_name="Rapor Oluşturucu Düzenleme İzni")
    #rapor_olusturucu_gorme = models.BooleanField(default=False, verbose_name="Rapor Oluşturucu Görme İzni")
    
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class bagli_kullanicilar(models.Model):
    #bu izinler kime ait
    izinler = models.ForeignKey(personel_izinleri, on_delete = models.CASCADE,blank  =True,null = True,verbose_name="Kullanıcı Bilgisi")
    kullanicilar = models.ForeignKey(CustomUser, on_delete = models.CASCADE,blank  =True,null = True,verbose_name="Kullanıcı Bilgisi")

from datetime import datetime
from simple_history.models import HistoricalRecords
class calisanlar_kategorisi(models.Model):
    kategori_kime_ait = models.ForeignKey(CustomUser,verbose_name="Çalışan Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    kategori_isimi = models.CharField(max_length= 200 ,verbose_name="Çalışan Kategori İsmi")
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class calisanlar_pozisyonu(models.Model):
    kategori_kime_ait = models.ForeignKey(CustomUser,verbose_name="Çalışan Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    kategori_isimi = models.CharField(max_length= 200 ,verbose_name="Çalışan Kategori İsmi")
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class calisanlar(models.Model):
    STATUS = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        
    )#0 Çalışıyor # diğerleri Çalışmıyor 
    calisan_kime_ait = models.ForeignKey(CustomUser,verbose_name="Çalışan Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    calisan_kategori = models.ForeignKey(calisanlar_kategorisi,verbose_name="Çalışan Kategorisi",blank=True,null=True,on_delete=models.SET_NULL)
    calisan_pozisyonu = models.ForeignKey(calisanlar_pozisyonu,verbose_name="Çalışan Kategorisi",blank=True,null=True,on_delete=models.SET_NULL)
    uyrugu = models.CharField(max_length=200,null=True,verbose_name="uyruğu",blank = True)
    pasaport_numarasi = models.CharField(max_length=200,null=True,verbose_name="Pasaport Numarası",blank = True)
    isim = models.CharField(max_length=200,null=True,verbose_name="İsim",blank = True)
    soyisim = models.CharField(max_length=200,null=True,verbose_name="Soyisim",blank = True)
    profile  = models.FileField(upload_to='calisanprofili/',verbose_name="Sayfaya Logo Light",blank=True,null=True)
    dogum_tarihi = models.DateField(null=True,verbose_name="Doğum Tarihi",blank = True)
    telefon_numarasi = models.CharField(max_length=20,null=True,verbose_name="Telefon Numarasi",blank = True)
    status = models.CharField(max_length=100, choices=STATUS, default='0')
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class calisan_maas_durumlari(models.Model):
    calisan = models.ForeignKey(calisanlar,verbose_name="işlem Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    maas = models.FloatField(verbose_name="Maaş",default=0,blank=True,null=True)
    yevmiye = models.FloatField(verbose_name="Puantaj",default=0,blank=True,null=True)
    fazla_mesai_orani = models.FloatField(verbose_name="Fazla_mesai Orani",default=0.20,blank=True,null=True)
    durum = models.BooleanField(default=False) #True Maaşlı , False Yevmiye
    para_birimi =models.BooleanField(default=False) #True dolor , False dinar
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class calisan_belgeleri(models.Model):
    calisan = models.ForeignKey(calisanlar,verbose_name="işlem Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    belge_turu = models.CharField(max_length=200,null=True,verbose_name="Soyisim",blank = True)
    belge  = models.FileField(upload_to='belge/',verbose_name="Sayfaya Logo Light",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
from django.utils import timezone
class calisanlar_calismalari(models.Model):
    mesai_orani = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    calisan = models.ForeignKey(calisanlar,verbose_name="Çalışan",blank=True,null=True,on_delete=models.SET_NULL)
    maas = models.ForeignKey(calisan_maas_durumlari,verbose_name="işlem Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    normal_calisma_saati = models.FloatField(verbose_name="Normal Çalışma Saati",default=0,blank=True,null=True)
    mesai_calisma_saati = models.FloatField(verbose_name="Mesai Çalışma Saati",default=0,blank=True,null=True)
    mesai_oran_tutma = models.CharField(max_length=100, choices=mesai_orani, default='1')
    tarihi = models.DateTimeField(null=True,verbose_name="Çalışma Tarihi",blank = True)
    guncelleme_tarihi = models.DateTimeField("Date modified", default=timezone.now)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(CustomUser, related_name='user_groups')
    image  = models.FileField(upload_to='chatgrup_resimleri/',verbose_name="Profile",blank=True,null=True,)
    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_messages')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_messages')
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
