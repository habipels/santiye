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

# Salt değeri ve minimum hash uzunluğu belirleyin
HASHIDS_SALT = "habip_elis_12345"
HASHIDS_MIN_LENGTH = 32

hashids = Hashids(salt=HASHIDS_SALT, min_length=HASHIDS_MIN_LENGTH)

def encode_id(id):
    return hashids.encode(id)

def decode_id(hash_id):
    ids = hashids.decode(hash_id)
    return ids[0] if ids else None
def page_not_found_view(request, exception):
    return render(request, '404.html')
"""
trans = translate(language='tr')
    z = BlogPost.objects.all()
    content = {"trans":trans,"z":z,"dil":dil_bilgisi}
"""
def yetkisiz(request):
    return render(request,"yetkisiz.html",sozluk_yapisi())
def super_admin_kontrolu(request):
    if request.user.is_superuser:
            return 1
    else:
        return 0
def dil_bilgisi():
    return get_language()
def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext('Hello')

    finally:
        activate(cur_language)
    return text

def sozluk_yapisi():
    trans = translate(language='tr')
    sozluk = {"trans":trans,"dil":dil_bilgisi()}
    sozluk ["diller"] = dil_ayarla.objects.all()
    sozluk ["sayfalogusu"] = sayfa_logosu.objects.last()
    sozluk ["sayfa_iconu"] = sayfa_iconu.objects.last()
    sozluk ["site_adi"] = site_adi.objects.last()
    sozluk ["layout"] = layout.objects.last()
    sozluk ["color_sheme"] = color_sheme.objects.last()
    sozluk["sidebar_boyutu"] = sidebar_boyutu.objects.last()
    sozluk["side_bar_gorunum"] = side_bar_gorunum.objects.last()
    sozluk["layout_pozisyonu"] = layout_pozisyonu.objects.last()
    sozluk["topbar_color"] = topbar_color.objects.last()
    sozluk["sidebar_rengi"] = sidebar_rengi.objects.last()
    sozluk["layout_uzunlugu"] = layout_uzunlugu.objects.last()
    sozluk["layout_sitili"] = layout_sitili.objects.last()
    sozluk["etiketler"] = faturalardaki_gelir_gider_etiketi.objects.last()
    sozluk["latest_actions"] =LogEntry.objects.all().order_by('-action_time')[:10]
    return sozluk
def loglar(request):
    content = sozluk_yapisi()
    if request.user.is_authenticated:
        if request.user.is_superuser :
            content["latest_actions"] =LogEntry.objects.all().order_by('-action_time')
        if request.GET.get("search"):
            search = request.GET.get("search")
            if search:
                profile = LogEntry.objects.all().order_by('-action_time')
            else:
                profile = LogEntry.objects.all().order_by('-action_time')
        else:
            profile = LogEntry.objects.all().order_by('-action_time')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(profile, 10) # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        content["santiyeler"] = page_obj
        content["top"]  = profile
        content["medya"] = page_obj

    else:
        return redirect("/users/login/")

    return render(request,"santiye_yonetimi/loglar.html",content)

#superadmin Kontrol
def yetki(request):
    if request.user.is_superuser:

        pass
    else:

        return redirect("main:yetkisiz")
# Create your views here,
# Anasayfa
def homepage(request):
    content = sozluk_yapisi()
    if request.user.is_authenticated:
        content = sozluk_yapisi()
        if super_admin_kontrolu(request):
            profile =Gelir_Bilgisi.objects.all()
            kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-id")
            content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        if request.GET:
            search = request.GET.get("search")
            tarih = request.GET.get("tarih")
            if search:
                if super_admin_kontrolu(request):
                    profile =Gelir_Bilgisi.objects.filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)| Q(gelir_kime_ait_oldugu__first_name__icontains = search)| Q(aciklama__icontains = search) | Q(gelir_kategorisi__gelir_kategori_adi__icontains = search))
                    kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
                    content["kullanicilar"] =kullanicilar
                else:
                    profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)| Q(gelir_kime_ait_oldugu__first_name__icontains = search)| Q(aciklama__icontains = search) | Q(gelir_kategorisi__gelir_kategori_adi__icontains = search))
                    content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
            if tarih :
                profile = profile.filter(Q(fatura_tarihi__gt  = tarih) | Q(vade_tarihi__lt  = tarih) )
        page_num = request.GET.get('page', 1)
        paginator = Paginator(profile, 5) # 6 employees per page

        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
                # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
                # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)

        content["santiyeler"] = page_obj
        if super_admin_kontrolu(request):
            profile =Gider_Bilgisi.objects.all()
            kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-id")
            content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        if request.GET:
            search = request.GET.get("search")
            tarih = request.GET.get("tarih")
            if search:
                if super_admin_kontrolu(request):
                    profile =Gider_Bilgisi.objects.filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)| Q(gelir_kime_ait_oldugu__first_name__icontains = search)| Q(aciklama__icontains = search) | Q(gelir_kategorisi__gelir_kategori_adi__icontains = search))
                    kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
                    content["kullanicilar"] =kullanicilar
                else:
                    profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)| Q(gelir_kime_ait_oldugu__first_name__icontains = search)| Q(aciklama__icontains = search) | Q(gelir_kategorisi__gelir_kategori_adi__icontains = search))
                    content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
            if tarih :
                profile = profile.filter(Q(fatura_tarihi__gt  = tarih) | Q(vade_tarihi__lt  = tarih) )
        page_num = request.GET.get('page', 1)
        paginator = Paginator(profile, 5) # 6 employees per page

        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
                # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
                # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        bilgi_ver = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-fatura_tarihi")
        sonuc = []
        for i in bilgi_ver:
            y =  gider_urun_bilgisi.objects.filter(gider_bilgis = i)
            urun_tutari = 0
            for j in y:
                urun_tutari = urun_tutari + (float(j.urun_adeti)*float(j.urun_fiyati))
            y =  Gider_odemesi.objects.filter(gelir_kime_ait_oldugu = i)
            odeme_tutari = 0
            for j in y:
                odeme_tutari = odeme_tutari + float(j.tutar)
            if urun_tutari > odeme_tutari:
                sonuc.append(i)
            if len(sonuc) >= 5 :
                break
        content["gider"] = sonuc
        content["bilgi"] = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-id")[:5]
    else:
        return redirect("/users/login/")

    return render(request,"index.html",content)
def homepage_2(request,hash):
    content = sozluk_yapisi()
    if request.user.is_authenticated:
        content = sozluk_yapisi()
        if super_admin_kontrolu(request):
            d = decode_id(hash)
            content["hashler"] = hash
            users = get_object_or_404(CustomUser,id = d)
            content["hash_bilgi"] = users
            kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
            profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = users).order_by("-id")
            content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = users)
        else:
            profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-id")
            content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        if request.GET:
            search = request.GET.get("search")
            tarih = request.GET.get("tarih")
            if search:
                if super_admin_kontrolu(request):
                    d = decode_id(hash)
                    users = get_object_or_404(CustomUser,id = d)
                    content["hash_bilgi"] = users
                    kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
                    profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = users).order_by("-id")
                    content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = users)
                else:
                    profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)| Q(gelir_kime_ait_oldugu__first_name__icontains = search)| Q(aciklama__icontains = search) | Q(gelir_kategorisi__gelir_kategori_adi__icontains = search))
                    content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
            if tarih :
                profile = profile.filter(Q(fatura_tarihi__gt  = tarih) | Q(vade_tarihi__lt  = tarih) )
        page_num = request.GET.get('page', 1)
        paginator = Paginator(profile, 5) # 6 employees per page

        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
                # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
                # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)

        content["santiyeler"] = page_obj
        if super_admin_kontrolu(request):
            profile =Gider_Bilgisi.objects.all()
            kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-id")
            content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        if request.GET:
            search = request.GET.get("search")
            tarih = request.GET.get("tarih")
            if search:
                if super_admin_kontrolu(request):
                    profile =Gider_Bilgisi.objects.filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)| Q(gelir_kime_ait_oldugu__first_name__icontains = search)| Q(aciklama__icontains = search) | Q(gelir_kategorisi__gelir_kategori_adi__icontains = search))
                    kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
                    content["kullanicilar"] =kullanicilar
                else:
                    profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)| Q(gelir_kime_ait_oldugu__first_name__icontains = search)| Q(aciklama__icontains = search) | Q(gelir_kategorisi__gelir_kategori_adi__icontains = search))
                    content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
            if tarih :
                profile = profile.filter(Q(fatura_tarihi__gt  = tarih) | Q(vade_tarihi__lt  = tarih) )
        page_num = request.GET.get('page', 1)
        paginator = Paginator(profile, 5) # 6 employees per page

        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
                # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
                # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)

        bilgi_ver = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = users).order_by("-fatura_tarihi")
        sonuc = []
        for i in bilgi_ver:
            y =  gider_urun_bilgisi.objects.filter(gider_bilgis = i)
            urun_tutari = 0
            for j in y:
                urun_tutari = urun_tutari + (float(j.urun_adeti)*float(j.urun_fiyati))
            y =  Gider_odemesi.objects.filter(gelir_kime_ait_oldugu = i)
            odeme_tutari = 0
            for j in y:
                odeme_tutari = odeme_tutari + float(j.tutar)
            if urun_tutari > odeme_tutari:
                sonuc.append(i)
            if len(sonuc) >= 5 :
                break
        content["gider"] = sonuc
        content["bilgi"] = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = users).order_by("-id")[:5]
    else:
        return redirect("/users/login/")

    return render(request,"index.html",content)

#site ayarı
def site_ayarlari(request):
    content = sozluk_yapisi()
    if request.user.is_authenticated:
        if request.user.is_superuser :

            pass
        else:

            return redirect("main:yetkisiz")
    else:
        return redirect("/users/login/")

    return render(request,"santiye_yonetimi/site_ayarlari.html",content)

