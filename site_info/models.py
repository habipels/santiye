from django.db import models
from users.models import * 
from datetime import datetime


class proje_tipi(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Tipi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    Proje_tipi_adi = models.CharField(max_length=400,verbose_name="Proje Tipi Adı",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    durum_bilgisi = models.BooleanField(default=True)


class santiye(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_tipi = models.ForeignKey(proje_tipi,verbose_name="Proje Tipi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_adi = models.CharField(max_length = 200,verbose_name="Proje Adı",blank=True,null = True)
    kat_sayisi =models.FloatField(default = 1,verbose_name="Kat Bilgisi")
    blog_sayisi =models.BigIntegerField(default = 1,verbose_name="Blog Bilgisi")
    blog_adi = models.CharField(max_length = 200,verbose_name="Blog Adı",blank=True,null = True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)

class bloglar(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    blog_adi = models.CharField(max_length=200,verbose_name="Blog Adı",blank=True,null = True)
    blog_numarasi = models.BigIntegerField(default = 1,verbose_name="Blog Numarasi")

class santiye_kalemleri(models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    kalem_adi = models.CharField(max_length= 200,verbose_name="Kalem Adı",blank = True,null = True)
    santiye_agirligi = models.FloatField(default = 0 ,verbose_name = "Kalem Şantiye Ağırlığı")
    santiye_finansal_agirligi = models.FloatField(default = 0,verbose_name = "Kalem Finansal Ağırlık")
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)

class santiye_kalemlerin_dagilisi (models.Model):
    proje_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Proje Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    proje_santiye_Ait = models.ForeignKey(santiye,verbose_name="santiye Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    kat = models.IntegerField(default = 0,verbose_name="kat Numarası")
    blog_bilgisi = models.ForeignKey(bloglar,verbose_name="Blog Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    degistirme_tarihi = models.DateTimeField(default=datetime.now,null=True)
    tamamlanma_bilgisi = models.BooleanField(default=False)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)