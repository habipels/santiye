from django.db import models
from users.models import * 
from datetime import datetime
from simple_history.models import HistoricalRecords
from django.conf import settings
from django.utils import timezone
import pytz
import geoip2.database
from django.http import JsonResponse
def get_country_from_ip(ip_address):
    # IP adresine göre ülkeyi döndüren fonksiyon
    try:
        with geoip2.database.Reader('geoip/GeoLite2-Country.mmdb') as reader:
            response = reader.country(ip_address)
            country = response.country.iso_code  # Ülke kodunu alıyoruz (örn. 'TR' için Türkiye)
            return country
    except geoip2.errors.AddressNotFoundError:
        return 'Unknown'  # Eğer ülke bulunamazsa 'Unknown' dönebiliriz

def get_time_zone_from_country(country):
    # Ülke ISO kodlarına göre zaman dilimlerini döndüren harita
    time_zones = {
        'AF': 'Asia/Kabul',
        'AL': 'Europe/Tirane',
        'DZ': 'Africa/Algiers',
        'AS': 'Pacific/Pago_Pago',
        'AD': 'Europe/Andorra',
        'AO': 'Africa/Luanda',
        'AR': 'America/Argentina/Buenos_Aires',
        'AM': 'Asia/Yerevan',
        'AU': 'Australia/Sydney',
        'AT': 'Europe/Vienna',
        'AZ': 'Asia/Baku',
        'BS': 'America/Nassau',
        'BH': 'Asia/Bahrain',
        'BD': 'Asia/Dhaka',
        'BB': 'America/Barbados',
        'BY': 'Europe/Minsk',
        'BE': 'Europe/Brussels',
        'BZ': 'America/Belize',
        'BJ': 'Africa/Porto-Novo',
        'BT': 'Asia/Thimphu',
        'BO': 'America/La_Paz',
        'BA': 'Europe/Sarajevo',
        'BW': 'Africa/Gaborone',
        'BR': 'America/Sao_Paulo',
        'BN': 'Asia/Brunei',
        'BG': 'Europe/Sofia',
        'BF': 'Africa/Ouagadougou',
        'BI': 'Africa/Bujumbura',
        'KH': 'Asia/Phnom_Penh',
        'CM': 'Africa/Douala',
        'CA': 'America/Toronto',
        'CV': 'Atlantic/Cape_Verde',
        'KY': 'America/Cayman',
        'CF': 'Africa/Bangui',
        'TD': 'Africa/Ndjamena',
        'CL': 'America/Santiago',
        'CN': 'Asia/Shanghai',
        'CO': 'America/Bogota',
        'KM': 'Indian/Comoro',
        'CG': 'Africa/Brazzaville',
        'CD': 'Africa/Kinshasa',
        'CK': 'Pacific/Rarotonga',
        'CR': 'America/Costa_Rica',
        'CI': 'Africa/Abidjan',
        'HR': 'Europe/Zagreb',
        'CU': 'America/Havana',
        'CY': 'Asia/Nicosia',
        'CZ': 'Europe/Prague',
        'DK': 'Europe/Copenhagen',
        'DJ': 'Africa/Djibouti',
        'DM': 'America/Dominica',
        'DO': 'America/Santo_Domingo',
        'EC': 'America/Guayaquil',
        'EG': 'Africa/Cairo',
        'SV': 'America/El_Salvador',
        'GQ': 'Africa/Malabo',
        'ER': 'Africa/Asmara',
        'EE': 'Europe/Tallinn',
        'ET': 'Africa/Addis_Ababa',
        'FJ': 'Pacific/Fiji',
        'FI': 'Europe/Helsinki',
        'FR': 'Europe/Paris',
        'GA': 'Africa/Libreville',
        'GB': 'Europe/London',
        'GE': 'Asia/Tbilisi',
        'GH': 'Africa/Accra',
        'GR': 'Europe/Athens',
        'GD': 'America/Grenada',
        'GT': 'America/Guatemala',
        'GN': 'Africa/Conakry',
        'GW': 'Africa/Bissau',
        'GY': 'America/Guyana',
        'HT': 'America/Port-au-Prince',
        'HN': 'America/Tegucigalpa',
        'HK': 'Asia/Hong_Kong',
        'HU': 'Europe/Budapest',
        'IS': 'Atlantic/Reykjavik',
        'IN': 'Asia/Kolkata',
        'ID': 'Asia/Jakarta',
        'IR': 'Asia/Tehran',
        'IQ': 'Asia/Baghdad',
        'IE': 'Europe/Dublin',
        'IL': 'Asia/Jerusalem',
        'IT': 'Europe/Rome',
        'JM': 'America/Jamaica',
        'JP': 'Asia/Tokyo',
        'JO': 'Asia/Amman',
        'KZ': 'Asia/Almaty',
        'KE': 'Africa/Nairobi',
        'KI': 'Pacific/Tarawa',
        'KW': 'Asia/Kuwait',
        'KG': 'Asia/Bishkek',
        'LA': 'Asia/Vientiane',
        'LV': 'Europe/Riga',
        'LB': 'Asia/Beirut',
        'LS': 'Africa/Maseru',
        'LR': 'Africa/Monrovia',
        'LY': 'Africa/Tripoli',
        'LT': 'Europe/Vilnius',
        'LU': 'Europe/Luxembourg',
        'MO': 'Asia/Macau',
        'MK': 'Europe/Skopje',
        'MG': 'Indian/Antananarivo',
        'MW': 'Africa/Blantyre',
        'MY': 'Asia/Kuala_Lumpur',
        'MV': 'Indian/Maldives',
        'ML': 'Africa/Bamako',
        'MT': 'Europe/Malta',
        'MH': 'Pacific/Majuro',
        'MQ': 'America/Martinique',
        'MR': 'Africa/Nouakchott',
        'MU': 'Indian/Mauritius',
        'YT': 'Indian/Mayotte',
        'MX': 'America/Mexico_City',
        'FM': 'Pacific/Guam',
        'MD': 'Europe/Chisinau',
        'MC': 'Europe/Monaco',
        'MN': 'Asia/Ulaanbaatar',
        'ME': 'Europe/Belgrade',
        'MS': 'America/Port_of_Spain',
        'MA': 'Africa/Casablanca',
        'MZ': 'Africa/Maputo',
        'MM': 'Asia/Yangon',
        'MW': 'Africa/Blantyre',
        'NA': 'Africa/Windhoek',
        'NP': 'Asia/Kathmandu',
        'NI': 'America/Managua',
        'NE': 'Africa/Niamey',
        'NG': 'Africa/Lagos',
        'NO': 'Europe/Oslo',
        'NP': 'Asia/Kathmandu',
        'PK': 'Asia/Karachi',
        'PA': 'America/Panama',
        'PG': 'Pacific/Port_Moresby',
        'PY': 'America/Asuncion',
        'PE': 'America/Lima',
        'PH': 'Asia/Manila',
        'PL': 'Europe/Warsaw',
        'PT': 'Europe/Lisbon',
        'PR': 'America/Puerto_Rico',
        'QA': 'Asia/Qatar',
        'RO': 'Europe/Bucharest',
        'RU': 'Europe/Moscow',
        'RW': 'Africa/Kigali',
        'SA': 'Asia/Riyadh',
        'RS': 'Europe/Belgrade',
        'SC': 'Indian/Mahe',
        'SL': 'Africa/Freetown',
        'SG': 'Asia/Singapore',
        'SK': 'Europe/Bratislava',
        'SI': 'Europe/Ljubljana',
        'SE': 'Europe/Stockholm',
        'CH': 'Europe/Zurich',
        'SY': 'Asia/Damascus',
        'TJ': 'Asia/Dushanbe',
        'TH': 'Asia/Bangkok',
        'TG': 'Africa/Lome',
        'TO': 'Pacific/Tongatapu',
        'TT': 'America/Port_of_Spain',
        'TN': 'Africa/Tunis',
        'TR': 'Europe/Istanbul',
        'TM': 'Asia/Ashgabat',
        'UG': 'Africa/Kampala',
        'UA': 'Europe/Kiev',
        'AE': 'Asia/Dubai',
        'GB': 'Europe/London',
        'US': 'America/New_York',
        'UY': 'America/Montevideo',
        'UZ': 'Asia/Tashkent',
        'VU': 'Pacific/Efate',
        'VE': 'America/Caracas',
        'VN': 'Asia/Ho_Chi_Minh',
        'YE': 'Asia/Aden',
        'ZM': 'Africa/Lusaka',
        'ZW': 'Africa/Harare',
    }
    return time_zones.get(country, 'UTC')  # Varsayılan olarak UTC döner