def site_ayari_kaydet(request):
    if request.POST:
        data_layout = request.POST.get("data-layout")
        if data_layout:
            layout.objects.create(isim =data_layout,data_layout =data_layout )
        data_bs_theme = request.POST.get("data-bs-theme")
        if data_bs_theme:
            color_sheme.objects.create(isim =data_bs_theme,data_bs_theme =data_bs_theme )
        data_sidebar_visibility = request.POST.get("data-sidebar-visibility")
        if data_sidebar_visibility :
            side_bar_gorunum.objects.create(isim =data_sidebar_visibility,data_sidebar_visibility =data_sidebar_visibility )
        data_layout_width = request.POST.get("data-layout-width")
        if data_layout_width:
            layout_uzunlugu.objects.create(isim =data_layout_width,data_layout_width =data_layout_width )
        data_layout_position = request.POST.get("data-layout-position")
        if data_layout_position:
            layout_pozisyonu.objects.create(isim =data_layout_position,data_layout_position =data_layout_position )
        data_topbar = request.POST.get("data-topbar")
        if data_topbar:
            topbar_color.objects.create(isim =data_topbar,data_topbar =data_topbar )
        data_sidebar_size = request.POST.get("data-sidebar-size")
        if data_sidebar_size:
            sidebar_boyutu.objects.create(isim =data_sidebar_size,data_sidebar_size =data_sidebar_size )
        data_layout_style = request.POST.get("data-layout-style")
        if data_layout_style:
            layout_sitili.objects.create(isim =data_layout_style,data_layout_style =data_layout_style )
        data_sidebar = request.POST.get("data-sidebar")
        if data_sidebar:
            sidebar_rengi.objects.create(isim =data_sidebar,data_sidebar =data_sidebar )
        dark_logo = request.FILES.get("dark_logo")

        site_adi_bilgisi = request.POST.get("site_adi")
        footeryazisi = request.POST.get("footeryazisi")
        if site_adi_bilgisi:
            site_adi.objects.create(site_adi_sekme_tr = site_adi_bilgisi)
        if footeryazisi:
            site_adi.objects.create(footer = footeryazisi)
        gideretiketi = request.POST.get("gideretiketi")
        geliretiketi = request.POST.get("gelir_etiketi")
        if gideretiketi and geliretiketi :
            faturalardaki_gelir_gider_etiketi.objects.create(gider_etiketi = gideretiketi,gelir_etiketi = geliretiketi )


        if dark_logo:
            u = sayfa_logosu.objects.last()
            u.image = dark_logo
            u.save()
        light_logo = request.FILES.get("light_logo")
        if light_logo:
            u = sayfa_logosu.objects.last()
            u.dark_image = light_logo
            u.save()
        icon = request.FILES.get("icon")
        if icon:
            u = sayfa_iconu.objects.last()
            u.sayfa_icon = icon
            u.save()
    return redirect("main:site_ayarlari")
#site ayarı

# Create your views here.
#şantiye Ekleme
def santiye_ekle(request):
    if request.user.is_authenticated:
        if request.user.is_superuser :

            pass
        else:

            return redirect("main:yetkisiz")
        if request.POST:
            yetkiliAdSoyad = request.POST.get("yetkiliAdSoyad")
            email = request.POST.get("email")
            santiyeAdi = request.POST.get("santiyeAdi")
            sfire = request.POST.get("sfire")
            print(yetkiliAdSoyad,email,santiyeAdi,sfire)
            newUser = CustomUser(username =email,email=email,first_name = santiyeAdi,last_name =yetkiliAdSoyad )
            newUser.set_password(sfire)
            newUser.save()
            return redirect("main:santiye_listele")

    else:
        return redirect("/users/login/")

    return render(request,"santiye_yonetimi/santiye_ekleme.html",sozluk_yapisi())
#şantiye Listleme Ve Ayarları

def santiye_listele(request):
    content = sozluk_yapisi()
    if request.user.is_authenticated:
        if request.user.is_superuser :

            pass
        else:

            return redirect("main:yetkisiz")
        if request.GET.get("search"):
            search = request.GET.get("search")
            if search:
                profile = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).filter(Q(last_name__icontains = search)|Q(first_name__icontains = search)|Q(email__icontains = search) ).order_by("-id")
            else:
                profile = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        else:
            profile = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        page_num = request.GET.get('page', 1)
        paginator = Paginator(profile, 10) # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        content["santiyeler"] = page_obj
        content["top"]  = profile
        content["medya"] = page_obj

    else:
        return redirect("/users/login/")

    return render(request,"santiye_yonetimi/santiye_ayarlari.html",content)

#şantiye Silme
def santiye_sil(request):
    content = {}
    if request.user.is_authenticated:
        yetki(request)
        content["santiyeler"] = CustomUser.objects.all()
        if request.POST:
            sil = request.POST.get("buttonId")
            CustomUser.objects.filter(id = sil).update(kullanici_silme_bilgisi = True)
        return redirect("main:santiye_listele")
    else:
        return redirect("/users/login/")

    return redirect("main:santiye_listele")

#şantiye düzeltme
def santiye_duzelt(request):
    content = {}
    if request.user.is_authenticated:
        if request.user.is_superuser :

            pass
        else:

            return redirect("main:yetkisiz")
        content["santiyeler"] = CustomUser.objects.all()
        if request.POST:
            sil = request.POST.get("buttonId")
            yetkili_adi = request.POST.get("yetkili_adi")
            email = request.POST.get("email")
            santiyeadi = request.POST.get("santiyeadi")
            CustomUser.objects.filter(id = sil).update(email=email,first_name = santiyeadi,last_name =yetkili_adi)
        return redirect("main:santiye_listele")
    else:
        return redirect("/users/login/")

    return redirect("main:santiye_listele")

#dil_ayarlari
def dil_ayari_listele(request):
    content = sozluk_yapisi()
    if request.user.is_authenticated:
        if request.user.is_superuser :

            pass
        else:

            return redirect("main:yetkisiz")
        if request.GET.get("search"):
            search = request.GET.get("search")
            if search:
                profile = dil_ayarla.objects.filter(Q(dil_adi__icontains = search)|Q(dil_kisaltması__icontains = search)).order_by("-id")
            else:
                profile = dil_ayarla.objects.all().order_by("-id")
        else:
            profile = dil_ayarla.objects.all().order_by("-id")
        page_num = request.GET.get('page', 1)
        paginator = Paginator(profile, 10) # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        content["santiyeler"] = page_obj
        content["top"]  = profile
        content["medya"] = page_obj

    else:
        return redirect("/users/login/")

    return render(request,"santiye_yonetimi/dil_ayarlari.html",content)

#dil Ekleme
def dil_ekle(request):
    if request.user.is_authenticated:
        if request.user.is_superuser :

            pass
        else:

            return redirect("main:yetkisiz")
        if request.POST:
            yetkili_adi = request.POST.get("yetkili_adi")
            dilkisitlamasi = request.POST.get("dilkisitlamasi")
            santiyeadi = request.FILES.get("santiyeadi")
            dil_aktiflik_durumu = request.POST.get("dil_aktiflik_durumu")
            if dil_aktiflik_durumu == "1":
                dil_aktiflik_durumu = True
            else:
                dil_aktiflik_durumu = False

            dil =dil_ayarla(dil_adi =yetkili_adi,dil_kisaltması =  dilkisitlamasi,dil_bayragi_icon =santiyeadi,
                                      dil_aktiflik_durumu = dil_aktiflik_durumu )

            dil.save()

            return redirect("main:dil_ayari_listele")

    else:
        return redirect("/users/login/")

#dil düzeltme
def dil_duzelt(request):
    if request.user.is_authenticated:
        if request.user.is_superuser :

            pass
        else:

            return redirect("main:yetkisiz")
        if request.POST:
            yetkili_adi = request.POST.get("yetkili_adi")
            dilkisitlamasi = request.POST.get("dilkisitlamasi")
            santiyeadi = request.FILES.get("santiyeadi")
            dil_aktiflik_durumu = request.POST.get("dil_aktiflik_durumu")
            buttonId = request.POST.get("buttonId")
            if dil_aktiflik_durumu == "1":
                dil_aktiflik_durumu = True
            else:
                dil_aktiflik_durumu = False
            dil_ayarla.objects.filter(id =buttonId ).delete()
            dil =dil_ayarla(dil_adi =yetkili_adi,dil_kisaltması =  dilkisitlamasi,dil_bayragi_icon =santiyeadi,
                                      dil_aktiflik_durumu = dil_aktiflik_durumu )

            dil.save()

            return redirect("main:dil_ayari_listele")

    else:
        return redirect("/users/login/")

#dil sil
def dil_sil(request):
    if request.user.is_authenticated:
        if request.user.is_superuser :

            pass
        else:

            return redirect("main:yetkisiz")
        if request.POST:
            sil = request.POST.get("buttonId")
            dil_ayarla.objects.filter(id = sil).delete()
        return redirect("main:dil_ayari_listele")
    else:
        return redirect("main:dil_ayari_listele")
#Proje Tipi
def proje_tipi_(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =proje_tipi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = proje_tipi.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =proje_tipi.objects.filter(Q(proje_ait_bilgisi__last_name__icontains = search)|Q(Proje_tipi_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = proje_tipi.objects.filter(Q(proje_ait_bilgisi = request.user) & Q(Proje_tipi_adi__icontains = search)& Q(silinme_bilgisi = False))
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 10) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/proje_tipi.html",content)
#Proje Tipi
def proje_tipi_2(request,hash):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        users = get_object_or_404(CustomUser,id = d)
        content["hashler"] = hash
        content["hash_bilgi"] = users
        profile = proje_tipi.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = users)
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = proje_tipi.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            d = decode_id(hash)
            users = get_object_or_404(CustomUser,id = d)
            content["hashler"] = hash
            content["hash_bilgi"] = users
            profile = proje_tipi.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = users)
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = proje_tipi.objects.filter(Q(proje_ait_bilgisi = request.user) & Q(Proje_tipi_adi__icontains = search)& Q(silinme_bilgisi = False))
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 10) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/proje_tipi.html",content)
#Proje Ekleme
def proje_ekleme(request):
    if request.POST:
        #yetkili_adi
        if super_admin_kontrolu(request):
            kullanici_bilgisi  = request.POST.get("kullanici")
            proje_tip_adi   = request.POST.get("yetkili_adi")
            proje_tipi.objects.create(proje_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,Proje_tipi_adi = proje_tip_adi)
        else:
            proje_tip_adi   = request.POST.get("yetkili_adi")
            proje_tipi.objects.create(proje_ait_bilgisi = request.user,Proje_tipi_adi = proje_tip_adi)
    return redirect("main:proje_tipi_")
