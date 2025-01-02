from django import template
from django.utils.safestring import mark_safe
from site_info.models import *
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from site_settings.models import *
import locale
import os

from django.contrib.gis.geoip2 import GeoIP2



"""
# İşletim sistemi kontrolü ile locale ayarı
def set_locale():
    try:
        if os.name == 'nt':  # Windows
            locale.setlocale(locale.LC_ALL, 'Turkish_Turkey.1254')
        else:  # MacOS ve Linux
            locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
    except locale.Error:
        # Eğer locale ayarı başarısız olursa, varsayılanı kullan
        print("Uyarı: Sisteminizde bu yerel ayar desteklenmiyor.")

# İlk fonksiyon: fiyat_duzelt
def fiyat_duzelt(deger, i=0):
    set_locale()  # Locale ayarını işletim sistemine göre yap
    if deger < 0:
        deger = abs(deger)
        y = locale.format_string("%.2f", deger, grouping=True)
        y = "-" + y
        return y
    else:
        return locale.format_string("%.2f", deger, grouping=True)

# İkinci fonksiyon: fiyat_duzelt_html
register = template.Library()

@register.simple_tag
def fiyat_duzelt_html(deger):
    deger = str(deger)
    deger = deger.replace('.', '')  # Noktaları kaldır
    deger = deger.replace(',', '.')  # Virgülleri noktayla değiştir
    deger = float(deger)
    
    set_locale()  # Locale ayarını işletim sistemine göre yap
    return locale.format_string("%.2f", deger, grouping=True)

"""

def fiyat_duzelt(deger, i=0):
    if deger < 0:
        deger = abs(deger)
        y = f"-{deger:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return y
    else:
        return f"{deger:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
register = template.Library()
@register.simple_tag
def personel_maas_bilgisi(id):
    bilgi = faturalar_icin_bilgiler.objects.filter(gelir_kime_ait_oldugu  = get_object_or_none(calisanlar, id=id).calisan_kime_ait).last()
    if True:
        calismalar = calisanlar_calismalari.objects.filter(
            calisan=get_object_or_none(calisanlar, id=id)
        ).annotate(
            year=ExtractYear('tarihi'),
            month=ExtractMonth('tarihi')
        ).values(
            'year', 'month', 'maas__id'  # Maas ID ile gruplanıyor
        ).annotate(
            total_normal_calisma_saati=Sum('normal_calisma_saati'),
            total_mesai_calisma_saati=Sum('mesai_calisma_saati')
        ).order_by('year', 'month')

        odemeler = calisanlar_calismalari_odemeleri.objects.filter(
            calisan=get_object_or_none(calisanlar, id=id)
        ).annotate(
            year=ExtractYear('tarihi'),
            month=ExtractMonth('tarihi')
        ).values(
            'year', 'month'  # Maas ID ile gruplanıyor
        ).annotate(
            total_tutar=Sum('tutar')
        ).order_by('year', 'month')

        odemeler_dict = {(odeme['year'], odeme['month']): odeme['total_tutar'] for odeme in odemeler}

        maas_bilgisi = [
            {
                'tarih': str(calis['year']) + "-" + str(calis['month']),
                'parabirimi': get_object_or_none(calisan_maas_durumlari, id=calis["maas__id"]).para_birimi,
                'hakedis_tutari':fiyat_duzelt( (calis["total_normal_calisma_saati"] * get_object_or_none(calisan_maas_durumlari, id=calis["maas__id"]).maas)/bilgi.gunluk_calisma_saati + 
                                  (calis["total_mesai_calisma_saati"] * get_object_or_none(calisan_maas_durumlari, id=calis["maas__id"]).yevmiye)),
                'odenen':fiyat_duzelt(odemeler_dict.get((calis['year'], calis['month']), 0)),
                'kalan': fiyat_duzelt(((calis["total_normal_calisma_saati"] * get_object_or_none(calisan_maas_durumlari, id=calis["maas__id"]).maas)/bilgi.gunluk_calisma_saati + 
                          (calis["total_mesai_calisma_saati"] * get_object_or_none(calisan_maas_durumlari, id=calis["maas__id"]).yevmiye)) - 
                          odemeler_dict.get((calis['year'], calis['month']), 0)),
            } for calis in calismalar
        ]
        
        return maas_bilgisi
@register.simple_tag
def bodro_cek(id,tarih):
    bilgi = faturalar_icin_bilgiler.objects.filter(gelir_kime_ait_oldugu  = get_object_or_none(calisanlar, id=id).calisan_kime_ait).last()
    if True:
        yil, ay = map(int, tarih.split('-'))
        calismalar = calisanlar_calismalari.objects.filter(
            calisan=get_object_or_none(calisanlar, id=id),
            tarihi__year=yil,  # Yıl filtresi
        tarihi__month=ay   # Ay filtresi
        ).annotate(
            year=ExtractYear('tarihi'),
            month=ExtractMonth('tarihi')
        ).values(
            'year', 'month', 'maas__id'  # Maas ID ile gruplanıyor
        ).annotate(
            total_normal_calisma_saati=Sum('normal_calisma_saati'),
            total_mesai_calisma_saati=Sum('mesai_calisma_saati')
        ).order_by('year', 'month')
        odemeler = calisanlar_calismalari_odemeleri.objects.filter(
        calisan=get_object_or_none(calisanlar, id=id),
        tarihi__year=yil,  # Yıl filtresi
        tarihi__month=ay   # Ay filtresi
    )
        for calis in calismalar:
            hakedis_tutari=fiyat_duzelt( (calis["total_normal_calisma_saati"]/bilgi.gunluk_calisma_saati * get_object_or_none(calisan_maas_durumlari, id=calis["maas__id"]).maas) + 
                                  (calis["total_mesai_calisma_saati"] * get_object_or_none(calisan_maas_durumlari, id=calis["maas__id"]).yevmiye))
        return {"odemeler":odemeler,"odenecek_tutar":hakedis_tutari}
@register.simple_tag
def fiyat_duzelt_html(deger):
    # String dönüşümleri ve noktaları kaldırma işlemi
    if isinstance(deger, str):
        deger = deger.replace('.', '').replace(',', '.')
    deger = float(deger)
    
    # Formatlama işlemi
    formatted_value = f"{deger:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return formatted_value


#@register.filter
@register.simple_tag
def to_int(veri):
    return int(veri)
@register.simple_tag
def kalemleri_td_gonder(veri):
    deger = santiye_kalemleri.objects.filter(proje_santiye_Ait = veri,silinme_bilgisi = False)

    return deger
@register.simple_tag
def blog_td_gonder(veri):
    deger = bloglar.objects.filter(proje_santiye_Ait = veri)

    return deger
@register.simple_tag
def bloglar_getir(veri):
    deger = bloglar.objects.filter(proje_santiye_Ait = veri)
    veri_esiti = ""
    for i in  deger:
        veri_esiti = veri_esiti + str(i.blog_adi)+" ,"
    return int(deger.count())

@register.simple_tag
def bloglar_form_gonder(veri):
    deger = bloglar.objects.filter(proje_santiye_Ait = veri)
    veri_esiti = ""
    for i in deger:
        veri_esiti = veri_esiti + """<option value="{}">{}</option>""".format(i.id,i.blog_adi)
    return mark_safe(veri_esiti)
@register.simple_tag
def bloglar_form_gonder_kaleme(veri):
    deger = bloglar.objects.filter(proje_santiye_Ait = veri)

    return deger

@register.simple_tag
def kalemler_getir(veri):
    deger = santiye_kalemleri.objects.filter(proje_santiye_Ait = veri,silinme_bilgisi = False)

    return int(deger.count())
@register.simple_tag
def ilk_giris_verileri(kat_sayis,blok):
    veri_gonder = []
    for i in range(0,kat_sayis):
        santiye_kalemleri_bilgisi = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi = blok,kalem_bilgisi__silinme_bilgisi = False,silinme_bilgisi = False,kat =i ).count()
        santiye_kalemleri_bilgisi_tamamlanan = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi = blok,kalem_bilgisi__silinme_bilgisi = False,silinme_bilgisi = False,kat =i ,tamamlanma_bilgisi = True).count()
      
        if santiye_kalemleri_bilgisi == santiye_kalemleri_bilgisi_tamamlanan:
            veri_gonder.append(100)
        else:
            veri_gonder.append(0)
    return veri_gonder
@register.simple_tag
def ilk_giris_verileri_kalem(kat_sayis,blok,kalem):
    if kalem == "0"  or kalem == 0 :
        veri_gonder = []
        for i in range(0,kat_sayis):
            santiye_kalemleri_bilgisi = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi = blok,kalem_bilgisi__silinme_bilgisi = False,silinme_bilgisi = False,kat =i ).count()
            santiye_kalemleri_bilgisi_tamamlanan = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi = blok,kalem_bilgisi__silinme_bilgisi = False,silinme_bilgisi = False,kat =i ,tamamlanma_bilgisi = True).count()
          
            if santiye_kalemleri_bilgisi == santiye_kalemleri_bilgisi_tamamlanan:
                veri_gonder.append(100)
            else:
                veri_gonder.append(0)
        return veri_gonder
    else:
        veri_gonder =  []
        for i in range(0,kat_sayis):
            santiye_kalemleri_bilgisi = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi = blok,kalem_bilgisi = kalem,kalem_bilgisi__silinme_bilgisi = False,silinme_bilgisi = False,kat =i ).count()
            santiye_kalemleri_bilgisi_tamamlanan = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi = blok,kalem_bilgisi__silinme_bilgisi = False,silinme_bilgisi = False,kat =i ,kalem_bilgisi = kalem,tamamlanma_bilgisi = True).count()
            if santiye_kalemleri_bilgisi == santiye_kalemleri_bilgisi_tamamlanan:
                veri_gonder.append(100)
            else:
                veri_gonder.append(0)
        return veri_gonder
@register.simple_tag
def bloglari_rapora_yansitma(veri):
    deger = bloglar.objects.filter(proje_santiye_Ait = veri)
    santiye_kalemleri_bilgisi = santiye_kalemleri.objects.filter(proje_santiye_Ait = veri,silinme_bilgisi = False)

    degerler = []
    bloglar_getirme = []
    kalemleri_gonder= []
    kalemler_dagilisi_gonder= []
    kalemeler_ = []

    for i in santiye_kalemleri_bilgisi:
        if i.silinme_bilgisi:
            pass
        else:
            kalemleri_gonder.append(i.kalem_adi)
            kalemeler_.append(i)
    for i in deger:
        unique_values = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi =i.id,tamamlanma_bilgisi = True)
        bloglar_getirme.append(i.blog_adi+str(i.blog_numarasi))
        degerler.append(unique_values.count())

    return {"blog" : bloglar_getirme,"degerler" : degerler,"k":kalemeler_,"kalemler":kalemleri_gonder,"kalem_dagilisi" : kalemler_dagilisi_gonder}
@register.simple_tag
def bloglar_daireleri_kalemleri(id):
    toplam_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id).count()
    toplam_yapilan_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,tamamlanma_bilgisi = True).count()
    toplam_yapilmayan_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,tamamlanma_bilgisi = False).count()
    yuzde = (toplam_yapilan_kalem*100)/toplam_kalem
    return round(yuzde,2)
