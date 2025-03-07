from django.db import models
from users.models import *
from datetime import datetime
from muhasebe.models import *
from simple_history.models import HistoricalRecords
from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords
from users.models import calisanlar_kategorisi
from django.utils import timezone

class proje_tipi(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Tipi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    Proje_tipi_adi = models.CharField(max_length=400,verbose_name="Proje Tipi Adı",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    durum_bilgisi = models.BooleanField(default=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class birimler(models.Model):
    Proje_tipi_adi = models.CharField(max_length=400,verbose_name="Birim  Adı",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    durum_bilgisi = models.BooleanField(default=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class bina_goruntuleri(models.Model):
    isimi = models.CharField(max_length=400,verbose_name="Görüntü Adı",blank=True,null=True)
    ondden_goruntu = models.FileField(upload_to='bina_goruntuleri/',verbose_name="Önden Görüntü",blank=True,null=True)
    arkadan_goruntu = models.FileField(upload_to='bina_goruntuleri/',verbose_name="Arka Görüntü",blank=True,null=True)
    sagdan_goruntu = models.FileField(upload_to='bina_goruntuleri/',verbose_name="Sağdan Görüntü",blank=True,null=True)
    soldan_goruntu = models.FileField(upload_to='bina_goruntuleri/',verbose_name="Soldan Görüntü",blank=True,null=True)
    ustten_goruntu = models.FileField(upload_to='bina_goruntuleri/',verbose_name="Üstten Görüntü",blank=True,null=True)
    alttan_goruntu = models.FileField(upload_to='bina_goruntuleri/',verbose_name="Alttan Görüntü",blank=True,null=True)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class santiye(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_tipi = models.ForeignKey(proje_tipi,verbose_name="Proje Tipi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    bina_goruntuleri_aitlik = models.ForeignKey(bina_goruntuleri,verbose_name="Bina Görüntüleri",blank=True,null=True,on_delete=models.SET_NULL)
    proje_adi = models.CharField(max_length = 200,verbose_name="Proje Adı",blank=True,null = True)
    lat = models.TextField(null = True,blank=True)
    lon = models.TextField(null = True,blank=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class santiye_sablonlari(models.Model):
    status=(("0","0"),("1","1"),("2","2"))

    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    sablon_adi = models.CharField(max_length=200,verbose_name="Sablon Adı",blank=True,null = True)
    sablon_durumu = models.CharField(max_length=200,verbose_name="Sablon Durumu",blank=True,null = True,choices=status)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class sanytiye_sablon_bolumleri(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    sablon_adi = models.ForeignKey(santiye_sablonlari,verbose_name="Sablon Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    bolum = models.CharField(max_length=200,verbose_name="Sablon Bölüm Adı",blank=True,null = True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class santiye_imalat_kalemleri(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    detay = models.ForeignKey(sanytiye_sablon_bolumleri,verbose_name="Detay Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    icerik = models.CharField(max_length=200,verbose_name="İçerik Adı",blank=True,null = True)
    is_grubu = models.CharField(max_length=200,verbose_name="İçerik Adı",blank=True,null = True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class imalat_kalemleri_imalat_detaylari(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    icerik = models.ForeignKey(santiye_imalat_kalemleri,verbose_name="İçerik Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    imalat_detayi = models.CharField(max_length=200,verbose_name="İmalat Detayı",blank=True,null = True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class bloglar(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    blog_adi = models.CharField(max_length=200,verbose_name="Blog Adı",blank=True,null = True)
    blog_numarasi = models.BigIntegerField(default = 1,verbose_name="Blog Numarasi")
    kat_sayisi =models.FloatField(default = 1,verbose_name="Kat Bilgisi")
    baslangic_tarihi = models.DateTimeField(default=datetime.now,null=True)
    bitis_tarihi = models.DateTimeField(default=datetime.now,null=True)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class checkdaireleri(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    blog_bilgisi = models.ForeignKey(bloglar,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    kat = models.IntegerField(default = 1,verbose_name="Kat Bilgisi")
    kat_daire_sayisi = models.IntegerField(default = 1,verbose_name="Kat Bilgisi")
    daire_no = models.CharField(max_length=200,verbose_name="Daire No", blank=True,null=True)
    genel_notlar = models.TextField()
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class imalat_daire_balama(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    blog_bilgisi = models.ForeignKey(bloglar,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    daire_bilgisi = models.ForeignKey(checkdaireleri,verbose_name="Daire Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    imalat_detayi = models.ForeignKey(santiye_imalat_kalemleri,verbose_name="İmalat Detayı",blank=True,null=True,on_delete=models.SET_NULL)
    tamamlanma_bilgisi = models.BooleanField(default=False)
    tamamlamayi_yapan = models.ForeignKey(CustomUser,verbose_name="Tamamlamayı Yapan",blank=True,null=True,on_delete=models.SET_NULL,related_name="tamamlamayi_yapan")
    tarih = models.DateTimeField(default=datetime.now,null=True,blank=True)  # Updates automatically on save
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class check_liste_onaylama_gruplari(models.Model):
    imalat_kalemi_ait = models.ForeignKey(imalat_daire_balama,verbose_name="İmalat Kalemi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    onaylayan = models.ForeignKey(CustomUser,verbose_name="Onaylayan",blank=True,null=True,on_delete=models.SET_NULL,related_name="onaylayan")
    onaylma_tarihi = models.DateTimeField(default=datetime.now,null=True,blank=True)  # Updates automatically on save
    onaylama_notu = models.TextField(blank=True,null=True)
    tamamlanma_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class daire_resimleri_chjeckdaireleri(models.Model):
    daire_bilgisi = models.ForeignKey(checkdaireleri,verbose_name="Daire Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    resim = models.FileField(upload_to='daire_resimleri/',verbose_name="Resim Adı",blank=True,null=True)
    resim_aciklamasi = models.CharField(max_length=200,verbose_name="Resim Açıklaması", blank=True,null=True)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class blog_ortak_alan_ve_cepheleri(models.Model):
    status=(("0","0"),("1","1"),("2","2"))
    genel_icerik = (("0","0"),("1","1"),("2","2"),("3","3"))
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    blog_ait_bilgisi = models.ForeignKey(bloglar,verbose_name="Blog Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    aciklama_adi = models.CharField(max_length=200,verbose_name="Aciklama Adı",blank=True,null = True)
    bolum_icerigi = models.CharField(max_length=200, default="0",choices=status,verbose_name="Bolum İçeriği")
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class daire_bilgisi(models.Model):
    daire_kime_ait = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    blog_bilgisi = models.ForeignKey(bloglar,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    kat = models.IntegerField(default = 1,verbose_name="Kat Bilgisi")
    daire_no = models.CharField(max_length=200,verbose_name="Daire No", blank=True,null=True)
    oda_sayisi = models.FloatField(default = 1,verbose_name="Oda Sayısı")
    metre_kare_brut = models.FloatField(default = 1,verbose_name="Metre Kare ")
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class musteri_bilgisi(models.Model):
    musteri_kime_ait = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    musteri_adi = models.CharField(max_length=200,verbose_name="Müşteri Adı ", blank=True,null=True)
    musteri_soyadi = models.CharField(max_length=200,verbose_name="Müşteri Soyadı ", blank=True,null=True)
    musteri_telefon_numarasi = models.CharField(max_length=200,verbose_name="Telefon Numarası", blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class musteri_notlari(models.Model):
    kime_ait = models.ForeignKey(CustomUser, verbose_name="Proje Ait Olduğu", blank=True, null=True, on_delete=models.SET_NULL)
    musterisi = models.ForeignKey(musteri_bilgisi, verbose_name="Müşterisi", blank=True, null=True, on_delete=models.SET_NULL)
    not_basligi = models.CharField(max_length=400, verbose_name="Not Başlığı", blank=True, null=True)
    not_aciklamasi = models.TextField()
    not_tarihi = models.DateTimeField(default=datetime.now, null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now, null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class talep_ve_sikayet(models.Model):
    talep_sikayet_kategorisi =(
        ('0', '0'), #talep
        ('1', '1'), #şikayet
    )
    durum_bilgisi =(
        ('0', '0'),
        ('1', '1'),
        ('2','2'),
    )
    sikayet_kime_ait = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    musteri = models.ForeignKey(musteri_bilgisi,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    sikayet_nedeni = models.CharField(max_length=10,verbose_name="Şikayet_nedeni",blank=True,null=True)
    sikayet_aciklamasi = models.TextField()
    talep_sikayet_ayrimi = models.CharField(max_length=100, choices=talep_sikayet_kategorisi, default='0')
    daire = models.ForeignKey(daire_bilgisi,verbose_name="Daire",blank=True,null=True,on_delete=models.SET_NULL)
    durum = models.CharField(max_length=100, choices=durum_bilgisi, default='0')
    islem_tarihi = models.DateTimeField(default=datetime.now,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class musteri_daire_baglama(models.Model):
    durum_bilgisi =(
        ('0', '0'),
        ('1', '1'),
        ('2','2'),
    )
    baglama_kime_ait = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL,related_name="baglama_kime_ait")
    musterisi = models.ForeignKey(musteri_bilgisi,verbose_name="Müşeterisi",blank=True,null=True,on_delete=models.SET_NULL)
    daire = models.ForeignKey(daire_bilgisi,verbose_name="Daire",blank=True,null=True,on_delete=models.SET_NULL)
    durum = models.CharField(max_length=100, choices=durum_bilgisi, default='0')
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class musteri_evraklari(models.Model):
    belge_kime_ait = models.ForeignKey(CustomUser, verbose_name="Proje Ait Olduğu", blank=True, null=True, on_delete=models.SET_NULL, related_name="belge_kime_ait")
    musterisi = models.ForeignKey(musteri_bilgisi, verbose_name="Müşterisi", blank=True, null=True, on_delete=models.SET_NULL)
    belgenin_ait_oldugu_yer = models.ForeignKey(musteri_daire_baglama, verbose_name="Proje Ait Olduğu", blank=True, null=True, on_delete=models.SET_NULL, related_name="belgenin_ait_oldugu_yer")
    evrak_detayi = models.CharField(max_length=200, verbose_name="Evrak Adı", blank=True, null=True)
    evrak = models.FileField(upload_to='evrak/', verbose_name="Evrak", blank=True, null=True)
    kayit_tarihi = models.DateTimeField(default=datetime.now, null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class teklifler(models.Model):
    durum_bilgisi =(
        ('0', '0'),
        ('1', '1'),
        ('2','2'),
    )
    teklif_kime_ait = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL,related_name="teklif_kime_ait")
    teklif_basligi = models.CharField(max_length=200,verbose_name="Teklif Başlığı",blank=True,null=True)
    musterisi = models.ForeignKey(musteri_bilgisi,verbose_name="Müşeterisi",blank=True,null=True,on_delete=models.SET_NULL)
    toplam_tutar  = models.FloatField(default=0,verbose_name="Toplam Tutar")
    durum = models.CharField(max_length=100, choices=durum_bilgisi, default='0')
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class teklif_icerikleri(models.Model):
    kime_ait = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    hangi_teklif = models.ForeignKey(teklifler,verbose_name="Teklif ",blank=True,null=True,on_delete=models.SET_NULL)
    urun_hizmet = models.CharField(max_length=200,verbose_name="Ürün Başlığı",blank=True,null=True)
    urun_aciklama = models.CharField(max_length=400,verbose_name="Ürün Açıklama",blank=True,null=True)
    indirim = models.FloatField(default=0,verbose_name="İndirim Oranı")
    miktar = models.FloatField(default=0,verbose_name="Miktar")
    birim_fiyati = models.FloatField(default=0,verbose_name="Birim Fİyati")
    birim_fiyati_ıqd = models.FloatField(default=0,verbose_name="Birim Fİyati")
    genel_toplam = models.FloatField(default=0,verbose_name="Genel Toplam")
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class santiye_kalemleri(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    birimi = models.ForeignKey(birimler,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    kalem_adi = models.CharField(max_length= 200,verbose_name="Kalem Adı",blank = True,null = True)
    santiye_agirligi = models.FloatField(default = 0 ,verbose_name = "Kalem Şantiye Ağırlığı")
    santiye_finansal_agirligi = models.FloatField(default = 0,verbose_name = "Kalem Finansal Ağırlık")
    metraj = models.FloatField(default = 0 ,verbose_name = "Metraj Bilgisi")
    tutari = models.FloatField(default = 0 ,verbose_name = "Tutarı Bilgisi")
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class katman(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    katman_adi = models.CharField(max_length=200,verbose_name="Katman Adı",blank=True,null = True)
    katman_dosyasi = models.FileField(upload_to='katman_dosyalari/',verbose_name="Dosya Adı",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class santiye_kalemlerin_dagilisi (models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.CASCADE)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.CASCADE)
    kalem_bilgisi = models.ForeignKey(santiye_kalemleri,verbose_name="Kalem Ait Olduğu",blank=True,null=True,on_delete=models.CASCADE)
    kat = models.IntegerField(default = 0,verbose_name="kat Numarası")
    blog_bilgisi = models.ForeignKey(bloglar,verbose_name="Blog Ait Olduğu",blank=True,null=True,on_delete=models.CASCADE)
    degistirme_tarihi = models.DateTimeField(default=datetime.now,null=True)
    tamamlanma_bilgisi = models.BooleanField(default=False)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class projeler (models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    blog_bilgisi = models.ForeignKey(bloglar,blank=True,null=True,on_delete=models.CASCADE)
    kalem_bilgisi = models.ForeignKey(santiye_kalemleri,blank=True,null=True,on_delete=models.CASCADE)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class proje_dosyalari(models.Model):
    proje_ait_bilgisi = models.ForeignKey(projeler,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    dosya = models.FileField(upload_to='proje_dosyalari/',verbose_name="Dosya Adı",blank=True,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class taseronlar(models.Model):
    taseron_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    taseron_adi = models.CharField(max_length = 200,verbose_name="Taşeron Adı",blank = True,null = True)
    email = models.EmailField(verbose_name="Email adresi",blank = True,null=True,max_length=200)
    telefon_numarasi = models.CharField(max_length = 200,verbose_name="Telefon Numarası",blank = True,null = True)
    aciklama = models.TextField(verbose_name = "Açıklama",blank = True,null = True)
    proje_bilgisi = models.ManyToManyField(projeler,blank=True,null=True)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)


class taseron_sozlesme_dosyalari(models.Model):
    proje_ait_bilgisi = models.ForeignKey(taseronlar,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    dosya = models.FileField(upload_to='taseron_sozlesme/',verbose_name="Dosya Adı",blank=True,null=True)
    dosya_adi = models.CharField(max_length = 400,verbose_name="Sözleşme Adı",blank = True,null = True)
    tarih = models.DateField(verbose_name = "Proje Tarihi",blank = True,null = True)
    aciklama = models.TextField(verbose_name = "Açıklama",blank = True,null = True)
    durum = models.BooleanField(default = True,verbose_name = "Durum",blank = True,null = True)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class ust_yuklenici(models.Model):
    taseron_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    taseron_adi = models.CharField(max_length = 200,verbose_name="Taşeron Adı",blank = True,null = True)
    email = models.EmailField(verbose_name="Email adresi",blank = True,null=True,max_length=200)
    telefon_numarasi = models.CharField(max_length = 200,verbose_name="Telefon Numarası",blank = True,null = True)
    aciklama = models.TextField(verbose_name = "Açıklama",blank = True,null = True)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)


class ust_yuklenici_dosyalari(models.Model):
    proje_ait_bilgisi = models.ForeignKey(ust_yuklenici,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    dosya = models.FileField(upload_to='ust_yuklenici_sozlesme/',verbose_name="Dosya Adı",blank=True,null=True)
    dosya_adi = models.CharField(max_length = 400,verbose_name="Sözleşme Adı",blank = True,null = True)
    tarih = models.DateField(verbose_name = "Proje Tarihi",blank = True,null = True)
    aciklama = models.TextField(verbose_name = "Açıklama",blank = True,null = True)
    durum = models.BooleanField(default = True,verbose_name = "Durum",blank = True,null = True)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class cari_taseron_baglantisi(models.Model):
    gelir_kime_ait_oldugu = models.ForeignKey(taseronlar,verbose_name="Gelir Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    cari_bilgisi = models.ForeignKey(cari,verbose_name="Cari Bilgisi",blank=True,null=True,on_delete=models.SET_NULL)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)



class taseron_hakedisles(models.Model):
    proje_ait_bilgisi = models.ForeignKey(taseronlar,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    dosya = models.FileField(upload_to='taseron_sozlesme/',verbose_name="Dosya Adı",blank=True,null=True)
    dosya_adi = models.CharField(max_length = 400,verbose_name="Sözleşme Adı",blank = True,null = True)
    tarih = models.DateField(verbose_name = "Proje Tarihi",blank = True,null = True)
    aciklama = models.TextField(verbose_name = "Açıklama",blank = True,null = True)
    fatura_numarasi = models.CharField(max_length = 200,verbose_name = "Fatura Numarası " ,blank = True,null = True)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class klasorler(models.Model):
    dosya_sahibi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    klasor_adi = models.CharField(max_length = 200,verbose_name="Klasor Adı",blank = True,null = True)
    klasor_adi_db = models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class klasor_dosyalari(models.Model):
    dosya_sahibi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_ait_bilgisi = models.ForeignKey(klasorler,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    dosya = models.FileField(upload_to='klasor_dosyalari/',verbose_name="Dosya Adı",blank=True,null=True)
    dosya_adi = models.CharField(max_length = 400,verbose_name="Sözleşme Adı",blank = True,null = True)
    tarih = models.DateField(verbose_name = "Proje Tarihi",blank = True,null = True)
    aciklama = models.TextField(verbose_name = "Açıklama",blank = True,null = True)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class Event(models.Model):
    dosya_sahibi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    takvim_turu  =models.CharField(max_length=200,verbose_name="Takvim Etkinlik Türü",blank= True,null = True)
    baslangic_tarihi  = models.DateField(verbose_name = "Başlangıç Tarihi",blank = True,null = True)
    bitis_tarihi  = models.DateField(verbose_name = "Bitiş Tarihi",blank = True,null = True)
    baslangic_saati = models.TimeField(verbose_name = "Başlangıç Tarihi",blank = True,null = True)
    bitis_saati = models.TimeField(verbose_name = "Başlangıç Tarihi",blank = True,null = True)
    takvim_lokasyon  =models.CharField(max_length=200,verbose_name="Takvim Etkinlik Türü",blank= True,null = True)
    aciklma  =models.TextField(verbose_name="Açıklama",blank= True,null = True)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)



class YapilacakPlanlari(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser, verbose_name="Proje Ait Olduğu", blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=400, verbose_name="Adı", blank=True, null=True)
    teslim_tarihi = models.DateField(verbose_name="Proje Tarihi", blank=True, null=True)
    aciklama = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    status = models.CharField(max_length=200, verbose_name="Durum", blank=True, null=True)
    oncelik_durumu = models.CharField(max_length=200, verbose_name="öncelik Adı", blank=True, null=True)
    yapacaklar = models.ManyToManyField(CustomUser, blank=True, null=True, related_name="yapilacak_planlari")
    kayit_tarihi = models.DateTimeField(default=datetime.now, null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)



class YapilacakDosyalari(models.Model):
    dosya_sahibi = models.ForeignKey(CustomUser, verbose_name="Proje Ait Olduğu", blank=True, null=True, on_delete=models.SET_NULL, related_name="dosya_sahibi")
    proje_ait_bilgisi = models.ForeignKey(YapilacakPlanlari, verbose_name="Proje Ait Olduğu", blank=True, null=True, on_delete=models.SET_NULL, related_name="todo_sahibi")
    dosya = models.FileField(upload_to='yapilacak_dosyalari/', verbose_name="Dosya Adı", blank=True, null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class IsplaniPlanlari(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser, verbose_name="Proje Ait Olduğu", blank=True, null=True, on_delete=models.SET_NULL)
    katman = models.ForeignKey(katman, verbose_name="Proje KAtmanı", blank=True, null=True, on_delete=models.SET_NULL)
    locasyonx = models.CharField(max_length=400, verbose_name="Lokasyon", blank=True, null=True)
    locasyony = models.CharField(max_length=400, verbose_name="Lokasyon", blank=True, null=True)
    blok = models.ForeignKey(bloglar, verbose_name="Proje bloglari", blank=True, null=True, on_delete=models.SET_NULL)
    kat = models.IntegerField(default=0)
    title = models.CharField(max_length=400, verbose_name="Adı", blank=True, null=True)
    teslim_tarihi = models.DateField(verbose_name="Proje Tarihi", blank=True, null=True)
    aciklama = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    status = models.CharField(max_length=200, verbose_name="Durum", blank=True, null=True)
    oncelik_durumu = models.CharField(max_length=200, verbose_name="Öncelik Adı", blank=True, null=True)
    yapacaklar = models.ManyToManyField(CustomUser, blank=True, null=True, related_name="isplani_planlari")
    kayit_tarihi = models.DateTimeField(default=datetime.now, null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class IsplaniPlanlariIlerleme(models.Model):
    proje_ait_bilgisi = models.ForeignKey(IsplaniPlanlari, verbose_name="Proje Ait Olduğu", blank=True, null=True, on_delete=models.SET_NULL)
    teslim_tarihi = models.DateField(verbose_name="Proje Tarihi", blank=True, null=True)
    aciklama = models.TextField(verbose_name="Açıklama", blank=True, null=True)
    status = models.CharField(max_length=200, verbose_name="Durum", blank=True, null=True)
    yapan_kisi = models.ForeignKey(CustomUser, verbose_name="Yapan Kişi", related_name="isplani_planlari_ilerleme_yapanlar", blank=True, null=True, on_delete=models.SET_NULL)
    kayit_tarihi = models.DateTimeField(default=datetime.now, null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class IsplaniIlerlemeDosyalari(models.Model):
    dosya_sahibi = models.ForeignKey(IsplaniPlanlari, verbose_name="Proje Ait Olduğu", blank=True, null=True, on_delete=models.SET_NULL, related_name="dosya_sahibi_isplani_ilerleme_dosyalari")
    yapan_kisi = models.ForeignKey(CustomUser, verbose_name="Yapan Kişi", related_name="isplani_ilerleme_dosyalari_yapanlar", blank=True, null=True, on_delete=models.SET_NULL)
    proje_ait_bilgisi = models.ForeignKey(IsplaniPlanlariIlerleme, verbose_name="Proje Ait Olduğu", blank=True, null=True, on_delete=models.SET_NULL, related_name="dosya_sahibi_isplani_ilerleme_dosyalari")
    dosya = models.FileField(upload_to='isplani_dosyalari/', verbose_name="Dosya Adı", blank=True, null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class IsplaniDosyalari(models.Model):
    dosya_sahibi = models.ForeignKey(CustomUser, verbose_name="Proje Ait Olduğu", blank=True, null=True, on_delete=models.SET_NULL, related_name="dosya_sahibi_isplani_dosyalari")
    proje_ait_bilgisi = models.ForeignKey(IsplaniPlanlari, verbose_name="Proje Ait Olduğu", blank=True, null=True, on_delete=models.SET_NULL, related_name="dosya_sahibi_isplani_dosyalari")
    pin = models.CharField(max_length=400, verbose_name="pinmi", blank=True, null=True)
    dosya = models.FileField(upload_to='isplani_dosyalari/', verbose_name="Dosya Adı", blank=True, null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)


class gantt_olayi(models.Model):
    gantt_sahibii = models.ForeignKey(CustomUser, verbose_name="Gantt Sahibi", blank=True, null=True, on_delete=models.SET_NULL, related_name="gantt_sahibii")
    ganti_degistiren_kisi = models.ForeignKey(CustomUser, verbose_name="Gantt değiştiren kişi", blank=True, null=True, on_delete=models.SET_NULL, related_name="ganti_degistiren_kisi")
    gantt_verisi = models.TextField(verbose_name="json verisi")
    kayit_tarihi = models.DateTimeField(default=datetime.now, null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class gantt_verileri(models.Model):
    gantt_sahibi = models.ForeignKey(CustomUser, verbose_name="Gantt Sahibi", blank=True, null=True, on_delete=models.SET_NULL, related_name="gantt_sahibi")
    name = models.CharField(max_length=200,verbose_name="Gantt Adı",blank=True,null=True)
    progress = models.FloatField(verbose_name="İlerleme Druumu",default=0)
    progressByWorklog = models.BooleanField(default= False)
    relevance = models.IntegerField(default=0)
    type_ver = models.CharField(max_length=200,default="")
    typeId = models.CharField(max_length=200,default="")
    description = models.CharField(max_length=400,default="")
    code = models.CharField(max_length=200,default="")
    level = models.IntegerField(default=0)
    status = models.CharField(max_length=200,default="")
    depends = models.CharField(max_length=200,default="")
    canWrite = models.BooleanField(default=True)
    duration = models.FloatField(default=0)
    start = models.DateField(verbose_name="Başlangıç Tarihi", blank=True, null=True)
    bitis = models.DateField(verbose_name="Bitiş Tarihi", blank=True, null=True)
    startIsMilestone = models.BooleanField(default=False)
    endIsMilestone = models.BooleanField(default=False)
    collapsed = models.BooleanField(default=False)
    hasChild = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now, null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)


class genel_rapor(models.Model):
    Kayip_gun_sabepleri = (
        ('-1', '-1'),
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    raporu_olusturan = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL,related_name="raporu_olusturan")
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    tarih = models.DateTimeField(default=datetime.now,null=True)
    bitis_tarih = models.DateTimeField(default=datetime.now,null=True)
    raporu_onaylayan = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL,related_name="raporu_onaylayan")
    kayip_gun_sayisi = models.IntegerField(default=0,verbose_name="Kayıp Gün Sayısı")
    kayip_gun_aciklamasi = models.CharField(max_length=200,verbose_name="Kayıp Gün Açıklaması",blank=True,null=True)
    kayip_gun_sebebi = models.CharField(default='0',choices=Kayip_gun_sabepleri,max_length=200)
    onaylama_tarihi = models.DateTimeField(default=datetime.now,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class gelen_malzeme(models.Model):
    proje_ait_bilgisi = models.ForeignKey(genel_rapor,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    hangi_rapor = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    urun = models.ForeignKey(urunler,verbose_name="Gelen Ürün",blank=True,null=True,on_delete=models.SET_NULL)
    urun_adeti = models.FloatField(blank=True,null=True,verbose_name="Ürün Adeti")
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class genel_personel(models.Model):
    proje_ait_bilgisi = models.ForeignKey(genel_rapor,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    hangi_rapor = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    personel_departmani = models.ForeignKey(calisanlar_kategorisi,verbose_name="Gelen Ürün",blank=True,null=True,on_delete=models.SET_NULL)
    personel_sayisi = models.FloatField(blank=True,null=True,verbose_name="Personel Sayısı")
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class genel_imalat(models.Model):
    proje_ait_bilgisi = models.ForeignKey(genel_rapor,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    hangi_rapor = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    imalet_kalemi =  models.ForeignKey(santiye_kalemleri,verbose_name="Kalem Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    imalat_aciklama = models.TextField()
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class genel_aciklamalar(models.Model):
    proje_ait_bilgisi = models.ForeignKey(genel_rapor,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    hangi_rapor = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    genel_aciklama =  models.TextField()
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class genel_hava_durumu(models.Model):
    proje_ait_bilgisi = models.ForeignKey(genel_rapor,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    hangi_rapor = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    hava_durumu_sicaklik = models.FloatField(blank=True,null=True,verbose_name="hava_durumu Sıcaklık")
    hava_durumu_ruzgar = models.FloatField(blank=True,null=True,verbose_name="hava_durumu rüzgar") 
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class daire_evraklari(models.Model):
    evrak_kime_ait = models.ForeignKey(CustomUser, verbose_name="Proje Ait Olduğu", blank=True, null=True, on_delete=models.SET_NULL)
    daire = models.ForeignKey(daire_bilgisi, verbose_name="Daire", blank=True, null=True, on_delete=models.SET_NULL)
    evrak_adi = models.CharField(max_length=200, verbose_name="Evrak Adı", blank=True, null=True)
    evrak = models.FileField(upload_to='daire_evraklari/', verbose_name="Evrak", blank=True, null=True)
    kayit_tarihi = models.DateTimeField(default=datetime.now, null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)