#Proje Adı Silme
def proje_Adi_sil(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        proje_tipi.objects.filter(id = id).update(silinme_bilgisi = True)
    else:
        proje_tipi.objects.filter(proje_ait_bilgisi = request.user,id = id).update(silinme_bilgisi = True)
    return redirect("main:proje_tipi_")
#Proje Düzenlme
def proje_duzenle(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        silinmedurumu = request.POST.get("silinmedurumu")
        if silinmedurumu == "1":
            silinmedurumu = False
            proje_tipi.objects.filter(id = id).update(proje_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,Proje_tipi_adi = proje_tip_adi,silinme_bilgisi = silinmedurumu)
        elif silinmedurumu == "2":
            silinmedurumu = True
            proje_tipi.objects.filter(id = id).update(proje_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,Proje_tipi_adi = proje_tip_adi,silinme_bilgisi = silinmedurumu)

    else:
        proje_tip_adi   = request.POST.get("yetkili_adi")
        proje_tipi.objects.filter(proje_ait_bilgisi = request.user,id = id).update(Proje_tipi_adi = proje_tip_adi)
    return redirect("main:proje_tipi_")
#Şantiye Projesi Ekleme
def santiye_projesi_ekle_(request):
    content = sozluk_yapisi()
    content["proje_tipleri"] = proje_tipi.objects.filter(proje_ait_bilgisi =  request.user)
    if super_admin_kontrolu(request):
        profile =santiye.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =santiye.objects.filter(Q(proje_ait_bilgisi__last_name__icontains = search)|Q(Proje_tipi_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = santiye.objects.filter(Q(proje_ait_bilgisi = request.user) & Q(Proje_tipi_adi__icontains = search)& Q(silinme_bilgisi = False))
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 10) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/santiye_projesi.html",content)
def santiye_projesi_ekle_2(request,hash):
    content = sozluk_yapisi()
    content["proje_tipleri"] = proje_tipi.objects.filter(proje_ait_bilgisi =  request.user)
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        users = get_object_or_404(CustomUser,id = d)
        content["hashler"] = hash
        content["hash_bilgi"] = users
        profile =santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = users)
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            d = decode_id(hash)
            users = get_object_or_404(CustomUser,id = d)
            content["hashler"] = hash
            content["hash_bilgi"] = users
            profile =santiye.objects.filter(Q(proje_ait_bilgisi = users) & Q(proje_ait_bilgisi__last_name__icontains = search)|Q(Proje_tipi_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = santiye.objects.filter(Q(proje_ait_bilgisi = request.user) & Q(Proje_tipi_adi__icontains = search)& Q(silinme_bilgisi = False))
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 10) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/santiye_projesi.html",content)
#asdas
def santiye_projesi_bloklar_ekle_(request,id):
    content = sozluk_yapisi()
    content["id_bilgisi"] = id
    content["proje_tipleri"] = proje_tipi.objects.filter(proje_ait_bilgisi =  request.user)
    if super_admin_kontrolu(request):
        profile =bloglar.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = bloglar.objects.filter(proje_santiye_Ait__id = id)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =bloglar.objects.filter(Q(proje_santiye_Ait__proje_ait_bilgisi__last_name__icontains = search)|Q(proje_santiye_Ait__Proje_tipi_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = bloglar.objects.filter(Q(proje_ait_bilgisi = request.user) & Q(blog_adi__icontains = search))
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 10) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/santiye_projesi_blok_ekle.html",content)

def blog_ekle(request):
    if request.POST:
        santiye_bilgisi = request.POST.get("santiye_bilgisi")
        blok_adi = request.POST.get("blok_adi")
        kat_sayisi = request.POST.get("kat_sayisi")
        baslangictarihi = request.POST.get("baslangictarihi")
        bitistarihi =request.POST.get("bitistarihi")
        bloglar.objects.create(
            proje_ait_bilgisi = get_object_or_404(santiye,id = santiye_bilgisi).proje_ait_bilgisi,
            proje_santiye_Ait = get_object_or_404(santiye,id = santiye_bilgisi),
            blog_adi = blok_adi,kat_sayisi = kat_sayisi,
            baslangic_tarihi = baslangictarihi,bitis_tarihi = bitistarihi
        )
        y = "/siteblog/"+santiye_bilgisi+"/"
    return redirect(y)
def blog_duzenle(request):
    if request.POST:
        santiye_bilgisi = request.POST.get("santiye_bilgisi")
        blog = request.POST.get("blog")
        blok_adi = request.POST.get("blok_adi")
        kat_sayisi = request.POST.get("kat_sayisi")
        baslangictarihi = request.POST.get("baslangictarihi")
        bitistarihi =request.POST.get("bitistarihi")
        bloglar.objects.filter(id = blog).update(
            proje_ait_bilgisi = get_object_or_404(santiye,id = santiye_bilgisi).proje_ait_bilgisi,
            proje_santiye_Ait = get_object_or_404(santiye,id = santiye_bilgisi),
            blog_adi = blok_adi,kat_sayisi = kat_sayisi,
            baslangic_tarihi = baslangictarihi,bitis_tarihi = bitistarihi
        )
        y = "/siteblog/"+santiye_bilgisi+"/"
    return redirect(y)
def blog_sil(request):
    if request.POST:
        buttonId = request.POST.get("buttonId")
        geri = request.POST.get("geri")
        blog_bilgisi = get_object_or_404(bloglar,id = buttonId)
        bloglar.objects.filter(id = buttonId).delete()
        y = "/siteblog/"+geri+"/"
    return redirect(y)
def santiye_ekleme_sahibi(request):
    if request.POST:
        if super_admin_kontrolu(request):
            kullanici = request.POST.get("kullanici")
            link = "/addsitesuperadmin/"+kullanici
            return redirect(link)

        projetipi = request.POST.get("projetipi")
        proje_adi = request.POST.get("yetkili_adi")

        a = santiye.objects.create(proje_ait_bilgisi = request.user,proje_tipi = get_object_or_404(proje_tipi,id = projetipi),
                               proje_adi = proje_adi
                               )
    return redirect("main:santiye_projesi_ekle_")

def santiye_ekleme_super_admin(request,id):
    content = sozluk_yapisi()
    content["proje_tipleri"] = proje_tipi.objects.filter(proje_ait_bilgisi =  get_object_or_404(CustomUser,id = id))
    if request.user.is_superuser :

        pass
    else:

        return redirect("main:yetkisiz")
    if request.POST:
        projetipi = request.POST.get("projetipi")
        proje_adi = request.POST.get("yetkili_adi")
        baslangic_tarihi = request.POST.get("baslangic_tarihi")
        bitis_tarihi = request.POST.get("bitis_tarihi")
        a = santiye.objects.create(proje_ait_bilgisi = get_object_or_404(CustomUser,id = id),proje_tipi = get_object_or_404(proje_tipi,id = projetipi),
                               proje_adi = proje_adi,baslangic_tarihi = baslangic_tarihi,
                               tahmini_bitis_tarihi = bitis_tarihi
                               )
        return redirect("main:santiye_projesi_ekle_")
    return render(request,"santiye_yonetimi/super_admin_santiye_ekleme.html",content)


def santiye_projesi_sil(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        santiye.objects.filter(id = id).update(silinme_bilgisi = True)
    else:
        santiye.objects.filter(proje_ait_bilgisi = request.user,id = id).update(silinme_bilgisi = True)
    return redirect("main:santiye_projesi_ekle_")


def santiye_projesi_duzenle(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        silinmedurumu = request.POST.get("silinmedurumu")
        if silinmedurumu == "1":
            silinmedurumu = False
            santiye.objects.filter(id = id).update(proje_adi = proje_tip_adi,silinme_bilgisi = silinmedurumu)
        elif silinmedurumu == "2":
            silinmedurumu = True
            santiye.objects.filter(id = id).update(proje_adi = proje_tip_adi,silinme_bilgisi = silinmedurumu)

    else:
        proje_tip_adi   = request.POST.get("yetkili_adi")
        santiye.objects.filter(proje_ait_bilgisi = request.user,id = id).update(proje_adi = proje_tip_adi)
    return redirect("main:santiye_projesi_ekle_")

#şantiye Kalemleri
def santtiye_kalemleri(request,id):
    content = sozluk_yapisi()
    content["birim_bilgisi"] = birimler.objects.filter(silinme_bilgisi = False)
    if request.user.is_authenticated:
        if request.user.is_superuser:
            kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
            profile = santiye_kalemleri.objects.filter(proje_santiye_Ait = get_object_or_404(santiye,id = id))
            content["santiyeler_bilgileri"] = santiye.objects.all()
        else:
            content["santiyeler_bilgileri"] = santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)
            profile = santiye_kalemleri.objects.filter(proje_santiye_Ait = get_object_or_404(santiye,id = id) ,silinme_bilgisi = False,proje_ait_bilgisi = request.user)

        if request.GET.get("search"):
            search = request.GET.get("search")
            if request.user.is_superuser:
                kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
                content["kullanicilar"] =kullanicilar
                profile = santiye_kalemleri.objects.filter(proje_santiye_Ait = get_object_or_404(santiye,id = id)).filter(Q(proje_ait_bilgisi__last_name__icontains =search)| Q(kalem_adi__icontains =search)|  Q(proje_santiye_Ait__proje_adi__icontains =search))
                content["santiyeler_bilgileri"] = santiye.objects.all()
            else:
                content["santiyeler_bilgileri"] = santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)
                profile = santiye_kalemleri.objects.filter(proje_santiye_Ait = get_object_or_404(santiye,id = id) ,silinme_bilgisi = False,proje_ait_bilgisi = request.user).filter(Q(kalem_adi__icontains =search) | Q(proje_santiye_Ait__proje_adi__icontains =search))

        page_num = request.GET.get('page', 1)
        paginator = Paginator(profile, 10) # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
                # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
                # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        content["santiyeler"] = page_obj
        content["top"]  = profile
        content["medya"] = page_obj
    else:
        return redirect("/users/login/")
    return render(request,"santiye_yonetimi/santiye_kalemleri.html",content)

def santiyeye_kalem_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            return redirect("main:santiye_kalem_ekle_admin",kullanici)
        else:
            projetipi = request.POST.get("projetipi")
            yetkili_adi = request.POST.get("yetkili_adi")
            santiye_agirligi = request.POST.get("katsayisi")
            finansal_agirlik = request.POST.get("blogsayisi")
            metraj = request.POST.get("metraj")
            tutar = request.POST.get("tutar")
            birim_bilgisi = request.POST.get("birim_bilgisi")
            kalem = santiye_kalemleri.objects.create(
                proje_ait_bilgisi = request.user,
                proje_santiye_Ait = get_object_or_404(santiye,id =projetipi ),
                kalem_adi = yetkili_adi,santiye_agirligi = santiye_agirligi,
                santiye_finansal_agirligi = finansal_agirlik,
                birimi = get_object_or_404(birimler,id =birim_bilgisi ),metraj = metraj,
                tutari = tutar
            )
            blog_lar = bloglar.objects.filter(proje_santiye_Ait = get_object_or_404(santiye,id =projetipi ))
            for i in blog_lar:
                for j in range(0,int(i.kat_sayisi)):
                    santiye_kalemlerin_dagilisi.objects.create(
                        proje_ait_bilgisi = request.user,
                        proje_santiye_Ait = get_object_or_404(santiye,id =projetipi ),
                        kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =kalem.id ),
                        kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                    )
    return redirect("main:santtiye_kalemleri",projetipi)

def kalem_sil(request):
    if request.POST:
        buttonId = request.POST.get("buttonId")
        geri_don = request.POST.get("geri_don")
        santiye_kalemleri.objects.filter(id = buttonId).update(
            silinme_bilgisi = True
        )
    return redirect("main:santtiye_kalemleri",geri_don)
def santiye_kalemleri_duzenle(request):
    if request.POST:
        buttonId = request.POST.get("buttonId")
        yetkili_adi = request.POST.get("yetkili_adi")
        santiye_agirligi = request.POST.get("katsayisi")
        finansal_agirlik = request.POST.get("blogsayisi")
        geri_don = request.POST.get("geri_don")
        metraj = request.POST.get("metraj")
        tutar = request.POST.get("tutar")
        birim_bilgisi = request.POST.get("birim_bilgisi")
        if request.user.is_superuser:
            silinmedurumu = request.POST.get("silinmedurumu")
            if silinmedurumu == "3":
                santiye_kalemleri.objects.filter(id  = buttonId).update(
                        kalem_adi = yetkili_adi,santiye_agirligi = santiye_agirligi,
                        santiye_finansal_agirligi = finansal_agirlik,
                        birimi = get_object_or_404(birimler,id =birim_bilgisi ),metraj = metraj,
                tutari = tutar)
            elif silinmedurumu == "2":
                santiye_kalemleri.objects.filter(id  = buttonId).update(
                        kalem_adi = yetkili_adi,santiye_agirligi = santiye_agirligi,
                        santiye_finansal_agirligi = finansal_agirlik,
                        silinme_bilgisi = True,birimi = get_object_or_404(birimler,id =birim_bilgisi ),metraj = metraj,
                tutari = tutar)

            elif silinmedurumu == "1":
                santiye_kalemleri.objects.filter(id  = buttonId).update(
                        kalem_adi = yetkili_adi,santiye_agirligi = santiye_agirligi,
                        santiye_finansal_agirligi = finansal_agirlik,
                        silinme_bilgisi = False,birimi = get_object_or_404(birimler,id =birim_bilgisi ),metraj = metraj,
                tutari = tutar
                    )
        else:
            santiye_kalemleri.objects.filter(id  = buttonId).update(
                    proje_ait_bilgisi = request.user,
                    kalem_adi = yetkili_adi,santiye_agirligi = santiye_agirligi,
                    santiye_finansal_agirligi = finansal_agirlik,birimi = get_object_or_404(birimler,id =birim_bilgisi ),metraj = metraj,
                tutari = tutar
                )
        return redirect("main:santtiye_kalemleri",geri_don)

def kalem_blog_dagilis_sil(request,id,ik):
    a = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id).first()
    a = a.proje_santiye_Ait.id
    santiye_kalemlerin_dagilisi.objects.filter(kalem_bilgisi__id= ik,blog_bilgisi__id = id).delete()
    return redirect("main:santtiye_kalemleri",a)

def santiye_kalem_ve_blog(request):
    content = sozluk_yapisi()
    content["proje_tipleri"] = proje_tipi.objects.filter(proje_ait_bilgisi =  request.user)
    if super_admin_kontrolu(request):
        profile =bloglar.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = bloglar.objects.filter(proje_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =bloglar.objects.filter(Q(proje_ait_bilgisi__last_name__icontains = search)|Q(proje_santiye_Ait__Proje_tipi_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = bloglar.objects.filter(Q(proje_ait_bilgisi = request.user) & Q(proje_santiye_Ait__Proje_tipi_adi__icontains = search))
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 10) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/santiye_blog_kalem.html",content)

def santiye_kalem_ve_blog_2(request,hash):
    content = sozluk_yapisi()
    content["proje_tipleri"] = proje_tipi.objects.filter(proje_ait_bilgisi =  request.user)
    if super_admin_kontrolu(request):
        profile =bloglar.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = bloglar.objects.filter(proje_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =bloglar.objects.filter(Q(proje_ait_bilgisi__last_name__icontains = search)|Q(proje_santiye_Ait__Proje_tipi_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = bloglar.objects.filter(Q(proje_ait_bilgisi = request.user) & Q(proje_santiye_Ait__Proje_tipi_adi__icontains = search))
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 10) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/santiye_blog_kalem.html",content)

def blogtan_kaleme_ilerleme_takibi(request,id,slug):
    content = sozluk_yapisi()
    content["id"] = get_object_or_404(bloglar,id = id)
    content["blog_id"] = id
    if request.user.is_authenticated:
        if request.user.is_superuser:
            content["santiyeler_bilgileri"] = santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = get_object_or_404(bloglar,id = id).proje_ait_bilgisi)
            kalemler = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id)
            kalem_id = []
            for i in kalemler:
                if i.kalem_bilgisi.id in kalem_id:
                    pass
                else:
                    kalem_id.append(i.kalem_bilgisi.id)

            profile =  santiye_kalemleri.objects.filter(id__in = kalem_id,silinme_bilgisi = False)
            page_num = request.GET.get('page', 1)
            paginator = Paginator(profile, 10) # 6 employees per page
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                # if page is not an integer, deliver the first page
                page_obj = paginator.page(1)
            except EmptyPage:
                # if the page is out of range, deliver the last page
                page_obj = paginator.page(paginator.num_pages)
            content["santiyeler"] = page_obj
            content["top"]  = profile
            content["medya"] = page_obj

        else:
            content["santiyeler_bilgileri"] = santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)
            kalemler = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id)
            kalem_id = []
            for i in kalemler:
                if i.kalem_bilgisi.id in kalem_id:
                    pass
                else:
                    kalem_id.append(i.kalem_bilgisi.id)

            profile =  santiye_kalemleri.objects.filter(id__in = kalem_id,silinme_bilgisi = False)
            page_num = request.GET.get('page', 1)
            paginator = Paginator(profile, 10) # 6 employees per page
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                # if page is not an integer, deliver the first page
                page_obj = paginator.page(1)
            except EmptyPage:
                # if the page is out of range, deliver the last page
                page_obj = paginator.page(paginator.num_pages)
            content["santiyeler"] = page_obj
            content["top"]  = profile
            content["medya"] = page_obj
    else:
        return redirect("/users/login/")
    return render(request,"santiye_yonetimi/ilerleme_takibi.html",content)
def ilerleme_kaydet(request):
    if request.POST:
        geri_don = request.POST.get("geri_don")
        veri_cek = request.POST.get("veri_cek")
        kalem = request.POST.getlist("kalem")
        tumbilgi = request.POST.getlist("tumbilgi")
        a = []
        for i in tumbilgi:
            k = i.split(",")
            for j in k :
                a.append(j)
        print(a)
        for i in kalem:
            a.remove(i)
            santiye_kalemlerin_dagilisi.objects.filter(id = int(i)).update(tamamlanma_bilgisi = True)
        for i in a:
            if i != "":
                santiye_kalemlerin_dagilisi.objects.filter(id = int(i)).update(tamamlanma_bilgisi = False)

    return redirect("main:blogtan_kaleme_ilerleme_takibi",geri_don,veri_cek)


def santiye_kalem_ekle_admin(request,id):
    content = sozluk_yapisi()
    content["santiyeler_bilgileri"] = santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = id)
    if request.POST:
        projetipi = request.POST.get("projetipi")
        yetkili_adi = request.POST.get("yetkili_adi")
        santiye_agirligi = request.POST.get("katsayisi")
        finansal_agirlik = request.POST.get("blogsayisi")
        metraj = request.POST.get("metraj")
        tutar = request.POST.get("tutar")
        birim_bilgisi = request.POST.get("birim_bilgisi")
        
        kalem = santiye_kalemleri.objects.create(
                proje_ait_bilgisi = get_object_or_404(CustomUser,id = id),
                proje_santiye_Ait = get_object_or_404(santiye,id =projetipi ),
                kalem_adi = yetkili_adi,santiye_agirligi = santiye_agirligi,
                santiye_finansal_agirligi = finansal_agirlik,
                birimi = get_object_or_404(birimler,id =birim_bilgisi ),metraj = metraj,
                tutari = tutar
            )
        blog_lar = bloglar.objects.filter(proje_santiye_Ait = get_object_or_404(santiye,id =projetipi ))
        kat_sayisi = int(get_object_or_404(santiye,id =projetipi ).kat_sayisi)
        for i in blog_lar:
            for j in range(0,kat_sayisi):
                santiye_kalemlerin_dagilisi.objects.create(
                    proje_ait_bilgisi = get_object_or_404(CustomUser,id = id) ,
                    proje_santiye_Ait = get_object_or_404(santiye,id =projetipi ),
                    kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =kalem.id ),
                    kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                    )
        return redirect("main:santtiye_kalemleri",get_object_or_404(santiye,id =projetipi ).id)
    return render(request,"santiye_yonetimi/santiyeyekalem_ekle_admin.html",content)