@register.simple_tag
def bloglar_daireleri_kalemleri_finansal(id):
    toplam_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id).count()
    toplam_yapilan_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,tamamlanma_bilgisi = True).count()
    toplam_yapilmayan_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,tamamlanma_bilgisi = False).count()
    yuzde = (toplam_yapilan_kalem*100)/toplam_kalem
    return round(yuzde,2)
@register.simple_tag
def bloglar_daireleri_kalemleri_fiziksel_bilgileri(id,k_b):
    genel_toplam = 0
    for i in k_b:
        toplam_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,kalem_bilgisi__id = i.id).count()
        toplam_yapilan_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,tamamlanma_bilgisi = True,kalem_bilgisi__id = i.id).count()
        toplam_yapilmayan_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,tamamlanma_bilgisi = False,kalem_bilgisi__id = i.id).count()
        try:
            genel_toplam = ((toplam_yapilan_kalem*(i.santiye_agirligi))/toplam_kalem)+genel_toplam
        except:
            genel_toplam = genel_toplam
    return round(genel_toplam,2)
@register.simple_tag
def bloglar_daireleri_kalemleri_finansal_bilgileri(id,k_b):
    genel_toplam = 0
    for i in k_b:
        toplam_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,kalem_bilgisi__id = i.id).count()
        toplam_yapilan_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,tamamlanma_bilgisi = True,kalem_bilgisi__id = i.id).count()
        toplam_yapilmayan_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,tamamlanma_bilgisi = False,kalem_bilgisi__id = i.id).count()
        try:
            genel_toplam = ((toplam_yapilan_kalem*(i.santiye_finansal_agirligi))/toplam_kalem)+genel_toplam
        except:
            genel_toplam = genel_toplam
    return round(genel_toplam,2)
from collections import defaultdict
from datetime import timedelta
from django import template
from django.utils import timezone
from collections import defaultdict
from django.utils import timezone
from datetime import timedelta

@register.simple_tag
def get_son_bir_hafta_icinde_degisenler(id):
    """
    Son bir hafta içinde değişen ve tamamlanma bilgisi True olan santiye_kalemlerin_dagilisi kayıtlarını gün gün ayırarak
    fiziksel ve finansal değerleri gün bazında döndürür.
    """
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)

    # Son bir hafta içinde değişen ve tamamlanma bilgisi True olan kayıtlar
    degisen_kalemler = santiye_kalemlerin_dagilisi.objects.filter(
        blog_bilgisi__id=id,
        degistirme_tarihi__gte=one_week_ago,
        tamamlanma_bilgisi=True
    )

    # Gün gün ayırmak için defaultdict kullanıyoruz
    gun_gun_kalemler = defaultdict(list)
    gun_gun_kalemlerfiz = defaultdict(list)
    gun_gun_kalemlerfin = defaultdict(list)

    for kalem in degisen_kalemler:
        degisme_gunu = kalem.degistirme_tarihi.date()
        fiziksel = kalem.kalem_bilgisi.santiye_agirligi
        finansal = kalem.kalem_bilgisi.santiye_finansal_agirligi
        kat = kalem.blog_bilgisi.kat_sayisi

        sonuc_fiziksel = fiziksel / kat
        sonuc_finansal = finansal / kat

        gun_gun_kalemler[degisme_gunu].append(kalem)
        gun_gun_kalemlerfiz[degisme_gunu].append(sonuc_fiziksel)
        gun_gun_kalemlerfin[degisme_gunu].append(sonuc_finansal)

    # Gün adlarını tanımlıyoruz (Pazartesi'den başlayarak)
    gun_adlari = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    
    # Son bir haftadaki günlerin listesini oluşturuyoruz
    gunler = [now.date() - timedelta(days=i) for i in range(7)]
    
    # Günleri sıraya göre döndürüyoruz ve o günün kayıtlarını varsa ekliyoruz
    gun_gonder = []
    deger_gonder_fizi = []
    deger_gonder_finn = []

    for gun in reversed(gunler):  # Günleri doğru sırada döndürecek
        gun_ad = gun_adlari[gun.weekday()]  # Doğrudan gun.weekday() ile günü alıyoruz

        sayi = len(gun_gun_kalemler.get(gun, []))
        fiziksel_toplam = round(sum(gun_gun_kalemlerfiz.get(gun, [])), 2)
        finansal_toplam = round(sum(gun_gun_kalemlerfin.get(gun, [])), 2)

        gun_gonder.append(gun_ad)
        deger_gonder_fizi.append(fiziksel_toplam)
        deger_gonder_finn.append(finansal_toplam)

    return {
        "gunler": gun_gonder,
        "degerler": deger_gonder_fizi,
        "degerler2": deger_gonder_finn
    }



@register.simple_tag
def get_yil_icinde_degisenler(id):
    """
    Yıl içinde değişen ve tamamlanma bilgisi True olan santiye_kalemlerin_dagilisi kayıtlarını ay bazında ayırarak
    fiziksel ve finansal değerleri ay bazında döndürür.
    """
    now = timezone.now()
    baslangic_tarihi = now.replace(month=1, day=1)  # Yıl başına gidiyoruz

    # Yıl içinde değişen ve tamamlanma bilgisi True olan kayıtlar
    degisen_kalemler = santiye_kalemlerin_dagilisi.objects.filter(
        blog_bilgisi__id=id,
        degistirme_tarihi__gte=baslangic_tarihi,
        tamamlanma_bilgisi=True
    )

    # Ay bazında ayırmak için defaultdict kullanıyoruz
    ay_bazinda_kalemlerfiz = defaultdict(float)
    ay_bazinda_kalemlerfin = defaultdict(float)

    for kalem in degisen_kalemler:
        degisme_ayi = kalem.degistirme_tarihi.strftime("%Y-%m")  # Ay ve yılı belirlemek için
        fiziksel = kalem.kalem_bilgisi.santiye_agirligi
        finansal = kalem.kalem_bilgisi.santiye_finansal_agirligi
        kat = kalem.blog_bilgisi.kat_sayisi

        sonuc_fiziksel = fiziksel / kat
        sonuc_finansal = finansal / kat

        ay_bazinda_kalemlerfiz[degisme_ayi] += sonuc_fiziksel
        ay_bazinda_kalemlerfin[degisme_ayi] += sonuc_finansal

    # Yılın tüm aylarını sıraya göre döndürüyoruz
    aylar = [f"{now.year}-{str(i).zfill(2)}" for i in range(1, 13)]
    deger_gonder_fizi = []
    deger_gonder_finn = []

    for ay in aylar:
        fiziksel_toplam = round(ay_bazinda_kalemlerfiz.get(ay, 0), 2)
        finansal_toplam = round(ay_bazinda_kalemlerfin.get(ay, 0), 2)

        deger_gonder_fizi.append(fiziksel_toplam)
        deger_gonder_finn.append(finansal_toplam)

    return {
        "aylar": aylar,
        "degerler": deger_gonder_fizi,
        "degerler2": deger_gonder_finn
    }

@register.simple_tag
def bloglar_daireleri_kalemleri_fiziksel_bilgileri_genel(k_b):
    genel_toplam = 0
    for i in k_b:
        toplam_kalem = santiye_kalemlerin_dagilisi.objects.filter(kalem_bilgisi__id = i.id).count()
        toplam_yapilan_kalem = santiye_kalemlerin_dagilisi.objects.filter(tamamlanma_bilgisi = True,kalem_bilgisi__id = i.id).count()
        toplam_yapilmayan_kalem = santiye_kalemlerin_dagilisi.objects.filter(tamamlanma_bilgisi = False,kalem_bilgisi__id = i.id).count()
        genel_toplam = ((toplam_yapilan_kalem*(i.santiye_agirligi))/toplam_kalem)+genel_toplam
    return round(genel_toplam,2)
@register.simple_tag
def bloglar_daireleri_kalemleri_finansal_bilgileri_genel(k_b):
    genel_toplam = 0
    for i in k_b:
        toplam_kalem = santiye_kalemlerin_dagilisi.objects.filter(kalem_bilgisi__id = i.id).count()
        toplam_yapilan_kalem = santiye_kalemlerin_dagilisi.objects.filter(tamamlanma_bilgisi = True,kalem_bilgisi__id = i.id).count()
        toplam_yapilmayan_kalem = santiye_kalemlerin_dagilisi.objects.filter(tamamlanma_bilgisi = False,kalem_bilgisi__id = i.id).count()
        genel_toplam = ((toplam_yapilan_kalem*(i.santiye_finansal_agirligi))/toplam_kalem)+genel_toplam
    return round(genel_toplam,2)
@register.simple_tag
def bloglar_daireleri_kalemleri_fiziksel_bilgileri_toplama_gonderme(id,k_b):
    genel_toplam = []
    a = 0
    b = 0
    kat = get_object_or_404(bloglar,id = id).kat_sayisi
    for i in k_b:
        
        toplam_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,kalem_bilgisi__id = i.id).count()
        toplam_yapilan_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,tamamlanma_bilgisi = True,kalem_bilgisi__id = i.id).count()
        toplam_yapilmayan_kalem = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,tamamlanma_bilgisi = False,kalem_bilgisi__id = i.id).count()
        try:
            a = int(((toplam_yapilan_kalem*(i.santiye_agirligi))/toplam_kalem)*100/(i.santiye_agirligi))
            b =int(((toplam_yapilan_kalem*(i.santiye_finansal_agirligi))/toplam_kalem)*100/(i.santiye_finansal_agirligi))
        except:
            pass
        genel_toplam.append({"isim":i.kalem_adi,"id": i.id,"ilerleme1":a,"ilerleme2":b})

    return genel_toplam
@register.simple_tag
def days_until(bitis_tarihi):
    from django.utils import timezone
    now = timezone.now()
    
    delta = bitis_tarihi - now
    return delta.days
    #return 0  # Eğer bitiş tarihi geçmişse 0 döndür
@register.simple_tag
def proje_dosyalarini(id):
    a = proje_dosyalari.objects.filter(proje_ait_bilgisi__id = id).count()
    return a

@register.simple_tag
def proje_dosyalarini_bilgi(id):
    a = proje_dosyalari.objects.filter(proje_ait_bilgisi__id = id)
    return a



@register.simple_tag
def taseronsozlesme_saysisi(id):
    a = taseron_sozlesme_dosyalari.objects.filter(proje_ait_bilgisi__id = id).count()
    return a
@register.simple_tag
def taseronsozlesme_dosyalari(id):
    a = taseron_sozlesme_dosyalari.objects.filter(proje_ait_bilgisi__id = id)
    return a
@register.simple_tag
def ust_yuklenici_d_dosyalari(id):
    a = ust_yuklenici_dosyalari.objects.filter(proje_ait_bilgisi__id = id)
    return a
@register.simple_tag
def taseron_gorev_saysisi(id):
    a = get_object_or_404(taseronlar,id = id)
    a = a.proje_bilgisi.all().count()

    return a

@register.simple_tag
def isim(id):
    a = id.split("/")
    if len(a) >1:
        return a[1]
    return a[0]