# Create your models here.
class cari(models.Model):
    cari_kart_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Cari Kartın Kime Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    cari_adi = models.CharField(max_length=400,verbose_name="Cari Adı",blank=True,null=True)
    telefon_numarasi = models.CharField(max_length=20,verbose_name="Telefon Numarası",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Cari Açkıklama",blank=True,null=True)
    bakiye = models.FloatField(verbose_name="Cari Bakiyesi",default=0)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(cari, self).save(*args, **kwargs)

class Kasa(models.Model):
    kasa_kart_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Kasa Kime Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    kasa_adi = models.CharField(max_length=400,verbose_name="Kasa Adı",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Kasa Açkıklama",blank=True,null=True)
    bakiye = models.FloatField(verbose_name="Kasa Bakiyesi",default=0)
    avans_icin_kullan = models.BooleanField(default=False)
    maas_icin_kullan = models.BooleanField(default=False)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(Kasa, self).save(*args, **kwargs)

class gelir_kategorisi(models.Model):
    gelir_kategoris_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Gelir Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    gelir_kategori_adi = models.CharField(max_length=400,verbose_name="Gelir Adı",blank=True,null=True)
    gelir_kategorisi_renk = models.CharField(max_length=200,verbose_name="Gelir Kaqtegorisi Renk",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Gelir Kategorisi Açkıklama",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(gelir_kategorisi, self).save(*args, **kwargs)

class gider_kategorisi(models.Model):
    gider_kategoris_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Gider Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    gider_kategori_adi = models.CharField(max_length=400,verbose_name="Gider Adı",blank=True,null=True)
    gider_kategorisi_renk = models.CharField(max_length=200,verbose_name="Gider Kaqtegorisi Renk",blank=True,null=True)
    aciklama = models.TextField(verbose_name="Gider Kategorisi Açkıklama",blank=True,null=True)
    avans_icin_kullan = models.BooleanField(default=False)
    maas_icin_kullan = models.BooleanField(default=False)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(gider_kategorisi, self).save(*args, **kwargs)

class gelir_etiketi(models.Model):
    gelir_kategoris_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Gelir Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    gelir_etiketi_adi = models.CharField(max_length=400,verbose_name="Gelir Adı",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(gelir_etiketi, self).save(*args, **kwargs)

class gider_etiketi(models.Model):
    gider_kategoris_ait_bilgisi = models.ForeignKey(CustomUser,verbose_name="Gider Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    gider_etiketi_adi = models.CharField(max_length=400,verbose_name="Gider Adı",blank=True,null=True)
    avans_icin_kullan = models.BooleanField(default=False)
    maas_icin_kullan = models.BooleanField(default=False)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(gider_etiketi, self).save(*args, **kwargs)

class Gelir_Bilgisi(models.Model):
    gelir_kime_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Gelir Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    cari_bilgisi = models.ForeignKey(cari,verbose_name="Cari Bilgisi",blank=True,null=True,on_delete=models.SET_NULL)
    fatura_tarihi = models.DateTimeField(null=True,verbose_name="Fatura Tarihi",blank = True)
    vade_tarihi = models.DateTimeField(null=True,verbose_name="Vade Tarihi",blank = True)
    fatura_no = models.CharField(verbose_name="Fatura No",max_length=200,blank=True,null=True)
    doviz = models.CharField(verbose_name="Döviz",max_length=200,blank=True,null=True)
    aciklama = models.TextField(verbose_name="Gelir Açıklaması",blank=True,null=True)
    gelir_kategorisii = models.ForeignKey(gelir_kategorisi,verbose_name="Gelirin Kategori Bilgisi",blank=True,null=True,on_delete=models.SET_NULL)
    gelir_etiketi_sec = models.ManyToManyField(gelir_etiketi,blank=True,null=True)
    toplam_tutar = models.FloatField(verbose_name="Toplam Tutar",default=0)
    kalan_tutar = models.FloatField(verbose_name="Kalan Tutar",default=0)
    silinme_bilgisi = models.BooleanField(default=False)
    fatura_gorseli = models.FileField(upload_to='fatura_gorseli/',verbose_name="fatura Görseli",blank=True,null=True)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(Gelir_Bilgisi, self).save(*args, **kwargs)

class Gider_Bilgisi(models.Model):
    gelir_kime_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Gelir Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    cari_bilgisi = models.ForeignKey(cari,verbose_name="Cari Bilgisi",blank=True,null=True,on_delete=models.SET_NULL)
    fatura_tarihi = models.DateTimeField(null=True,verbose_name="Fatura Tarihi",blank = True)
    vade_tarihi = models.DateTimeField(null=True,verbose_name="Vade Tarihi",blank = True)
    fatura_no = models.CharField(verbose_name="Fatura No",max_length=200,blank=True,null=True)
    doviz = models.CharField(verbose_name="Döviz",max_length=200,blank=True,null=True)
    aciklama = models.TextField(verbose_name="Gelir Açıklaması",blank=True,null=True)
    gelir_kategorisii = models.ForeignKey(gider_kategorisi,verbose_name="Gelirin Kategori Bilgisi",blank=True,null=True,on_delete=models.SET_NULL)
    gelir_etiketi_sec = models.ManyToManyField(gider_etiketi,blank=True,null=True)
    toplam_tutar = models.FloatField(verbose_name="Toplam Tutar",default=0)
    kalan_tutar = models.FloatField(verbose_name="Kalan Tutar",default=0)
    silinme_bilgisi = models.BooleanField(default=False)
    fatura_gorseli = models.FileField(upload_to='fatura_gorseli/',verbose_name="fatura Görseli",blank=True,null=True)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(Gider_Bilgisi, self).save(*args, **kwargs)

class virman(models.Model):
    virman_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Virman Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    virman_tarihi = models.DateTimeField(null=True,verbose_name="Virman Tarihi",blank = True)
    gonderen_kasa = models.ForeignKey(Kasa,verbose_name="Gonderen Kasa",blank=True,null=True,on_delete=models.SET_NULL,related_name ="virman_gonderen_kasa")
    alici_kasa = models.ForeignKey(Kasa,verbose_name="gönderilen Kasa",blank=True,null=True,on_delete=models.SET_NULL,related_name ="virman_alici_kasa")
    tutar = models.FloatField(verbose_name="Toplam Tutar",default=0)
    aciklama = models.TextField(verbose_name="Virman Açıklaması",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(virman, self).save(*args, **kwargs)

class urun_kategorileri(models.Model):
    kategrori_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="KAtegori Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    kategori_adi = models.CharField(max_length=400,verbose_name="Kategori ADı",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(urun_kategorileri, self).save(*args, **kwargs)

class urunler(models.Model):
    urun_turu = (
        ("1","1"),
        ("2","2")
    )
    urun_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="ürün Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    urun_kategorisi = models.ForeignKey(urun_kategorileri,verbose_name="ürün Kategorisi",blank=True,null=True,on_delete=models.SET_NULL)
    urun_adi = models.CharField(max_length=400,verbose_name="Ürün ADı",blank=True,null=True)
    urun_fiyati = models.FloatField(verbose_name="Ürün Fiyatı",default=0)
    stok_mu = models.BooleanField(default=False,verbose_name="Stok İse Tik Seçilidir")
    urun_turu_secim = models.CharField(max_length=5,verbose_name="Urun Türü",choices = urun_turu, default="1")
    avans_icin_kullan = models.BooleanField(default=False)
    maas_icin_kullan = models.BooleanField(default=False)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(urunler, self).save(*args, **kwargs)

class zimmet_olayi(models.Model):
    urun_turu = (
        ("0","0"),
        ("1","1"),
        ("2","2")
    )
    zimmet_kime_ait = models.ForeignKey(CustomUser,verbose_name="ürün Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL,related_name = "zimmet_kime_ait")
    zimmeti_veren = models.ForeignKey(CustomUser,verbose_name="Talebin Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL,related_name = "zimmeti_veren")
    zimmet_alan_personel = models.ForeignKey(calisanlar,verbose_name="Talebin Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL,related_name = "Zimmet_alan_personel")
    zimmet_verilen_urun = models.ForeignKey(urunler,verbose_name="Talebin Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL,related_name = "Zimmet_alan_personel")
    zimmet_verilis_tarihi= models.DateTimeField(null=True,verbose_name="Zimmet Veriliş Tarihi",blank = True)
    zimmet_teslim_edilme_tarihi= models.DateTimeField(null=True,verbose_name="zimmet_teslim_edilme_tarihi",blank = True)
    zimmet_durumu = models.CharField(max_length=5,verbose_name="Urun Türü",choices = urun_turu, default="0")#0 verildi, 1 Hasarsız teslim alindı , 2 hasarlı alındı
    zimet_veris_belgesi = models.FileField(upload_to='zimmet_verilis_belgesi/',verbose_name="Zimmet Belgesi",blank=True,null=True)
    zimet_teslim_belgesi = models.FileField(upload_to='zimmet_teslim_belgesi/',verbose_name="Zimmet Belgesi",blank=True,null=True)
    zimmet_miktari = models.FloatField(default= 0)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(zimmet_olayi, self).save(*args, **kwargs)

class stok_giris_cikis(models.Model):
    urun_turu = (
        ("0","0"),
        ("1","1")
    )
    stok_kime_ait = models.ForeignKey(CustomUser,verbose_name="ürün Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL,related_name = "stok_kime_ait")
    stok_giren = models.ForeignKey(CustomUser,verbose_name="Talebin Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL,related_name = "stok_giren")
    stok_giren_urun = models.ForeignKey(urunler,verbose_name="Talebin Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL,related_name = "stok_giren_urun")
    stok_adeti = models.FloatField(default=0,verbose_name="Stok Miktari")
    stok_durumu = models.CharField(max_length=5,verbose_name="Urun Türü",choices = urun_turu, default="0")#0 Giriş, 1 çıkış 
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(stok_giris_cikis, self).save(*args, **kwargs)

class urun_talepleri(models.Model):
    talebi_onaylama=(
        ("1","1"),
        ("2","2"),
        ("3","3")
    )
    #1 Bekleniyor
    #2 Onaylandı
    #3 Red Edildi
    talebin_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Talebin Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL,related_name = "talebin_ait_oldugu")
    talebi_olusturan = models.ForeignKey(CustomUser,verbose_name="Talebi Oluşturan",blank=True,null=True,on_delete=models.SET_NULL,related_name="talebi_olusturan")
    talebi_onaylayan = models.ForeignKey(CustomUser,verbose_name="Talebi onaylayan",blank=True,null=True,on_delete=models.SET_NULL,related_name="talebi_onaylayan")
    satin_almayi_onaylayan = models.ForeignKey(CustomUser,verbose_name="SAtın Almayı Onaylayan",blank=True,null=True,on_delete=models.SET_NULL,related_name="satin_almayi_onaylayan")
    urun = models.ForeignKey(urunler,verbose_name="Ürün",blank=True,null=True,on_delete=models.SET_NULL)
    miktar = models.FloatField(default=0,verbose_name="Taleb Adet Miktarı")
    fiyati = models.FloatField(default=0,verbose_name="Fiyati")
    tedarikci = models.CharField(max_length=200 , verbose_name="Tedarikçi",blank=True,null=True)
    aciklama = models.CharField(max_length=500,verbose_name="Açıklama",blank=True,null=True)
    talep_Olusturma_tarihi =models.DateTimeField(null=True,verbose_name="Talep Başlangıç",blank = True)
    talep_durumu = models.CharField(max_length=3,verbose_name="Talep Durumu",choices=talebi_onaylama,default="1")
    talep_durum_tarihi = models.DateTimeField(null=True,verbose_name="Talep Durum Değiştirme Tarihi",blank = True)
    satin_alinma_durumu = models.BooleanField(default=False)#satın_almayı Onaylı İse Satın Alındı
    satin_alinma_tarihi = models.DateTimeField(null=True,verbose_name="Satın Alınma Tarihi",blank = True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(urun_talepleri, self).save(*args, **kwargs)

class gider_urun_bilgisi(models.Model):
    urun_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Ürün Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    urun_bilgisi = models.ForeignKey(urunler,blank=True,null=True,verbose_name="Ürün Bilgisi",on_delete=models.SET_NULL)
    urun_fiyati = models.FloatField(verbose_name="Ürün Fiyatı",default=0)
    urun_indirimi = models.FloatField(verbose_name="Ürün Fiyatı",default=0)
    urun_adeti = models.BigIntegerField(verbose_name="Ürün Adeti",default=0)
    aciklama = models.CharField(max_length = 400,verbose_name ="Açıklama",blank = True,null = True)
    gider_bilgis = models.ForeignKey(Gider_Bilgisi,blank=True,null=True,verbose_name="Gelir Bilgisi",on_delete=models.SET_NULL)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(gider_urun_bilgisi, self).save(*args, **kwargs)

class gelir_urun_bilgisi(models.Model):
    urun_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Ürün Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    urun_bilgisi = models.ForeignKey(urunler,blank=True,null=True,verbose_name="Ürün Bilgisi",on_delete=models.SET_NULL)
    urun_fiyati = models.FloatField(verbose_name="Ürün Fiyatı",default=0)
    urun_indirimi = models.FloatField(verbose_name="Ürün Fiyatı",default=0)
    urun_adeti = models.BigIntegerField(verbose_name="Ürün Adeti",default=0)
    aciklama = models.CharField(max_length = 400,verbose_name ="Açıklama",blank = True,null = True)
    gider_bilgis = models.ForeignKey(Gelir_Bilgisi,blank=True,null=True,verbose_name="Gelir Bilgisi",on_delete=models.SET_NULL)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)   
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(gelir_urun_bilgisi, self).save(*args, **kwargs)

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
    islemi_yapan = models.ForeignKey(CustomUser, on_delete = models.SET_NULL,blank = True,null = True,verbose_name = "İşlemi Yapan")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def set_gelir_makbuzu(self, file_path):
        self.gelir_makbuzu.name = file_path
        self.save()

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(Gelir_odemesi, self).save(*args, **kwargs)

class Gider_odemesi(models.Model):
    gelir_kime_ait_oldugu = models.ForeignKey(Gider_Bilgisi,verbose_name="Gelir Ödemesi Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    gelir_turu = models.CharField(max_length = 200,verbose_name="gelir_turu",blank = True,null=True)
    kasa_bilgisi = models.ForeignKey(Kasa,blank=True,null = True, verbose_name ="Kasa",on_delete=models.SET_NULL)
    tutar = models.FloatField(verbose_name = "Tutar",default = 0)
    tarihi = models.DateTimeField(blank=True,null=True)
    gelir_makbuzu = models.FileField(upload_to='makbuzlar/',verbose_name="Sayfaya Logo Light",blank=True,null=True)
    makbuz_no = models.CharField(max_length = 200,verbose_name="Makbuz No",blank = True,null=True)
    aciklama = models.CharField(max_length = 200,verbose_name="Açıklama",blank = True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    islemi_yapan = models.ForeignKey(CustomUser, on_delete = models.SET_NULL,blank = True,null = True,verbose_name = "İşlemi Yapan")
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def set_gelir_makbuzu(self, file_path):
        self.gelir_makbuzu.name = file_path
        self.save()

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(Gider_odemesi, self).save(*args, **kwargs)

class faturalar_icin_logo(models.Model):
    gelir_kime_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Gelir Ödemesi Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    gelir_makbuzu = models.FileField(upload_to='faturalogosu/',verbose_name="Sayfaya Logo Light",blank=True,null=True)
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(faturalar_icin_logo, self).save(*args, **kwargs)

class faturalar_icin_bilgiler(models.Model):
    gelir_kime_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Gelir Ödemesi Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    adress = models.CharField(max_length=200,verbose_name="Faturadaki Adress",blank=True , null= True)
    email = models.EmailField(max_length=200,verbose_name="Email",blank=True,null=True)
    telefon = models.CharField(max_length=20 ,verbose_name="Telefon" , blank=True,null=True)
    gunluk_calisma_saati = models.FloatField(default=9,verbose_name="Günlük Çalışma Saati")
    silinme_bilgisi = models.BooleanField(default=False)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(faturalar_icin_bilgiler, self).save(*args, **kwargs)

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

class gelir_qr(models.Model):
    gelir_kime_ait_oldugu = models.ForeignKey(Gelir_Bilgisi,verbose_name="Gelir Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    qr_bilgisi = models.ImageField(upload_to='faturaqr/',verbose_name="Sayfaya Logo Light",blank=True,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def _str_(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        qr_code_data = "https://cloud.biadago.com"+str("/accounting/viewcomeqr/")+str(self.gelir_kime_ait_oldugu.id)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        fname = f'qr_code-{str(self.gelir_kime_ait_oldugu.id)}.png'
        self.qr_bilgisi.save(fname, File(buffer), save=False)
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(gelir_qr, self).save(*args, **kwargs)

class gider_qr(models.Model):
    gelir_kime_ait_oldugu = models.ForeignKey(Gider_Bilgisi,verbose_name="Gelir Kategorisi Ait Olduğu",blank=True,null=True,on_delete=models.SET_NULL)
    qr_bilgisi = models.ImageField(upload_to='faturaqr/',verbose_name="Sayfaya Logo Light",blank=True,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def _str_(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        qr_code_data = "https://cloud.biadago.com"+str("/accounting/viewexpensesqr/")+str(self.gelir_kime_ait_oldugu.id)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        fname = f'qr_code-{str(self.gelir_kime_ait_oldugu.id)}.png'
        self.qr_bilgisi.save(fname, File(buffer), save=False)
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(gider_qr, self).save(*args, **kwargs)

class Gelir_excel_ekleme(models.Model):
    gelir_kime_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Gelir Ödemesi Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    gelir_makbuzu = models.FileField(upload_to='excel/',verbose_name="Sayfaya Logo Light",blank=True,null=True)
    kasa = models.ForeignKey(Kasa,blank=True,null = True, verbose_name ="Kasa",on_delete=models.SET_NULL)

class Gider_excel_ekleme(models.Model):
    gelir_kime_ait_oldugu = models.ForeignKey(CustomUser,verbose_name="Gelir Ödemesi Kime Ait",blank=True,null=True,on_delete=models.SET_NULL)
    gelir_makbuzu = models.FileField(upload_to='excel/',verbose_name="Sayfaya Logo Light",blank=True,null=True)
    kasa = models.ForeignKey(Kasa,blank=True,null = True, verbose_name ="Kasa",on_delete=models.SET_NULL)

class calisanlar_calismalari_odemeleri(models.Model):
    fatura = models.ForeignKey(Gider_Bilgisi,verbose_name="Gider Faturası",blank=True,null=True,on_delete=models.SET_NULL)
    calisan = models.ForeignKey(calisanlar,verbose_name="Çalışan",blank=True,null=True,on_delete=models.SET_NULL)
    tutar = models.FloatField(verbose_name="Tutar",default=0,blank=True,null=True)
    kur = models.FloatField(verbose_name="kur",default=0,blank=True,null=True)
    tarihi = models.DateTimeField(null=True,verbose_name="Çalışma Tarihi",blank = True)
    odeme_tarihi = models.DateTimeField(null=True,verbose_name="Çdeme Tarihi",blank = True)
    odeme_turu = models.BooleanField(default=False) #False ise Maaş True İse Avans
    aciklama = models.CharField(max_length=400,verbose_name="Açıklama", blank=True,null=True)
    dosya = models.FileField(upload_to='personel_odeme/',verbose_name="Sayfaya Logo Light",blank=True,null=True)
    guncelleme_tarihi = models.DateTimeField("Date modified", default=timezone.now)
    kayit_tarihi = models.DateTimeField(default=datetime.now,null=True)
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ip_address = kwargs.get('request').META.get('REMOTE_ADDR', None)
        if ip_address == '127.0.0.1':
            ip_address = '8.8.8.8'
        country = get_country_from_ip(ip_address)
        country_time_zone = get_time_zone_from_country(country)
        local_time = timezone.now().astimezone(pytz.timezone(country_time_zone))
        if local_time:
            self.kayit_tarihi = local_time
        super(calisanlar_calismalari_odemeleri, self).save(*args, **kwargs)