#şantiye Kalemleri
#Proje Bilgisi
def projeler_sayfasi(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile =projeler.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = projeler.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)

    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =projeler.objects.filter(Q(proje_ait_bilgisi__last_name__icontains = search)|Q(Proje_tipi_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = projeler.objects.filter(Q(proje_ait_bilgisi = request.user) & Q(silinme_bilgisi = False)).filter(Q(aciklama__icontains = search)| Q(proje_Adi__icontains = search))
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 10) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    content["blog_bilgisi"]  =bloglar.objects.filter(proje_ait_bilgisi = request.user,proje_santiye_Ait__silinme_bilgisi = False)
    return render(request,"santiye_yonetimi/proje_sayfai.html",content)

#proje Ekleme
def proje_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            return redirect("main:proje_ekle_admin",id = kullanici)
        else:
            yetkili_adi = request.POST.get("yetkili_adi")
            tarih_bilgisi = request.POST.get("tarih_bilgisi")
            aciklama = request.POST.get("aciklama")
            durumu  = request.POST.get("durumu")
            if durumu == "1":
                durumu = True
            else:
                durumu = False
            blogbilgisi = request.POST.getlist("blogbilgisi")
            new_project = projeler(
                proje_ait_bilgisi = request.user,
                proje_Adi = yetkili_adi,
                tarih = tarih_bilgisi,
                aciklama = aciklama,
                durum = durumu,silinme_bilgisi = False
            )
            new_project.save()
            bloglar_bilgisi = []
            for i in blogbilgisi:
                bloglar_bilgisi.append(bloglar.objects.get(id=int(i)))
            new_project.blog_bilgisi.add(*bloglar_bilgisi)
            images = request.FILES.getlist('file')
            for images in images:
                proje_dosyalari.objects.create(dosya=images,proje_ait_bilgisi = get_object_or_404(projeler,id = new_project.id))  # Urun_resimleri modeline resimleri kaydet

    return redirect("main:projeler_sayfasi")

def proje_ekle_admin(request,id):
    content = sozluk_yapisi()
    content["blog_bilgisi"]  =bloglar.objects.filter(proje_ait_bilgisi = get_object_or_404(CustomUser,id = id),proje_santiye_Ait__silinme_bilgisi = False)
    if request.POST:
        yetkili_adi = request.POST.get("yetkili_adi")
        tarih_bilgisi = request.POST.get("tarih_bilgisi")
        aciklama = request.POST.get("aciklama")
        durumu  = request.POST.get("durumu")
        if durumu == "1":
            durumu = True
        else:
            durumu = False
        blogbilgisi = request.POST.getlist("blogbilgisi")
        new_project = projeler(
                proje_ait_bilgisi = get_object_or_404(CustomUser,id = id ),
                proje_Adi = yetkili_adi,
                tarih = tarih_bilgisi,
                aciklama = aciklama,
                durum = durumu,silinme_bilgisi = False
            )
        new_project.save()
        bloglar_bilgisi = []
        for i in blogbilgisi:
            bloglar_bilgisi.append(bloglar.objects.get(id=int(i)))
        new_project.blog_bilgisi.add(*bloglar_bilgisi)

        images = request.FILES.getlist('file')
        for images in images:
            proje_dosyalari.objects.create(dosya=images,proje_ait_bilgisi = get_object_or_404(projeler,id = new_project.id))  # Urun_resimleri modeline resimleri kaydet
        return redirect("main:projeler_sayfasi")

    return render(request,"santiye_yonetimi/proje_ekle_admin.html",content)
#Proje Ekeleme
#proje silme
def proje_silme(request):
    if request.POST:
        buttonId = request.POST.get("buttonId")
        projeler.objects.filter(id = buttonId).update(silinme_bilgisi = True)
    return redirect("main:projeler_sayfasi")

#proje silme
#proje düzenleme
def proje_duzenle_bilgi(request):
    c = request.POST
    if c:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            yetkili_adi = request.POST.get("yetkili_adi")
            tarih_bilgisi = request.POST.get("tarih_bilgisi")
            aciklama = request.POST.get("aciklama")
            durumu  = request.POST.get("durumu")
            buttonIdInput = request.POST.get("buttonId")
            if durumu == "1":
                durumu = True
            else:
                durumu = False
            blogbilgisi = request.POST.getlist("blogbilgisi")
            projeler.objects.filter(id = buttonIdInput).update(
                proje_ait_bilgisi = get_object_or_404(CustomUser,id =kullanici ),
                proje_Adi = yetkili_adi,
                tarih = tarih_bilgisi,
                aciklama = aciklama,
                durum = durumu,silinme_bilgisi = False
            )
            z = get_object_or_404(projeler,id = buttonIdInput)
            bloglar_bilgisi = []
            for i in blogbilgisi:
                bloglar_bilgisi.append(bloglar.objects.get(id=int(i)))
            z.blog_bilgisi.add(*bloglar_bilgisi)
            images = request.FILES.getlist('file')
            for images in images:
                proje_dosyalari.objects.create(dosya=images,proje_ait_bilgisi = get_object_or_404(projeler,id = buttonIdInput))  # Urun_resimleri modeline resimleri kaydet
        else:
            yetkili_adi = request.POST.get("yetkili_adi")
            tarih_bilgisi = request.POST.get("tarih_bilgisi")
            aciklama = request.POST.get("aciklama")
            durumu  = request.POST.get("durumu")
            buttonIdInput = request.POST.get("buttonId")
            if durumu == "1":
                durumu = True
            else:
                durumu = False
            blogbilgisi = request.POST.getlist("blogbilgisi")
            projeler.objects.filter(id = buttonIdInput).update(
                proje_Adi = yetkili_adi,
                tarih = tarih_bilgisi,
                aciklama = aciklama,
                durum = durumu,silinme_bilgisi = False
            )
            z = get_object_or_404(projeler,id = buttonIdInput)
            bloglar_bilgisi = []
            for i in blogbilgisi:
                bloglar_bilgisi.append(bloglar.objects.get(id=int(i)))
            z.blog_bilgisi.add(*bloglar_bilgisi)
            images = request.FILES.getlist('file')
            for images in images:
                proje_dosyalari.objects.create(dosya=images,proje_ait_bilgisi = get_object_or_404(projeler,id = buttonIdInput))  # Urun_resimleri modeline resimleri kaydet
    return redirect("main:projeler_sayfasi")
#proje düzenleme

#taseron olaylari
def taseron_sayfasi(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile =taseronlar.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = taseronlar.objects.filter(silinme_bilgisi = False,taseron_ait_bilgisi = request.user)

    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =taseronlar.objects.filter(Q(taseron_ait_bilgisi__last_name__icontains = search)|Q(taseron_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = taseronlar.objects.filter(Q(taseron_ait_bilgisi = request.user) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 10) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    return render(request,"santiye_yonetimi/taseronlar.html",content)
#taseron olaylari


def taseron_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            return redirect("main:taseron_ekle_admin",kullanici)
        else:
            taseron_adi = request.POST.get("taseron_adi")
            telefonnumarasi = request.POST.get("telefonnumarasi")
            email_adresi = request.POST.get("email_adresi")
            blogbilgisi = request.POST.getlist("blogbilgisi")
            aciklama = request.POST.get("aciklama")
            new_project = taseronlar(
                taseron_ait_bilgisi = request.user,
                taseron_adi = taseron_adi,
                email = email_adresi,
                aciklama = aciklama,
                telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
            )
            new_project.save()
            bloglar_bilgisi = []
            for i in blogbilgisi:
                bloglar_bilgisi.append(projeler.objects.get(id=int(i)))
            new_project.proje_bilgisi.add(*bloglar_bilgisi)
            images = request.FILES.getlist('file')
            isim = 1
            for images in images:
                taseron_sozlesme_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(taseronlar,id = new_project.id))  # Urun_resimleri modeline resimleri kaydet
                isim = isim+1
            car = cari.objects.create(
                cari_kart_ait_bilgisi = request.user,
                cari_adi = taseron_adi,
                telefon_numarasi = telefonnumarasi,
                aciklama = aciklama
            )
            cari_taseron_baglantisi.objects.create(
                gelir_kime_ait_oldugu = get_object_or_404(taseronlar,id = new_project.id ),
                cari_bilgisi = get_object_or_404(cari,id = car.id)
            )
    return redirect("main:taseron_sayfasi")
def taseron_ekle_admin(request,id):
    content = sozluk_yapisi()
    content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi__id = id,silinme_bilgisi = False)
    if request.POST:
        if True:
            taseron_adi = request.POST.get("taseron_adi")
            telefonnumarasi = request.POST.get("telefonnumarasi")
            email_adresi = request.POST.get("email_adresi")
            blogbilgisi = request.POST.getlist("blogbilgisi")
            aciklama = request.POST.get("aciklama")
            new_project = taseronlar(
                taseron_ait_bilgisi = get_object_or_404(CustomUser,id = id),
                taseron_adi = taseron_adi,
                email = email_adresi,
                aciklama = aciklama,
                telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
            )
            new_project.save()
            bloglar_bilgisi = []
            for i in blogbilgisi:
                bloglar_bilgisi.append(projeler.objects.get(id=int(i)))
            new_project.proje_bilgisi.add(*bloglar_bilgisi)
            images = request.FILES.getlist('file')
            isim = 1
            for images in images:
                taseron_sozlesme_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(taseronlar,id = new_project.id))  # Urun_resimleri modeline resimleri kaydet
                isim = isim+1
            car = cari.objects.create(
                cari_kart_ait_bilgisi = get_object_or_404(CustomUser,id = id),
                cari_adi = taseron_adi,
                telefon_numarasi = telefonnumarasi,
                aciklama = aciklama
            )
            cari_taseron_baglantisi.objects.create(
                gelir_kime_ait_oldugu = get_object_or_404(taseronlar,id = new_project.id ),
                cari_bilgisi = get_object_or_404(cari,id = car.id)
            )
        return redirect("main:taseron_sayfasi")
    return render(request,"santiye_yonetimi/admin_taseron_ekle.html",content)
#proje silme
def taseron_silme(request):
    if request.POST:
        buttonId = request.POST.get("buttonId")
        taseronlar.objects.filter(id = buttonId).update(silinme_bilgisi = True)
    return redirect("main:taseron_sayfasi")
#taşeron Düzenleme

def taseron_duzelt(request):
    if request.POST:
        if request.user.is_superuser:
            id_bilgisi = request.POST.get("id_bilgisi")
            taseron_adi = request.POST.get("taseron_adi")
            telefonnumarasi = request.POST.get("telefonnumarasi")
            email_adresi = request.POST.get("email_adresi")
            blogbilgisi = request.POST.getlist("blogbilgisi")
            aciklama = request.POST.get("aciklama")
            silinmedurumu = request.POST.get("silinmedurumu")
            if silinmedurumu == "1":
                taseronlar.objects.filter(id =id_bilgisi ).update(
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                )
            elif silinmedurumu == "2":
                taseronlar.objects.filter(id =id_bilgisi ).update(
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi,silinme_bilgisi = True
                )
            else:
                taseronlar.objects.filter(id =id_bilgisi ).update(
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi
                )
            bloglar_bilgisi = []
            for i in blogbilgisi:
                bloglar_bilgisi.append(projeler.objects.get(id=int(i)))
            get_object_or_404(taseronlar,id =id_bilgisi).proje_bilgisi.add(*bloglar_bilgisi)
            images = request.FILES.getlist('file')
            isim = 1
            for images in images:
                taseron_sozlesme_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(taseronlar,id = id_bilgisi))  # Urun_resimleri modeline resimleri kaydet
                isim = isim+1
        else:

            id_bilgisi = request.POST.get("id_bilgisi")
            taseron_adi = request.POST.get("taseron_adi")
            telefonnumarasi = request.POST.get("telefonnumarasi")
            email_adresi = request.POST.get("email_adresi")
            blogbilgisi = request.POST.getlist("blogbilgisi")
            aciklama = request.POST.get("aciklama")
            new_project = taseronlar.objects.filter(id =id_bilgisi ).update(
                taseron_adi = taseron_adi,
                email = email_adresi,
                aciklama = aciklama,
                telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
            )
            bloglar_bilgisi = []
            for i in blogbilgisi:
                bloglar_bilgisi.append(projeler.objects.get(id=int(i)))
            get_object_or_404(taseronlar,id =id_bilgisi).proje_bilgisi.add(*bloglar_bilgisi)
            images = request.FILES.getlist('file')
            isim = 1
            for images in images:
                taseron_sozlesme_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(taseronlar,id = id_bilgisi))  # Urun_resimleri modeline resimleri kaydet
                isim = isim+1
    return redirect("main:taseron_sayfasi")