@register.simple_tag
def kullanici_dosya_sayisi(id):
    a = personel_dosyalari.objects.filter(kullanici__id = id).count()
    return a


@register.simple_tag
def klasor_olayi(id):
    k = id
    a = ""
    m = []
    while True:
        z = get_object_or_404(klasorler,id = k)
        m.append(z.klasor_adi)
        m.append(z.id)
        if z.klasor_adi_db:
            k = z.klasor_adi_db.id
        else:
            break
    for i in range(len(m)-1,-1,-2):
        a = a+'<a href="/storage/mydir/{}/{}/">{}</a> > '.format(m[i],m[i-1],m[i-1])
    return mark_safe(a)


@register.simple_tag
def kullanici_dosya_boyutu(id):
    boyut = 0
    try:
        a = klasor_dosyalari.objects.filter(dosya_sahibi__id = id)
    except:
        a = 0
    try:
        for  i in a:
            boyut = boyut+ i.dosya.size
    except:
        pass
        
    boyut = boyut/1024
    #kb oldu
    boyut = boyut /1024
    #mb oldu
    boyut = boyut /1024
    #gb oldu
    full = 5
    full =( boyut * 100 ) / full
    full = round(float(full),2)
    boyut = round(float(boyut),2)
    if boyut < 5:
        k = """<div class="progress mb-2 progress-sm">
                                                <div class="progress-bar bg-success" role="progressbar" style="width: {}%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                                            </div>
                                            <span class="text-muted fs-12 d-block text-truncate"><b>{}</b>GB used of <b>5</b>GB</span>""".format(full,boyut)
        return mark_safe(k)
    elif 5 < boyut:
        k = """<div class="progress mb-2 progress-sm">
                                                <div class="progress-bar bg-danger" role="progressbar" style="width: {}%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                                            </div>
                                            <span class="text-muted fs-12 d-block text-truncate"><b>{}</b>GB used of <b>5</b>GB</span>""".format(full,boyut)
        return mark_safe(k)



@register.simple_tag
def dosya_ekleme_yetenegi(id):
    boyut = 0
    a = klasor_dosyalari.objects.filter(dosya_sahibi__id = id)
    for  i in a:
        try:
            boyut = boyut+ i.dosya.size
        except:
            continue
    boyut = boyut/1024
    #kb oldu
    boyut = boyut /1024
    #mb oldu
    boyut = boyut /1024
    #gb oldu
    full = 5
    full =( boyut * 100 ) / full
    full = round(float(full),2)
    boyut = round(float(boyut),2)
    sonuc = None
    if boyut > 5:
        k = """<button class="btn btn-danger w-sm create-folder-modal flex-shrink-0" data-bs-toggle="modal" data-bs-target=""><i class="ri-add-line align-bottom me-1"></i> Depolama Dolu</button>"""
        return False
    elif 5 > boyut:
        k = """<button class="btn btn-success w-sm create-folder-modal flex-shrink-0" data-bs-toggle="modal" data-bs-target="#dosyaekle"><i class="ri-add-line align-bottom me-1"></i> Dosya Ekle</button>"""
        return True
@register.simple_tag
def mb_donusturme(id):
    try:
        id = id.size
        id  = id /1024
        id = id /1024
        return round(float(id),2)
    except:
        return 0

@register.simple_tag
def dosya_sayisi_ve_boyutu (id):

    klasor_sayisi = klasorler.objects.filter(klasor_adi_db__id=id).count()
    dosya_sayisi =  klasor_dosyalari.objects.filter(proje_ait_bilgisi__id=id).count()
    dosya_boyutu  = 0
    z = klasor_dosyalari.objects.filter(proje_ait_bilgisi__id=id)
    try:
        for i in z:
            dosya_boyutu = dosya_boyutu+i.dosya.size
        dosya_boyutu = ((dosya_boyutu/1024)/1024)/1024
    except:
        dosya_boyutu = 0
    a = """<span class="me-auto"><b>{}</b> Files</span>
            <span><b>{}</b>GB</span>""".format(klasor_sayisi+dosya_sayisi,round(float(dosya_boyutu),2))
    return mark_safe(a)



@register.simple_tag
def veri_siralama(veri,id):
    bilgi = []
    for i in veri :
        bilgi.append(i.id)
    cevap = bilgi.index(id)
    if cevap % 2:
        return "right"
    else:
        return "left"


@register.simple_tag
def dosya_varsa_indirme(id):

    z = ""
    veri = YapilacakDosyalari.objects.filter(proje_ait_bilgisi__id = id)
    for i in veri:
        k = str(i.dosya.url).split("/")
        k = k[ -1]

        z = z+ '<div class="d-flex border border-dashed p-2 rounded position-relative"><div class="flex-shrink-0 avatar-xs"><div class="avatar-title bg-info-subtle text-info fs-15 rounded"><i class="ri-file-zip-line"></i></div></div><div class="flex-grow-1 overflow-hidden ms-2"><h6 class="text-truncate mb-0"><a href="{}" download class="stretched-link">{}</a></h6><small>{} KB</small></div></div>'.format(i.dosya.url,k,round(float(i.dosya.size/1024),2))
    return mark_safe(z)

@register.simple_tag
def kalem_blog(id):

    unique_values = santiye_kalemlerin_dagilisi.objects.filter(kalem_bilgisi__id =id)
    a = []
    for i in unique_values:
        if i.blog_bilgisi in a:
            pass
        else:
            a.append(i.blog_bilgisi)
    bilgiler = ""
    for i in a:
        #/delbuldingsites/{}/{}
        bilgiler = bilgiler+ '<a href="#" >{}</a>'.format(str(i.blog_adi))+" , "
    return mark_safe(bilgiler)
@register.simple_tag
def calisan_maasi(id):
    maasli = calisan_maas_durumlari.objects.filter(calisan = get_object_or_none(calisanlar, id = id)).last()
    return maasli
@register.simple_tag
def secililer_yapi_kalem(id):

    unique_values = santiye_kalemlerin_dagilisi.objects.filter(kalem_bilgisi__id =id)
    a = []
    for i in unique_values:
        if i.blog_bilgisi in a:
            pass
        else:
            a.append(i.blog_bilgisi)
    return a
@register.simple_tag
def kalemler_sadece(id):
    kalemelr = santiye_kalemleri.objects.filter(proje_santiye_Ait = id,silinme_bilgisi = False)
    form = ""
    for i in kalemelr:
        unique_values = santiye_kalemlerin_dagilisi.objects.filter(kalem_bilgisi__id =i.id)
        a = []
        for j in unique_values:
            if j.blog_bilgisi in a:
                pass
            else:
                a.append(j.blog_bilgisi)
        for j in a:
            #/delbuldingsites/{}/{}
            form = form+ """<option selected value="{},{}">{}&#8594;{}&#8594;{}</option>""".format(str(i.id ),str(j.id),str(i.proje_santiye_Ait.proje_adi),str(j.blog_adi),str(i.kalem_adi))

    return mark_safe(form)
@register.simple_tag
def kalemler_sadece_duzeltmeli(id,z):
    kalemelr = santiye_kalemleri.objects.filter(proje_santiye_Ait = id,silinme_bilgisi = False)
    form = ""
    for i in kalemelr:
        unique_values = santiye_kalemlerin_dagilisi.objects.filter(kalem_bilgisi__id =i.id)
        a = []
        for j in unique_values:
            if j.blog_bilgisi in a:
                pass
            else:
                a.append(j.blog_bilgisi)
        for j in a:
            #/delbuldingsites/{}/{}
            if z.filter(kalem_bilgisi__id = i.id ,blog_bilgisi__id = j.id):
                form = form+ """<option selected value="{},{}">{}&#8594;{}&#8594;{}</option>""".format(str(i.id ),str(j.id),str(i.proje_santiye_Ait.proje_adi),str(j.blog_adi),str(i.kalem_adi))
            else:
                form = form+ """<option selected value="{},{}">{}&#8594;{}&#8594;{}</option>""".format(str(i.id ),str(j.id),str(i.proje_santiye_Ait.proje_adi),str(j.blog_adi),str(i.kalem_adi))
    return mark_safe(form)
@register.simple_tag

def blogtan_kaleme_ilerleme(id):
    a = ""
    blog_bilgis = bloglar.objects.filter(proje_santiye_Ait__id=id)
    for i in blog_bilgis:
        a = a+'<a style="padding:2px !important;margin:0px 2px 0px 0px!important;" class="btn btn-info " href="progresstracking/progress/{}/{}" >{}</a>'.format(str(i.id),str(i.blog_adi)+str(i.blog_numarasi),str(i.blog_adi)+str(i.blog_numarasi))
    return mark_safe(a)

@register.simple_tag
def kat_sirala(id):
    #z = bloglar.objects.filter(proje_santiye_Ait = id)
    a = ""
    b = 0

    b= int(id.kat_sayisi)
    for i in range(1,b+1):
        a = a+'<th class="text-uppercase" data-sort="{}">{}</th>'.format(i,i)
    return mark_safe(a)
@register.simple_tag
def ckboxlar(id,kalem,kat_siniri):
    bilgi = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,kalem_bilgisi__id =kalem).order_by("kat")
    a = ""
    for i in bilgi:
        if kat_siniri > i.kat and kat_siniri -10 <= i.kat :
            if i.tamamlanma_bilgisi:
                a = a+"""<div class="progress-tracking-toggle">
                                                    <span>{}</span>
                                                    <label class="progress-tracking-toggle-input">
                                                        <input name="kalem" type="checkbox" value="{}" checked>
                                                        <span class="ptti-slide"></span>
                                                    </label>
                                                </div>""".format(i.kat+1,str(i.id))
            else:
                a = a+"""<div class="progress-tracking-toggle">
                                                    <span>{}</span>
                                                    <label class="progress-tracking-toggle-input">
                                                        <input name="kalem" type="checkbox" value="{}" >
                                                        <span class="ptti-slide"></span>
                                                    </label>
                                                </div>""".format(i.kat+1,str(i.id))
        
    return mark_safe(a)
@register.simple_tag
def tum_bilgiler(id,kalem):
    bilgi = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,kalem_bilgisi__id =kalem).order_by("kat")
    a = ""
    for i in bilgi:
        a = a+str(i.id)+","
    return a

@register.simple_tag
def cari_taseron_mu(id):
    a = cari_taseron_baglantisi.objects.filter(cari_bilgisi__id = id)
    b = ""
    for i in a:
        b = b+ str(i.gelir_kime_ait_oldugu.taseron_adi)
    return b

@register.simple_tag
def gelir_faturasi_no(id):
    a = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu__id = id).count()
    a = a+1
    a = str(a)
    b = len(a)
    c = 8 - b
    if faturalardaki_gelir_gider_etiketi_ozel.objects.filter(kullanici__id = id).last():
        a = faturalardaki_gelir_gider_etiketi_ozel.objects.filter(kullanici__id = id).last().gelir_etiketi+(c*"0")+a
    else:
        a = "E"+(c*"0")+a
    return a
