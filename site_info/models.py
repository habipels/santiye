from django.db import models
from users.models import *
from datetime import datetime
from muhasebe.models import *
from simple_history.models import HistoricalRecords
from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords
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

class santiye(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_tipi = models.ForeignKey(proje_tipi,verbose_name="Proje Tipi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_adi = models.CharField(max_length = 200,verbose_name="Proje Adı",blank=True,null = True)
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
    dosya = models.FileField(upload_to='isplani_dosyalari/', verbose_name="Dosya Adı", blank=True, null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)