#proje silme


#sözleşmeler
#sözleşme olaylari
def sozlesmler_sayfasi(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile = taseron_sozlesme_dosyalari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = taseron_sozlesme_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user)

    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =taseron_sozlesme_dosyalari.objects.filter(Q(taseron_ait_bilgisi__proje_ait_bilgisi__last_name__icontains = search)|Q(taseron_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = taseron_sozlesme_dosyalari.objects.filter(Q(taseron_ait_bilgisi = request.user) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 10) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user,silinme_bilgisi = False)
    return render(request,"santiye_yonetimi/sozlesmler.html",content)
#sözleşme olaylari

def sozlesme_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            return redirect("main:sozlesme_ekle_admin",kullanici)
        else:
            taseron = request.POST.get("taseron")
            dosyaadi = request.POST.get("dosyaadi")
            tarih = request.POST.get("tarih")
            aciklama = request.POST.get("aciklama")
            durumu = request.POST.get("durumu")
            file = request.FILES.get("file")
            if durumu == "1":
                durumu = True
            else:
                durumu = False
            taseron_sozlesme_dosyalari.objects.create(
                proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                dosya = file,dosya_adi = dosyaadi,
                tarih = tarih,aciklama = aciklama,
                durum = durumu
            )
    return redirect("main:sozlesmler_sayfasi")
def sozlesme_ekle_admin(request,id):
    content = sozluk_yapisi()
    content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi__id= id,silinme_bilgisi = False)
    if request.POST:
        if True:
            taseron = request.POST.get("taseron")
            dosyaadi = request.POST.get("dosyaadi")
            tarih = request.POST.get("tarih")
            aciklama = request.POST.get("aciklama")
            durumu = request.POST.get("durumu")
            file = request.FILES.get("file")
            if durumu == "1":
                durumu = True
            else:
                durumu = False
            taseron_sozlesme_dosyalari.objects.create(
                proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                dosya = file,dosya_adi = dosyaadi,
                tarih = tarih,aciklama = aciklama,
                durum = durumu
            )
        return redirect("main:sozlesmler_sayfasi")
    return render(request,"santiye_yonetimi/admin_sozlesme_ekle.html",content)