@register.simple_tag
def gider_faturasi_no(id):
    a = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu__id = id).count()
    a = a+1
    a = str(a)
    b = len(a)
    c = 8 - b
    if faturalardaki_gelir_gider_etiketi_ozel.objects.filter(kullanici__id  = id).last():
        a = faturalardaki_gelir_gider_etiketi_ozel.objects.filter(kullanici__id  = id).last().gider_etiketi+(c*"0")+a
    else:
        a = "I"+(c*"0")+a
    return a
@register.simple_tag
def jhson_gonder(i):
    if i.silinme_bilgisi:
        pass
    else:
        s = i.gelir_etiketi_sec.all()

        j = s[0].gider_etiketi_adi if len(s) > 0 else ""
        l = s[1].gider_etiketi_adi if len(s) > 1 else ""
        v = s[2].gider_etiketi_adi if len(s) > 2 else ""

        tutar = toplam_tutar_cikarmai(i)
        odeme = toplam_odenme_tutari(i)

        if odeme == tutar:
            b = "Ödendi"
        elif odeme > 0:
            b = "Parçalı Ödendi"
        else:
            b = "Ödenmedi"

        y = {
            "incele": f'<button class="faturabilgisi bg-sucsses" id="{i.id}" onclick="loadFaturaDetails({i.id})">İncele</button>',
            "fatura_no": str(i.fatura_no),
            "cari": i.cari_bilgisi.cari_adi if i.cari_bilgisi.cari_adi else "",
            "aciklama": f'<span class="monospace-bold" title="{str(i.aciklama)}">{str(i.aciklama)[:15]}</span>',
            "etiket1": j,
            "etiket2": l,
            "etiket3": v,
            "duzenleme_tarihi": str(i.fatura_tarihi.strftime("%d.%m.%Y")),
            "vade_tarihi": str(i.vade_tarihi.strftime("%d.%m.%Y")),
            "fatura_bedeli": "$" + str(toplam_tutar_cikarmai(i)),
            "kalan_tutar": "$" + str(kalan_tutuari(i)),
            "durum": b
        }
        
        return mark_safe(y)
@register.simple_tag
def jhson_gonder_2(i):
    if True:
        if i.silinme_bilgisi:
            pass
        else:
            s = i.gelir_etiketi_sec.all()
            
            try:
                j = s[0].gelir_etiketi_adi
                
            except:
                j = ""
            try:
                l = s[1].gelir_etiketi_adi
                
            except:
                l = ""
            try:
                v = s[2].gelir_etiketi_adi
                
            except:
                v = ""
            if i.silinme_bilgisi:
                b = "İPTAL"
            tutar = toplam_tutar_cikarma(i)
            odeme = toplam_odenme_tutar(i)
            id = i.id
            if odeme == tutar :
                b = "Ödendi"
            elif odeme > 0:
                b  = "Parçalı Ödendi"
            elif odeme == 0:
                b = "Ödenmedi"
            if i.cari_bilgisi:
                cari_bilgi = i.cari_bilgisi.cari_adi
            else:
                cari_bilgi = ""
            y =   {
            "incele":f'<button class="faturabilgisi bg-sucsses" id="{id}" onclick="loadFaturaDetails({id})">İncele</button>',
            "fatura_no": str(i.fatura_no),
            "cari": cari_bilgi,
            "aciklama": f'<span class="monospace-bold" title="{str(i.aciklama)}">{str(i.aciklama)[:15]}</span>',
            "etiket1": j ,
            "etiket2": l,       
            "etiket3": v ,
            "duzenleme_tarihi": str(i.fatura_tarihi.strftime("%d.%m.%Y")),
            "vade_tarihi": str(i.vade_tarihi.strftime("%d.%m.%Y")),
            "fatura_bedeli": "$"+str(toplam_tutar_cikarma(i)),
            "kalan_tutar": "$"+str(kalan_tutuar(i)),
            "durum": b
            }
            
    
    return mark_safe(y)

@register.simple_tag
def saat_bilgisi():
    from datetime import datetime
    su_an = datetime.now()
    saat = su_an.strftime("%H")
    #
    return  int(saat)

@register.simple_tag
def yaziyi_duzelt(isim):
    isim = str(isim).split(" ")
    isim = str(isim[0]).capitalize()
    return isim

@register.simple_tag
def isplani_durumu_kontrol(id):
    a = IsplaniPlanlariIlerleme.objects.filter(proje_ait_bilgisi__id = id)
    b = ""
    for i in a:
        b = i.status

    return b

@register.simple_tag
def dosya_varsa_indirme_isplani(id):

    z = ""
    veri = IsplaniDosyalari.objects.filter(proje_ait_bilgisi__id = id.id)
    for i in veri:
        k = str(i.dosya.url).split("/")
        k = k[ -1]

        if "pdf" in i.dosya.url :
            z = z+ """<div class="ilerleme-durumu-dosya">
                                    <a href="{}" >{}</a>
                                    <img src="https://play-lh.googleusercontent.com/LvJB3SJdelN1ZerrndNgRcDTcgKO49d1A63C5hNJP06rMvsGkei-lwV52eYZJmMknCwW">
                                </div>""".format(i.dosya.url,k)
        else:
            z = z+ """<div class="ilerleme-durumu-dosya">
                                        <a href="{}" >{}</a>
                                        <img src="{}">
                                    </div>""".format(i.dosya.url,k,i.dosya.url)
    return mark_safe(z)
@register.simple_tag
def ilerleme_goster(id):
    ilerlemeler = IsplaniPlanlariIlerleme.objects.filter(proje_ait_bilgisi__id = id).order_by("-teslim_tarihi")

    return ilerlemeler
@register.simple_tag
def dosya_varsa_indirme_isplani_ilerleme(id):

    z = ""
    veri = IsplaniIlerlemeDosyalari.objects.filter(proje_ait_bilgisi__id = id)
    for i in veri:
        a = str(i.dosya.url).split("/")
        if "pdf" in i.dosya.url :
            z = z+ """<div class="ilerleme-durumu-dosya">
                                    <a href="{}" >{}</a>
                                    <img src="https://play-lh.googleusercontent.com/LvJB3SJdelN1ZerrndNgRcDTcgKO49d1A63C5hNJP06rMvsGkei-lwV52eYZJmMknCwW">
                                </div>""".format(i.dosya.url,a[-1])
        else:
            z = z+ """<div class="ilerleme-durumu-dosya">
                                        <span>{}</span>
                                        <img src="{}">
                                    </div>""".format(a[-1],i.dosya.url)
        #z = z+ '<div class="d-flex border border-dashed p-2 rounded position-relative"><div class="flex-shrink-0 avatar-xs"><div class="avatar-title bg-info-subtle text-info fs-15 rounded"><i class="ri-file-zip-line"></i></div></div><div class="flex-grow-1 overflow-hidden ms-2"><h6 class="text-truncate mb-0"><a href="{}" download class="stretched-link">{}</a></h6><small></small></div></div>'.format(i.dosya.url,a[-1])
        
    return mark_safe(z)

@register.simple_tag
def toplam_tutar_cikarma(id):
    a = gelir_urun_bilgisi.objects.filter(gider_bilgis = id)
    topla = 0
    for i in a:
        topla = topla + ((i.urun_fiyati*i.urun_adeti)-i.urun_indirimi)
    return topla
@register.simple_tag
def toplam_tutar_cikarmai(id):
    a = gider_urun_bilgisi.objects.filter(gider_bilgis = id)
    topla = 0
    for i in a:
        topla = topla + ((i.urun_fiyati*i.urun_adeti)-i.urun_indirimi)
    return topla
@register.simple_tag
def toplam_odenme_tutar(id):
    a = Gelir_odemesi.objects.filter(gelir_kime_ait_oldugu = id)
    topla = 0
    for i in a:
        topla = topla + i.tutar
    return topla
@register.simple_tag
def toplam_odenme_tutari(id):
    a = Gider_odemesi.objects.filter(gelir_kime_ait_oldugu = id)
    topla = 0
    for i in a:
        topla = topla + i.tutar
    return topla
@register.simple_tag
def kalemleri_getir_gelir_faturasi_icin(id):
    a = gelir_urun_bilgisi.objects.filter(gider_bilgis = id)
    return a
@register.simple_tag
def kalemleri_getir_gelir_faturasi_icini(id):
    a = gider_urun_bilgisi.objects.filter(gider_bilgis = id)
    return a
@register.simple_tag
def carpma_islemi(a,b):
    return a*b

@register.simple_tag
def kalemleri_getir_gelir_faturasi_icin_toplam_flan(id):
    a = gelir_urun_bilgisi.objects.filter(gider_bilgis = id)

    toplam_urun_fiyati = 0
    genel_toplam = 0
    for i in a:
        toplam_urun_fiyati = toplam_urun_fiyati+i.urun_fiyati
        genel_toplam = genel_toplam+(i.urun_fiyati*i.urun_adeti)
    sonuc = {"toplam" : toplam_urun_fiyati,
             "genel":genel_toplam}

    return sonuc
@register.simple_tag
def kalemleri_getir_gelir_faturasi_icin_toplam_flani(id):
    a = gider_urun_bilgisi.objects.filter(gider_bilgis = id)

    toplam_urun_fiyati = 0
    genel_toplam = 0
    for i in a:
        toplam_urun_fiyati = toplam_urun_fiyati+i.urun_fiyati
        genel_toplam = genel_toplam+(i.urun_fiyati*i.urun_adeti)
    sonuc = {"toplam" : toplam_urun_fiyati,
             "genel":genel_toplam}

    return sonuc
@register.simple_tag
def kalan_tutuar(id):
    a = Gelir_odemesi.objects.filter(gelir_kime_ait_oldugu = id)
    toplam = 0
    for i in a:
        toplam = toplam+i.tutar
    a = gelir_urun_bilgisi.objects.filter(gider_bilgis = id)
    genel_toplam = 0
    indirim = 0
    for i in a:
        genel_toplam = genel_toplam+(i.urun_fiyati*i.urun_adeti)
        indirim = indirim+ i.urun_indirimi
    return fiyat_duzelt(float(genel_toplam - toplam-indirim))
@register.simple_tag
def kalan_tutuari(id):
    a = Gider_odemesi.objects.filter(gelir_kime_ait_oldugu = id)
    toplam = 0
    indirim = 0
    for i in a:
        toplam = toplam+i.tutar
    a = gider_urun_bilgisi.objects.filter(gider_bilgis = id)
    genel_toplam = 0
    for i in a:
        genel_toplam = genel_toplam+(i.urun_fiyati*i.urun_adeti)
        indirim = indirim+ i.urun_indirimi
    return fiyat_duzelt(float(genel_toplam - toplam -indirim),2)
@register.simple_tag

def makbuzlari_getir(id):
    a = Gelir_odemesi.objects.filter(gelir_kime_ait_oldugu__id = id)
    return a
@register.simple_tag
def makbuzlari_getiri(id):
    a = Gider_odemesi.objects.filter(gelir_kime_ait_oldugu__id = id)
    return a
