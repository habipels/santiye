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
from django.core.files.storage import FileSystemStorage
from site_info.models import daire_evraklari
from functools import reduce
import operator
import os
from main.views import decode_id
from main.views import super_admin_kontrolu,dil_bilgisi,translate,sozluk_yapisi,yetki,get_kayit_tarihi_from_request,get_time_zone_from_country,get_country
from django.urls import reverse

def redirect_with_language(view_name, *args, **kwargs):
    lang = get_language()
    url = reverse(view_name, args=args, kwargs=kwargs)
    return redirect(f'/{lang}{url}')

def musteri_bilgisi_views(request):
    term = request.GET.get('term', '')
    if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.gelir_faturasi_kesme_izni or a.izinler.gider_faturasi_kesme_izni:
                    user = request.user.kullanicilar_db
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                return redirect_with_language("main:yetkisiz")
    else:
        user = request.user
    results = musteri_bilgisi.objects.filter(musteri_adi__icontains=term, musteri_kime_ait=user)
    suggestions = [{'label': result.musteri_adi +" "+result.musteri_soyadi , 'value':result.musteri_telefon_numarasi,
                    "adi" :result.musteri_adi , "soyadi": result.musteri_soyadi } for result in results]
    return JsonResponse(suggestions, safe=False)
def crm_dashboard(request):
    content = sozluk_yapisi()
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar, kullanicilar=request.user)
        if a:
            if a.izinler.crm_musteri_gorme:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else:
        kullanici = request.user

    content["toplam_daire"] = daire_bilgisi.objects.filter(daire_kime_ait=kullanici).count()
    content["atanan_daire"] = musteri_daire_baglama.objects.filter(baglama_kime_ait=kullanici, durum="1").count()
    content["atanmamis_daire"] = content["toplam_daire"] - content["atanan_daire"]
    content["acik_talep"] = talep_ve_sikayet.objects.filter(sikayet_kime_ait=kullanici, talep_sikayet_ayrimi="0", durum="0",silinme_bilgisi = False).count()
    content["acik_sikayet"] = talep_ve_sikayet.objects.filter(sikayet_kime_ait=kullanici, talep_sikayet_ayrimi="1", durum="0",silinme_bilgisi = False).count()
    content["beklemedeki_teklifler"] = teklifler.objects.filter(teklif_kime_ait=kullanici, durum="0").count()
    content["toplam_musteri"] = musteri_bilgisi.objects.filter(musteri_kime_ait=kullanici).count()
    content["daireler"] = daire_bilgisi.objects.filter(daire_kime_ait=kullanici)
    content["talepler"] = talep_ve_sikayet.objects.filter(sikayet_kime_ait=kullanici, talep_sikayet_ayrimi="0",silinme_bilgisi = False)
    content["sikayetler"] = talep_ve_sikayet.objects.filter(sikayet_kime_ait=kullanici, talep_sikayet_ayrimi="1",silinme_bilgisi = False)

    # Document statistics
    image_files = daire_evraklari.objects.filter(evrak_kime_ait=kullanici, evrak__iregex=r'\.(jpg|jpeg|png|gif|webp)$')
    media_files = daire_evraklari.objects.filter(evrak_kime_ait=kullanici, evrak__iregex=r'\.(mp4|avi|mov|wmv)$')
    other_files = daire_evraklari.objects.filter(evrak_kime_ait=kullanici).exclude(evrak__iregex=r'\.(jpg|jpeg|png|gif|webp|mp4|avi|mov|wmv)$')

    content["total_documents"] = image_files.count() + media_files.count() + other_files.count()
    content["image_documents"] = image_files.count()
    content["media_documents"] = media_files.count()
    content["other_documents"] = other_files.count()
    
    content["image_size"] = sum([file.evrak.size for file in image_files]) / (1024 * 1024)  # size in MB
    content["media_size"] = sum([file.evrak.size for file in media_files]) / (1024 * 1024)  # size in MB
    content["other_size"] = sum([file.evrak.size for file in other_files]) / (1024 * 1024)  # size in MB

    return render(request, "crm/crm-dashboard.html", content)