#sözleşme düzenleme

def sozlesme_duzenle(request):
    if request.POST:
        id_bilgisi = request.POST.get("id_bilgisi")
        taseron = request.POST.get("taseron")
        dosyaadi = request.POST.get("dosyaadi")
        tarih = request.POST.get("tarih")
        aciklama = request.POST.get("aciklama")
        durumu = request.POST.get("durumu")
        file = request.FILES.get("file")
        if durumu == "1":
            durumu = True
        else:
            durumu = False
        if request.user.is_superuser:
            silinmedurumu = request.POST.get("silinmedurumu")
            if silinmedurumu == "3":
                taseron_sozlesme_dosyalari.objects.filter(id = id_bilgisi).update(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                    dosya = file,dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu
                )
            elif silinmedurumu == "2":
                taseron_sozlesme_dosyalari.objects.filter(id = id_bilgisi).update(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                    dosya = file,dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu,silinme_bilgisi = True
                )
            elif silinmedurumu == "1":
                taseron_sozlesme_dosyalari.objects.filter(id = id_bilgisi).update(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                    dosya = file,dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu,silinme_bilgisi = False
                )
        else:

            taseron_sozlesme_dosyalari.objects.filter(id = id_bilgisi).update(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                    dosya = file,dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu
                )
    return redirect("main:sozlesmler_sayfasi")

#sözleşmeler sil
def sozlesme_silme(request):
    if request.POST:
        buttonId = request.POST.get("buttonId")
        taseron_sozlesme_dosyalari.objects.filter(id = buttonId).update(silinme_bilgisi = True)
    return redirect("main:sozlesmler_sayfasi")

#sözleşmeler sil
#sözleşmeler
#hakedişler
def hakedis_sayfasi(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile = taseron_hakedisles.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = taseron_hakedisles.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user)

    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =taseron_hakedisles.objects.filter(Q(proje_ait_bilgisi__taseron_ait_bilgisi__last_name__icontains = search)|Q(dosya_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = taseron_hakedisles.objects.filter(Q(proje_ait_bilgisi__taseron_ait_bilgisi = request.user) & Q(proje_ait_bilgisi__taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 10) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user,silinme_bilgisi = False)
    return render(request,"santiye_yonetimi/hakedis.html",content)

def hakedis_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            return redirect("main:hakedis_ekle_admin",kullanici)
        else:
            taseron = request.POST.get("taseron")
            dosyaadi = request.POST.get("yetkili_adi")
            tarih = request.POST.get("tarih_bilgisi")
            aciklama = request.POST.get("aciklama")
            durumu = request.POST.get("durumu")
            file = request.FILES.get("file")
            tutar = request.POST.get("tutar")
            fatura_no = request.POST.get("fatura_no")
            if durumu == "1":
                durumu = True
            else:
                durumu = False
            taseron_hakedisles.objects.create(
                proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                dosya = file,
                dosya_adi = dosyaadi,
                tarih = tarih,aciklama = aciklama,
                durum = durumu,
                tutar = tutar,
                fatura_numarasi = fatura_no
            )
    return redirect("main:hakedis_sayfasi")
#hakedisekle
def hakedis_silme(request):
    if request.POST:
        buttonId = request.POST.get("buttonId")
        taseron_hakedisles.objects.filter(id = buttonId).update(silinme_bilgisi = True)
    return redirect("main:hakedis_sayfasi")

def hakedis_ekle_admin(request,id):
    content = sozluk_yapisi()
    content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi__id= id,silinme_bilgisi = False)
    if request.POST:
        if request.user.is_superuser:
            taseron = request.POST.get("taseron")
            dosyaadi = request.POST.get("yetkili_adi")
            tarih = request.POST.get("tarih_bilgisi")
            aciklama = request.POST.get("aciklama")
            durumu = request.POST.get("durumu")
            file = request.FILES.get("file")
            tutar = request.POST.get("tutar")
            fatura_no = request.POST.get("fatura_no")
            if durumu == "1":
                durumu = True
            else:
                durumu = False
            taseron_hakedisles.objects.create(
                proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                dosya = file,
                dosya_adi = dosyaadi,
                tarih = tarih,aciklama = aciklama,
                durum = durumu,
                tutar = tutar,
                fatura_numarasi = fatura_no
            )
        return redirect("main:hakedis_sayfasi")
    return render(request,"santiye_yonetimi/hakedis_admin_ekle.html",content)

#hakediş düzenle
def hakedis_duzenle(request):
    if request.POST:
        if request.user.is_superuser:
            buttonId = request.POST.get("buttonId")
            taseron = request.POST.get("taseron")
            dosyaadi = request.POST.get("yetkili_adi")
            tarih = request.POST.get("tarih_bilgisi")
            aciklama = request.POST.get("aciklama")
            durumu = request.POST.get("durumu")
            file = request.FILES.get("file")
            tutar = request.POST.get("tutar")
            fatura_no = request.POST.get("fatura_no")
            silinmedurumu = request.POST.get("silinmedurumu")
            if durumu == "1":
                durumu = True
            else:
                durumu = False
            if silinmedurumu == "3":
                taseron_hakedisles.objects.filter(id=buttonId).update(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                    dosya = file,
                    dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu,
                    tutar = tutar,
                    fatura_numarasi = fatura_no
                )
            elif silinmedurumu == "2":
                taseron_hakedisles.objects.filter(id=buttonId).update(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                    dosya = file,
                    dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu,
                    tutar = tutar,
                    fatura_numarasi = fatura_no,silinme_bilgisi = True
                )
            elif silinmedurumu == "1":
                taseron_hakedisles.objects.filter(id=buttonId).update(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                    dosya = file,
                    dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu,
                    tutar = tutar,
                    fatura_numarasi = fatura_no,silinme_bilgisi = False
                )

        else:
            buttonId = request.POST.get("buttonId")
            taseron = request.POST.get("taseron")
            dosyaadi = request.POST.get("yetkili_adi")
            tarih = request.POST.get("tarih_bilgisi")
            aciklama = request.POST.get("aciklama")
            durumu = request.POST.get("durumu")
            file = request.FILES.get("file")
            tutar = request.POST.get("tutar")
            fatura_no = request.POST.get("fatura_no")
            if durumu == "1":
                durumu = True
            else:
                durumu = False
            taseron_hakedisles.objects.filter(id=buttonId).update(
                proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                dosya = file,
                dosya_adi = dosyaadi,
                tarih = tarih,aciklama = aciklama,
                durum = durumu,
                tutar = tutar,
                fatura_numarasi = fatura_no
            )
    return redirect("main:hakedis_sayfasi")


def depolama_sistemim(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile = klasorler.objects.all()

    else:
        profile = klasorler.objects.filter(klasor_adi_db = None).filter(silinme_bilgisi = False,dosya_sahibi = request.user)

    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(klasor_adi_db = None).filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = klasorler.objects.filter(klasor_adi_db = None).filter(Q(dosya_sahibi = request.user) & Q(klasor_adi__icontains = search)& Q(silinme_bilgisi = False))
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 25) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/depolama_sistemim.html",content)



def klasor_olustur(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:
            ust_klasor = request.POST.get("ust_klasor")
            if ust_klasor:
                klasor = request.POST.get("klasor")

                klasorler.objects.create(
                    dosya_sahibi = request.user,
                    klasor_adi = klasor,
                    klasor_adi_db = get_object_or_404(klasorler,id =ust_klasor )
                )
            else:
                klasor = request.POST.get("klasor")

                klasorler.objects.create(
                    dosya_sahibi = request.user,
                    klasor_adi = klasor
                )
    return redirect("main:depolama_sistemim")

def klasor__yeniden_adlandir(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:
            klasor = request.POST.get("klasor")
            idbilgisi = request.POST.get("idbilgisi")
            klasorler.objects.filter(id = idbilgisi).update(
                dosya_sahibi = request.user,
                klasor_adi = klasor
            )
    return redirect("main:depolama_sistemim")

def klasor_sil(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:
            idbilgisi = request.POST.get("idbilgisi")
            klasorler.objects.filter(id = idbilgisi).update(
                silinme_bilgisi = True
            )
    return redirect("main:depolama_sistemim")

#klasöre Gir
def klasore_gir(request,id,slug):
    content = sozluk_yapisi()
    content["id_bilgisi"] = id
    if super_admin_kontrolu(request):
        profile = klasorler.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = klasorler.objects.filter(klasor_adi_db__id =id,silinme_bilgisi = False,dosya_sahibi = request.user)
        dosyalarim = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user,proje_ait_bilgisi__id =id)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = klasorler.objects.filter(klasor_adi_db__id =id).filter(Q(dosya_sahibi = request.user) & Q(klasor_adi__icontains = search)& Q(silinme_bilgisi = False))
            dosyalarim = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user,proje_ait_bilgisi__id =id).filter(__icontains = search)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 25) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    content["dosyalarim"] = dosyalarim
    return render(request,"santiye_yonetimi/klasorici.html",content)
#klasöre Gir


#klasore Dosya Ekle
def dosya_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:

            ust_klasor = request.POST.get("ust_klasor")
            dosya_Adi = request.POST.get("klasor")
            tarih = request.POST.get("tarih")
            aciklama = request.POST.get("aciklama")
            dosya = request.FILES.get("file")

            klasor_dosyalari.objects.create(
                dosya_sahibi=request.user,
                proje_ait_bilgisi=get_object_or_404(klasorler, id=ust_klasor),
                dosya=dosya,
                dosya_adi=dosya_Adi,
                tarih=tarih,
                aciklama=aciklama
            )
    z = "/storage/mydir/"+str(ust_klasor)+"/"+str(get_object_or_404(klasorler,id = ust_klasor).klasor_adi)+"/"
    return redirect(z)

#klasore Dosya Ekle

#dosya_ sil
def dosya_sil(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:

            ust_klasor = request.POST.get("ust_klasor")
            dosya_Adi = request.POST.get("klasor")

            klasor_dosyalari.objects.filter(id = dosya_Adi).update(silinme_bilgisi = True)
    if ust_klasor:
        z = "/storage/mydir/"+str(ust_klasor)+"/"+str(get_object_or_404(klasorler,id = ust_klasor).klasor_adi)+"/"
        return redirect(z)
    else:
        return redirect("main:depolama_sistemim")
def dosya_geri_getir(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:

            ust_klasor = request.POST.get("ust_klasor")
            dosya_Adi = request.POST.get("klasor")

            klasor_dosyalari.objects.filter(id = dosya_Adi).update(silinme_bilgisi = False)
    return redirect("main:silinen_dosyalari")
#dosya_sil
from functools import reduce
import operator
#dokumanlari_gosterme
def dokumanlar(request):
    dosya_turu = [".xlsx",".pdf",".xlx",".txt",".docx",".doc",".ppt",".pptx"]
    content = sozluk_yapisi()
    content["id_bilgisi"] = id
    if super_admin_kontrolu(request):
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user).filter(reduce(operator.or_, (Q(dosya__icontains = x) for x in dosya_turu)))
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user).filter(__icontains = search)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 25) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/dokuman.html",content)