@register.simple_tag
def cari_gelirleri(bilgi):
    b = get_object_or_404(Gelir_Bilgisi,id = bilgi)
    c = gelir_urun_bilgisi.objects.filter(gider_bilgis__id  =  b.id)
    gelir_toplami = 0
    for j in c:
        gelir_toplami = gelir_toplami + (j.urun_fiyati*j.urun_adeti) - j.urun_indirimi
    d = Gelir_odemesi.objects.filter(silinme_bilgisi = False,gelir_kime_ait_oldugu__id = b.id).order_by("tarihi")

    return {"gelir_toplama":gelir_toplami,"gider_odemesi":d}
@register.simple_tag
def cari_gelirlerii(bilgi):
    b = get_object_or_404(Gelir_Bilgisi,id = bilgi)
    c = gelir_urun_bilgisi.objects.filter(gider_bilgis__id  =  b.id)
    gelir_toplami = 0
    gider_odemesi = 0
    for j in c:
        gelir_toplami = gelir_toplami + (j.urun_fiyati*j.urun_adeti) - j.urun_indirimi
    d = Gelir_odemesi.objects.filter(gelir_kime_ait_oldugu__id = b.id,silinme_bilgisi = False)
    for j in d:
        gider_odemesi = gider_odemesi+j.tutar
    return fiyat_duzelt(float(gelir_toplami-gider_odemesi),2)
@register.simple_tag
def cikarma(a,b):
    y = float(a)+float(b)
    return round(float(y),2)

@register.simple_tag
def cari_islemleri_bilgi(bilgi):
    a = list(Gider_odemesi.objects.filter(silinme_bilgisi = False,gelir_kime_ait_oldugu__cari_bilgisi = bilgi))+list(Gelir_odemesi.objects.filter(silinme_bilgisi = False,gelir_kime_ait_oldugu__cari_bilgisi = bilgi))
    return a
@register.simple_tag
def cari_giderleri(bilgi):
    b = get_object_or_404(Gider_Bilgisi,id = bilgi)
    c = gider_urun_bilgisi.objects.filter(gider_bilgis__id  =  b.id)
    gelir_toplami = 0
    for j in c:
        gelir_toplami = gelir_toplami + (j.urun_fiyati*j.urun_adeti) - j.urun_indirimi
    d = Gider_odemesi.objects.filter(gelir_kime_ait_oldugu__id = b.id).order_by("tarihi")

    return {"gelir_toplama":gelir_toplami,"gider_odemesi":d}
@register.simple_tag
def cari_giderlerii(bilgi):
    b = get_object_or_404(Gider_Bilgisi,id = bilgi)
    c = gider_urun_bilgisi.objects.filter(gider_bilgis__id  =  b.id)
    gelir_toplami = 0
    gider_odemesi = 0
    for j in c:
        gelir_toplami = gelir_toplami + (j.urun_fiyati*j.urun_adeti) - j.urun_indirimi
    d = Gider_odemesi.objects.filter(gelir_kime_ait_oldugu__id = b.id,silinme_bilgisi = False)
    for j in d:
        gider_odemesi = gider_odemesi+j.tutar
    return fiyat_duzelt(float(gelir_toplami-gider_odemesi),2)
@register.simple_tag
def cari_islemleri(bilgi):
    b = Gider_Bilgisi.objects.filter(silinme_bilgisi = False,cari_bilgisi__id = bilgi.id).order_by("-fatura_tarihi")
    gider_toplami = 0
    gider_odemesi = 0
    gider_bilgisi = 0
    a = Gelir_Bilgisi.objects.filter(silinme_bilgisi = False,cari_bilgisi__id = bilgi.id).order_by("-fatura_tarihi")
    gelir_toplami = 0
    gelir_odemesi = 0
    gelir_bilgisi = 0
    for i in b:
        c = gider_urun_bilgisi.objects.filter(gider_bilgis__id =  i.id)
        for j in c:
            gider_toplami = gider_toplami + (j.urun_fiyati*j.urun_adeti) - j.urun_indirimi
        d = Gider_odemesi.objects.filter(silinme_bilgisi = False,gelir_kime_ait_oldugu__id = i.id)
        for j in d:
            gider_odemesi = gider_odemesi+j.tutar
    gider_bilgisi = gider_toplami-gider_odemesi
    for i in a:
        c = gelir_urun_bilgisi.objects.filter(gider_bilgis__id  =  i.id)
        for j in c:
            gelir_toplami = gelir_toplami + (j.urun_fiyati*j.urun_adeti) - j.urun_indirimi
        d = Gelir_odemesi.objects.filter(silinme_bilgisi = False,gelir_kime_ait_oldugu__id = i.id)
        for j in d:
            gelir_odemesi = gelir_odemesi+j.tutar
    gelir_bilgisi = gelir_toplami - gelir_odemesi
    sonuc = gelir_bilgisi - gider_bilgisi
    return {"gelir_bilgisi":gelir_bilgisi,"gider_bilgisi":gider_bilgisi,"sonuc":round(sonuc,2),"b":b,"a":a}
@register.simple_tag
def gelirler_tutari(bilgi):
    if bilgi.is_superuser:
        a = Gelir_odemesi.objects.filter(gelir_kime_ait_oldugu__silinme_bilgisi= False)
        toplam = 0
        for i in a:
            toplam = toplam+i.tutar
        a = gelir_urun_bilgisi.objects.filter(gider_bilgis__silinme_bilgisi= False)
        genel_toplam = 0
        indirim = 0
        for i in a:
            genel_toplam = genel_toplam+(i.urun_fiyati*i.urun_adeti)
            indirim = indirim+ i.urun_indirimi
        return {"tutar":str(fiyat_duzelt(float(genel_toplam),2)),"genel_odeme":fiyat_duzelt(float(toplam-indirim),2)}
    else:
        a = Gelir_odemesi.objects.filter(gelir_kime_ait_oldugu__gelir_kime_ait_oldugu = bilgi,gelir_kime_ait_oldugu__silinme_bilgisi= False)
        toplam = 0
        for i in a:
            toplam = toplam+i.tutar
        a = gelir_urun_bilgisi.objects.filter(gider_bilgis__gelir_kime_ait_oldugu = bilgi,gider_bilgis__silinme_bilgisi= False)
        genel_toplam = 0
        indirim = 0
        for i in a:
            genel_toplam = genel_toplam+(i.urun_fiyati*i.urun_adeti)
            indirim = indirim+ i.urun_indirimi
        return {"tutar":str(fiyat_duzelt(float(genel_toplam),2)),"genel_odeme":fiyat_duzelt(float(toplam-indirim),2)}

@register.simple_tag
def giderler_tutari(bilgi):
    if bilgi.is_superuser:
        a = Gider_odemesi.objects.filter(gelir_kime_ait_oldugu__silinme_bilgisi= False)
        toplam = 0
        for i in a:
            toplam = toplam+i.tutar
        a = gider_urun_bilgisi.objects.filter(gider_bilgis__silinme_bilgisi= False)
        genel_toplam = 0
        indirim = 0
        for i in a:
            genel_toplam = genel_toplam+(i.urun_fiyati*i.urun_adeti)
            indirim = indirim+ i.urun_indirimi

        return {"tutar":str(fiyat_duzelt(float(genel_toplam),2)),"genel_odeme":fiyat_duzelt(float(toplam-indirim),2),"genel_odeme2":str(fiyat_duzelt(float(toplam-indirim),2))}
    else:
        a = Gider_odemesi.objects.filter(gelir_kime_ait_oldugu__gelir_kime_ait_oldugu = bilgi,gelir_kime_ait_oldugu__silinme_bilgisi= False)
        toplam = 0
        for i in a:
            toplam = toplam+i.tutar
        a = gider_urun_bilgisi.objects.filter(gider_bilgis__gelir_kime_ait_oldugu = bilgi,gider_bilgis__silinme_bilgisi= False)
        genel_toplam = 0
        indirim = 0
        for i in a:
            genel_toplam = genel_toplam+(i.urun_fiyati*i.urun_adeti)
            indirim = indirim+ i.urun_indirimi
        return {"tutar":str(fiyat_duzelt(float(genel_toplam),2)),"genel_odeme":fiyat_duzelt(float(toplam-indirim),2),"genel_odeme2":str(fiyat_duzelt(float(toplam-indirim),2))}
#
@register.simple_tag
def basit_cikarma(a,b):
    a = str(a)
    b = str(b)
    a = a.replace('.', '')
    b = b.replace('.', '')
    a = a.replace(',', '.')
    b = b.replace(',', '.')
    y = float(a)-float(b)

    return str(fiyat_duzelt(y,2))
@register.simple_tag
def basit_cikarma_duzenli(a,b):
   
    y = float(a)-float(b)

    return str(round(y,2))
@register.simple_tag
def sorgu(a):
    y = float(a)
    return str(round(y,2))

@register.simple_tag
def basit_toplama(a,b):
    y = float(a)+float(b)
    return str(round(y,2))
@register.simple_tag
def kategori_bilgi_ver(b):
    genel_tutar = 0
    if b.is_superuser:
        bilgi = gider_kategorisi.objects.filter(silinme_bilgisi = False)
    else:
        bilgi = gider_kategorisi.objects.filter(silinme_bilgisi = False,gider_kategoris_ait_bilgisi = b)
    a = []
    isimleri = []
    renk = []

    for i in bilgi:
        isimleri.append(str(i.gider_kategori_adi))
        renk.append(str(i.gider_kategorisi_renk))
        a.append(round(Gider_Bilgisi.objects.filter(gelir_kategorisii_id = i.id,silinme_bilgisi = False).aggregate(total=Sum('toplam_tutar'))['total'] or 0 ,2))
        genel_tutar = genel_tutar + round( float(Gider_Bilgisi.objects.filter(gelir_kategorisii_id = i.id,silinme_bilgisi = False).aggregate(total=Sum('toplam_tutar'))['total'] or 0),2)
    
    return {"isimleri":isimleri,"a":a,"renk":renk,"tutar":fiyat_duzelt(genel_tutar)}
@register.simple_tag
def ekstra(id,k):
    bilgi =  faturalardaki_gelir_gider_etiketi.objects.last()
    if bilgi.gelir_etiketi in k:
        a = gider_urun_bilgisi.objects.filter(gider_bilgis = id)
        topla = 0
        for i in a:
            topla = topla + ((i.urun_fiyati*i.urun_adeti)-i.urun_indirimi)
        return topla
    else:
        a = gider_urun_bilgisi.objects.filter(gider_bilgis = id)
        topla = 0
        for i in a:
            topla = topla + ((i.urun_fiyati*i.urun_adeti)-i.urun_indirimi)
        return topla
@register.simple_tag
def ekstra_odeme(id,k):
    bilgi =  faturalardaki_gelir_gider_etiketi.objects.last()
    if bilgi.gelir_etiketi in k:
        a = Gelir_odemesi.objects.filter(gelir_kime_ait_oldugu = id)
        topla = 0
        for i in a:
            topla = topla +  i.tutar
        return topla
    else:
        a = Gider_odemesi.objects.filter(gelir_kime_ait_oldugu = id)
        topla = 0
        for i in a:
            topla = topla +  i.tutar
        return topla

@register.simple_tag
def gelir_qr_cek(id):
    a = get_object_or_404(gelir_qr,gelir_kime_ait_oldugu__id = id)
    return a.qr_bilgisi.url
