from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
from io import BytesIO
from simple_history.models import HistoricalRecords
from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
#from muhasebe.models import Gider_Bilgisi
# Create your models here.
class CustomUser(AbstractUser):

    STATUS = (
        ('sirket', 'sirket'),
        ('sirketcalisani', 'sirketcalisani'),
        ('moderator', 'moderator'),
    )

    email = models.EmailField(_('email address'), unique=True)
    status = models.CharField(_('status'), max_length=100, choices=STATUS, default='sirket')
    description = models.TextField(_("description"), max_length=600, default='', blank=True)
    kullanicilar_db = models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    kullanici_silme_bilgisi = models.BooleanField(_('user deletion info'), default= False)
    image  = models.FileField(upload_to='profile/',verbose_name=_("Profile"),blank=True,null=True,)
    background_image  = models.FileField(upload_to='background/',verbose_name=_("background"),blank=True,null=True,)
    telefon_numarasi =  models.CharField(_('phone number'), max_length= 20 , blank=True,null = True)
    imza_sifresi = models.CharField(_('approval password'), null= True,blank=True ,max_length=400)
    gorevi = models.CharField(_('duty'), max_length = 250 ,blank = True,null = True)
    adrrsi = models.TextField(_("address"), max_length=600, default='', blank=True)
    online  = models.BooleanField(_('online'), default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
    kullanici_tercih_dili = models.CharField(_('preferred language'), max_length=10, default="en")
    last_seen = models.DateTimeField(_('last seen'), default=timezone.now)

    def __str__(self):
        return self.username

    def update_last_seen(self):
        self.last_seen = timezone.now()
        self.save()

    def is_online(self):
        now = timezone.now()
        return now - self.last_seen < timezone.timedelta(minutes=5)

class faturalardaki_gelir_gider_etiketi_ozel(models.Model):
    kullanici = models.ForeignKey(CustomUser, on_delete = models.SET_NULL,blank  =True,null = True,verbose_name=_("user info"))
    gelir_etiketi = models.CharField(_('income tag'), max_length=10,blank = True,null=True)
    gider_etiketi = models.CharField(_('expense tag'), max_length=10,blank = True,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class LockScreenStatus(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_locked = models.BooleanField(_('is locked'), default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class personel_dosyalari(models.Model):
    kullanici = models.ForeignKey(CustomUser, on_delete = models.SET_NULL,blank  =True,null = True,verbose_name=_("user info"))
    dosyalari  = models.FileField(verbose_name=_("user file"),upload_to='kullanici_dosyasi/',blank=True,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class personel_izinleri(models.Model):
    #bu izinler kime ait
    isim = models.CharField(_('duty'), max_length = 250 ,blank = True,null = True)
    izinlerin_sahibi_kullanici = models.ForeignKey(CustomUser, on_delete = models.SET_NULL,blank  =True,null = True,verbose_name=_("user info"))
    #kasada virman yapma özelliği
    kasa_virman_olusturma_izni = models.BooleanField(_('cash transfer creation permission'), default= False)
    kasa_virman_gorme_izni = models.BooleanField(_('cash transfer viewing permission'), default= False)
    #kasada işlem yapma özelliği
    kasa_gosterme_izni = models.BooleanField(_('cash creation permission'), default = False)
    kasa_olusturma_izni = models.BooleanField(_('cash creation permission'), default = False)
    kasa_guncelleme_izni = models.BooleanField(_('cash update permission'), default = False)
    Kasa_silme_izni = models.BooleanField(_('cash deletion permission'), default = False)
    #kasada işlem yapma özelliği
    kasa_detay_izni = models.BooleanField(_('cash detail permission'), default = False)
    cari_detay_izni = models.BooleanField(_('current detail permission'), default = False)
    #cari hesaplarda işlem yapmöa özelliği
    cari_gosterme_izni = models.BooleanField(_('current creation permission'), default = False)
    cari_guncelleme_izni = models.BooleanField(_('current update permission'), default = False)
    cari_olusturma = models.BooleanField(_('current creation permission'), default= False)
    cari_silme_izni = models.BooleanField(_('current deletion permission'), default = False)
    #gelir gider kategori ve etiket  oluşturma silme düzenlme işlemi
    gelir_etiketi_olusturma = models.BooleanField(_('income tag creation permission'), default = False)
    gelir_etiketi_silme = models.BooleanField(_('income tag deletion permission'), default = False)
    gelir_etiketi_guncelleme = models.BooleanField(_('income tag update permission'), default = False)
    gelir_etiketi_gorme = models.BooleanField(_('income tag viewing permission'), default = False)
    gider_etiketi_olusturma = models.BooleanField(_('expense tag creation permission'), default = False)
    gider_etiketi_silme = models.BooleanField(_('expense tag deletion permission'), default = False)
    gider_etiketi_guncelleme = models.BooleanField(_('expense tag update permission'), default = False)
    gider_etiketi_gorme = models.BooleanField(_('expense tag viewing permission'), default = False)
    gider_kategorisi_olusturma = models.BooleanField(_('expense category creation permission'), default = False)
    gider_kategorisi_silme = models.BooleanField(_('expense category deletion permission'), default = False)
    gider_kategorisi_guncelleme = models.BooleanField(_('expense category update permission'), default = False)
    gider_kategorisi_gorme = models.BooleanField(_('expense category viewing permission'), default = False)
    gelir_kategorisi_olusturma = models.BooleanField(_('income category creation permission'), default = False)
    gelir_kategorisi_silme = models.BooleanField(_('income category deletion permission'), default = False)
    gelir_kategorisi_gorme = models.BooleanField(_('income category viewing permission'), default = False)
    gelir_kategorisi_guncelleme = models.BooleanField(_('income category update permission'), default = False)
    #ürün oluşturma silme özelliği
    urun_olusturma = models.BooleanField(_('product creation permission'), default = False)
    urun_silme = models.BooleanField(_('product deletion permission'), default = False)
    urun_guncelleme = models.BooleanField(_('product update permission'), default = False)
    urun_gorme = models.BooleanField(_('product viewing permission'), default = False)
    #Muhasabe Ayarları
    muhasabe_ayarlari_gorme = models.BooleanField(_('accounting settings viewing permission'), default = False)
    muhasabe_ayarlari_guncelleme = models.BooleanField(_('accounting settings update permission'), default = False)
    # gelir gider faturası oluştuma silme ve düzenleme özelliği
    gelir_faturasi_kesme_izni = models.BooleanField(_('income invoice creation permission'), default = False)
    gelir_faturasi_silme_izni = models.BooleanField(_('income invoice deletion permission'), default = False)
    gelir_faturasi_duzenleme_izni = models.BooleanField(_('income invoice update permission'), default = False)
    gelir_faturasi_gorme_izni = models.BooleanField(_('income invoice viewing permission'), default = False)
    gider_faturasi_kesme_izni = models.BooleanField(_('expense invoice creation permission'), default = False)
    gider_faturasi_silme_izni = models.BooleanField(_('expense invoice deletion permission'), default = False)
    gider_faturasi_duzenleme_izni = models.BooleanField(_('expense invoice update permission'), default = False)
    gider_faturasi_gorme_izni = models.BooleanField(_('expense invoice viewing permission'), default = False)
    #gelir gider makbuz işlemleri
    gider_faturasi_makbuz_kesme_izni = models.BooleanField(_('expense invoice receipt creation permission'), default = False)
    gider_faturasi_makbuz_silme_izni = models.BooleanField(_('expense invoice receipt deletion permission'), default = False)
    gider_faturasi_makbuz_duzenleme_izni = models.BooleanField(_('expense invoice receipt update permission'), default = False)
    gider_faturasi_makbuz_gorme_izni = models.BooleanField(_('expense invoice receipt viewing permission'), default = False)
    
    gelir_faturasi_makbuz_kesme_izni = models.BooleanField(_('income invoice receipt creation permission'), default = False)
    gelir_faturasi_makbuz_silme_izni = models.BooleanField(_('income invoice receipt deletion permission'), default = False)
    gelir_faturasi_makbuz_duzenleme_izni = models.BooleanField(_('income invoice receipt update permission'), default = False)
    gelir_faturasi_makbuz_gorme_izni = models.BooleanField(_('income invoice receipt viewing permission'), default = False)
    #şantiye proje oluştuma özelliği
    proje_tipi_olusturma = models.BooleanField(_('project type creation permission'), default = False)
    proje_tipi_silme = models.BooleanField(_('project type deletion permission'), default = False)
    proje_tipi_gorme = models.BooleanField(_('project type viewing permission'), default = False)
    proje_tipi_duzenleme = models.BooleanField(_('project type update permission'), default = False)
    #Şantiye Oluştuma
    santiye_olusturma = models.BooleanField(_('construction site creation permission'), default = False)
    santiye_silme = models.BooleanField(_('construction site deletion permission'), default = False)
    santiye_gorme = models.BooleanField(_('construction site viewing permission'), default = False)
    santiye_duzenleme = models.BooleanField(_('construction site update permission'), default = False)
    #Şantiye Blogları
    blog_olusturma = models.BooleanField(_('blog creation permission'), default = False)
    blog_silme = models.BooleanField(_('blog deletion permission'), default = False)
    blog_gorme = models.BooleanField(_('blog viewing permission'), default = False)
    blog_duzenleme = models.BooleanField(_('blog update permission'), default = False)
    #Şantiye Kalemleri
    kalemleri_olusturma = models.BooleanField(_('item creation permission'), default = False)
    kalemleri_silme = models.BooleanField(_('item deletion permission'), default = False)
    kalemleri_gorme = models.BooleanField(_('item viewing permission'), default = False)
    kalemleri_duzenleme = models.BooleanField(_('item update permission'), default = False)
    #Şantiye raporu
    santiye_raporu_olusturma = models.BooleanField(_('construction site report creation permission'), default = False)
    santiye_raporu_silme = models.BooleanField(_('construction site report deletion permission'), default = False)
    santiye_raporu_gorme = models.BooleanField(_('construction site report viewing permission'), default = False)
    santiye_raporu_duzenleme = models.BooleanField(_('construction site report update permission'), default = False)
    #Sözleşmeler Kategorileri
    sozlesmeler_olusturma = models.BooleanField(_('contract creation permission'), default = False)
    sozlesmeler_silme = models.BooleanField(_('contract deletion permission'), default = False)
    sozlesmeler_gorme = models.BooleanField(_('contract viewing permission'), default = False)
    sozlesmeler_duzenleme = models.BooleanField(_('contract update permission'), default = False)
    #Hakedişler Kategorileri
    hakedisler_olusturma = models.BooleanField(_('progress payment creation permission'), default = False)
    hakedisler_silme = models.BooleanField(_('progress payment deletion permission'), default = False)
    hakedisler_gorme = models.BooleanField(_('progress payment viewing permission'), default = False)
    hakedisler_duzenleme = models.BooleanField(_('progress payment update permission'), default = False)
    #Taşeronlar Kategorileri
    taseronlar_olusturma = models.BooleanField(_('subcontractor creation permission'), default = False)
    taseronlar_silme = models.BooleanField(_('subcontractor deletion permission'), default = False)
    taseronlar_gorme = models.BooleanField(_('subcontractor viewing permission'), default = False)
    taseronlar_duzenleme = models.BooleanField(_('subcontractor update permission'), default = False)
    #Üst Yüklenici Kategorileri
    ust_yuklenici_olusturma = models.BooleanField(_('main contractor creation permission'), default = False)
    ust_yuklenici_silme = models.BooleanField(_('main contractor deletion permission'), default = False)
    ust_yuklenici_gorme = models.BooleanField(_('main contractor viewing permission'), default = False)
    ust_yuklenici_duzenleme = models.BooleanField(_('main contractor update permission'), default = False)
    #
    #İlerleme Takibi Kategorileri
    ilerleme_takibi_olusturma = models.BooleanField(_('progress tracking creation permission'), default = False)
    ilerleme_takibi_silme = models.BooleanField(_('progress tracking deletion permission'), default = False)
    ilerleme_takibi_gorme = models.BooleanField(_('progress tracking viewing permission'), default = False)
    ilerleme_takibi_duzenleme = models.BooleanField(_('progress tracking update permission'), default = False)
    #İş Planı Kategorileri
    is_plani_olusturma = models.BooleanField(_('work plan creation permission'), default = False)
    is_plani_silme = models.BooleanField(_('work plan deletion permission'), default = False)
    is_plani_gorme = models.BooleanField(_('work plan viewing permission'), default = False)
    is_plani_duzenleme = models.BooleanField(_('work plan update permission'), default = False)
    #Yapacaklar Kategorileri
    yapilacaklar_olusturma = models.BooleanField(_('to-do creation permission'), default = False)
    yapilacaklar_silme = models.BooleanField(_('to-do deletion permission'), default = False)
    yapilacaklar_gorme = models.BooleanField(_('to-do viewing permission'), default = False)
    yapilacaklar_duzenleme = models.BooleanField(_('to-do update permission'), default = False)
    #Dosya Yöneticisi Kategorileri
    dosya_yoneticisi_olusturma = models.BooleanField(_('file manager creation permission'), default = False)
    dosya_yoneticisi_silme = models.BooleanField(_('file manager deletion permission'), default = False)
    dosya_yoneticisi_gorme = models.BooleanField(_('file manager viewing permission'), default = False)
    dosya_yoneticisi_duzenleme = models.BooleanField(_('file manager update permission'), default = False)
    #Projeler Kategorileri
    projeler_olusturma = models.BooleanField(_('project creation permission'), default = False)
    projeler_silme = models.BooleanField(_('project deletion permission'), default = False)
    projeler_gorme = models.BooleanField(_('project viewing permission'), default = False)
    projeler_duzenleme = models.BooleanField(_('project update permission'), default = False)
    #Personeller Kategorileri back end olarak yapılmadı
    personeller_olusturma = models.BooleanField(_('personnel creation permission'), default = False)
    personeller_silme = models.BooleanField(_('personnel deletion permission'), default = False)
    personeller_gorme = models.BooleanField(_('personnel viewing permission'), default = False)
    personeller_duzenleme = models.BooleanField(_('personnel update permission'), default = False)
    #Dashboard Kategorileri
    dashboard_olusturma = models.BooleanField(_('dashboard creation permission'), default = False)
    dashboard_silme = models.BooleanField(_('dashboard deletion permission'), default = False)
    dashboard_gorme = models.BooleanField(_('dashboard viewing permission'), default = False)
    dashboard_duzenleme = models.BooleanField(_('dashboard update permission'), default = False)
    #Gelir Özeti Kategorileri
    gelir_ozeti_olusturma = models.BooleanField(_('income summary creation permission'), default = False)
    gelir_ozeti_silme = models.BooleanField(_('income summary deletion permission'), default = False)
    gelir_ozeti_gorme = models.BooleanField(_('income summary viewing permission'), default = False)
    gelir_ozeti_duzenleme = models.BooleanField(_('income summary update permission'), default = False)
    #Gider Özeti Kategorileri
    gider_ozeti_olusturma = models.BooleanField(_('expense summary creation permission'), default = False)
    gider_ozeti_silme = models.BooleanField(_('expense summary deletion permission'), default = False)
    gider_ozeti_gorme = models.BooleanField(_('expense summary viewing permission'), default = False)
    gider_ozeti_duzenleme = models.BooleanField(_('expense summary update permission'), default = False)
    #hesap Ekstra Kategorileri
    hesap_ekstra_olusturma = models.BooleanField(_('account extra creation permission'), default = False)
    hesap_ekstra_silme = models.BooleanField(_('account extra deletion permission'), default = False)
    hesap_ekstra_gorme = models.BooleanField(_('account extra viewing permission'), default = False)
    hesap_ekstra_duzenleme = models.BooleanField(_('account extra update permission'), default = False)
    #virman Raporu Kategorileri
    virman_raporu_olusturma = models.BooleanField(_('transfer report creation permission'), default = False)
    virman_raporu_silme = models.BooleanField(_('transfer report deletion permission'), default = False)
    virman_raporu_gorme = models.BooleanField(_('transfer report viewing permission'), default = False)
    virman_raporu_duzenleme = models.BooleanField(_('transfer report update permission'), default = False)
    #stok back end olarak bağlanmmadı
    satin_alma_talebi_olusturma = models.BooleanField(_('purchase request creation permission'), default = False)
    satin_alma_talebi_silme = models.BooleanField(_('purchase request deletion permission'), default = False)
    satin_alma_talebi_gorme = models.BooleanField(_('purchase request viewing permission'), default = False)
    satin_alma_talebi_duzenleme = models.BooleanField(_('purchase request update permission'), default = False)
    #stok back end olarak bağlanmmadı
    satin_alma_talebi_onaylama_olusturma = models.BooleanField(_('purchase request approval creation permission'), default = False)
    satin_alma_talebi_onaylama_silme = models.BooleanField(_('purchase request approval deletion permission'), default = False)
    satin_alma_talebi_onaylama_gorme = models.BooleanField(_('purchase request approval viewing permission'), default = False)
    satin_alma_talebi_onaylama_duzenleme = models.BooleanField(_('purchase request approval update permission'), default = False)
    stok_olusturma = models.BooleanField(_('stock creation permission'), default = False)
    stok_talebi_onaylama_silme = models.BooleanField(_('stock request approval deletion permission'), default = False)
    stok_talebi_onaylama_gorme = models.BooleanField(_('stock request approval viewing permission'), default = False)
    stok_talebi_onaylama_duzenleme = models.BooleanField(_('stock request approval update permission'), default = False)
    zimmet_olusturma = models.BooleanField(_('assignment creation permission'), default = False)
    zimmet_silme = models.BooleanField(_('assignment deletion permission'), default = False)
    zimmet_gorme = models.BooleanField(_('assignment viewing permission'), default = False)
    #puantaj durum
    personeller_puantaj_olusturma = models.BooleanField(_('personnel attendance creation permission'), default = False)
    personeller_puantaj_silme = models.BooleanField(_('personnel attendance deletion permission'), default = False)
    personeller_puantaj_gorme = models.BooleanField(_('personnel attendance viewing permission'), default = False)
    personeller_puantaj_duzenleme = models.BooleanField(_('personnel attendance update permission'), default = False)
    #personel maaş ödeme
    personeller_odeme_olusturma = models.BooleanField(_('personnel payment creation permission'), default = False)
    personeller_odeme_silme = models.BooleanField(_('personnel payment deletion permission'), default = False)
    personeller_odeme_gorme = models.BooleanField(_('personnel payment viewing permission'), default = False)
    personeller_odeme_duzenleme = models.BooleanField(_('personnel payment update permission'), default = False)
    #personel maaş ödeme
    katman_olusturma = models.BooleanField(_('layer creation permission'), default = False)
    katman_silme = models.BooleanField(_('layer deletion permission'), default = False)
    katman_gorme = models.BooleanField(_('layer viewing permission'), default = False)
    katman_duzenleme = models.BooleanField(_('layer update permission'), default = False)

    #gant
    gant_olusturma = models.BooleanField(_('gant creation permission'), default = False)
    gant_gorme = models.BooleanField(_('gant viewing permission'), default = False)
    gant_duzenleme = models.BooleanField(_('gant update permission'), default = False)
    #genel Rapor
    genel_rapor_olusturma = models.BooleanField(_('general report creation permission'), default = False)
    genel_rapor_gorme = models.BooleanField(_('general report viewing permission'), default = False)
    genel_rapor_duzenleme = models.BooleanField(_('general report update permission'), default = False)
    genel_rapor_silme = models.BooleanField(_('general report deletion permission'), default = False)
    genel_rapor_onaylama = models.BooleanField(_('general report approval permission'), default = False)
    #musteri Kısmı
    musteri_olusturma = models.BooleanField(_('customer creation permission'), default = False)
    musteri_gorme = models.BooleanField(_('customer viewing permission'), default = False)
    musteri_duzenleme = models.BooleanField(_('customer update permission'), default = False)
    musteri_silme = models.BooleanField(_('customer deletion permission'), default = False)
    # CRM permissions
    crm_musteri_olusturma = models.BooleanField(_('CRM customer creation permission'), default=False)
    crm_musteri_silme = models.BooleanField(_('CRM customer deletion permission'), default=False)
    crm_musteri_gorme = models.BooleanField(_('CRM customer viewing permission'), default=False)
    crm_musteri_duzenleme = models.BooleanField(_('CRM customer update permission'), default=False)
    
    crm_talep_olusturma = models.BooleanField(_('CRM request creation permission'), default=False)
    crm_talep_silme = models.BooleanField(_('CRM request deletion permission'), default=False)
    crm_talep_gorme = models.BooleanField(_('CRM request viewing permission'), default=False)
    crm_talep_duzenleme = models.BooleanField(_('CRM request update permission'), default=False)
    
    crm_teklif_olusturma = models.BooleanField(_('CRM offer creation permission'), default=False)
    crm_teklif_silme = models.BooleanField(_('CRM offer deletion permission'), default=False)
    crm_teklif_gorme = models.BooleanField(_('CRM offer viewing permission'), default=False)
    crm_teklif_duzenleme = models.BooleanField(_('CRM offer update permission'), default=False)
    
    crm_daire_olusturma = models.BooleanField(_('CRM apartment creation permission'), default=False)
    crm_daire_silme = models.BooleanField(_('CRM apartment deletion permission'), default=False)
    crm_daire_gorme = models.BooleanField(_('CRM apartment viewing permission'), default=False)
    crm_daire_duzenleme = models.BooleanField(_('CRM apartment update permission'), default=False)
    
    crm_evrak_olusturma = models.BooleanField(_('CRM document creation permission'), default=False)
    crm_evrak_silme = models.BooleanField(_('CRM document deletion permission'), default=False)
    crm_evrak_gorme = models.BooleanField(_('CRM document viewing permission'), default=False)
    crm_evrak_duzenleme = models.BooleanField(_('CRM document update permission'), default=False)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

class bagli_kullanicilar(models.Model):
    #bu izinler kime ait
    izinler = models.ForeignKey(personel_izinleri, on_delete = models.CASCADE,blank  =True,null = True,verbose_name=_("user info"))
    kullanicilar = models.ForeignKey(CustomUser, on_delete = models.CASCADE,blank  =True,null = True,verbose_name=_("user info"))

from datetime import datetime
from simple_history.models import HistoricalRecords
class calisanlar_kategorisi(models.Model):
    kategori_kime_ait = models.ForeignKey(CustomUser,verbose_name=_("employee owner"),blank=True,null=True,on_delete=models.SET_NULL)
    kategori_isimi = models.CharField(_('employee category name'), max_length= 200)
    silinme_bilgisi = models.BooleanField(_('deletion info'), default=False)
    kayit_tarihi = models.DateTimeField(_('record date'), default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class calisanlar_pozisyonu(models.Model):
    kategori_kime_ait = models.ForeignKey(CustomUser,verbose_name=_("employee owner"),blank=True,null=True,on_delete=models.SET_NULL)
    kategori_isimi = models.CharField(_('employee category name'), max_length= 200)
    silinme_bilgisi = models.BooleanField(_('deletion info'), default=False)
    kayit_tarihi = models.DateTimeField(_('record date'), default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class calisanlar(models.Model):
    STATUS = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        
    )#0 Çalışıyor # diğerleri Çalışmıyor 
    calisan_kime_ait = models.ForeignKey(CustomUser,verbose_name=_("employee owner"),blank=True,null=True,on_delete=models.SET_NULL)
    calisan_kategori = models.ForeignKey(calisanlar_kategorisi,verbose_name=_("employee category"),blank=True,null=True,on_delete=models.SET_NULL)
    calisan_pozisyonu = models.ForeignKey(calisanlar_pozisyonu,verbose_name=_("employee position"),blank=True,null=True,on_delete=models.SET_NULL)
    uyrugu = models.CharField(_('nationality'), max_length=200,null=True,blank = True)
    pasaport_numarasi = models.CharField(_('passport number'), max_length=200,null=True,blank = True)
    isim = models.CharField(_('name'), max_length=200,null=True,blank = True)
    soyisim = models.CharField(_('surname'), max_length=200,null=True,blank = True)
    profile  = models.FileField(upload_to='calisanprofili/',verbose_name=_("profile"),blank=True,null=True)
    dogum_tarihi = models.DateTimeField(_('birth date'), null=True,blank = True)
    telefon_numarasi = models.CharField(_('phone number'), max_length=20,null=True,blank = True)
    status = models.CharField(_('status'), max_length=100, choices=STATUS, default='0')
    silinme_bilgisi = models.BooleanField(_('deletion info'), default=False)
    kayit_tarihi = models.DateTimeField(_('record date'), default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class calisan_maas_durumlari(models.Model):
    calisan = models.ForeignKey(calisanlar,verbose_name=_("employee"),blank=True,null=True,on_delete=models.SET_NULL)
    maas = models.FloatField(_('salary'), default=0,blank=True,null=True)
    yevmiye = models.FloatField(_('daily wage'), default=0,blank=True,null=True)
    fazla_mesai_orani = models.FloatField(_('overtime rate'), default=0.20,blank=True,null=True)
    durum = models.BooleanField(_('status'), default=False) #True Maaşlı , False Yevmiye
    para_birimi =models.BooleanField(_('currency'), default=False) #True dolor , False dinar
    silinme_bilgisi = models.BooleanField(_('deletion info'), default=False)
    kayit_tarihi = models.DateTimeField(_('record date'), default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
class calisan_belgeleri(models.Model):
    calisan = models.ForeignKey(calisanlar,verbose_name=_("employee"),blank=True,null=True,on_delete=models.SET_NULL)
    belge_turu = models.CharField(_('document type'), max_length=200,null=True,blank = True)
    belge  = models.FileField(upload_to='belge/',verbose_name=_("document"),blank=True,null=True)
    silinme_bilgisi = models.BooleanField(_('deletion info'), default=False)
    kayit_tarihi = models.DateTimeField(_('record date'), default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
from django.utils import timezone
class calisanlar_calismalari(models.Model):
    mesai_orani = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    calisan = models.ForeignKey(calisanlar,verbose_name=_("employee"),blank=True,null=True,on_delete=models.SET_NULL)
    maas = models.ForeignKey(calisan_maas_durumlari,verbose_name=_("employee"),blank=True,null=True,on_delete=models.SET_NULL)
    normal_calisma_saati = models.FloatField(_('normal working hours'), default=0,blank=True,null=True)
    mesai_calisma_saati = models.FloatField(_('overtime working hours'), default=0,blank=True,null=True)
    mesai_oran_tutma = models.CharField(_('overtime rate'), max_length=100, choices=mesai_orani, default='1')
    tarihi = models.DateTimeField(_('working date'), null=True,blank = True)
    guncelleme_tarihi = models.DateTimeField(_('date modified'), default=timezone.now)
    kayit_tarihi = models.DateTimeField(_('record date'), default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)
from django.db import models


class Group(models.Model):
    name = models.CharField(_('name'), max_length=100)
    members = models.ManyToManyField(CustomUser, related_name='user_groups')
    image  = models.FileField(upload_to='chatgrup_resimleri/',verbose_name=_("Profile"),blank=True,null=True,)
    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_messages')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_messages')
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    content = models.TextField(_('content'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    read = models.BooleanField(_('read'), default=False)  # Yeni alan

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