def crm_dairedetayi(request, id):
    content = sozluk_yapisi()
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar, kullanicilar=request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else:
        kullanici = request.user

    daire = get_object_or_none(daire_bilgisi, id=id, daire_kime_ait=kullanici)
    content["daire_detayi"] = daire
    content["daire_evraklari"] = daire_evraklari.objects.filter(daire=daire, evrak_kime_ait=kullanici)
    content["talepler"] = talep_ve_sikayet.objects.filter(daire=daire, sikayet_kime_ait=kullanici, talep_sikayet_ayrimi="0")
    content["sikayetler"] = talep_ve_sikayet.objects.filter(daire=daire, sikayet_kime_ait=kullanici, talep_sikayet_ayrimi="1")
    content["atanan_musteri"] = get_object_or_none(musteri_daire_baglama, daire=daire, durum="1")
    dosya_turu = [".jpg", ".jpeg", ".png", ".ico", ".css", ".JFIF", ".GIF", ".WEBP"]
    content["image_extensions"] = daire_evraklari.objects.filter(daire=daire, evrak_kime_ait=kullanici).filter(reduce(operator.or_, (Q(evrak__icontains=x) for x in dosya_turu)))
    content["birinci_resim"] = daire_evraklari.objects.filter(daire=daire, evrak_kime_ait=kullanici).filter(reduce(operator.or_, (Q(evrak__icontains=x) for x in dosya_turu))).first()
    content["musteriler"] = musteri_bilgisi.objects.filter(musteri_kime_ait=kullanici)
    content["bloglar"] = bloglar.objects.filter(proje_ait_bilgisi=kullanici, proje_santiye_Ait__silinme_bilgisi=False)
    return render(request, "crm/crm-daire-detay.html", content)

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
def get_daireler(request):
    blok_id = request.GET.get('blok_id')
    kat_bilgisi = request.GET.get("kat")
    if blok_id and kat_bilgisi:
        daireler  = daire_bilgisi.objects.filter(blog_bilgisi__id = blok_id , kat = kat_bilgisi)
        if daireler:
            daireler = [{"id": i.id, "daire_adi": f"{i.daire_no}"} for i in daireler]
            print(daireler)
            return JsonResponse(daireler, safe=False)
    return JsonResponse({'error': 'Blok bulunamadı veya kat bilgisi yok'}, status=400)
def crm_daireyonetimi(request):
    content = sozluk_yapisi()
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar, kullanicilar=request.user)
        if a:
            if a.izinler.crm_daire_gorme:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else:
        kullanici = request.user
    content["daireler"]  = daire_bilgisi.objects.filter(daire_kime_ait = request.user)
    content["santiyeler"] = santiye.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    content["bloglar"] = bloglar.objects.filter(proje_ait_bilgisi = request.user,proje_santiye_Ait__silinme_bilgisi = False)
    print(daire_bilgisi.objects.filter(daire_kime_ait = request.user))
    return render(request,"crm/crm-daire-yonetimi.html",content)
def daire_ekle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.crm_daire_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        santiye_bilgisi = request.POST.get("santiye")
        blok = request.POST.get("blok")
        kat = request.POST.get("kat")
        daire_no = request.POST.get("daire_no")
        oda_Sayisi = request.POST.get("oda_Sayisi")
        metrekare = request.POST.get("metrekare")
        daire_bilgisi.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),daire_kime_ait = kullanici,blog_bilgisi = get_object_or_none(bloglar,id = blok),kat =kat,
         daire_no = daire_no,oda_sayisi = oda_Sayisi,
        metre_kare_brut = metrekare )
        return redirect_with_language("crm:crm_daireyonetimi")
def crm_evr(request):
    content = sozluk_yapisi()
    return render(request,"crm/crm-evrak-ve-dokuman-detay.html",content)
def crm_evrak_dokuman(request):
    content = sozluk_yapisi()
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar, kullanicilar=request.user)
        if a:
            if a.izinler.crm_evrak_gorme:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else:
        kullanici = request.user

    content["daireler"] = daire_bilgisi.objects.filter(daire_kime_ait=kullanici)
    return render(request, "crm/crm-evrak-ve-dokuman.html", content)

