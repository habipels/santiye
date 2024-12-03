from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from users.models import *
from django.contrib.auth.models import User
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from django.db.models.query_utils import Q
from site_settings.models import *
from django.utils.translation  import gettext as _
from django.utils.translation import get_language, activate, gettext
from site_info.models import *
from muhasebe.models import *
from django.contrib.admin.models import LogEntry
from hashids import Hashids
from django.middleware.csrf import get_token
from django.http import JsonResponse
import requests
from main.views import sozluk_yapisi ,get_object_or_none

def crm_dashboard(request):
    content = sozluk_yapisi()
    return render(request,"crm/crm-dashboard.html",content)

def crm_dairedetayi(request):
    content = sozluk_yapisi()
    return render(request,"crm/crm-daire-detay.html",content)
def get_bloglar(request):
    santiye_id = request.GET.get('santiye_id')
    if santiye_id:
        blog_list = bloglar.objects.filter(proje_santiye_Ait_id=santiye_id).values('id', 'blog_adi')
        return JsonResponse(list(blog_list), safe=False)

    return JsonResponse({'error': 'Şantiye bulunamadı'}, status=400)
def get_katlar(request):
    blok_id = request.GET.get('blok_id')
    if blok_id:
        kat_sayisi = bloglar.objects.filter(id=blok_id).values_list('kat_sayisi', flat=True).first()
        if kat_sayisi:
            katlar = [{"id": i, "kat_adi": f"{i}. Kat"} for i in range(1, int(kat_sayisi) + 1)]
            return JsonResponse(katlar, safe=False)
    return JsonResponse({'error': 'Blok bulunamadı veya kat bilgisi yok'}, status=400)

def crm_daireyonetimi(request):
    content = sozluk_yapisi()
    content["daireler"]  = daire_bilgisi.objects.filter(daire_kime_ait = request.user)
    content["santiyeler"] = santiye.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    content["bloglar"] = bloglar.objects.filter(proje_ait_bilgisi = request.user,proje_santiye_Ait__silinme_bilgisi = False)
    print(daire_bilgisi.objects.filter(daire_kime_ait = request.user))
    return render(request,"crm/crm-daire-yonetimi.html",content)
def daire_ekle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        santiye_bilgisi = request.POST.get("santiye")
        blok = request.POST.get("blok")
        kat = request.POST.get("kat")
        daire_no = request.POST.get("daire_no")
        oda_Sayisi = request.POST.get("oda_Sayisi")
        metrekare = request.POST.get("metrekare")
        daire_bilgisi.objects.create(daire_kime_ait = kullanici,blog_bilgisi = get_object_or_none(bloglar,id = blok),kat =kat,
         daire_no = daire_no,oda_sayisi = oda_Sayisi,
        metre_kare_brut = metrekare )
        return redirect("crm:crm_daireyonetimi")
def crm_evr(request):
    content = sozluk_yapisi()
    return render(request,"crm/crm-evrak-ve-dokuman-detay.html",content)
def crm_evrak_dokuman(request):
    content = sozluk_yapisi()
    return render(request,"crm/crm-evrak-ve-dokuman.html",content)

def crm_musteri_detayi(request):
    content = sozluk_yapisi()
    return render(request,"crm/musteri-detay.html",content)

def musteri_sayfasi(request):
    content = sozluk_yapisi()
    content["musteriler"] = musteri_bilgisi.objects.filter(musteri_kime_ait = request.user )
    return render(request,"crm/musteri-yonetimi.html",content)
def musteri_ekleme(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        musteri_adi = request.POST.get("musteri_adi")
        musteri_soyadi = request.POST.get("musteri_soyadi")
        musteri_bilgisi.objects.create(musteri_kime_ait = kullanici,musteri_adi = musteri_adi , musteri_soyadi =musteri_soyadi )
    return redirect("crm:musteri_sayfasi")
def musteri_silme(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        buttonId = request.POST.get("buttonId")
        
        musteri_bilgisi.objects.filter(id =buttonId ).delete()
    return redirect("crm:musteri_sayfasi")
def musteri_duzenleme(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        buttonId = request.POST.get("buttonId")
        musteri_adi = request.POST.get("musteri_adi")
        musteri_soyadi = request.POST.get("musteri_soyadi")
        musteri_bilgisi.objects.filter(id = buttonId,musteri_kime_ait = kullanici).update(musteri_kime_ait = kullanici,musteri_adi = musteri_adi , musteri_soyadi =musteri_soyadi )
    return redirect("crm:musteri_sayfasi")
def crm_talepler_sikayetler(request):
    content = sozluk_yapisi()
    return render(request,"crm/talep-ve-sikayetler.html",content)

def crm_teklif_olustur(request):
    content = sozluk_yapisi()
    return render(request,"crm/teklif-olustur.html",content)

def crm_teklif_yonetimi(request):
    content = sozluk_yapisi()
    return render(request,"crm/teklif-yonetimi.html",content)