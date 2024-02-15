from django import template 
from django.utils.safestring import mark_safe
from site_info.models import *
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from site_settings.models import *
register = template.Library()

#@register.filter
@register.simple_tag
def to_int(veri):
    return int(veri)

@register.simple_tag
def bloglar_getir(veri):
    deger = bloglar.objects.filter(proje_santiye_Ait = veri)
    veri_esiti = ""
    for i in  deger:
        veri_esiti = veri_esiti + str(i.blog_adi)+str(i.blog_numarasi)+" ,"
    return str(veri_esiti)


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
def taseron_gorev_saysisi(id):
    a = get_object_or_404(taseronlar,id = id)
    a = a.proje_bilgisi.all().count()

    return a

    
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
    a = klasor_dosyalari.objects.filter(dosya_sahibi__id = id)
    for  i in a:
        boyut = boyut+ i.dosya.size
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
        boyut = boyut+ i.dosya.size
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
        return mark_safe(k)
    elif 5 > boyut:
        k = """<button class="btn btn-success w-sm create-folder-modal flex-shrink-0" data-bs-toggle="modal" data-bs-target="#dosyaekle"><i class="ri-add-line align-bottom me-1"></i> Dosya Ekle</button>"""
        return mark_safe(k)
@register.simple_tag
def mb_donusturme(id):
    id  = id /1024
    id = id /1024
    return round(float(id),2)

@register.simple_tag
def dosya_sayisi_ve_boyutu (id):
    
    klasor_sayisi = klasorler.objects.filter(klasor_adi_db__id=id).count()
    dosya_sayisi =  klasor_dosyalari.objects.filter(proje_ait_bilgisi__id=id).count()
    dosya_boyutu  = 0
    z = klasor_dosyalari.objects.filter(proje_ait_bilgisi__id=id)
    for i in z:
        dosya_boyutu = dosya_boyutu+i.dosya.size
    dosya_boyutu = ((dosya_boyutu/1024)/1024)/1024
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
        bilgiler = bilgiler+ '<a href="/delbuldingsites/{}/{}" >{}{}</a>'.format(str(i.id),id,str(i.blog_adi),str(i.blog_numarasi))+" , "
    return mark_safe(bilgiler)


@register.simple_tag

def blogtan_kaleme_ilerleme(id):
    a = ""
    blog_bilgis = bloglar.objects.filter(proje_santiye_Ait__id=id)
    for i in blog_bilgis:
        a = a+'<a style="padding:2px !important;margin:0px 2px 0px 0px!important;" class="btn btn-info " href="progresstracking/progress/{}/{}" >{}</a>'.format(str(i.id),str(i.blog_adi)+str(i.blog_numarasi),str(i.blog_adi)+str(i.blog_numarasi))
    return mark_safe(a)

@register.simple_tag
def kat_sirala(id):
    a = ""
    b = get_object_or_404(santiye,id = id).kat_sayisi
    b= int(b)
    for i in range(1,b+1):
        a = a+'<th class="text-uppercase" data-sort="{}">{}</th>'.format(i,i)
    return mark_safe(a)
@register.simple_tag
def ckboxlar(id,kalem):
    bilgi = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id,kalem_bilgisi__id =kalem).order_by("kat")
    a = ""
    for i in bilgi:
        if i.tamamlanma_bilgisi:
            a = a+'<td class="kat"><input checked type="checkbox" name="kalem" value="{}" ></td>'.format(str(i.id))
        else:
            a = a+'<td class="kat"><input  type="checkbox" name="kalem" value="{}" ></td>'.format(str(i.id))
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
    a = faturalardaki_gelir_gider_etiketi.objects.last().gelir_etiketi+(c*"0")+a
    return a
@register.simple_tag
def gider_faturasi_no(id):
    a = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu__id = id).count()
    a = a+1
    a = str(a)
    b = len(a)
    c = 8 - b
    a = faturalardaki_gelir_gider_etiketi.objects.last().gider_etiketi+(c*"0")+a
    return a
from datetime import datetime

@register.simple_tag
def saat_bilgisi():
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
    veri = IsplaniDosyalari.objects.filter(proje_ait_bilgisi__id = id)
    for i in veri:
        k = str(i.dosya.url).split("/")
        k = k[ -1]
        
        z = z+ '<div class="d-flex border border-dashed p-2 rounded position-relative"><div class="flex-shrink-0 avatar-xs"><div class="avatar-title bg-info-subtle text-info fs-15 rounded"><i class="ri-file-zip-line"></i></div></div><div class="flex-grow-1 overflow-hidden ms-2"><h6 class="text-truncate mb-0"><a href="{}" download class="stretched-link">{}</a></h6><small>{} KB</small></div></div>'.format(i.dosya.url,k,round(float(i.dosya.size/1024),2))
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
        k = str(i.dosya.url).split("/")
        k = k[ -1]
        
        z = z+ '<div class="d-flex border border-dashed p-2 rounded position-relative"><div class="flex-shrink-0 avatar-xs"><div class="avatar-title bg-info-subtle text-info fs-15 rounded"><i class="ri-file-zip-line"></i></div></div><div class="flex-grow-1 overflow-hidden ms-2"><h6 class="text-truncate mb-0"><a href="{}" download class="stretched-link">{}</a></h6><small>{} KB</small></div></div>'.format(i.dosya.url,k,round(float(i.dosya.size/1024),2))
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
    return round(float(genel_toplam - toplam-indirim),2)
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
    return round(float(genel_toplam - toplam -indirim),2)
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
    d = Gelir_odemesi.objects.filter(gelir_kime_ait_oldugu__id = b.id).order_by("tarihi")

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
    return round(float(gelir_toplami-gider_odemesi),2)
@register.simple_tag
def cikarma(a,b):
    y = float(a)+float(b)
    return round(float(y),2)


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
    return round(float(gelir_toplami-gider_odemesi),2)
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
        d = Gider_odemesi.objects.filter(gelir_kime_ait_oldugu__id = i.id)
        for j in d:
            gider_odemesi = gider_odemesi+j.tutar
    gider_bilgisi = gider_toplami-gider_odemesi
    for i in a:
        c = gelir_urun_bilgisi.objects.filter(gider_bilgis__id  =  i.id)
        for j in c:
            gelir_toplami = gelir_toplami + (j.urun_fiyati*j.urun_adeti) - j.urun_indirimi
        d = Gelir_odemesi.objects.filter(gelir_kime_ait_oldugu__id = i.id)
        for j in d:
            gelir_odemesi = gelir_odemesi+j.tutar
    gelir_bilgisi = gelir_toplami - gelir_odemesi
    sonuc = gelir_bilgisi - gider_bilgisi
    return {"gelir_bilgisi":gelir_bilgisi,"gider_bilgisi":gider_bilgisi,"sonuc":round(sonuc,2),"b":b,"a":a}
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import hashlib

"""@register.simple_tag
def generate_token(object_id):
    hash_input = force_bytes(object_id)
    hash_value = hashlib.sha256(hash_input).digest()
    return urlsafe_base64_encode(hash_value)"""

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