def crm_musteri_detayi(request, id):
    content = sozluk_yapisi()
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar, kullanicilar=request.user)
        if a:
            if a.izinler.crm_musteri_gorme:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else:
        kullanici = request.user

    musteri = get_object_or_none(musteri_bilgisi, id=id, musteri_kime_ait=kullanici)
    content["musteri_detayi"] = musteri
    content["bloglar"] = bloglar.objects.filter(proje_ait_bilgisi=kullanici, proje_santiye_Ait__silinme_bilgisi=False)
    content["santiyeler"] = santiye.objects.filter(proje_ait_bilgisi=kullanici, silinme_bilgisi=False)
    content["musteri_daireleri"] = musteri_daire_baglama.objects.filter(baglama_kime_ait=kullanici, musterisi=musteri)
    content["talepler"] = talep_ve_sikayet.objects.filter(musteri=musteri, sikayet_kime_ait=kullanici, talep_sikayet_ayrimi="0", silinme_bilgisi=False)
    content["sikayetler"] = talep_ve_sikayet.objects.filter(musteri=musteri, sikayet_kime_ait=kullanici, talep_sikayet_ayrimi="1", silinme_bilgisi=False)
    content["musteri_gorusme_notu"] = musteri_notlari.objects.filter(kime_ait=kullanici, musterisi=musteri, silinme_bilgisi=False)
    content["teklifler"] = teklifler.objects.filter(musterisi=musteri)
    content["musteri_evraklari"] = musteri_evraklari.objects.filter(musterisi=musteri, silinme_bilgisi=False)

    return render(request, "crm/musteri-detay.html", content)

def daire_musteriye_ata(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.crm_daire_duzenleme:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        musteri = request.POST.get("musteri")
        blok = request.POST.get("blok")
        kat = request.POST.get("kat")
        daire = request.POST.get("daire")
        musteri_sec = get_object_or_none(musteri_bilgisi,musteri_kime_ait = kullanici,id = musteri)
        daire = get_object_or_none(daire_bilgisi,id = daire,daire_kime_ait = kullanici,kat = kat,blog_bilgisi__id =blok)
        if musteri_sec and daire:
            if get_object_or_none(musteri_daire_baglama,baglama_kime_ait = kullanici,musterisi = musteri_sec,
                                                 daire = daire):
                pass
            else:
                musteri_daire_baglama.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),baglama_kime_ait = kullanici,musterisi = musteri_sec,
                                                    daire = daire)
    return redirect_with_language("crm:crm_musteri_detayi",musteri)
def daire_musteriye_duzenle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.crm_daire_duzenleme:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        duzenle = request.POST.get("duzenle")
        musteri = request.POST.get("musteri")
        blok = request.POST.get("blok")
        kat = request.POST.get("kat")
        daire = request.POST.get("daire")
        musteri_sec = get_object_or_none(musteri_bilgisi,musteri_kime_ait = kullanici,id = musteri)
        daire = get_object_or_none(daire_bilgisi,id = daire,daire_kime_ait = kullanici,kat = kat,blog_bilgisi__id =blok)
        if musteri_sec and daire:
            if get_object_or_none(musteri_daire_baglama,baglama_kime_ait = kullanici,musterisi = musteri_sec,
                                                 daire = daire):
                pass
            else:
                musteri_daire_baglama.objects.filter(id =duzenle ).update(baglama_kime_ait = kullanici,musterisi = musteri_sec,
                                                    daire = daire)
    return redirect_with_language("crm:crm_musteri_detayi",musteri)
def daire_musteriye_sil(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.crm_daire_silme:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        duzenle = request.POST.get("buttonId")
        musteri = request.POST.get("musteri")

        musteri_daire_baglama.objects.filter(id =duzenle ).delete()
    return redirect_with_language("crm:crm_musteri_detayi",musteri)
def daire_musteriye_onayla(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        duzenle = request.POST.get("buttonId")
        musteri = request.POST.get("musteri")

        
        daire = get_object_or_404(musteri_daire_baglama,id = duzenle)
        musteri_daire_baglama.objects.filter(daire =daire.daire ).update(durum = "2")
        musteri_daire_baglama.objects.filter(id =duzenle ).update(durum = "1")
    return redirect_with_language("crm:crm_musteri_detayi",musteri)
def museri_notu_ekle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        musteri = request.POST.get("musteri")
        tarih = request.POST.get("tarih")
        not_basligi = request.POST.get("not_basligi")
        aciklama = request.POST.get("aciklama")
        musteri_sec = get_object_or_none(musteri_bilgisi,musteri_kime_ait = kullanici,id = musteri)
        musteri_notlari.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),
            kime_ait = kullanici,
            musterisi = musteri_sec,
            not_basligi = not_basligi,
            not_aciklamasi = aciklama,
            not_tarihi = tarih
        )
    
        return redirect_with_language("crm:crm_musteri_detayi",musteri)