@register.simple_tag
def gider_qr_cek(id):
    a = get_object_or_404(gider_qr,gelir_kime_ait_oldugu__id = id)
    return a.qr_bilgisi.url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import hashlib
@register.simple_tag
def toplama_yaptirma(bilgi):
    toplama = 0
    for i in bilgi:
        toplama = toplama + (i.urun_fiyati*i.urun_adeti)

    return toplama
@register.simple_tag
def kasa_toplam(bilgi):
    if bilgi:
        toplam = 0
        a = Gider_odemesi.objects.filter(kasa_bilgisi = bilgi,silinme_bilgisi = False)
        b = Gelir_odemesi.objects.filter(kasa_bilgisi = bilgi,silinme_bilgisi = False)
        for i in a : 
            toplam = toplam - i.tutar
        for i in b : 
            toplam = toplam + i.tutar
        toplam = toplam + bilgi.bakiye
        return fiyat_duzelt(float(toplam),2)
    return 0
"""@register.simple_tag
def generate_token(object_id):
    hash_input = force_bytes(object_id)
    hash_value = hashlib.sha256(hash_input).digest()
    return urlsafe_base64_encode(hash_value)"""
import datetime
@register.simple_tag
def tarih_cek():
    from datetime import datetime, timedelta

    # Bugünün tarihini al
    bugun = datetime.today()

    # Bir hafta ekle
    bir_hafta_sonra = bugun + timedelta(weeks=1)

    # Belirtilen formatta tarihleri yazdır
    bugun_formatli = bugun.strftime("%m/%d/%Y")
    bir_hafta_sonra_formatli = bir_hafta_sonra.strftime("%m/%d/%Y")
    a =  bugun_formatli + " - " + bir_hafta_sonra_formatli

    return a
import base64
import hashlib
@register.simple_tag
def generate_token(number):
    # Sayıyı stringe dönüştür
    number_str = str(number)

    # Stringi bayt dizisine dönüştür
    byte_str = number_str.encode('utf-8')

    # Bayt dizisini SHA-256 ile şifrele
    hashed_bytes = hashlib.sha256(byte_str).digest()

    # Şifrelenmiş bayt dizisini base64 formatında kodla
    token = base64.urlsafe_b64encode(hashed_bytes)

    # Oluşturulan tokeni döndür
    return token
@register.simple_tag
def ayiklama(k):
    gelir = faturalardaki_gelir_gider_etiketi.objects.last().gelir_etiketi
    gider = faturalardaki_gelir_gider_etiketi.objects.last().gider_etiketi
    if gelir in k:
        return 0
    elif gider in k :
        return 1

@register.simple_tag
def kasa_verisi(bakiye,id):
    a = Gelir_odemesi.objects.filter(kasa_bilgisi = id,silinme_bilgisi = False)
    toplam_tutar = 0
    for i in a:
        toplam_tutar = toplam_tutar +i.tutar
    toplam_tutar = toplam_tutar + bakiye
    a = Gider_odemesi.objects.filter(kasa_bilgisi = id,silinme_bilgisi = False)

    for i in a:
        toplam_tutar = toplam_tutar -i.tutar
    return round(toplam_tutar,2)
@register.simple_tag
def kasa_islemleri(bilgi):
    a = list(Gider_odemesi.objects.filter(silinme_bilgisi = False,kasa_bilgisi__id = bilgi.id))+list(Gelir_odemesi.objects.filter(silinme_bilgisi = False,kasa_bilgisi__id = bilgi.id))
    return a
@register.simple_tag
def fatura_durumu(k):
    bilgi =  faturalardaki_gelir_gider_etiketi.objects.last()
    if bilgi.gelir_etiketi in k:
        return 0
    else:
        return 1
from django.db.models import Sum
from django.utils.timezone import now
@register.simple_tag
def ozellikler(bilgi):
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    from django.utils.translation import gettext as _

    today = datetime.today()
    aylar = []
    gelirler = []
    giderler = []

    # Ay isimleri için kullanılacak format
    month_names = {
        1: _("Ocak"),
        2: _("Şubat"),
        3: _("Mart"),
        4: _("Nisan"),
        5: _("Mayıs"),
        6: _("Haziran"),
        7: _("Temmuz"),
        8: _("Ağustos"),
        9: _("Eylül"),
        10: _("Ekim"),
        11: _("Kasım"),
        12: _("Aralık")
    }

    # Son 12 ayı bul ve her aya ait gelir ve giderleri hesapla
    for i in range(12):
        # Bu aydan i ay geriye git
        start_of_month = (today - relativedelta(months=i)).replace(day=1)
        end_of_month = (start_of_month + relativedelta(months=1)) - relativedelta(days=1)

        if bilgi.is_superuser:
            # Gelirleri al
            total_gelir = Gelir_odemesi.objects.filter(
                tarihi__gte=start_of_month,
                tarihi__lte=end_of_month,
                silinme_bilgisi=False
            ).aggregate(total=Sum('tutar'))['total'] or 0
            gelirler.append(round(total_gelir, 2))

            # Giderleri al
            total_gider = Gider_odemesi.objects.filter(
                tarihi__gte=start_of_month,
                tarihi__lte=end_of_month,
                silinme_bilgisi=False
            ).aggregate(total=Sum('tutar'))['total'] or 0
            giderler.append(round(total_gider, 2))
        else:
            # Gelirleri al
            total_gelir = Gelir_odemesi.objects.filter(
                tarihi__gte=start_of_month,
                tarihi__lte=end_of_month,
                gelir_kime_ait_oldugu__gelir_kime_ait_oldugu=bilgi,
                silinme_bilgisi=False
            ).aggregate(total=Sum('tutar'))['total'] or 0
            gelirler.append(round(total_gelir, 2))

            # Giderleri al
            total_gider = Gider_odemesi.objects.filter(
                tarihi__gte=start_of_month,
                tarihi__lte=end_of_month,
                gelir_kime_ait_oldugu__gelir_kime_ait_oldugu=bilgi,
                silinme_bilgisi=False
            ).aggregate(total=Sum('tutar'))['total'] or 0
            giderler.append(round(total_gider, 2))

        # Ay adı ve yılı listeye ekle
        aylar.append(f"{month_names[start_of_month.month]} {start_of_month.year}")

    # Listeleri ters çevir (eski tarihlerden yeniye doğru sıralamak için)
    aylar.reverse()
    gelirler.reverse()
    giderler.reverse()

    return {
        "gelir": gelirler,
        "gider": giderler,
        "aylar": aylar
    }

#@register.filter
@register.simple_tag
def toplam_kalem_orani_toplami(veri):
    a = 0
    b = 0
    for i in veri:
        a = a + i.santiye_agirligi
        b = b + i.santiye_finansal_agirligi
    return {"a":a,"b":b}
from hashids import Hashids

# Salt değeri ve minimum hash uzunluğu belirleyin
HASHIDS_SALT = "habip_elis_12345"
HASHIDS_MIN_LENGTH = 32

hashids = Hashids(salt=HASHIDS_SALT, min_length=HASHIDS_MIN_LENGTH)
@register.simple_tag
def encode_id(id):
    return hashids.encode(id)
@register.simple_tag
def decode_id(hash_id):
    ids = hashids.decode(hash_id)
    return ids[0] if ids else None
@register.simple_tag
def mutlak_deger(a):
    a = a.replace('.', '')
    a = a.replace(',', '.')
    if float(a) < 0:
        return fiyat_duzelt((float(a)*-1),2)
    elif float(a) > 0:
        return (fiyat_duzelt((float(a)),2))
    return 0.0
def tsasa(a):
   
    return 100-a
@register.simple_tag
def get_object_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except :
        return None
@register.simple_tag
def fatura_hakedis_baglama(fatura_numari,fatura_kime_ait):
    a = get_object_or_none(Gider_Bilgisi,fatura_no = fatura_numari , gelir_kime_ait_oldugu = fatura_kime_ait)
    b = get_object_or_none(Gelir_Bilgisi,fatura_no = fatura_numari , gelir_kime_ait_oldugu = fatura_kime_ait)
    if a:
        return {"tutar" : a.toplam_tutar,"kalan_tuar":a.kalan_tutar}
    elif b:
        return {"tutar" : b.toplam_tutar,"kalan_tuar":b.kalan_tutar}
    else:
        return 0
@register.simple_tag
def hakedistoplam_kalan(id):
    toplam = 0
    kalan = 0
    for i in id:
        a = get_object_or_none(Gider_Bilgisi,fatura_no = i.fatura_numarasi , gelir_kime_ait_oldugu = i.proje_ait_bilgisi.taseron_ait_bilgisi)
        b = get_object_or_none(Gelir_Bilgisi,fatura_no = i.fatura_numarasi , gelir_kime_ait_oldugu = i.proje_ait_bilgisi.taseron_ait_bilgisi)
        if a:
            toplam = toplam+ a.toplam_tutar
            kalan = kalan+a.kalan_tutar
            
        elif b:
            toplam = toplam+ a.toplam_tutar
            kalan = kalan+a.kalan_tutar
    return {"toplam":toplam,"kalan":kalan}
@register.simple_tag
def kulanici_yetkileri_goster(kullanici):
    a = get_object_or_none(bagli_kullanicilar,kullanicilar = kullanici)
    if a:
        return a.izinler
    else: 
        return 0
@register.simple_tag
def indirim_toplam_fonksiyonu(a=0, b=0):
    try:
        a = float(a) if a not in ("", None) else 0
        b = float(b) if b not in ("", None) else 0
    except ValueError:
        a = 0
        b = 0

    return a + b
@register.simple_tag
def kulanici_yetkileri_kullandirt(kullanici,ust_kullanici):
    a = get_object_or_none(bagli_kullanicilar,kullanicilar = kullanici,izinler__izinlerin_sahibi_kullanici = ust_kullanici)
    if a:
        return a.izinler
    else: 
        return 0

@register.simple_tag
def pozisyon_calisan_sayisi(id):
    a = calisanlar.objects.filter(silinme_bilgisi = False,status = "0",calisan_pozisyonu = id).count()
    return a
@register.simple_tag
def departman_calisan_sayisi(id):
    a = calisanlar.objects.filter(silinme_bilgisi = False,status = "0",calisan_kategori = id).count()
    return a
from django.db.models.query_utils import Q
@register.simple_tag
def stok_sayisi(id):
    toplam = 0
    a = gider_urun_bilgisi.objects.filter(urun_bilgisi = id,gider_bilgis__silinme_bilgisi = False)
    b = gelir_urun_bilgisi.objects.filter(urun_bilgisi = id,gider_bilgis__silinme_bilgisi = False)
    stok_giris_cikisi = stok_giris_cikis.objects.filter(stok_giren_urun = id,stok_durumu = "0")
    for i in a:
        toplam = toplam+float(i.urun_adeti)
    for i in b:
        toplam = toplam-float(i.urun_adeti)
    for i in stok_giris_cikisi:
        toplam = toplam+float(i.stok_adeti)
    stok_giris_cikisi = stok_giris_cikis.objects.filter(stok_giren_urun = id,stok_durumu = "1")
    for i in stok_giris_cikisi:
        toplam = toplam-float(i.stok_adeti)
    zimmet = zimmet_olayi.objects.filter(zimmet_verilen_urun = id).filter(Q(zimmet_durumu = "0")|Q(zimmet_durumu = "2"))
    for i in zimmet:
        toplam = toplam - float(i.zimmet_miktari)
    return fiyat_duzelt(toplam)

