from django import template 
from django.utils.safestring import mark_safe
from site_info.models import *
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
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