def musteri_notu_sil(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar, kullanicilar=request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else:
        kullanici = request.user

    if request.POST:
        not_id = request.POST.get("not_id")
        musteri = request.POST.get("musteri")
        musteri_notlari.objects.filter(id=not_id).delete()
    return redirect_with_language("crm:crm_musteri_detayi", musteri)

def musteri_notu_duzenle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar, kullanicilar=request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else:
        kullanici = request.user

    if request.POST:
        not_id = request.POST.get("not_id")
        musteri = request.POST.get("musteri")
        not_basligi = request.POST.get("not_basligi")
        aciklama = request.POST.get("aciklama")
        tarih = request.POST.get("tarih")
        musteri_notlari.objects.filter(id=not_id).update(
            not_basligi=not_basligi,
            not_aciklamasi=aciklama,
            not_tarihi=tarih
        )
    return redirect_with_language("crm:crm_musteri_detayi", musteri)

def talep_veya_sikayet_duzenle_musteri_detayi(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        talep_id = request.POST.get("talep_id")
        tur = request.POST.get("tur")
        talep_nedeni = request.POST.get("talep_nedeni")
        aciklama = request.POST.get("aciklama")
        musteri = request.POST.get("musteri")
        daireler = request.POST.get("daireler")
        talep_ve_sikayet.objects.filter(id = talep_id).update(
            sikayet_kime_ait = kullanici,
            sikayet_nedeni = talep_nedeni,
            talep_sikayet_ayrimi = tur,
            sikayet_aciklamasi = aciklama,
            daire = get_object_or_none(daire_bilgisi,id = daireler),
            musteri = get_object_or_none(musteri_bilgisi , id = musteri)
        )
    return redirect_with_language("crm:crm_musteri_detayi",musteri)


def talep_veya_sikayet_olustur_musteri_detayi(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        tur = request.POST.get("tur")
        talep_nedeni = request.POST.get("talep_nedeni")
        aciklama = request.POST.get("aciklama")
        musteri = request.POST.get("musteri")
        daireler = request.POST.get("daireler")
        talep_ve_sikayet.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),
            sikayet_kime_ait = kullanici,
            sikayet_nedeni = talep_nedeni,
            talep_sikayet_ayrimi = tur,
            sikayet_aciklamasi = aciklama,
            daire = get_object_or_none(daire_bilgisi,id = daireler),
            musteri = get_object_or_none(musteri_bilgisi , id = musteri)
        )
    return redirect_with_language("crm:crm_musteri_detayi",musteri)

def musteri_sayfasi(request):
    content = sozluk_yapisi()
    content["musteriler"] = musteri_bilgisi.objects.filter(musteri_kime_ait = request.user )
    return render(request,"crm/musteri-yonetimi.html",content)
def musteri_ekleme(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.crm_musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        musteri_adi = request.POST.get("musteri_adi")
        musteri_soyadi = request.POST.get("musteri_soyadi")
        musteri_telefon_numarasi = request.POST.get("musteri_telefon_numarasi")
        musteri_bilgisi.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),musteri_kime_ait = kullanici,musteri_adi = musteri_adi , musteri_soyadi =musteri_soyadi ,
                                       musteri_telefon_numarasi = musteri_telefon_numarasi)
    return redirect_with_language("crm:musteri_sayfasi")