@register.simple_tag
def zimmet_sayisi(id):
    toplam = 0
    zimmet = zimmet_olayi.objects.filter(zimmet_verilen_urun = id).filter(Q(zimmet_durumu = "0")|Q(zimmet_durumu = "2"))
    for i in zimmet:
        toplam = toplam + float(i.zimmet_miktari)
    return toplam

# myapp/templatetags/custom_tags.py

from django import template
from django.http import JsonResponse
from users.models import calisanlar_calismalari, calisanlar
from django.shortcuts import get_object_or_404
import json
from datetime import datetime



@register.simple_tag
def calismalari_cek(personel, gun, tarih):
    tarih = str(tarih).split("-")
    yil = tarih[0]
    ay = tarih[1]
    date_obj = datetime(int(yil), int(ay), int(gun))
    sonuc = get_object_or_none(calisanlar_calismalari, calisan=get_object_or_404(calisanlar, id=personel), tarihi=date_obj)
    if sonuc:
        return { 'normal_saat': sonuc.normal_calisma_saati, 'mesai_saati': sonuc.mesai_calisma_saati}
    else:
        return { 'normal_saat': 0, 'mesai_saati': 0}
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
@register.simple_tag
def dashboard_bilgisi(kisi):
    content = {}
    cali = calisanlar.objects.filter(calisan_kime_ait = kisi,status = "0")
    content["personel_sayisi"] = cali.count()
    try:
        cali = cali.order_by("-id")[:2]
    except:
        cali = 0
    html = []
    for i in cali:
        try:
            calismalar = calisanlar_calismalari.objects.filter(
                    calisan=get_object_or_none(calisanlar, id=i.id)
                    ).annotate(
                        year=ExtractYear('tarihi'),
                        month=ExtractMonth('tarihi')
                    ).values(
                        'year', 'month', 'maas__id'  # Maas ID ve ismi ile gruplanıyor
                    ).annotate(
                        total_normal_calisma_saati=Sum('normal_calisma_saati'),
                        total_mesai_calisma_saati=Sum('mesai_calisma_saati')
                    ).order_by('year', 'month', 'maas__id')
            
            person = {"resim":i.profile.url if i.profile.url else "{% static 'go/images/avatar.png' %}",
            "isim_soyisim" : i.isim +" "+ i.soyisim,
            "toplam_calisma_saati" : calismalar.last()["total_normal_calisma_saati"],
            "iletisim" : i.telefon_numarasi}
            html.append(person)
        except:
            pass
    content["aktif_santiye"] = santiye.objects.filter(proje_ait_bilgisi = kisi,silinme_bilgisi = False).count()
    content["aktif_proje"] = proje_tipi.objects.filter(proje_ait_bilgisi = kisi,silinme_bilgisi = False).count()
    
    content["personeller"] = html
    return content
from django.utils.timezone import now, timedelta
@register.simple_tag
def gelir_yuzde_farki(customuser):
    # Bu haftanın başlangıcını ve geçen haftanın başlangıcını hesapla
    today = now().date()
    this_week_start = today - timedelta(days=today.weekday())
    last_week_start = this_week_start - timedelta(weeks=1)

    # Geçen hafta ve bu hafta yapılan ödemeleri al
    last_week_payments = Gelir_odemesi.objects.filter(
        tarihi__gte=last_week_start,
        tarihi__lt=this_week_start,
        gelir_kime_ait_oldugu__gelir_kime_ait_oldugu=customuser,
        gelir_kime_ait_oldugu__silinme_bilgisi=False
    ).aggregate(total=models.Sum('tutar'))['total'] or 0

    this_week_payments = Gelir_odemesi.objects.filter(
        tarihi__gte=this_week_start,
        gelir_kime_ait_oldugu__gelir_kime_ait_oldugu=customuser,
        gelir_kime_ait_oldugu__silinme_bilgisi=False
    ).aggregate(total=models.Sum('tutar'))['total'] or 0

    # Yüzde farkını hesapla
    if last_week_payments == 0:
        tutar = 100 if this_week_payments > 0 else 0  # Geçen hafta ödeme yoksa, bu hafta varsa %100 artış
    else:
        tutar = ((this_week_payments - last_week_payments) / last_week_payments) * 100
        tutar =  round(tutar, 2)
    if tutar >=0:
        arti = True
    else:
        arti = False
    return {"fark":tutar,"arti":arti}
@register.simple_tag
def gider_yuzde_farki(customuser):
    # Bu haftanın başlangıcını ve geçen haftanın başlangıcını hesapla
    today = now().date()
    this_week_start = today - timedelta(days=today.weekday())
    last_week_start = this_week_start - timedelta(weeks=1)

    # Geçen hafta ve bu hafta yapılan ödemeleri al
    last_week_payments = Gider_odemesi.objects.filter(
        tarihi__gte=last_week_start,
        tarihi__lt=this_week_start,
        gelir_kime_ait_oldugu__gelir_kime_ait_oldugu=customuser,
        gelir_kime_ait_oldugu__silinme_bilgisi=False
    ).aggregate(total=models.Sum('tutar'))['total'] or 0

    this_week_payments = Gider_odemesi.objects.filter(
        tarihi__gte=this_week_start,
        gelir_kime_ait_oldugu__gelir_kime_ait_oldugu=customuser,
        gelir_kime_ait_oldugu__silinme_bilgisi=False
    ).aggregate(total=models.Sum('tutar'))['total'] or 0

    # Yüzde farkını hesapla
    if last_week_payments == 0:
        tutar = 100 if this_week_payments > 0 else 0  # Geçen hafta ödeme yoksa, bu hafta varsa %100 artış
    else:
        tutar = ((this_week_payments - last_week_payments) / last_week_payments) * 100
        tutar =  round(tutar, 2)
    if tutar >=0:
        arti = True
    else:
        arti = False
    return {"fark":tutar,"arti":arti}
    
from django import template
from django.utils.translation import gettext as _
from django.db.models import Sum
from datetime import datetime
from dateutil.relativedelta import relativedelta


@register.simple_tag
def son_dort_ay_tutar(customuser):
    today = datetime.today()
    aylar = []
    tutarlar = []

    # Ay isimleri için kullanılacak format
    month_names = {
        1: _("January"),
        2: _("February"),
        3: _("March"),
        4: _("April"),
        5: _("May"),
        6: _("June"),
        7: _("July"),
        8: _("August"),
        9: _("September"),
        10: _("October"),
        11: _("November"),
        12: _("December"),
    }

    # Son 4 ayı bul ve her aya ait ödemeleri hesapla
    for i in range(4):
        # Bu aydan i ay geriye git
        start_of_month = (today - relativedelta(months=i)).replace(day=1)
        end_of_month = (start_of_month + relativedelta(months=1)) - relativedelta(days=1)

        # O ay içerisindeki ödemeleri al
        total_payment = Gelir_odemesi.objects.filter(
            tarihi__gte=start_of_month,
            tarihi__lte=end_of_month,
            gelir_kime_ait_oldugu__gelir_kime_ait_oldugu=customuser,
            gelir_kime_ait_oldugu__silinme_bilgisi=False
        ).aggregate(total=Sum('tutar'))['total'] or 0

        # Ay adı ve toplam tutarı listeye ekle
        ay_adi = f"{month_names[start_of_month.month]} {start_of_month.year}"  # Örneğin: "September 2023"
        tutarlar.append(round(total_payment, 2))
        aylar.append(ay_adi)

    return {"aylar": aylar, "tutarlar": tutarlar}

@register.simple_tag
def son_dort_ay_tutar_gider(customuser):
    today = datetime.today()
    aylar = []
    tutarlar = []

    # Ay isimleri için kullanılacak format
    month_names = {
        1: _("January"),
        2: _("February"),
        3: _("March"),
        4: _("April"),
        5: _("May"),
        6: _("June"),
        7: _("July"),
        8: _("August"),
        9: _("September"),
        10: _("October"),
        11: _("November"),
        12: _("December"),
    }

    # Son 4 ayı bul ve her aya ait ödemeleri hesapla
    for i in range(4):
        # Bu aydan i ay geriye git
        start_of_month = (today - relativedelta(months=i)).replace(day=1)
        end_of_month = (start_of_month + relativedelta(months=1)) - relativedelta(days=1)

        # O ay içerisindeki ödemeleri al
        total_payment = Gider_odemesi.objects.filter(
            tarihi__gte=start_of_month,
            tarihi__lte=end_of_month,
            gelir_kime_ait_oldugu__gelir_kime_ait_oldugu=customuser,
            gelir_kime_ait_oldugu__silinme_bilgisi=False
        ).aggregate(total=Sum('tutar'))['total'] or 0

        # Ay adı ve toplam tutarı listeye ekle
        ay_adi = f"{month_names[start_of_month.month]} {start_of_month.year}"  # Örneğin: "September 2023"
        tutarlar.append(round(total_payment, 2))
        aylar.append(ay_adi)

    return {"aylar": aylar, "tutarlar": tutarlar}



from django import template
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum



@register.simple_tag
def borc_yuzde_farki(customuser):
    today = now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_last_week = start_of_week - timedelta(days=1)
    start_of_last_week = end_of_last_week - timedelta(days=6)
    
    # Bu haftanın giderleri
    this_week_total = Gider_Bilgisi.objects.filter(
        fatura_tarihi__gte=start_of_week,
        fatura_tarihi__lte=end_of_last_week,
        gelir_kime_ait_oldugu=customuser,
        silinme_bilgisi=False
    ).aggregate(total=Sum('kalan_tutar'))['total'] or 0
    
    # Geçen haftanın giderleri
    last_week_total = Gider_Bilgisi.objects.filter(
        fatura_tarihi__gte=start_of_last_week,
        fatura_tarihi__lte=end_of_last_week,
        gelir_kime_ait_oldugu=customuser,
        silinme_bilgisi=False
    ).aggregate(total=Sum('kalan_tutar'))['total'] or 0

    
    # Yüzde farkını hesapla
    if last_week_total == 0:
        tutar = 100 if this_week_total > 0 else 0  # Geçen hafta ödeme yoksa, bu hafta varsa %100 artış
    else:
        tutar = ((this_week_total - last_week_total) / last_week_total) * 100
        tutar =  round(tutar, 2)
    if tutar >=0:
        arti = True
    else:
        arti = False
    return {"fark":tutar,"arti":arti}
    

