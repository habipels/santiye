from django.db import models
from users.models import * 
from datetime import datetime

# Create your models here.
class cari (models.Model):
    cari_kart_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Cari Kartın Kime Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    cari_adi = models.CharField(max_length=400,verbose_name="Cari Adı",blank=True,null=True)
    telefon_numarasi = models.CharField(max_length=20,verbose_name="Telefon Numarası",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Cari Açkıklama",blank=True,null=True)
    bakiye = models.FloatField(verbose_name="Cari Bakiyesi",default=0)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    

class Kasa (models.Model):
    kasa_kart_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Kasa Kime Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    kasa_adi = models.CharField(max_length=400,verbose_name="Kasa Adı",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Kasa Açkıklama",blank=True,null=True)
    bakiye = models.FloatField(verbose_name="Kasa Bakiyesi",default=0)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)

class gelir_kategorisi(models.Model):
    gelir_kategoris_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Gelir Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    gelir_kategori_adi = models.CharField(max_length=400,verbose_name="Gelir Adı",blank=True,null=True)
    gelir_kategorisi_renk = models.CharField(max_length=200,verbose_name="Gelir Kaqtegorisi Renk",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Gelir Kategorisi Açkıklama",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)

class gider_kategorisi(models.Model):
    gider_kategoris_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Gider Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    gider_kategori_adi = models.CharField(max_length=400,verbose_name="Gider Adı",blank=True,null=True)
    gider_kategorisi_renk = models.CharField(max_length=200,verbose_name="Gider Kaqtegorisi Renk",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Gider Kategorisi Açkıklama",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
class gelir_etiketi(models.Model):
    gelir_kategoris_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Gelir Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    gelir_etiketi_adi = models.CharField(max_length=400,verbose_name="Gelir Adı",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
class gider_etiketi(models.Model):
    gider_kategoris_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Gider Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    gider_etiketi_adi = models.CharField(max_length=400,verbose_name="Gider Adı",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
class Gelir_Bilgisi(models.Model):
    gelir_kime_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Gelir Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    cari_bilgisi = models.ForeignKey(cari,verbose_name="Cari Bilgisi",blank=True,null=True,on_delete=models.SET_NULL)
    fatura_tarihi = models.DateTimeField(null=True,verbose_name="Fatura Tarihi",blank = True)
    vade_tarihi = models.DateTimeField(null=True,verbose_name="Vade Tarihi",blank = True)
    fatura_no = models.CharField(verbose_name="Fatura No",max_length=200,blank=True,null=True)
    aciklama = models.TextField(verbose_name="Gelir Açıklaması",blank=True,null=True)
    gelir_kategorisi = models.ForeignKey(gelir_kategorisi,verbose_name="Gelirin Kategori Bilgisi",blank=True,null=True,on_delete=models.SET_NULL)
    gelir_etiketi_sec = models.ManyToManyField(gelir_etiketi,blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
class Gider_Bilgisi(models.Model):
    gider_kime_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Gider Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    cari_bilgisi = models.ForeignKey(cari,verbose_name="Cari Bilgisi",blank=True,null=True,on_delete=models.SET_NULL)
    fatura_tarihi = models.DateTimeField(null=True,verbose_name="Fatura Tarihi",blank = True)
    fatura_no = models.CharField(verbose_name="Fatura No",max_length=200,blank=True,null=True)
    aciklama = models.TextField(verbose_name="Gelir Açıklaması",blank=True,null=True)
    gider_kategorisi = models.ForeignKey(gider_kategorisi,verbose_name="Gider Kategori Bilgisi",blank=True,null=True,on_delete=models.SET_NULL)
    gider_etiketi_sec = models.ManyToManyField(gider_etiketi,blank=True,null=True)
    tutar = models.FloatField(verbose_name="Toplam Tutar",default=0)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)


class virman(models.Model):
    virman_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Virman Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    virman_tarihi = models.DateTimeField(null=True,verbose_name="Virman Tarihi",blank = True)
    gonderen_kasa = models.ForeignKey(Kasa,verbose_name="Gonderen Kasa",blank=True,null=True,on_delete=models.SET_NULL,related_name ="virman_gonderen_kasa")
    alici_kasa = models.ForeignKey(Kasa,verbose_name="gönderilen Kasa",blank=True,null=True,on_delete=models.SET_NULL,related_name ="virman_alici_kasa")
    tutar = models.FloatField(verbose_name="Toplam Tutar",default=0)
    aciklama = models.TextField(verbose_name="Virman Açıklaması",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)


class urunler(models.Model):
    urun_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="ürün Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    urun_adi = models.CharField(max_length=400,verbose_name="Ürün ADı",blank=True,null=True)
    urun_fiyati = models.FloatField(verbose_name="Ürün Fiyatı",default=0)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)

class gider_urun_bilgisi(models.Model):
    urun_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Ürün Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    urun_bilgisi = models.ForeignKey(urunler,blank=True,null=True,verbose_name="Ürün Bilgisi",on_delete=models.SET_NULL)
    urun_fiyati = models.FloatField(verbose_name="Ürün Fiyatı",default=0)
    urun_adeti = models.FloatField(verbose_name="Ürün Adeti",default=0)
    gider_bilgis = models.ForeignKey(Gider_Bilgisi,blank=True,null=True,verbose_name="Gider Bilgisi",on_delete=models.SET_NULL)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
class gelir_urun_bilgisi(models.Model):
    urun_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Ürün Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    urun_bilgisi = models.ForeignKey(urunler,blank=True,null=True,verbose_name="Ürün Bilgisi",on_delete=models.SET_NULL)
    urun_fiyati = models.FloatField(verbose_name="Ürün Fiyatı",default=0)
    urun_indirimi = models.FloatField(verbose_name="Ürün Fiyatı",default=0)
    urun_adeti = models.BigIntegerField(verbose_name="Ürün Adeti",default=0)
    aciklama = models.CharField(max_length = 400,verbose_name ="Açıklama",blank = True,null = True)
    gider_bilgis = models.ForeignKey(Gelir_Bilgisi,blank=True,null=True,verbose_name="Gelir Bilgisi",on_delete=models.SET_NULL)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)    
    

class Gelir_odemesi(models.Model):
    gelir_kime_ait_oldugu = models.ForeignKey(Gelir_Bilgisi,verbose_name="Gelir Ödemesi Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    gelir_turu = models.CharField(max_length = 200,verbose_name="gelir_turu",blank = True,null=True)
    kasa_bilgisi = models.ForeignKey(Kasa,blank=True,null = True, verbose_name ="Kasa",on_delete=models.SET_NULL)
    tutar = models.FloatField(verbose_name = "Tutar",default = 0)
    tarihi = models.DateTimeField(blank=True,null=True)
    gelir_makbuzu = models.FileField(upload_to='makbuzlar/',verbose_name="Sayfaya Logo Light",blank=True,null=True)
    makbuz_no = models.CharField(max_length = 200,verbose_name="Makbuz No",blank = True,null=True)
    aciklama = models.CharField(max_length = 200,verbose_name="Açıklama",blank = True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)

class Gider_odemesi(models.Model):
    gider_kime_ait_oldugu = models.ForeignKey(Gider_Bilgisi,verbose_name="Gelir Ödemesi Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    tutar = models.FloatField(verbose_name = "Tutar",default = 0)
    gider_makbuzu = models.FileField(upload_to='makbuzlar/',verbose_name="Sayfaya Logo Light",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)

class faturalar_icin_logo(models.Model):
    gelir_kime_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Gelir Ödemesi Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    gelir_makbuzu = models.FileField(upload_to='faturalogosu/',verbose_name="Sayfaya Logo Light",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)