def musteri_silme(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.crm_musteri_silme:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        buttonId = request.POST.get("buttonId")
        
        musteri_bilgisi.objects.filter(id =buttonId ).delete()
    return redirect_with_language("crm:musteri_sayfasi")
def musteri_duzenleme(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.crm_musteri_duzenleme:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        buttonId = request.POST.get("buttonId")
        musteri_adi = request.POST.get("musteri_adi")
        musteri_soyadi = request.POST.get("musteri_soyadi")
        musteri_bilgisi.objects.filter(id = buttonId,musteri_kime_ait = kullanici).update(musteri_kime_ait = kullanici,musteri_adi = musteri_adi , musteri_soyadi =musteri_soyadi )
    return redirect_with_language("crm:musteri_sayfasi")
def crm_talepler_sikayetler(request):
    content = sozluk_yapisi()
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    content["talepler"] = talep_ve_sikayet.objects.filter(sikayet_kime_ait = kullanici,talep_sikayet_ayrimi = "0",silinme_bilgisi = False)
    content["sikayetler"] = talep_ve_sikayet.objects.filter(sikayet_kime_ait = kullanici,talep_sikayet_ayrimi = "1",silinme_bilgisi = False)
    return render(request,"crm/talep-ve-sikayetler.html",content)
def get_talep(request):
    talep_id = request.GET.get('talep_id')
    talep =get_object_or_none(talep_ve_sikayet,id = talep_id)  
    daire_no = ""
    musteri = ""
    if talep.musteri:
        musteri = f"{talep.musteri.musteri_adi} {talep.musteri.musteri_soyadi}"
    if talep.daire:
        daire_no = talep.daire.daire_no
    veriler = {
        "id": talep.id, "musteri":  musteri,
        "daire" :daire_no,"durum" : talep.durum,
        "islem_tarihi" : talep.islem_tarihi,
        "sikayet_aciklamasi" :talep.sikayet_aciklamasi
    }
            
    return JsonResponse(veriler, safe=False)
    #return JsonResponse({'error': 'Blok bulunamadı veya kat bilgisi yok'}, status=400)
def talep_veya_sikayet_duzenle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        tur = request.POST.get("tur")
        talep_nedeni = request.POST.get("talep_nedeni")
        aciklama = request.POST.get("aciklama")
        talep_id = request.POST.get("talep_id")
        talep_ve_sikayet.objects.filter(id = talep_id).update(
            sikayet_kime_ait = kullanici,
            sikayet_nedeni = talep_nedeni,
            talep_sikayet_ayrimi = tur,
            sikayet_aciklamasi = aciklama
        )
    return redirect_with_language("crm:crm_talepler_sikayetler")
def talep_veya_sikayet_sil(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        talep_id = request.POST.get("buttonId")
        talep_ve_sikayet.objects.filter(id = talep_id).update(
            silinme_bilgisi = True
        )
    return redirect_with_language("crm:crm_talepler_sikayetler")
def talep_veya_sikayet_olustur(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.musteri_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        tur = request.POST.get("tur")
        talep_nedeni = request.POST.get("talep_nedeni")
        aciklama = request.POST.get("aciklama")

        talep_ve_sikayet.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),
            sikayet_kime_ait = kullanici,
            sikayet_nedeni = talep_nedeni,
            talep_sikayet_ayrimi = tur,
            sikayet_aciklamasi = aciklama
        )
    return redirect_with_language("crm:crm_talepler_sikayetler")
def crm_teklif_olustur(request):
    content = sozluk_yapisi()
    return render(request,"crm/teklif-olustur.html",content)

def crm_teklif_yonetimi(request):
    content = sozluk_yapisi()
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.crm_teklif_gorme:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    tekliff = teklifler.objects.filter(
            teklif_kime_ait = kullanici,
            
        )
    content["teklifler"] = tekliff
    return render(request,"crm/teklif-yonetimi.html",content)
def teklif_silme(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.crm_teklif_silme:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else : 
        kullanici = request.user
    if request.POST:
        teklif_id = request.POST.get("buttonId")
        teklifler.objects.filter(id = teklif_id).delete()
    return redirect_with_language("crm:crm_teklif_yonetimi")
def teklif_duzenleme(request,id):
    content = sozluk_yapisi()
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            kullanici = request.user.kullanicilar_db
        else:
            return redirect_with_language("main:yetkisiz")
    else : 
        kullanici = request.user
    
    
    tekif_bilgisi = get_object_or_none(teklifler,id = id)
    content["teklifler"] = tekif_bilgisi
    content["teklif_icerikleri"] = teklif_icerikleri.objects.filter(hangi_teklif = tekif_bilgisi)
    return render(request,"crm/teklif_duzenle.html",content)
def crm_teklif_olustur_gonder(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.crm_teklif_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
        
    else : 
        kullanici = request.user
    if request.POST:
        adsoyad = request.POST.get("adsoyad")
        soyad = request.POST.get("soyad")
        telefon = request.POST.get("telefon")
        Teklif_basligi = request.POST.get("Teklif_basligi")
        urun= request.POST.getlist("kalem-urun-hizmet-adi")
        aciklama= request.POST.getlist("kalem-aciklama")
        indirim= request.POST.getlist("kalem-indirim")
        miktar= request.POST.getlist("kalem-miktar")
        birim_fiyat= request.POST.getlist("kalem-birim-fiyati")
        toplam= request.POST.getlist("kalem-toplam")
        iqd= request.POST.getlist("kalem-toplam-iqd")
        
        musteri = get_object_or_none(musteri_bilgisi,musteri_kime_ait = kullanici,
                                     musteri_adi = adsoyad,
                                     musteri_soyadi = soyad,
                                     musteri_telefon_numarasi =telefon)
        if musteri:
            pass
        else:
            musteri = musteri_bilgisi.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),musteri_kime_ait = kullanici,
                                     musteri_adi = adsoyad,
                                     musteri_soyadi = soyad,
                                     musteri_telefon_numarasi =telefon
            )
        toplam_tutar = 0
       
        tekliff = teklifler.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),
                teklif_kime_ait = kullanici,
                teklif_basligi = Teklif_basligi,
                musterisi = musteri
            )
        for i in range(0,len(urun)):
            teklif_icerikleri.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),
                kime_ait = kullanici,
                hangi_teklif= tekliff,
                urun_hizmet = urun[i],
                urun_aciklama = aciklama[i],
                indirim = indirim[i],
                miktar = miktar[i],
                birim_fiyati = birim_fiyat[i],
                birim_fiyati_ıqd = iqd[i],
                genel_toplam = toplam[i]
            )
            toplam_tutar += float(toplam[i])
        teklifler.objects.filter(id =tekliff.id ).update(
            toplam_tutar = toplam_tutar
        )
    return redirect_with_language("crm:crm_teklif_yonetimi")