@register.simple_tag
def borc_son_dort_ay_tutar(customuser):
    today = datetime.today()
    aylar = []
    tutarlar = []

    # Son 4 ayı bul ve her aya ait ödemeleri hesapla
    for i in range(4):
        # Bu aydan i ay geriye git
        start_of_month = (today - relativedelta(months=i)).replace(day=1)
        end_of_month = (start_of_month + relativedelta(months=1)) - relativedelta(days=1)

        # O ay içerisindeki giderleri al
        total_payment = Gider_Bilgisi.objects.filter(
            fatura_tarihi__gte=start_of_month,
            fatura_tarihi__lte=end_of_month,
            gelir_kime_ait_oldugu=customuser,
            silinme_bilgisi=False
        ).aggregate(total=Sum('kalan_tutar'))['total'] or 0

        # Ayın adını çevir
        ay_adi = start_of_month.strftime('%Y-%m')
        ay_adlari = {
            '01': _('January'),
            '02': _('February'),
            '03': _('March'),
            '04': _('April'),
            '05': _('May'),
            '06': _('June'),
            '07': _('July'),
            '08': _('August'),
            '09': _('September'),
            '10': _('October'),
            '11': _('November'),
            '12': _('December')
        }

        ay_kod = start_of_month.strftime('%m')
        ay_isim = f"{start_of_month.strftime('%Y')} {ay_adlari.get(ay_kod, 'Unknown')}"
        
        # Listeye ekle
        tutarlar.append(round(total_payment, 2))
        aylar.append(ay_isim)

    return {"aylar": aylar, "tutarlar": tutarlar}


@register.simple_tag
def odeme_para_birimi(bilgi2):
    para_birimi = calisan_maas_durumlari.objects.filter(calisan = bilgi2).last()
    return para_birimi.para_birimi
@register.simple_tag
def odeme_para_birimii(bilgi2):
    para_birimi = calisan_maas_durumlari.objects.filter(calisan = bilgi2).last()
    if para_birimi.para_birimi:
        return  "1"
    return "0"

@register.simple_tag
def maaslari_getirme(bilgi2):
    para_birimi = calisan_maas_durumlari.objects.filter(calisan = bilgi2).last()
    mesai_tutari  = faturalar_icin_bilgiler.objects.filter(gelir_kime_ait_oldugu = bilgi2.calisan_kime_ait).last()
    return {"saatlik": para_birimi.maas/mesai_tutari.gunluk_calisma_saati ,"fazla_mesai":para_birimi.yevmiye}
@register.simple_tag
def odeme_para_birimi_hesabi(bilgi2,kur,tutar):
    para_birimi = calisan_maas_durumlari.objects.filter(calisan = bilgi2).last()
    if para_birimi.para_birimi:
        veri = tutar
    else:
        veri = tutar/kur
    return veri

@register.simple_tag
def odeme_para_birimi_hesabi_deger(bilgi2,kur,tutar):
    para_birimi = calisan_maas_durumlari.objects.filter(calisan = bilgi2).last()

    if para_birimi.para_birimi:
        veri = tutar*kur
    else:
        veri = tutar
    return veri

from operator import attrgetter
from django.utils.timezone import now
from itertools import chain
@register.simple_tag
def bildirimler(kul):
    bil_gelir = Gelir_Bilgisi.objects.filter(silinme_bilgisi = False,gelir_kime_ait_oldugu=kul, kalan_tutar__gt=0, vade_tarihi__lt=now())
    bil_gider = Gider_Bilgisi.objects.filter(silinme_bilgisi = False,gelir_kime_ait_oldugu=kul, kalan_tutar__gt=0, vade_tarihi__lt=now())
    bil_urun_talebi = urun_talepleri.objects.filter(talebin_ait_oldugu=kul, talep_durumu="1").order_by("-kayit_tarihi")
    bil_IsplaniPlanlari = IsplaniPlanlari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi=kul).exclude(status="Completed")
    
    combined_list = list(chain(bil_gelir, bil_gider, bil_urun_talebi, bil_IsplaniPlanlari))
    sorted_list = sorted(combined_list, key=attrgetter('kayit_tarihi', 'id'), reverse=True)[:20]
    
    # Verilere model tipini ekle
    for item in sorted_list:
        if isinstance(item, Gelir_Bilgisi):
            item.type = 'Gelir'
        elif isinstance(item, Gider_Bilgisi):
            item.type = 'Gider'
        elif isinstance(item, urun_talepleri):
            item.type = 'UrunTalebi'
        elif isinstance(item, IsplaniPlanlari):
            item.type = 'IsplaniPlan'
    
    return sorted_list


from operator import attrgetter
from django.utils.timezone import now
from itertools import chain
@register.simple_tag
def bildirimler_tumu(kul):
    bil_gelir = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu=kul, kalan_tutar__gt=0, vade_tarihi__lt=now())
    bil_gider = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu=kul, kalan_tutar__gt=0, vade_tarihi__lt=now())
    bil_urun_talebi = urun_talepleri.objects.filter(talebin_ait_oldugu=kul, talep_durumu="1").order_by("-kayit_tarihi")
    bil_IsplaniPlanlari = IsplaniPlanlari.objects.filter(proje_ait_bilgisi=kul).exclude(status="Completed")
    
    combined_list = list(chain(bil_gelir, bil_gider, bil_urun_talebi, bil_IsplaniPlanlari))
    sorted_list = sorted(combined_list, key=attrgetter('kayit_tarihi', 'id'), reverse=True)
    
    # Verilere model tipini ekle
    for item in sorted_list:
        if isinstance(item, Gelir_Bilgisi):
            item.type = 'Gelir'
        elif isinstance(item, Gider_Bilgisi):
            item.type = 'Gider'
        elif isinstance(item, urun_talepleri):
            item.type = 'UrunTalebi'
        elif isinstance(item, IsplaniPlanlari):
            item.type = 'IsplaniPlan'
    
    return sorted_list


@register.simple_tag
def grup_kullanici_ayrimi(grup_id, kullanici):
    # Grup nesnesini al
    grup = get_object_or_404(Group, id=grup_id)

    # Kullanıcı grup adında var mı kontrol et
    if kullanici.username in grup.name:
        # Grup üyelerini kontrol et
        for member in grup.members.all():
            if kullanici.username != member.username:
                if member.image:
                   return {"isim":member.last_name ,"resim":member.image.url  } 
                else:
                    return {"isim":member.last_name ,"resim":"1"} 
    else:
        if grup.image:
            return {"isim":grup.name ,"resim":grup.image.url } 
        else:
            return {"isim":grup.name ,"resim":"0" } 

@register.simple_tag
def sonmesaj(grup_id):
    # Grup nesnesini al
    grup = get_object_or_404(Group, id=grup_id)
    mes = Message.objects.filter(group = grup).order_by("-timestamp").last()
    # Kullanıcı grup adında var mı kontrol et
    if mes:
        return mes.content
    else:
        return "" 

@register.simple_tag
def blok_bilgileri(users):
    bilgi = []
    bilgiler=bloglar.objects.filter(proje_ait_bilgisi = users,proje_santiye_Ait__silinme_bilgisi = False)
    for  i in bilgiler:
        try:
            gorsel = i.proje_santiye_Ait.bina_goruntuleri_aitlik.id
        except:
            gorsel = ""
        bilgi.append({"id":i.id,"yapi":i.blog_adi,"kat":int(i.kat_sayisi),"gorseli":gorsel})
    return bilgi
@register.simple_tag
def blok_bilgilerii(users):
    bilgi = []
    bilgiler = bloglar.objects.filter(proje_ait_bilgisi=users, proje_santiye_Ait__silinme_bilgisi=False)
    for i in bilgiler:
        try:
            gorsel = i.proje_santiye_Ait.bina_goruntuleri_aitlik.id
        except:
            gorsel = ""
        bilgi.append({"id": i.id, "yapi": i.blog_adi, "kat": int(i.kat_sayisi),"gorseli":gorsel})
    
    # Python nesnesini JSON'a dönüştür ve güvenli hale getir
    json_data = json.dumps(bilgi)
    return mark_safe(json_data)  # Güvenli JSON verisini döndür
@register.simple_tag
def bina_3d(veri):
    try:
        katlar = []
        katlar_modasl = []
        bina_kat_sayisi = veri.blok.kat_sayisi
        gor_olan_katlar = IsplaniPlanlari.objects.filter(blok = veri.blok).exclude(status = "Completed")
        for i in gor_olan_katlar:
            a = "Kat " + str(i.kat)
            katlar.append(a)
            katlar_modasl.append(i.kat)
    
        return {"kat_gonder":katlar_modasl,"kat_sayisi" : int(bina_kat_sayisi),"kat_bilgileri":katlar,"gorevler":gor_olan_katlar}
    except:
        return {"kat_sayisi" : int(20)}
@register.simple_tag
def bina_3d2(veri):
    
    try:
        blok = get_object_or_404(bloglar,id = veri)
        print(blok)
        katlar = []
        katlar_modasl = []
        bina_kat_sayisi = blok.kat_sayisi
        gor_olan_katlar = IsplaniPlanlari.objects.filter(blok= get_object_or_404(bloglar,id = veri) ).exclude(status = "Completed",blok = None )
        for i in gor_olan_katlar:
            a = "Kat " + str(i.kat)+"-"+str(blok.id)
            katlar.append(a)
            katlar_modasl.append(i.kat)
            #print({"kat_gonder":katlar_modasl,"kat_sayisi" : int(bina_kat_sayisi),"kat_bilgileri":katlar,"gorevler":gor_olan_katlar})
        return {"kat_gonder":katlar_modasl,"kat_sayisi" : int(bina_kat_sayisi),"kat_bilgileri":katlar,"gorevler":gor_olan_katlar}
    except:
        return {"kat_sayisi" : int(20)}
    
@register.simple_tag
def saatlik_ucret_hesabi(users):
    bilgi = faturalar_icin_bilgiler.objects.filter(gelir_kime_ait_oldugu  = users).last()
    return bilgi.gunluk_calisma_saati
@register.simple_tag
def hava_durumu_gonder(users):
    bilgi = genel_hava_durumu.objects.filter(proje_ait_bilgisi  = users).last()
    return bilgi


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@register.simple_tag(takes_context=True)
def show_content_for_country(context, country_code):
    """
    Belirli bir ülke kodu için içeriği gösterir.
    :param context: Django template context
    :param country_code: İçeriğin gösterilmesi gereken ülke kodu (örneğin 'TR' için Türkiye)
    :return: Eğer kullanıcının IP adresi belirli ülke koduyla eşleşiyorsa True döner
    """
    request = context['request']
    ip = get_client_ip(request)
    g = GeoIP2()
    try:
        location = g.city(ip)
        user_country_code = location['country_code']
        return user_country_code == country_code
    except Exception:
        return False
    
from geopy.geocoders import Nominatim
@register.simple_tag
def get_city_from_lat_lon(lat, lon):
    import requests
    api_key = 'dee0661903df4f2c76ccfd8afab8be69'
    weather_api_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}'
                
    weather_response = requests.get(weather_api_url)
    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        a = weather_data["weather"][0]
        return weather_data["name"]
    

@register.simple_tag
def atanan_musteri_sayisi(daire):
    bilgi = musteri_daire_baglama.objects.filter(daire = daire).count()
    return bilgi

@register.simple_tag
def musteriye_atanan_daire(musterisi):
    bilgi = musteri_daire_baglama.objects.filter(musterisi = musterisi).count()
    return bilgi
@register.simple_tag
def musteriye_atanan_daire_teslim_edilen(musterisi):
    bilgi = musteri_daire_baglama.objects.filter(musterisi = musterisi,durum ="1").count()
    return bilgi