#dokumanlari_gosterme

#media
def media_dosyalari(request):
    dosya_turu = [".jpg",".jpeg",".png",".ico",".css",".JFIF",".GIF",".WEBP"]
    content = sozluk_yapisi()
    content["id_bilgisi"] = id
    if super_admin_kontrolu(request):
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user).filter(reduce(operator.or_, (Q(dosya__icontains = x) for x in dosya_turu)))
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user).filter(__icontains = search)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 25) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/dokuman.html",content)


#media
#zamana göre

def zamana_dosyalari(request):

    content = sozluk_yapisi()
    content["id_bilgisi"] = id
    if super_admin_kontrolu(request):
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user).order_by("-id")
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user).filter(__icontains = search)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 25) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/dokuman.html",content)

#zamana göre

def silinen_dosyalari(request):

    content = sozluk_yapisi()
    content["id_bilgisi"] = id
    if super_admin_kontrolu(request):
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = True,dosya_sahibi = request.user).order_by("-id")
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = klasor_dosyalari.objects.filter(silinme_bilgisi = True,dosya_sahibi = request.user).filter(__icontains = search)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 25) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/dokuman.html",content)

#dokumanlari_gosterme

def yapilacaklar(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile = IsplaniPlanlari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = IsplaniPlanlari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)

    if request.GET:
        siralama = request.GET.get("siralama")
        status = request.GET.get("status")
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =IsplaniPlanlari.objects.filter(Q(proje_ait_bilgisi__last_name__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = IsplaniPlanlari.objects.filter(Q(proje_ait_bilgisi = request.user) & Q(silinme_bilgisi = False))
        if status:
            profile = profile.filter(status = status)
        if search:
            profile = profile.filter(title__icontains=search )
        if siralama == "1":
            profile = profile.order_by("-id")
        elif siralama == "2":
            profile = profile.order_by("-title")
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 10) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    content["blog_bilgisi"]  =CustomUser.objects.filter(kullanicilar_db = request.user,kullanici_silme_bilgisi = False,is_active = True)
    return render(request,"santiye_yonetimi/yapilacaklar.html",content)
#yapilacakalr

def yapilacalar_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:
            baslik = request.POST.get("baslik")
            durum = request.POST.get("durum")
            aciliyet =request.POST.get("aciliyet")
            teslim_tarihi = request.POST.get("teslim_tarihi")
            blogbilgisi = request.POST.getlist("blogbilgisi")
            aciklama = request.POST.get("aciklama")
            new_project = IsplaniPlanlari(
                proje_ait_bilgisi = request.user,
                title = baslik,
                status = durum,
                aciklama = aciklama,
                oncelik_durumu =aciliyet,
                teslim_tarihi = teslim_tarihi,silinme_bilgisi = False
            )
            new_project.save()
            bloglar_bilgisi = []
            for i in blogbilgisi:
                bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
            new_project.yapacaklar.add(*bloglar_bilgisi)
            images = request.FILES.getlist('file')
            isim = 1
            for images in images:
                IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                isim = isim+1
    return redirect("main:yapilacaklar")
def yapilacalar_ekle_toplu(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:
            baslik = request.POST.get("baslik")
            durum = request.POST.get("durum")
            aciliyet =request.POST.get("aciliyet")
            teslim_tarihi = request.POST.get("teslim_tarihi")
            blogbilgisi = request.POST.getlist("blogbilgisi")
            aciklama = request.POST.getlist("aciklama")
            for i in range(0,len(aciklama)):
                if aciklama[i]:
                    new_project = IsplaniPlanlari(
                        proje_ait_bilgisi = request.user,
                        title = baslik,
                        status = durum,
                        aciklama = aciklama[i],
                        oncelik_durumu =aciliyet,
                        teslim_tarihi = teslim_tarihi,silinme_bilgisi = False
                    )
                    new_project.save()
                    bloglar_bilgisi = []
                    for i in blogbilgisi:
                        bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
                    new_project.yapacaklar.add(*bloglar_bilgisi)
                    images = request.FILES.getlist('file')
                    isim = 1
                    for images in images:
                        IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                        isim = isim+1
    return redirect("main:yapilacaklar")

def yapilacalar_sil(request):
    if request.POST:
        id = request.POST.get("id_bilgisi")
        IsplaniPlanlari.objects.filter(id = id).update(silinme_bilgisi = True)
    return redirect("main:yapilacaklar")

def yapilacak_durumu_yenileme(request):
    if request.POST:
        yenilenecekeklemeyapilacak = request.POST.get("yenilenecekeklemeyapilacak")
        aciklama = request.POST.get("aciklama")
        durum  =request.POST.get("durum")
        teslim_tarihi  =request.POST.get("teslim_tarihi")
        new_project = IsplaniPlanlariIlerleme(
                proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id =yenilenecekeklemeyapilacak ),
                status = durum,
                aciklama = aciklama,
                teslim_tarihi = teslim_tarihi,silinme_bilgisi = False,
                yapan_kisi = request.user
            )
        new_project.save()
        images = request.FILES.getlist('file')
        isim = 1
        for images in images:
            IsplaniIlerlemeDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlariIlerleme,id = new_project.id),yapan_kisi = request.user,dosya=images,dosya_sahibi = get_object_or_404(IsplaniPlanlari,id =yenilenecekeklemeyapilacak))  # Urun_resimleri modeline resimleri kaydet
            isim = isim+1
    return redirect("main:yapilacaklar")
def yapilacalar_duzenle(request):
    if request.POST:
        if request.user.superuser:
            pass
        else:
            id = request.POSt.get("id_bilgisi")
            baslik = request.POST.get("baslik")
            durum = request.POST.get("durum")
            aciliyet =request.POST.get("aciliyet")
            teslim_tarihi = request.POST.get("teslim_tarihi")
            blogbilgisi = request.POST.getlist("blogbilgisi")
            aciklama = request.POST.get("aciklama")
            new_project = IsplaniPlanlari.objects.filter(id = id).update(
                proje_ait_bilgisi = request.user,
                title = baslik,
                status = durum,
                aciklama = aciklama,
                oncelik_durumu =aciliyet,
                teslim_tarihi = teslim_tarihi,silinme_bilgisi = False
            )
            new_project.save()
            bloglar_bilgisi = []
            for i in blogbilgisi:
                bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
            new_project.yapacaklar.add(*bloglar_bilgisi)
            images = request.FILES.getlist('file')
            isim = 1
            for images in images:
                IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                isim = isim+1
    return redirect("main:yapilacaklar")