def crm_teklif_duzenle_gonder(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar, kullanicilar=request.user)
        if a:
            if a.izinler.crm_teklif_duzenleme:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else:
        kullanici = request.user

    if request.POST:
        teklif_id = request.POST.get("teklif_id")
        adsoyad = request.POST.get("adsoyad")
        soyad = request.POST.get("soyad")
        telefon = request.POST.get("telefon")
        Teklif_basligi = request.POST.get("Teklif_basligi")
        urun = request.POST.getlist("kalem-urun-hizmet-adi")
        aciklama = request.POST.getlist("kalem-aciklama")
        indirim = request.POST.getlist("kalem-indirim")
        miktar = request.POST.getlist("kalem-miktar")
        birim_fiyat = request.POST.getlist("kalem-birim-fiyati")
        toplam = request.POST.getlist("kalem-toplam")
        iqd = request.POST.getlist("kalem-toplam-iqd")

        musteri = get_object_or_none(musteri_bilgisi, musteri_kime_ait=kullanici,
                                     musteri_adi=adsoyad,
                                     musteri_soyadi=soyad,
                                     musteri_telefon_numarasi=telefon)
        if not musteri:
            musteri = musteri_bilgisi.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),musteri_kime_ait=kullanici,
                                                     musteri_adi=adsoyad,
                                                     musteri_soyadi=soyad,
                                                     musteri_telefon_numarasi=telefon)

        teklif = get_object_or_none(teklifler, id=teklif_id)
        if teklif:
            teklif.teklif_basligi = Teklif_basligi
            teklif.musterisi = musteri
            teklif.save()

            # Delete all existing items before adding new ones
            teklif_icerikleri.objects.filter(hangi_teklif=teklif).delete()

            toplam_tutar = 0
            for i in range(len(urun)):
                teklif_icerikleri.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),
                    kime_ait=kullanici,
                    hangi_teklif=teklif,
                    urun_hizmet=urun[i],
                    urun_aciklama=aciklama[i],
                    indirim=indirim[i],
                    miktar=miktar[i],
                    birim_fiyati=birim_fiyat[i],
                    birim_fiyati_ıqd=iqd[i],
                    genel_toplam=toplam[i]
                )
                toplam_tutar += float(toplam[i])

            teklif.toplam_tutar = toplam_tutar
            teklif.save()

    return redirect_with_language("crm:crm_teklif_yonetimi")

def daire_evrak_ekle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar, kullanicilar=request.user)
        if a:
            if a.izinler.crm_evrak_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else:
        kullanici = request.user

    if request.method == 'POST':
        daire_id = request.POST.get('daire_id')
        evrak_adi = request.POST.get('evrak_adi')
        evrak = request.FILES.get('evrak')

        daire = get_object_or_none(daire_bilgisi, id=daire_id, daire_kime_ait=kullanici)
        if daire and evrak:
            daire_evraklari.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),
                evrak_kime_ait=kullanici,
                daire=daire,
                evrak_adi=evrak_adi,
                evrak=evrak
            )
        return redirect_with_language("crm:crm_dairedetayi", daire_id)

    return redirect_with_language("crm:crm_dairedetayi", daire_id)

def get_daire_evraklari(request):
    daire_id = request.GET.get('daire_id')
    if daire_id:
        evraklar = daire_evraklari.objects.filter(daire_id=daire_id).values('evrak_adi', 'evrak')
        image_extensions = [".jpg", ".jpeg", ".png"]
        evrak_list = [{'evrak_adi': evrak['evrak_adi'], 'evrak_url': evrak['evrak'], 'is_image': evrak['evrak'].lower().endswith(tuple(image_extensions))} for evrak in evraklar]
        return JsonResponse(evrak_list, safe=False)
    return JsonResponse({'error': 'Daire bulunamadı'}, status=400)

def musteri_evrak_ekle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar, kullanicilar=request.user)
        if a:
            if a.izinler.crm_evrak_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else:
        kullanici = request.user

    if request.method == 'POST':
        musteri_id = request.POST.get('musteri_id')
        evrak_adi = request.POST.get('evrak_adi')
        evrak = request.FILES.get('evrak')

        musteri = get_object_or_none(musteri_bilgisi, id=musteri_id, musteri_kime_ait=kullanici)
        if musteri and evrak:
            musteri_evraklari.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),
                belge_kime_ait=kullanici,
                musterisi=musteri,
                evrak_detayi=evrak_adi,
                evrak=evrak
            )
        return redirect_with_language("crm:crm_musteri_detayi", musteri_id)

    return redirect_with_language("crm:crm_musteri_detayi", musteri_id)

def musteri_evrak_duzenle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar, kullanicilar=request.user)
        if a:
            if a.izinler.crm_evrak_duzenleme:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else:
        kullanici = request.user

    if request.method == 'POST':
        evrak_id = request.POST.get('evrak_id')
        evrak_adi = request.POST.get('evrak_adi')
        evrak = request.FILES.get('evrak')

        musteri_evrak = get_object_or_none(musteri_evraklari, id=evrak_id, belge_kime_ait=kullanici)
        if musteri_evrak:
            musteri_evrak.evrak_detayi = evrak_adi
            if evrak:
                musteri_evrak.evrak = evrak
            musteri_evrak.save()
        return redirect_with_language("crm:crm_musteri_detayi", musteri_evrak.musterisi.id)

    return redirect_with_language("crm:crm_musteri_detayi", musteri_evrak.musterisi.id)

def musteri_evrak_sil(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar, kullanicilar=request.user)
        if a:
            if a.izinler.crm_evrak_silme:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else:
        kullanici = request.user

    if request.method == 'POST':
        evrak_id = request.POST.get('evrak_id')
        musteri_id = request.POST.get('musteri_id')

        musteri_evraklari.objects.filter(id=evrak_id, belge_kime_ait=kullanici).delete()
        return redirect_with_language("crm:crm_musteri_detayi", musteri_id)

    return redirect_with_language("crm:crm_musteri_detayi", musteri_id)