#time_lline
def yapilacaklar_timeline(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile = YapilacakPlanlari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = YapilacakPlanlari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user).order_by("teslim_tarihi")

    if request.GET:
        siralama = request.GET.get("siralama")
        status = request.GET.get("status")
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =YapilacakPlanlari.objects.filter(Q(proje_ait_bilgisi__last_name__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = YapilacakPlanlari.objects.filter(Q(proje_ait_bilgisi = request.user) & Q(silinme_bilgisi = False))
        if status:
            profile = profile.filter(status = status)
        if search:
            profile = profile.filter(title__icontains=search )
        if siralama == "1":
            profile = profile.order_by("-id")
        elif siralama == "2":
            profile = profile.order_by("-title")
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 10) # 6 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    content["blog_bilgisi"]  =CustomUser.objects.filter(kullanicilar_db = request.user,kullanici_silme_bilgisi = False,is_active = True)
    return render(request,"santiye_yonetimi/time_line.html",content)

def yapilacalar_time_line_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:
            baslik = request.POST.get("baslik")
            durum = request.POST.get("durum")
            aciliyet =request.POST.get("aciliyet")
            teslim_tarihi = request.POST.get("teslim_tarihi")
            blogbilgisi = request.POST.getlist("blogbilgisi")
            aciklama = request.POST.get("aciklama")
            new_project = YapilacakPlanlari(
                proje_ait_bilgisi = request.user,
                title = baslik,
                status = durum,
                aciklama = aciklama,
                oncelik_durumu =aciliyet,
                teslim_tarihi = teslim_tarihi,silinme_bilgisi = False
            )
            new_project.save()
            bloglar_bilgisi = []
            for i in blogbilgisi:
                bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
            new_project.yapacaklar.add(*bloglar_bilgisi)
            images = request.FILES.getlist('file')
            isim = 1
            for images in images:
                YapilacakDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(YapilacakPlanlari,id = new_project.id),dosya_sahibi = request.user,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                isim = isim+1
    return redirect("main:yapilacaklar_timeline")


def yapilacalar_time_line_sil(request):
    if request.POST:
        id = request.POST.get("buttonId")
        YapilacakPlanlari.objects.filter(id = id).update(silinme_bilgisi = True)
    return redirect("main:yapilacaklar_timeline")
#yapilacakalr
def yapilacalar_time_line_duzenle(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:
            id = request.POST.get("id")
            baslik = request.POST.get("baslik")
            durum = request.POST.get("durum")
            aciliyet =request.POST.get("aciliyet")
            teslim_tarihi = request.POST.get("teslim_tarihi")
            blogbilgisi = request.POST.getlist("blogbilgisi")
            aciklama = request.POST.get("aciklama")
            new_project = YapilacakPlanlari.objects.filter(id = id).update(
                proje_ait_bilgisi = request.user,
                title = baslik,
                status = durum,
                aciklama = aciklama,
                oncelik_durumu =aciliyet,
                teslim_tarihi = teslim_tarihi,silinme_bilgisi = False
            )
            bloglar_bilgisi = []
            for i in blogbilgisi:
                bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
            get_object_or_404(YapilacakPlanlari,id = id).yapacaklar.add(*bloglar_bilgisi)
            images = request.FILES.getlist('file')
            isim = 1
            for images in images:
                YapilacakDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(YapilacakPlanlari,id = new_project.id),dosya_sahibi = request.user,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                isim = isim+1
    return redirect("main:yapilacaklar_timeline")

from .utils import *
from django.utils.safestring import mark_safe
def takvim_olaylari(request):
    content = sozluk_yapisi()
    su_an = datetime.today()
    cal = Calendar(su_an.year, su_an.month)
    html_cal = cal.formatmonth(withyear=True)
    content["takvim_gelicek"] = mark_safe(html_cal)
    return render(request,"santiye_yonetimi/takvim.html",content)
#takvim


def santiye_raporu(request,id):
    content = sozluk_yapisi()

    profile =  get_object_or_404(bloglar,proje_ait_bilgisi = request.user,id = id )
    content["santiye"] = profile
    return render(request,"santiye_yonetimi/santiye_raporu.html",content)


def cari_history_view(request, cari_id):
    cari_instance = cari.objects.get(id=cari_id)
    history = cari_instance.history.all()
    return render(request, 'cari_history.html', {'history': history})
def get_object_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except :
        return None
def giderleri_excelden_ekle(request,id):
    import openpyxl
    
    Gider_excel_ekl = get_object_or_404(Gider_excel_ekleme,id = id)
    dataframe = openpyxl.load_workbook(Gider_excel_ekl.gelir_makbuzu)
    dataframe1 = dataframe.active
    data = []
    sadece_cari = []
    sadece_etiket = []
    sadece_kategorisi = []
    sadece_urunler = []
    sadece_fiyat = []
    sozluk_cari ={}
    sozluk_etiket = {}
    sozluk_kategorisi = {}
    sozluk_urun = {}
    for row in range(1, dataframe1.max_row):
        a = []
        a.append(row + 1)
        for col in dataframe1.iter_cols(1, dataframe1.max_column):
            a.append(col[row].value)
        data.append(a)
        print(a)
    print("-" * 50)
    for i in data:
        if i[3] not in sadece_cari:
            sadece_cari.append(i[3])
        if i[4] not in sadece_fiyat:
            y = float((str(str(str(i[4]).replace("$",""))).replace(".","")).replace(",","."))
            sadece_fiyat.append(y)
        if i[5] not in sadece_urunler:
            sadece_urunler.append(i[5])
        if i[6] not in sadece_etiket:
            sadece_etiket.append(i[6])
        if i[7] not in sadece_etiket:
            sadece_etiket.append(i[7])
        if i[8] not in sadece_etiket:
            sadece_etiket.append(i[8])
        if i[9] not in sadece_kategorisi:
            sadece_kategorisi.append(i[9])
    for i in sadece_cari:
        l = cari.objects.create(cari_kart_ait_bilgisi = Gider_excel_ekl.gelir_kime_ait_oldugu
                ,cari_adi = i,aciklama = "",telefon_numarasi = 0.0)
        sozluk_cari[i] = l.id
    k = 0
    for i in sadece_urunler:
        l = urunler.objects.create(urun_ait_oldugu = Gider_excel_ekl.gelir_kime_ait_oldugu
                                ,urun_adi = i,urun_fiyati = sadece_fiyat[k]

                                )
        print(i)
        k = k+1
        sozluk_urun[i] = l.id
    for i in sadece_kategorisi:
        z = gider_kategorisi.objects.create(gider_kategoris_ait_bilgisi = Gider_excel_ekl.gelir_kime_ait_oldugu
                                            ,gider_kategori_adi = i,gider_kategorisi_renk = "#000000",aciklama = "")
        sozluk_kategorisi[i] = z.id
    for i in sadece_etiket:
        z = gider_etiketi.objects.create(gider_kategoris_ait_bilgisi = Gider_excel_ekl.gelir_kime_ait_oldugu
                                         ,gider_etiketi_adi = i)
        sozluk_etiket[i] = z.id
    y = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = Gider_excel_ekl.gelir_kime_ait_oldugu).count()
    for i in data:
        y = y+1
        b = len(str(y))
        c = 8 - b
        m = faturalardaki_gelir_gider_etiketi.objects.last().gider_etiketi+(c*"0")+str(y)
        new_project =Gider_Bilgisi.objects.create(gelir_kime_ait_oldugu = Gider_excel_ekl.gelir_kime_ait_oldugu,
            cari_bilgisi = get_object_or_none(cari,id = sozluk_cari[i[3]]),
            fatura_tarihi=i[2],vade_tarihi=i[2],fatura_no = m,
            gelir_kategorisi = get_object_or_none( gider_kategorisi,id =sozluk_kategorisi[i[8]] ),doviz = i[11],aciklama = i[10]
                                         )
        print(sozluk_cari[i[3]])
        new_project.save()
        gelir_etiketi_sec = []
        gelir_etiketi_sec.append(gider_etiketi.objects.get(id=int(sozluk_etiket[i[5]])))
        gelir_etiketi_sec.append(gider_etiketi.objects.get(id=int(sozluk_etiket[i[6]])))
        new_project.gelir_etiketi_sec.add(*gelir_etiketi_sec)
        #bilgi_getirler = urunler.objects.create(urun_ait_oldugu =  Gider_excel_ekl.gelir_kime_ait_oldugu,urun_adi = sozluk_urun[i[5]],urun_fiyati = float((str(str(str(i[4]).replace("$",""))).replace(".","")).replace(",",".")))
        gider_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  Gider_excel_ekl.gelir_kime_ait_oldugu,urun_bilgisi = get_object_or_404(urunler, 
                            id = sozluk_urun[i[5]]),
                            urun_fiyati = float((str(str(str(i[4]).replace("$",""))).replace(".","")).replace(",",".")),urun_indirimi = 0.0,urun_adeti = 1,
                            gider_bilgis =  get_object_or_404(Gider_Bilgisi,id = new_project.id),
                            aciklama = "")
        bir = Gider_odemesi.objects.create(gelir_kime_ait_oldugu = get_object_or_404(Gider_Bilgisi,id = new_project.id ),kasa_bilgisi = Gider_excel_ekl.kasa,
                                     tutar =float((str(str(str(i[4]).replace("$",""))).replace(".","")).replace(",",".")),tarihi =i[2],
                                       aciklama = "",makbuz_no =str(i[13] ) ,gelir_makbuzu = str(i[12] ) )
        bir.set_gelir_makbuzu(str(i[13] ))
        gider_qr.objects.create(gelir_kime_ait_oldugu = get_object_or_404(Gider_Bilgisi,id = new_project.id))
    return redirect("/")

def gelirleri_excelden_ekle(request,id):
    import openpyxl
    Gider_excel_ekl = get_object_or_404(Gelir_excel_ekleme,id = id)
    dataframe = openpyxl.load_workbook(Gider_excel_ekl.gelir_makbuzu)
    dataframe1 = dataframe.active
    data = []
    sadece_cari = []
    sadece_etiket = []
    sadece_kategorisi = []
    sadece_urunler = []
    sadece_fiyat = []
    sozluk_cari ={}
    sozluk_etiket = {}
    sozluk_kategorisi = {}
    sozluk_urun = {}
    for row in range(1, dataframe1.max_row):
        a = []
        a.append(row + 1)
        for col in dataframe1.iter_cols(1, dataframe1.max_column):
            a.append(col[row].value)
        data.append(a)
        print(a)
    print("-" * 50)
    for i in data:
        if i[3] not in sadece_cari:
            sadece_cari.append(i[3])
        if i[4] not in sadece_fiyat:
            y = float(str(str(i[4]).replace("$","")).replace(",","."))
            sadece_fiyat.append(y)
        if i[5] not in sadece_urunler:
            sadece_urunler.append(i[5])
        if i[6] not in sadece_etiket:
            sadece_etiket.append(i[6])
        if i[7] not in sadece_etiket:
            sadece_etiket.append(i[7])
        if i[8] not in sadece_kategorisi:
            sadece_kategorisi.append(i[8])
    for i in sadece_cari:
        z = cari.objects.create(cari_kart_ait_bilgisi = Gider_excel_ekl.gelir_kime_ait_oldugu
                ,cari_adi = i,aciklama = "",telefon_numarasi = 0.0)
        sozluk_cari[i] = z.id
    k = 0
    for i in sadece_urunler:
        z = urunler.objects.create(urun_ait_oldugu = Gider_excel_ekl.gelir_kime_ait_oldugu
                                ,urun_adi = i,urun_fiyati = sadece_fiyat[k]

                                )
        k = k+1
        sozluk_urun[i] = z.id
    for i in sadece_kategorisi:
        z = gelir_kategorisi.objects.create(gider_kategoris_ait_bilgisi = Gider_excel_ekl.gelir_kime_ait_oldugu
                                            ,gider_kategori_adi = i,gider_kategorisi_renk = "#000000",aciklama = "")
        sozluk_kategorisi[i] = z.id
    for i in sadece_etiket:
        z = gelir_etiketi.objects.create(gider_kategoris_ait_bilgisi = Gider_excel_ekl.gelir_kime_ait_oldugu
                                         ,gider_etiketi_adi = i)
        sozluk_etiket[i] = z.id
    y = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = Gider_excel_ekl.gelir_kime_ait_oldugu).count()
    for i in data:
        y = y+1
        b = len(str(y))
        c = 8 - b
        m = faturalardaki_gelir_gider_etiketi.objects.last().gelir_etiketi+(c*"0")+str(y)
        new_project =Gider_Bilgisi.objects.create(gelir_kime_ait_oldugu = Gider_excel_ekl.gelir_kime_ait_oldugu,
            cari_bilgisi = get_object_or_none(cari,cari_adi = sozluk_cari[i[3]],cari_kart_ait_bilgisi = request.user),
            fatura_tarihi=i[2],vade_tarihi=i[2],fatura_no = m,
            gelir_kategorisi = get_object_or_none( gelir_kategorisi,id =sozluk_kategorisi[i[8]] ),doviz = i[10],aciklama = i[9]
                                         )
        new_project.save()
        gelir_etiketi_sec = []
        gelir_etiketi_sec.append(gelir_etiketi.objects.get(id=int(sozluk_etiket[i[5]])))
        gelir_etiketi_sec.append(gelir_etiketi.objects.get(id=int(sozluk_etiket[i[6]])))
        new_project.gelir_etiketi_sec.add(*gelir_etiketi_sec)
        gelir_urun_bilgisi_bi = gelir_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  Gider_excel_ekl.gelir_kime_ait_oldugu,urun_bilgisi = get_object_or_none(urunler, urun_ait_oldugu=Gider_excel_ekl.gelir_kime_ait_oldugu,urun_adi = sozluk_urun[i[5]]),
                            urun_fiyati = float(str(str(i[4]).replace("$","")).replace(",",".")),urun_indirimi = 0.0,urun_adeti = 1,
                            gider_bilgis =  get_object_or_none(Gelir_Bilgisi,id = new_project.id),
                            aciklama = ""
                        )
        Gelir_odemesi.objects.create(gelir_kime_ait_oldugu = get_object_or_404(Gelir_odemesi,id = new_project.id ),kasa_bilgisi = Gider_excel_ekl.kasa,
                                     tutar =float(str(str(i[4]).replace("$","")).replace(",",".")),tarihi =i[2],makbuz_no = new_project.id,
                                       aciklama = "deneme"  )
    return redirect("/")

