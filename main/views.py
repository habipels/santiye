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
def get_client_ip(request):
    """Kullanıcının IP adresini alır"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_csrf_token(request):
    token = get_token(request)
    print(token)
    return JsonResponse({'csrfToken': token})
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
    dil = dil_bilgisi()
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
    
    sozluk["trans"]=trans
    sozluk["dil"]=dil
    return sozluk
def loglar(request):
    content = sozluk_yapisi()
    if request.user.is_authenticated:
        if request.user.is_superuser :
            content["latest_actions"] =LogEntry.objects.filter(object_repr = get_object_or_none(calisan_maas_durumlari,id = 4)  ).order_by('-action_time')
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
        content["santiyeler"] = profile
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
        pass
    else:
        print("login")
        return redirect("/users/login/")
    if request.user.is_authenticated:
        content = sozluk_yapisi()
        if super_admin_kontrolu(request):
            profile =Gelir_Bilgisi.objects.all()
            kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dashboard_gorme:
                        profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user.kullanicilar_db).order_by("-id")
                        content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user.kullanicilar_db)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-id")
                content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
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

        content["santiyeler"] = profile
        if super_admin_kontrolu(request):
            profile =Gider_Bilgisi.objects.all()
            kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dashboard_gorme:
                        profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user.kullanicilar_db).order_by("-id")
                        content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user.kullanicilar_db)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-id")
                content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
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
        if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dashboard_gorme:
                        bilgi_ver = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user.kullanicilar_db).order_by("-fatura_tarihi")
                        sonuc = []
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
        else:
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dashboard_gorme:
                    content["gider"] = sonuc
                    content["bilgi"] = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user.kullanicilar_db).order_by("-id")[:5]
                    content["son_gorevler"] = IsplaniPlanlari.objects.filter(proje_ait_bilgisi =request.user.kullanicilar_db ).order_by("-id")[:5]
                    content["son_gorevler_bina"] = IsplaniPlanlari.objects.filter(proje_ait_bilgisi =request.user.kullanicilar_db ).exclude(blok = None).last()
                    konum = IsplaniPlanlari.objects.filter(proje_ait_bilgisi =request.user.kullanicilar_db ).exclude(blok = None).last()
                    kul = request.user.kullanicilar_db
                else:
                    return redirect("main:yetkisiz")

            else:
                return redirect("main:yetkisiz")
        else:
            content["gider"] = sonuc
            content["bilgi"] = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-id")[:5]
            content["son_gorevler"] = IsplaniPlanlari.objects.filter(proje_ait_bilgisi =request.user ).order_by("-id")[:5]
            content["son_gorevler_bina"] = IsplaniPlanlari.objects.filter(proje_ait_bilgisi =request.user ).exclude(blok = None).last()
            konum = IsplaniPlanlari.objects.filter(proje_ait_bilgisi =request.user ).exclude(blok = None).last()
            kul = request.user
        
    weather_data = None
    ip_info = None
    
    # Kullanıcının IP adresini alıyoruz
    ip = get_client_ip(request) #
    
    # ipinfo.io API'sini kullanarak IP'ye göre konum alıyoruz
    ipinfo_api_url = f"http://ipinfo.io/{ip}/json"
    ip_response = requests.get(ipinfo_api_url)
    if ip_response.status_code == 200:
        ip_info = ip_response.json()
        loc = ip_info.get('loc')
        
        if loc:  # Eğer 'loc' None değilse
            print(loc)
            location = loc.split(',')
            lat, lon = location[0], location[1]
            # OpenWeatherMap API'yi kullanarak hava durumu alıyoruz
            api_key = 'dee0661903df4f2c76ccfd8afab8be69'
            weather_api_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}'
            
            weather_response = requests.get(weather_api_url)
            print(weather_response)
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
            a = weather_data["weather"][0]
            icon = a["icon"]
            content['weather_data'] = weather_data
            content['ip_info'] = ip_info
            content['icon'] = icon
            content['sehir'] = weather_data["name"]
    try:
        if konum.blok.proje_santiye_Ait.lat and konum.blok.proje_santiye_Ait.lon:
            lat, lon = konum.blok.proje_santiye_Ait.lat, konum.blok.proje_santiye_Ait.lon
                # OpenWeatherMap API'yi kullanarak hava durumu alıyoruz
            api_key = 'dee0661903df4f2c76ccfd8afab8be69'
            weather_api_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}'
            
            weather_response = requests.get(weather_api_url)
            print(weather_response)
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
            a = weather_data["weather"][0]
            icon = a["icon"]
            content['weather_data'] = weather_data
            content['ip_info'] = ip_info
            content['icon'] = icon
            content['sehir'] = weather_data["name"]
    except:
        pass     
    return render(request,"index.html",content)
def ana_sayfa(request):
    content = sozluk_yapisi()
    if request.user.is_authenticated:
        pass
    else:
        return redirect("/users/login/")
    if request.user.is_authenticated:
        content = sozluk_yapisi()
        if super_admin_kontrolu(request):
            profile =Gelir_Bilgisi.objects.all()
            kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dashboard_gorme:
                        profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user.kullanicilar_db).order_by("-id")
                        content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user.kullanicilar_db)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-id")
                content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
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

        content["santiyeler"] = profile
        if super_admin_kontrolu(request):
            profile =Gider_Bilgisi.objects.all()
            kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dashboard_gorme:
                        profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user.kullanicilar_db).order_by("-id")
                        content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user.kullanicilar_db)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-id")
                content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
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
        if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dashboard_gorme:
                        bilgi_ver = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user.kullanicilar_db).order_by("-fatura_tarihi")
                        sonuc = []
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
        else:
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dashboard_gorme:
                    content["gider"] = sonuc
                    content["bilgi"] = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user.kullanicilar_db).order_by("-id")[:5]
                    content["son_gorevler"] = IsplaniPlanlari.objects.filter(proje_ait_bilgisi =request.user.kullanicilar_db ).order_by("-id")[:5]
                else:
                    return redirect("main:yetkisiz")

            else:
                return redirect("main:yetkisiz")
        else:
            content["gider"] = sonuc
            content["bilgi"] = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-id")[:5]
            content["son_gorevler"] = IsplaniPlanlari.objects.filter(proje_ait_bilgisi =request.user ).order_by("-id")[:5]
    weather_data = None
    ip_info = None
    
    # Kullanıcının IP adresini alıyoruz
    ip = get_client_ip(request) #
    
    # ipinfo.io API'sini kullanarak IP'ye göre konum alıyoruz
    ipinfo_api_url = f"http://ipinfo.io/{ip}/json"
    ip_response = requests.get(ipinfo_api_url)
    print(ip_response.json())
    if ip_response.status_code == 200:
        ip_info = ip_response.json()
        loc = ip_info.get('loc')
        
        if loc:  # Eğer 'loc' None değilse
            print(loc)
            location = loc.split(',')
            lat, lon = location[0], location[1]
            
            # OpenWeatherMap API'yi kullanarak hava durumu alıyoruz
            api_key = 'dee0661903df4f2c76ccfd8afab8be69'
            weather_api_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}'
            
            weather_response = requests.get(weather_api_url)
            print(weather_response)
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
            a = weather_data["weather"][0]
            icon = a["icon"]
            content['weather_data'] = weather_data
            content['ip_info'] = ip_info
            content['icon'] = icon
            content['sehir'] = weather_data["name"]
            
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
            content["kullanicilar"] =kullanicilar
            profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = users).order_by("-id")
            content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = users)
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
            content["son_gorevler"] = IsplaniPlanlari.objects.filter(proje_ait_bilgisi =users ).order_by("-id")[:5]
            content["son_gorevler_bina"] = IsplaniPlanlari.objects.filter(proje_ait_bilgisi =users).exclude(blok = None).last()
            konum = IsplaniPlanlari.objects.filter(proje_ait_bilgisi =users ).exclude(blok = None).last()
            kul = users
            weather_data = None
            ip_info = None
            
            # Kullanıcının IP adresini alıyoruz
            ip = get_client_ip(request) #
            
            # ipinfo.io API'sini kullanarak IP'ye göre konum alıyoruz
            ipinfo_api_url = f"http://ipinfo.io/{ip}/json"
            ip_response = requests.get(ipinfo_api_url)
            if ip_response.status_code == 200:
                ip_info = ip_response.json()
                loc = ip_info.get('loc')
                
                if loc:  # Eğer 'loc' None değilse
                    print(loc)
                    location = loc.split(',')
                    lat, lon = location[0], location[1]
                    # OpenWeatherMap API'yi kullanarak hava durumu alıyoruz
                    api_key = 'dee0661903df4f2c76ccfd8afab8be69'
                    weather_api_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}'
                    
                    weather_response = requests.get(weather_api_url)
                    print(weather_response)
                    if weather_response.status_code == 200:
                        weather_data = weather_response.json()
                    a = weather_data["weather"][0]
                    icon = a["icon"]
                    content['weather_data'] = weather_data
                    content['ip_info'] = ip_info
                    content['icon'] = icon
                    content['sehir'] = weather_data["name"]
            try:
                if konum.blok.proje_santiye_Ait.lat and konum.blok.proje_santiye_Ait.lon:
                    lat, lon = konum.blok.proje_santiye_Ait.lat, konum.blok.proje_santiye_Ait.lon
                        # OpenWeatherMap API'yi kullanarak hava durumu alıyoruz
                    api_key = 'dee0661903df4f2c76ccfd8afab8be69'
                    weather_api_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}'
                    
                    weather_response = requests.get(weather_api_url)
                    print(weather_response)
                    if weather_response.status_code == 200:
                        weather_data = weather_response.json()
                    a = weather_data["weather"][0]
                    icon = a["icon"]
                    content['weather_data'] = weather_data
                    content['ip_info'] = ip_info
                    content['icon'] = icon
                    content['sehir'] = weather_data["name"]
            except:
                pass    
        else:
            pass
        content["santiyeler"] = profile

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
        content["santiyeler"] = profile
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
        content["santiyeler"] = profile
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.projeler_gorme:
                    profile = proje_tipi.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user.kullanicilar_db)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = proje_tipi.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =proje_tipi.objects.filter(Q(proje_ait_bilgisi__last_name__icontains = search)|Q(Proje_tipi_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.projeler_gorme:
                        profile = proje_tipi.objects.filter(Q(proje_ait_bilgisi = request.user.kullanicilar_db) & Q(Proje_tipi_adi__icontains = search)& Q(silinme_bilgisi = False))

                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
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
    content["santiyeler"] = profile
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
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.projeler_olusturma:
                        proje_tip_adi   = request.POST.get("yetkili_adi")
                        proje_tipi.objects.create(proje_ait_bilgisi = request.user.kullanicilar_db,Proje_tipi_adi = proje_tip_adi)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.projeler_silme:
                    proje_tipi.objects.filter(proje_ait_bilgisi = request.user.kullanicilar_db,id = id).update(silinme_bilgisi = True)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            proje_tipi.objects.filter(proje_ait_bilgisi = request.user,id = id).update(silinme_bilgisi = True)
    return redirect("main:proje_tipi_")
#Proje Düzenlme
import folium
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.projeler_duzenleme:
                    proje_tip_adi   = request.POST.get("yetkili_adi")
                    proje_tipi.objects.filter(proje_ait_bilgisi = request.user.kullanicilar_db,id = id).update(Proje_tipi_adi = proje_tip_adi)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            proje_tip_adi   = request.POST.get("yetkili_adi")
            proje_tipi.objects.filter(proje_ait_bilgisi = request.user,id = id).update(Proje_tipi_adi = proje_tip_adi)
    return redirect("main:proje_tipi_")
#Şantiye Projesi Ekleme
def santiye_projesi_ekle_(request):
    content = sozluk_yapisi()
    m = folium.Map(location=[20, 0], zoom_start=2)
    # Haritayı HTML'ye dönüştürme
    map_html = m._repr_html_()
    content['map'] = map_html
    content["birim_bilgisi"] = birimler.objects.filter(silinme_bilgisi = False)
    content["proje_tipleri"] = proje_tipi.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi =  request.user)
    if super_admin_kontrolu(request):
        profile =santiye.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.santiye_gorme:
                    profile = santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user.kullanicilar_db)
                    content["proje_tipleri"] = proje_tipi.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi =  request.user.kullanicilar_db)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)
            content["proje_tipleri"] = proje_tipi.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi =  request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =santiye.objects.filter(Q(proje_ait_bilgisi__last_name__icontains = search)|Q(Proje_tipi_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.santiye_gorme:
                        profile = santiye.objects.filter(Q(proje_ait_bilgisi = request.user.kullanicilar_db) & Q(Proje_tipi_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/santiye_projesi.html",content)
def santiye_projesi_ekle_2(request,hash):
    content = sozluk_yapisi()
   
    if super_admin_kontrolu(request):
        content["birim_bilgisi"] = birimler.objects.filter(silinme_bilgisi = False)
        d = decode_id(hash)
        users = get_object_or_404(CustomUser,id = d)
        content["hashler"] = hash
        content["hash_bilgi"] = users
        profile =santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = users)
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        content["proje_tipleri"] = proje_tipi.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi =  users)
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
    content["santiyeler"] = profile
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.blog_gorme:
                    profile = bloglar.objects.filter(proje_santiye_Ait__id = id)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/santiye_projesi_blok_ekle.html",content)

def blog_ekle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.blog_olusturma:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    
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
    return redirect("main:santiye_projesi_ekle_")

def blog_duzenle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.blog_duzenleme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
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
    return redirect("main:santiye_projesi_ekle_")
def blog_sil(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.blog_silme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    if request.POST:
        buttonId = request.POST.get("buttonId")
        geri = request.POST.get("geri")
        blog_bilgisi = get_object_or_404(bloglar,id = buttonId)
        bloglar.objects.filter(id = buttonId).delete()
        y = "/siteblog/"+geri+"/"
    return redirect("main:santiye_projesi_ekle_")
def santiye_ekleme_sahibi(request):
    if request.POST:
        if super_admin_kontrolu(request):
            kullanici = request.POST.get("kullanici")
            link = "/addsitesuperadmin/"+kullanici
            return redirect(link)
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.santiye_olusturma:
                            projetipi = request.POST.get("projetipi")
                            proje_adi = request.POST.get("yetkili_adi")

                            a = santiye.objects.create(proje_ait_bilgisi = request.user.kullanicilar_db,proje_tipi = get_object_or_404(proje_tipi,id = projetipi),
                                                proje_adi = proje_adi
                                                )
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                projetipi = request.POST.get("projetipi")
                proje_adi = request.POST.get("yetkili_adi")

                a = santiye.objects.create(proje_ait_bilgisi = request.user,proje_tipi = get_object_or_404(proje_tipi,id = projetipi),
                                    proje_adi = proje_adi
                                    )
    return redirect("main:santiye_projesi_ekle_")
def santiye_ekleme_sahibi_2(request,hash):
    if request.POST:
        content = sozluk_yapisi()
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
        if super_admin_kontrolu(request):
            projetipi = request.POST.get("projetipi")
            proje_adi = request.POST.get("yetkili_adi")

            a = santiye.objects.create(proje_ait_bilgisi = users,proje_tipi = get_object_or_404(proje_tipi,id = projetipi),
                                    proje_adi = proje_adi
                                    )
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.santiye_olusturma:
                            projetipi = request.POST.get("projetipi")
                            proje_adi = request.POST.get("yetkili_adi")

                            a = santiye.objects.create(proje_ait_bilgisi = request.user.kullanicilar_db,proje_tipi = get_object_or_404(proje_tipi,id = projetipi),
                                                proje_adi = proje_adi
                                                )
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                projetipi = request.POST.get("projetipi")
                proje_adi = request.POST.get("yetkili_adi")

                a = santiye.objects.create(proje_ait_bilgisi = request.user,proje_tipi = get_object_or_404(proje_tipi,id = projetipi),
                                    proje_adi = proje_adi
                                    )
    return redirect("main:santiye_projesi_ekle_2",hash)
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
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        a = santiye.objects.create(proje_ait_bilgisi = get_object_or_404(CustomUser,id = id),proje_tipi = get_object_or_404(proje_tipi,id = projetipi),
                               proje_adi = proje_adi,baslangic_tarihi = baslangic_tarihi,
                               tahmini_bitis_tarihi = bitis_tarihi,lat = latitude,lon = longitude
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.santiye_silme:
                    santiye.objects.filter(proje_ait_bilgisi = request.user.kullanicilar_db,id = id).update(silinme_bilgisi = True)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.santiye_duzenleme:
                    proje_tip_adi   = request.POST.get("yetkili_adi")
                    santiye.objects.filter(proje_ait_bilgisi = request.user.kullanicilar_db,id = id).update(proje_adi = proje_tip_adi)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
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
            content["santiyeler_bilgileri"] = bloglar.objects.all()
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.kalemleri_gorme:
                            content["santiyeler_bilgileri"] = bloglar.objects.filter(proje_ait_bilgisi = request.user.kullanicilar_db,proje_santiye_Ait_id = id )
                            profile = santiye_kalemleri.objects.filter(proje_santiye_Ait = get_object_or_404(santiye,id = id) ,silinme_bilgisi = False,proje_ait_bilgisi = request.user.kullanicilar_db)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                content["santiyeler_bilgileri"] = bloglar.objects.filter(proje_ait_bilgisi = request.user,proje_santiye_Ait_id = id )
                profile = santiye_kalemleri.objects.filter(proje_santiye_Ait = get_object_or_404(santiye,id = id) ,silinme_bilgisi = False,proje_ait_bilgisi = request.user)

        if request.GET.get("search"):
            search = request.GET.get("search")
            if request.user.is_superuser:
                kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
                content["kullanicilar"] =kullanicilar
                profile = santiye_kalemleri.objects.filter(proje_santiye_Ait = get_object_or_404(santiye,id = id)).filter(Q(proje_ait_bilgisi__last_name__icontains =search)| Q(kalem_adi__icontains =search)|  Q(proje_santiye_Ait__proje_adi__icontains =search))
                content["santiyeler_bilgileri"] = santiye.objects.all()
            else:
                if request.user.kullanicilar_db:
                    a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                    if a:
                        if a.izinler.kalemleri_gorme:
                                content["santiyeler_bilgileri"] = santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user.kullanicilar_db)
                                profile = santiye_kalemleri.objects.filter(proje_santiye_Ait = get_object_or_404(santiye,id = id) ,silinme_bilgisi = False,proje_ait_bilgisi = request.user.kullanicilar_db).filter(Q(kalem_adi__icontains =search) | Q(proje_santiye_Ait__proje_adi__icontains =search))
                        else:
                            return redirect("main:yetkisiz")
                    else:
                        return redirect("main:yetkisiz")
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
        content["santiyeler"] = profile
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
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.kalemleri_olusturma:
                        projetipi = request.POST.getlist("projetipi")
                        yetkili_adi = request.POST.get("yetkili_adi")
                        santiye_agirligi = request.POST.get("katsayisi")
                        finansal_agirlik = request.POST.get("blogsayisi")
                        metraj = request.POST.get("metraj")
                        tutar = request.POST.get("tutar")
                        birim_bilgisi = request.POST.get("birim_bilgisi")
                        kata_veya_binaya_daihil = request.POST.get("kata_veya_binaya_daihil")
                        id = bloglar.objects.filter(id__in = projetipi).first()
                        kalem = santiye_kalemleri.objects.create(
                            proje_ait_bilgisi = request.user.kullanicilar_db,
                            proje_santiye_Ait =id.proje_santiye_Ait,
                            kalem_adi = yetkili_adi,santiye_agirligi = santiye_agirligi,
                            santiye_finansal_agirligi = finansal_agirlik,
                            birimi = get_object_or_404(birimler,id =birim_bilgisi ),metraj = metraj,
                            tutari = tutar
                        )
                        if kata_veya_binaya_daihil == "0":
                            blog_lar = bloglar.objects.filter(id__in = projetipi)
                            for i in blog_lar:
                                for j in range(0,int(i.kat_sayisi)):
                                    santiye_kalemlerin_dagilisi.objects.create(
                                        proje_ait_bilgisi = request.user.kullanicilar_db,
                                        proje_santiye_Ait = id.proje_santiye_Ait,
                                        kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =kalem.id ),
                                        kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                                    )
                        elif kata_veya_binaya_daihil == "1":
                            blog_lar = bloglar.objects.filter(id__in = projetipi)
                            for i in blog_lar:
                                for j in range(0,int(i.kat_sayisi)):
                                    santiye_kalemlerin_dagilisi.objects.create(
                                        proje_ait_bilgisi = request.user.kullanicilar_db,
                                        proje_santiye_Ait = id.proje_santiye_Ait,
                                        kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =kalem.id ),
                                        kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                                    )
                                    break
                        elif kata_veya_binaya_daihil == "2":
                            blog_lar = bloglar.objects.filter(id__in = projetipi)
                            for i in blog_lar:
                                for j in range(0,4):
                                    santiye_kalemlerin_dagilisi.objects.create(
                                        proje_ait_bilgisi = request.user.kullanicilar_db,
                                        proje_santiye_Ait = id.proje_santiye_Ait,
                                        kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =kalem.id ),
                                        kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                                    )
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                projetipi = request.POST.getlist("projetipi")
                yetkili_adi = request.POST.get("yetkili_adi")
                santiye_agirligi = request.POST.get("katsayisi")
                finansal_agirlik = request.POST.get("blogsayisi")
                metraj = request.POST.get("metraj")
                tutar = request.POST.get("tutar")
                birim_bilgisi = request.POST.get("birim_bilgisi")
                kata_veya_binaya_daihil = request.POST.get("kata_veya_binaya_daihil")
                id = bloglar.objects.filter(id__in = projetipi).first()
                kalem = santiye_kalemleri.objects.create(
                    proje_ait_bilgisi = request.user,
                    proje_santiye_Ait =id.proje_santiye_Ait,
                    kalem_adi = yetkili_adi,santiye_agirligi = santiye_agirligi,
                    santiye_finansal_agirligi = finansal_agirlik,
                    birimi = get_object_or_404(birimler,id =birim_bilgisi ),metraj = metraj,
                    tutari = tutar
                )
                if kata_veya_binaya_daihil == "0":
                    blog_lar = bloglar.objects.filter(id__in = projetipi)
                    for i in blog_lar:
                        for j in range(0,int(i.kat_sayisi)):
                            santiye_kalemlerin_dagilisi.objects.create(
                                proje_ait_bilgisi = request.user,
                                proje_santiye_Ait = id.proje_santiye_Ait,
                                kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =kalem.id ),
                                kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                            )
                elif kata_veya_binaya_daihil == "1":
                    blog_lar = bloglar.objects.filter(id__in = projetipi)
                    for i in blog_lar:
                        for j in range(0,int(i.kat_sayisi)):
                            santiye_kalemlerin_dagilisi.objects.create(
                                proje_ait_bilgisi = request.user,
                                proje_santiye_Ait = id.proje_santiye_Ait,
                                kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =kalem.id ),
                                kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                            )
                            break
                elif kata_veya_binaya_daihil == "2":
                    blog_lar = bloglar.objects.filter(id__in = projetipi)
                    for i in blog_lar:
                        for j in range(0,4):
                            santiye_kalemlerin_dagilisi.objects.create(
                                proje_ait_bilgisi = request.user,
                                proje_santiye_Ait = id.proje_santiye_Ait,
                                kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =kalem.id ),
                                kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                            )
                        
    return redirect("main:santiye_projesi_ekle_")

def kalem_sil(request):
    if request.POST:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.kalemleri_silme:
                    buttonId = request.POST.get("buttonId")
                    geri_don = request.POST.get("geri_don")
                    santiye_kalemleri.objects.filter(id = buttonId).update(
                        silinme_bilgisi = True
                    )
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            buttonId = request.POST.get("buttonId")
            geri_don = request.POST.get("geri_don")
            santiye_kalemleri.objects.filter(id = buttonId).update(
                silinme_bilgisi = True
            )
    return redirect("main:santiye_projesi_ekle_")
def santiye_kalemleri_duzenle(request):
    if request.POST:
        buttonId = request.POST.get("buttonId")
        santiye_kalemlerin_dagilisi.objects.filter(kalem_bilgisi__id =buttonId).delete()
        yetkili_adi = request.POST.get("yetkili_adi")
        santiye_agirligi = request.POST.get("katsayisi")
        finansal_agirlik = request.POST.get("blogsayisi")
        geri_don = request.POST.get("geri_don")
        metraj = request.POST.get("metraj")
        tutar = request.POST.get("tutar")
        birim_bilgisi = request.POST.get("birim_bilgisi")
        kata_veya_binaya_daihil = request.POST.get("kata_veya_binaya_daihil")
        projetipi = request.POST.getlist("projetipi")
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
            if request.user.kullanicilar_db:
                    a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                    if a:
                        if a.izinler.kalemleri_duzenleme:
                            santiye_kalemleri.objects.filter(id  = buttonId).update(
                            proje_ait_bilgisi = request.user.kullanicilar_db,
                            kalem_adi = yetkili_adi,santiye_agirligi = santiye_agirligi,
                            santiye_finansal_agirligi = finansal_agirlik,birimi = get_object_or_404(birimler,id =birim_bilgisi ),metraj = metraj,
                            tutari = tutar
                            )
                            if kata_veya_binaya_daihil == "0":
                                blog_lar = bloglar.objects.filter(id__in = projetipi)
                                for i in blog_lar:
                                    for j in range(0,int(i.kat_sayisi)):
                                        santiye_kalemlerin_dagilisi.objects.create(
                                            proje_ait_bilgisi = request.user.kullanicilar_db,
                                            proje_santiye_Ait_id = geri_don,
                                            kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =buttonId ),
                                            kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                                        )
                            elif kata_veya_binaya_daihil == "1":
                                blog_lar = bloglar.objects.filter(id__in = projetipi)
                                for i in blog_lar:
                                    for j in range(0,int(i.kat_sayisi)):
                                        santiye_kalemlerin_dagilisi.objects.create(
                                            proje_ait_bilgisi = request.user.kullanicilar_db,
                                            proje_santiye_Ait_id = geri_don,
                                            kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =buttonId ),
                                            kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                                        )
                                        break
                            elif kata_veya_binaya_daihil == "2":
                                blog_lar = bloglar.objects.filter(id__in = projetipi)
                                for i in blog_lar:
                                    for j in range(0,4):
                                        santiye_kalemlerin_dagilisi.objects.create(
                                            proje_ait_bilgisi = request.user.kullanicilar_db,
                                            proje_santiye_Ait_id = geri_don,
                                            kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =buttonId ),
                                            kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                                        )
                        else:
                            return redirect("main:yetkisiz")
                    else:
                        return redirect("main:yetkisiz")
            else:
                santiye_kalemleri.objects.filter(id  = buttonId).update(
                            proje_ait_bilgisi = request.user,
                            kalem_adi = yetkili_adi,santiye_agirligi = santiye_agirligi,
                            santiye_finansal_agirligi = finansal_agirlik,birimi = get_object_or_404(birimler,id =birim_bilgisi ),metraj = metraj,
                        tutari = tutar
                        )
                if kata_veya_binaya_daihil == "0":
                    blog_lar = bloglar.objects.filter(id__in = projetipi)
                    for i in blog_lar:
                        for j in range(0,int(i.kat_sayisi)):
                            santiye_kalemlerin_dagilisi.objects.create(
                                proje_ait_bilgisi = request.user,
                                proje_santiye_Ait_id = geri_don,
                                kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =buttonId ),
                                kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                            )
                elif kata_veya_binaya_daihil == "1":
                    blog_lar = bloglar.objects.filter(id__in = projetipi)
                    for i in blog_lar:
                        for j in range(0,int(i.kat_sayisi)):
                            santiye_kalemlerin_dagilisi.objects.create(
                                proje_ait_bilgisi = request.user,
                                proje_santiye_Ait_id = geri_don,
                                kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =buttonId),
                                kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                            )
                            break
                elif kata_veya_binaya_daihil == "2":
                    blog_lar = bloglar.objects.filter(id__in = projetipi)
                    for i in blog_lar:
                        for j in range(0,4):
                            santiye_kalemlerin_dagilisi.objects.create(
                                proje_ait_bilgisi = request.user,
                                proje_santiye_Ait_id = geri_don,
                                kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =buttonId ),
                                kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                            )
        return redirect("main:santiye_projesi_ekle_")

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
        kullanicilar = CustomUser.objects.filter(proje_santiye_Ait__silinme_bilgisi = False ,kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.ilerleme_takibi_gorme:
                        profile = bloglar.objects.filter(proje_santiye_Ait__silinme_bilgisi = False ,proje_ait_bilgisi = request.user.kullanicilar_db)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
        else:
            profile = bloglar.objects.filter(proje_santiye_Ait__silinme_bilgisi = False ,proje_ait_bilgisi = request.user)
    
    content["santiyeler"] = profile
    return render(request,"santiye_yonetimi/santiye_blog_kalem.html",content)

def santiye_kalem_ve_blog_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    
    content["proje_tipleri"] = proje_tipi.objects.filter(proje_ait_bilgisi =  request.user)
    if super_admin_kontrolu(request):
        profile = bloglar.objects.filter(proje_santiye_Ait__silinme_bilgisi = False ,proje_ait_bilgisi = users)
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = bloglar.objects.filter(proje_ait_bilgisi = request.user)
    
    content["santiyeler"] = profile

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
            content["santiyeler"] = profile
            content["top"]  = profile
            content["medya"] = page_obj

        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.kalemleri_gorme:
                        content["santiyeler_bilgileri"] = santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user.kullanicilar_db)
                        kalemler = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id)
                        kalem_id = []
                        for i in kalemler:
                            if i.kalem_bilgisi.id in kalem_id:
                                pass
                            else:
                                kalem_id.append(i.kalem_bilgisi.id)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
            content["santiyeler"] = profile
            content["top"]  = profile
            content["medya"] = page_obj
    else:
        return redirect("/users/login/")
    return render(request,"santiye_yonetimi/ilerleme_takibi.html",content)
def blogtan_kaleme_ilerleme_takibi_hash(request,id,slug,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
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
            content["santiyeler"] = profile
            content["top"]  = profile
            content["medya"] = page_obj

        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.kalemleri_gorme:
                        content["santiyeler_bilgileri"] = santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user.kullanicilar_db)
                        kalemler = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id = id)
                        kalem_id = []
                        for i in kalemler:
                            if i.kalem_bilgisi.id in kalem_id:
                                pass
                            else:
                                kalem_id.append(i.kalem_bilgisi.id)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
            content["santiyeler"] = profile
            content["top"]  = profile
            content["medya"] = page_obj
    else:
        return redirect("/users/login/")
    return render(request,"santiye_yonetimi/ilerleme_takibi.html",content)

def ilerleme_kaydet(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.ilerleme_takibi_duzenleme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        pass
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
        
        for i in kalem:
            a.remove(i)
            santiye_kalemlerin_dagilisi.objects.filter(id = int(i),tamamlanma_bilgisi = False).update(tamamlanma_bilgisi = True, degistirme_tarihi=timezone.now() )
        for i in a:
            if i != ""  :
                if i in kalem:
                    pass
                else:
                    santiye_kalemlerin_dagilisi.objects.filter(id = int(i),tamamlanma_bilgisi = True).update(tamamlanma_bilgisi = False, degistirme_tarihi=timezone.now() )
    return redirect("main:blogtan_kaleme_ilerleme_takibi",geri_don,veri_cek)

def ilerleme_kaydet_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.ilerleme_takibi_duzenleme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        pass
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
        
        for i in kalem:
            a.remove(i)
            santiye_kalemlerin_dagilisi.objects.filter(id = int(i),tamamlanma_bilgisi = False).update(tamamlanma_bilgisi = True, degistirme_tarihi=timezone.now() )
        for i in a:
            if i != ""  :
                if i in kalem:
                    pass
                else:
                    santiye_kalemlerin_dagilisi.objects.filter(id = int(i),tamamlanma_bilgisi = True).update(tamamlanma_bilgisi = False, degistirme_tarihi=timezone.now() )
    return redirect("main:blogtan_kaleme_ilerleme_takibi_hash",geri_don,veri_cek,hash)


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
    content["santiyeler"] = profile
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.taseronlar_gorme:
                    profile = taseronlar.objects.filter(silinme_bilgisi = False,taseron_ait_bilgisi = request.user.kullanicilar_db)
                    if a.izinler.santiye_gorme:
                        content["blog_bilgisi"] =santiye.objects.filter(proje_ait_bilgisi = request.user.kullanicilar_db,silinme_bilgisi = False)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = taseronlar.objects.filter(silinme_bilgisi = False,taseron_ait_bilgisi = request.user)
            content["blog_bilgisi"]  =santiye.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =taseronlar.objects.filter(Q(taseron_ait_bilgisi__last_name__icontains = search)|Q(taseron_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.taseronlar_gorme:
                        profile = taseronlar.objects.filter(Q(taseron_ait_bilgisi = request.user.kullanicilar_db) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    
    return render(request,"santiye_yonetimi/taseronlar.html",content)
#taseron olaylari
#taseron olaylari
def taseron_sayfasi_2(request,hash):
    content = sozluk_yapisi()

    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if super_admin_kontrolu(request):
        profile =taseronlar.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = taseronlar.objects.filter(silinme_bilgisi = False,taseron_ait_bilgisi = users)
        content["blog_bilgisi"]  =santiye.objects.filter(proje_ait_bilgisi = users,silinme_bilgisi = False)
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.taseronlar_gorme:
                    profile = taseronlar.objects.filter(silinme_bilgisi = False,taseron_ait_bilgisi = request.user.kullanicilar_db)
                    if a.izinler.santiye_gorme:
                        content["blog_bilgisi"] =santiye.objects.filter(proje_ait_bilgisi = request.user.kullanicilar_db,silinme_bilgisi = False)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = taseronlar.objects.filter(silinme_bilgisi = False,taseron_ait_bilgisi = request.user)
            content["blog_bilgisi"]  =santiye.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =taseronlar.objects.filter(Q(taseron_ait_bilgisi__last_name__icontains = search)|Q(taseron_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.taseronlar_gorme:
                        profile = taseronlar.objects.filter(Q(taseron_ait_bilgisi = request.user.kullanicilar_db) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    
    return render(request,"santiye_yonetimi/taseronlar.html",content)
#taseron olaylari

def taseron_ekle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            if True:
                taseron_adi = request.POST.get("taseron_adi")
                telefonnumarasi = request.POST.get("telefonnumarasi")
                email_adresi = request.POST.get("email_adresi")
                blogbilgisi = request.POST.getlist("blogbilgisi")
                aciklama = request.POST.get("aciklama")
                new_project = taseronlar(
                    taseron_ait_bilgisi = users,
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                )
                new_project.save()
                bloglar_bilgisi = []
                for i in blogbilgisi:
                    liste = str(i).split(",")
                    proje = projeler.objects.create(proje_ait_bilgisi = users,
                            blog_bilgisi = get_object_or_none(bloglar,id = liste[1]),
                            kalem_bilgisi = get_object_or_none(santiye_kalemleri,id = liste[0])
                            )
                    bloglar_bilgisi.append(projeler.objects.get(id=int(proje.id)))
                new_project.proje_bilgisi.add(*bloglar_bilgisi)
                images = request.FILES.getlist('file')
                isim = 1
                for images in images:
                    taseron_sozlesme_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(taseronlar,id = new_project.id))  # Urun_resimleri modeline resimleri kaydet
                    isim = isim+1
                car = cari.objects.create(
                    cari_kart_ait_bilgisi = users,
                    cari_adi = taseron_adi,
                    telefon_numarasi = telefonnumarasi,
                    aciklama = aciklama
                )
                cari_taseron_baglantisi.objects.create(
                    gelir_kime_ait_oldugu = get_object_or_404(taseronlar,id = new_project.id ),
                    cari_bilgisi = get_object_or_404(cari,id = car.id)
                )
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.taseronlar_olusturma:
                        taseron_adi = request.POST.get("taseron_adi")
                        telefonnumarasi = request.POST.get("telefonnumarasi")
                        email_adresi = request.POST.get("email_adresi")
                        blogbilgisi = request.POST.getlist("blogbilgisi")
                        aciklama = request.POST.get("aciklama")
                        new_project = taseronlar(
                            taseron_ait_bilgisi = request.user.kullanicilar_db,
                            taseron_adi = taseron_adi,
                            email = email_adresi,
                            aciklama = aciklama,
                            telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                        )
                        new_project.save()
                        bloglar_bilgisi = []
                        for i in blogbilgisi:
                            liste = str(i).split(",")
                            proje = projeler.objects.create(proje_ait_bilgisi = request.user.kullanicilar_db,
                                    blog_bilgisi = get_object_or_none(bloglar,id = liste[1]),
                                    kalem_bilgisi = get_object_or_none(santiye_kalemleri,id = liste[0])
                                    )
                            
                            bloglar_bilgisi.append(projeler.objects.get(id=int(proje.id)))
                        new_project.proje_bilgisi.add(*bloglar_bilgisi)
                        images = request.FILES.getlist('file')
                        isim = 1
                        for images in images:
                            taseron_sozlesme_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(taseronlar,id = new_project.id))  # Urun_resimleri modeline resimleri kaydet
                            isim = isim+1
                        car = cari.objects.create(
                            cari_kart_ait_bilgisi = request.user.kullanicilar_db,
                            cari_adi = taseron_adi,
                            telefon_numarasi = telefonnumarasi,
                            aciklama = aciklama
                        )
                        cari_taseron_baglantisi.objects.create(
                            gelir_kime_ait_oldugu = get_object_or_404(taseronlar,id = new_project.id ),
                            cari_bilgisi = get_object_or_404(cari,id = car.id)
                        )
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
                    liste = str(i).split(",")
                    proje = projeler.objects.create(proje_ait_bilgisi = request.user,
                            blog_bilgisi = get_object_or_none(bloglar,id = liste[1]),
                            kalem_bilgisi = get_object_or_none(santiye_kalemleri,id = liste[0])
                            )
                    bloglar_bilgisi.append(projeler.objects.get(id=int(proje.id)))
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
    return redirect("main:taseron_sayfasi_2",hash)

def taseron_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            return redirect("main:taseron_ekle_admin",kullanici)
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.taseronlar_olusturma:
                        taseron_adi = request.POST.get("taseron_adi")
                        telefonnumarasi = request.POST.get("telefonnumarasi")
                        email_adresi = request.POST.get("email_adresi")
                        blogbilgisi = request.POST.getlist("blogbilgisi")
                        aciklama = request.POST.get("aciklama")
                        new_project = taseronlar(
                            taseron_ait_bilgisi = request.user.kullanicilar_db,
                            taseron_adi = taseron_adi,
                            email = email_adresi,
                            aciklama = aciklama,
                            telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                        )
                        new_project.save()
                        bloglar_bilgisi = []
                        for i in blogbilgisi:
                            liste = str(i).split(",")
                            proje = projeler.objects.create(proje_ait_bilgisi = request.user.kullanicilar_db,
                                    blog_bilgisi = get_object_or_none(bloglar,id = liste[1]),
                                    kalem_bilgisi = get_object_or_none(santiye_kalemleri,id = liste[0])
                                    )
                            
                            bloglar_bilgisi.append(projeler.objects.get(id=int(proje.id)))
                        new_project.proje_bilgisi.add(*bloglar_bilgisi)
                        images = request.FILES.getlist('file')
                        isim = 1
                        for images in images:
                            taseron_sozlesme_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(taseronlar,id = new_project.id))  # Urun_resimleri modeline resimleri kaydet
                            isim = isim+1
                        car = cari.objects.create(
                            cari_kart_ait_bilgisi = request.user.kullanicilar_db,
                            cari_adi = taseron_adi,
                            telefon_numarasi = telefonnumarasi,
                            aciklama = aciklama
                        )
                        cari_taseron_baglantisi.objects.create(
                            gelir_kime_ait_oldugu = get_object_or_404(taseronlar,id = new_project.id ),
                            cari_bilgisi = get_object_or_404(cari,id = car.id)
                        )
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
                    liste = str(i).split(",")
                    proje = projeler.objects.create(proje_ait_bilgisi = request.user,
                            blog_bilgisi = get_object_or_none(bloglar,id = liste[1]),
                            kalem_bilgisi = get_object_or_none(santiye_kalemleri,id = liste[0])
                            )
                    bloglar_bilgisi.append(projeler.objects.get(id=int(proje.id)))
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
    content["blog_bilgisi"] =santiye.objects.filter(proje_ait_bilgisi__id = id,silinme_bilgisi = False)
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
                liste = str(i).split(",")
                proje = projeler.objects.create(proje_ait_bilgisi__id = id,
                        blog_bilgisi = get_object_or_none(bloglar,id = liste[1]),
                        kalem_bilgisi = get_object_or_none(santiye_kalemleri,id = liste[0])
                        )
                bloglar_bilgisi.append(projeler.objects.get(id=int(proje.id)))
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
def taseron_silme_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.taseronlar_silme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        pass
    if request.POST:
        buttonId = request.POST.get("buttonId")
        taseronlar.objects.filter(id = buttonId).update(silinme_bilgisi = True)
    return redirect("main:taseron_sayfasi_2",hash)
def taseron_silme(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.taseronlar_silme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        pass
    if request.POST:
        buttonId = request.POST.get("buttonId")
        taseronlar.objects.filter(id = buttonId).update(silinme_bilgisi = True)
    return redirect("main:taseron_sayfasi")
#taşeron Düzenleme
def taseron_duzelt_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
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
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.taseronlar_duzenleme:
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
                            liste = str(i).split(",")
                            j  = get_object_or_none(projeler,blog_bilgisi = get_object_or_none(bloglar,id = liste[1]),
                                    kalem_bilgisi = get_object_or_none(santiye_kalemleri,id = liste[0]),proje_ait_bilgisi = request.user.kullanicilar_db)
                            if j:
                                print(j,"geldi")
                                bloglar_bilgisi.append(projeler.objects.get(id=int(j.id)))
                            else:
                                proje = projeler.objects.create(proje_ait_bilgisi = request.user.kullanicilar_db,
                                        blog_bilgisi = get_object_or_none(bloglar,id = liste[1]),
                                        kalem_bilgisi = get_object_or_none(santiye_kalemleri,id = liste[0])
                                        )
                                bloglar_bilgisi.append(projeler.objects.get(id=int(proje.id)))
                        get_object_or_404(taseronlar,id =id_bilgisi).proje_bilgisi.clear()
                        get_object_or_404(taseronlar,id =id_bilgisi).proje_bilgisi.add(*bloglar_bilgisi)
                        images = request.FILES.getlist('file')
                        isim = 1
                        for images in images:
                            taseron_sozlesme_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(taseronlar,id = id_bilgisi))  # Urun_resimleri modeline resimleri kaydet
                            isim = isim+1
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
                    liste = str(i).split(",")
                    j  = projeler.objects.filter(blog_bilgisi = get_object_or_none(bloglar,id = liste[1]),
                        kalem_bilgisi = get_object_or_none(santiye_kalemleri,id = liste[0])).last()
                    if j:
                        print(j,"geldi")       
                        bloglar_bilgisi.append(projeler.objects.get(id=int(j.id)))
                    else:
                        proje = projeler.objects.create(proje_ait_bilgisi = request.user,
                        blog_bilgisi = get_object_or_none(bloglar,id = liste[1]),
                        kalem_bilgisi = get_object_or_none(santiye_kalemleri,id = liste[0])
                        )
                        bloglar_bilgisi.append(projeler.objects.get(id=int(proje.id)))
                get_object_or_404(taseronlar,id =id_bilgisi).proje_bilgisi.clear()
                get_object_or_404(taseronlar,id =id_bilgisi).proje_bilgisi.add(*bloglar_bilgisi)
                images = request.FILES.getlist('file')
                isim = 1
                for images in images:
                    taseron_sozlesme_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(taseronlar,id = id_bilgisi))  # Urun_resimleri modeline resimleri kaydet
                    isim = isim+1
    return redirect("main:taseron_sayfasi_2",hash)

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
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.taseronlar_duzenleme:
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
                            liste = str(i).split(",")
                            j  = get_object_or_none(projeler,blog_bilgisi = get_object_or_none(bloglar,id = liste[1]),
                                    kalem_bilgisi = get_object_or_none(santiye_kalemleri,id = liste[0]),proje_ait_bilgisi = request.user.kullanicilar_db)
                            if j:
                                print(j,"geldi")
                                bloglar_bilgisi.append(projeler.objects.get(id=int(j.id)))
                            else:
                                proje = projeler.objects.create(proje_ait_bilgisi = request.user.kullanicilar_db,
                                        blog_bilgisi = get_object_or_none(bloglar,id = liste[1]),
                                        kalem_bilgisi = get_object_or_none(santiye_kalemleri,id = liste[0])
                                        )
                                bloglar_bilgisi.append(projeler.objects.get(id=int(proje.id)))
                        get_object_or_404(taseronlar,id =id_bilgisi).proje_bilgisi.clear()
                        get_object_or_404(taseronlar,id =id_bilgisi).proje_bilgisi.add(*bloglar_bilgisi)
                        images = request.FILES.getlist('file')
                        isim = 1
                        for images in images:
                            taseron_sozlesme_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(taseronlar,id = id_bilgisi))  # Urun_resimleri modeline resimleri kaydet
                            isim = isim+1
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
                    liste = str(i).split(",")
                    j  = projeler.objects.filter(blog_bilgisi = get_object_or_none(bloglar,id = liste[1]),
                        kalem_bilgisi = get_object_or_none(santiye_kalemleri,id = liste[0])).last()
                    if j:
                        print(j,"geldi")       
                        bloglar_bilgisi.append(projeler.objects.get(id=int(j.id)))
                    else:
                        proje = projeler.objects.create(proje_ait_bilgisi = request.user,
                        blog_bilgisi = get_object_or_none(bloglar,id = liste[1]),
                        kalem_bilgisi = get_object_or_none(santiye_kalemleri,id = liste[0])
                        )
                        bloglar_bilgisi.append(projeler.objects.get(id=int(proje.id)))
                get_object_or_404(taseronlar,id =id_bilgisi).proje_bilgisi.clear()
                get_object_or_404(taseronlar,id =id_bilgisi).proje_bilgisi.add(*bloglar_bilgisi)
                images = request.FILES.getlist('file')
                isim = 1
                for images in images:
                    taseron_sozlesme_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(taseronlar,id = id_bilgisi))  # Urun_resimleri modeline resimleri kaydet
                    isim = isim+1
    return redirect("main:taseron_sayfasi")

#proje silme
def ust_yuklenici_sayfasi_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users

    if super_admin_kontrolu(request):
        profile =ust_yuklenici.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = ust_yuklenici.objects.filter(silinme_bilgisi = False,taseron_ait_bilgisi = users)
        content["blog_bilgisi"]  =santiye.objects.filter(proje_ait_bilgisi = users,silinme_bilgisi = False)
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.ust_yuklenici_gorme:
                    profile = ust_yuklenici.objects.filter(silinme_bilgisi = False,taseron_ait_bilgisi = request.user.kullanicilar_db)
                    
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = ust_yuklenici.objects.filter(silinme_bilgisi = False,taseron_ait_bilgisi = request.user)
            content["blog_bilgisi"]  =santiye.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =ust_yuklenici.objects.filter(Q(taseron_ait_bilgisi__last_name__icontains = search)|Q(taseron_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.ust_yuklenici_gorme:
                        profile = ust_yuklenici.objects.filter(Q(taseron_ait_bilgisi = request.user.kullanicilar_db) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                profile = ust_yuklenici.objects.filter(Q(taseron_ait_bilgisi = request.user) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))

            
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    
    return render(request,"santiye_yonetimi/ust_yuklenici.html",content)
#Üst Yüklenici olaylari
def ust_yuklenici_ekle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            if True:
                taseron_adi = request.POST.get("taseron_adi")
                telefonnumarasi = request.POST.get("telefonnumarasi")
                email_adresi = request.POST.get("email_adresi")
                
                aciklama = request.POST.get("aciklama")
                new_project = ust_yuklenici(
                    taseron_ait_bilgisi = users,
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                )
                new_project.save()
                
                images = request.FILES.getlist('file')
                print(images)
                isim = 1
                for images in images:
                    ust_yuklenici_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = new_project.id))  # Urun_resimleri modeline resimleri kaydet
                    isim = isim+1
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.taseronlar_olusturma:
                        taseron_adi = request.POST.get("taseron_adi")
                        telefonnumarasi = request.POST.get("telefonnumarasi")
                        email_adresi = request.POST.get("email_adresi")
                        aciklama = request.POST.get("aciklama")
                        new_project = ust_yuklenici(
                            taseron_ait_bilgisi = request.user.kullanicilar_db,
                            taseron_adi = taseron_adi,
                            email = email_adresi,
                            aciklama = aciklama,
                            telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                        )
                        new_project.save()
                        images = request.FILES.getlist('file')
                        print(images)
                        isim = 1
                        for images in images:
                            ust_yuklenici_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = new_project.id))  # Urun_resimleri modeline resimleri kaydet
                            isim = isim+1
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                taseron_adi = request.POST.get("taseron_adi")
                telefonnumarasi = request.POST.get("telefonnumarasi")
                email_adresi = request.POST.get("email_adresi")
                
                aciklama = request.POST.get("aciklama")
                new_project = ust_yuklenici(
                    taseron_ait_bilgisi = request.user,
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                )
                new_project.save()
                
                images = request.FILES.getlist('file')
                print(images)
                isim = 1
                for images in images:
                    ust_yuklenici_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = new_project.id))  # Urun_resimleri modeline resimleri kaydet
                    isim = isim+1

    return redirect("main:ust_yuklenici_sayfasi_2",hash)
#proje silme
def ust_yuklenici_silme_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.ust_yuklenici_silme:
                    pass
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            pass
        print("Üst Yüklenici Sil")
        buttonId = request.POST.get("buttonId")
        ust_yuklenici.objects.filter(id = buttonId).update(silinme_bilgisi = True)
    return redirect("main:ust_yuklenici_sayfasi_2",hash)
#Üst Yüklenivci Düzenleme
def ust_yuklenici_duzelt_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            id_bilgisi = request.POST.get("id_bilgisi")
            taseron_adi = request.POST.get("taseron_adi")
            telefonnumarasi = request.POST.get("telefonnumarasi")
            email_adresi = request.POST.get("email_adresi")
            aciklama = request.POST.get("aciklama")
            silinmedurumu = request.POST.get("silinmedurumu")
            if silinmedurumu == "1":
                ust_yuklenici.objects.filter(id =id_bilgisi ).update(
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                )
            elif silinmedurumu == "2":
                ust_yuklenici.objects.filter(id =id_bilgisi ).update(
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi,silinme_bilgisi = True
                )
            else:
                ust_yuklenici.objects.filter(id =id_bilgisi ).update(
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi
                )
        
            images = request.FILES.getlist('file')
            isim = 1
            for images in images:
                ust_yuklenici_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = id_bilgisi))  # Urun_resimleri modeline resimleri kaydet
                isim = isim+1
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.taseronlar_duzenleme:
                        id_bilgisi = request.POST.get("id_bilgisi")
                        taseron_adi = request.POST.get("taseron_adi")
                        telefonnumarasi = request.POST.get("telefonnumarasi")
                        email_adresi = request.POST.get("email_adresi")
                        
                        aciklama = request.POST.get("aciklama")
                        new_project = ust_yuklenici.objects.filter(id =id_bilgisi ).update(
                            taseron_adi = taseron_adi,
                            email = email_adresi,
                            aciklama = aciklama,
                            telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                        )
                        images = request.FILES.getlist('file')
                        isim = 1
                        for images in images:
                            ust_yuklenici_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = id_bilgisi))  # Urun_resimleri modeline resimleri kaydet
                            isim = isim+1
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
        
                id_bilgisi = request.POST.get("id_bilgisi")
                taseron_adi = request.POST.get("taseron_adi")
                telefonnumarasi = request.POST.get("telefonnumarasi")
                email_adresi = request.POST.get("email_adresi")
                
                aciklama = request.POST.get("aciklama")
                new_project = ust_yuklenici.objects.filter(id =id_bilgisi ).update(
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                )
                
                images = request.FILES.getlist('file')
                isim = 1
                for images in images:
                    ust_yuklenici_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = id_bilgisi))  # Urun_resimleri modeline resimleri kaydet
                    isim = isim+1
    return redirect("main:ust_yuklenici_sayfasi_2",hash)

#Üst Yükleneci olaylari
def ust_yuklenici_sayfasi(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile =ust_yuklenici.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.ust_yuklenici_gorme:
                    profile = ust_yuklenici.objects.filter(silinme_bilgisi = False,taseron_ait_bilgisi = request.user.kullanicilar_db)
                    
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = ust_yuklenici.objects.filter(silinme_bilgisi = False,taseron_ait_bilgisi = request.user)
            content["blog_bilgisi"]  =santiye.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =ust_yuklenici.objects.filter(Q(taseron_ait_bilgisi__last_name__icontains = search)|Q(taseron_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.ust_yuklenici_gorme:
                        profile = ust_yuklenici.objects.filter(Q(taseron_ait_bilgisi = request.user.kullanicilar_db) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                profile = ust_yuklenici.objects.filter(Q(taseron_ait_bilgisi = request.user) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))

            
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    
    return render(request,"santiye_yonetimi/ust_yuklenici.html",content)
#Üst Yüklenici olaylari
def ust_yuklenici_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            return redirect("main:taseron_ekle_admin",kullanici)
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.taseronlar_olusturma:
                        taseron_adi = request.POST.get("taseron_adi")
                        telefonnumarasi = request.POST.get("telefonnumarasi")
                        email_adresi = request.POST.get("email_adresi")
                        aciklama = request.POST.get("aciklama")
                        new_project = ust_yuklenici(
                            taseron_ait_bilgisi = request.user.kullanicilar_db,
                            taseron_adi = taseron_adi,
                            email = email_adresi,
                            aciklama = aciklama,
                            telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                        )
                        new_project.save()
                        images = request.FILES.getlist('file')
                        print(images)
                        isim = 1
                        for images in images:
                            ust_yuklenici_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = new_project.id))  # Urun_resimleri modeline resimleri kaydet
                            isim = isim+1
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                taseron_adi = request.POST.get("taseron_adi")
                telefonnumarasi = request.POST.get("telefonnumarasi")
                email_adresi = request.POST.get("email_adresi")
                
                aciklama = request.POST.get("aciklama")
                new_project = ust_yuklenici(
                    taseron_ait_bilgisi = request.user,
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                )
                new_project.save()
                
                images = request.FILES.getlist('file')
                print(images)
                isim = 1
                for images in images:
                    ust_yuklenici_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = new_project.id))  # Urun_resimleri modeline resimleri kaydet
                    isim = isim+1

    return redirect("main:ust_yuklenici_sayfasi")
#proje silme
def ust_yuklenici_silme(request):
    
    if request.POST:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.ust_yuklenici_silme:
                    pass
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            pass
        print("Üst Yüklenici Sil")
        buttonId = request.POST.get("buttonId")
        ust_yuklenici.objects.filter(id = buttonId).update(silinme_bilgisi = True)
    return redirect("main:ust_yuklenici_sayfasi")
#Üst Yüklenivci Düzenleme
def ust_yuklenici_duzelt(request):
    if request.POST:
        if request.user.is_superuser:
            id_bilgisi = request.POST.get("id_bilgisi")
            taseron_adi = request.POST.get("taseron_adi")
            telefonnumarasi = request.POST.get("telefonnumarasi")
            email_adresi = request.POST.get("email_adresi")
            aciklama = request.POST.get("aciklama")
            silinmedurumu = request.POST.get("silinmedurumu")
            if silinmedurumu == "1":
                ust_yuklenici.objects.filter(id =id_bilgisi ).update(
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                )
            elif silinmedurumu == "2":
                ust_yuklenici.objects.filter(id =id_bilgisi ).update(
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi,silinme_bilgisi = True
                )
            else:
                ust_yuklenici.objects.filter(id =id_bilgisi ).update(
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi
                )
        
            images = request.FILES.getlist('file')
            isim = 1
            for images in images:
                ust_yuklenici_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = id_bilgisi))  # Urun_resimleri modeline resimleri kaydet
                isim = isim+1
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.taseronlar_duzenleme:
                        id_bilgisi = request.POST.get("id_bilgisi")
                        taseron_adi = request.POST.get("taseron_adi")
                        telefonnumarasi = request.POST.get("telefonnumarasi")
                        email_adresi = request.POST.get("email_adresi")
                        
                        aciklama = request.POST.get("aciklama")
                        new_project = ust_yuklenici.objects.filter(id =id_bilgisi ).update(
                            taseron_adi = taseron_adi,
                            email = email_adresi,
                            aciklama = aciklama,
                            telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                        )
                        images = request.FILES.getlist('file')
                        isim = 1
                        for images in images:
                            ust_yuklenici_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = id_bilgisi))  # Urun_resimleri modeline resimleri kaydet
                            isim = isim+1
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
        
                id_bilgisi = request.POST.get("id_bilgisi")
                taseron_adi = request.POST.get("taseron_adi")
                telefonnumarasi = request.POST.get("telefonnumarasi")
                email_adresi = request.POST.get("email_adresi")
                
                aciklama = request.POST.get("aciklama")
                new_project = ust_yuklenici.objects.filter(id =id_bilgisi ).update(
                    taseron_adi = taseron_adi,
                    email = email_adresi,
                    aciklama = aciklama,
                    telefon_numarasi = telefonnumarasi,silinme_bilgisi = False
                )
                
                images = request.FILES.getlist('file')
                isim = 1
                for images in images:
                    ust_yuklenici_dosyalari.objects.create(aciklama="",dosya_adi = isim,dosya=images,proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = id_bilgisi))  # Urun_resimleri modeline resimleri kaydet
                    isim = isim+1
    return redirect("main:ust_yuklenici_sayfasi")


#sözleşmeler
#sözleşme olaylari
def sozlesmler_sayfasi_2(request,hash):
    content = sozluk_yapisi()
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if super_admin_kontrolu(request):
        profile = taseron_sozlesme_dosyalari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = taseron_sozlesme_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = users)
        #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
        content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi=users,silinme_bilgisi = False)
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.sozlesmeler_gorme:
                    profile = taseron_sozlesme_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user.kullanicilar_db)
                    #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user.kullanicilar_db,silinme_bilgisi = False)
                    content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user.kullanicilar_db,silinme_bilgisi = False)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = taseron_sozlesme_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user)
            #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
            content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user,silinme_bilgisi = False)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =taseron_sozlesme_dosyalari.objects.filter(Q(taseron_ait_bilgisi__proje_ait_bilgisi__last_name__icontains = search)|Q(taseron_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.sozlesmeler_gorme:
                        profile = taseron_sozlesme_dosyalari.objects.filter(Q(taseron_ait_bilgisi = request.user.kullanicilar_db) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    
    return render(request,"santiye_yonetimi/xxsozlesmler.html",content)
#sözleşme olaylari
#sözleşme olaylari
def ana_yuklenici_sozlesmler_sayfasi_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users

    if super_admin_kontrolu(request):
        profile = taseron_sozlesme_dosyalari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = ust_yuklenici_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = users)
        #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
        content["taseronlar"] = ust_yuklenici.objects.filter(taseron_ait_bilgisi= users,silinme_bilgisi = False)
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.ust_yuklenici_gorme:
                    profile = ust_yuklenici_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user.kullanicilar_db)
                    #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user.kullanicilar_db,silinme_bilgisi = False)
                    content["taseronlar"] = ust_yuklenici.objects.filter(taseron_ait_bilgisi= request.user.kullanicilar_db,silinme_bilgisi = False)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = ust_yuklenici_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user)
            #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
            content["taseronlar"] = ust_yuklenici.objects.filter(taseron_ait_bilgisi= request.user,silinme_bilgisi = False)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =ust_yuklenici_dosyalari.objects.filter(Q(taseron_ait_bilgisi__proje_ait_bilgisi__last_name__icontains = search)|Q(taseron_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.sozlesmeler_gorme:
                        profile = ust_yuklenici_dosyalari.objects.filter(Q(taseron_ait_bilgisi = request.user.kullanicilar_db) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                profile = ust_yuklenici_dosyalari.objects.filter(Q(taseron_ait_bilgisi = request.user) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                
           
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    
    return render(request,"santiye_yonetimi/ana_yuklenici_sozlesme.html",content)
#sözleşme olaylari
def ust_yuklenici_sozlesme_ekle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
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
            ust_yuklenici_dosyalari.objects.create(
                proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = taseron),
                dosya = file,dosya_adi = dosyaadi,
                tarih = tarih,aciklama = aciklama,
                durum = durumu
            )
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.ust_yuklenici_olusturma:
                        pass
                    else:
                        return redirect("main:yetkisiz")
            else:
                pass
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
            ust_yuklenici_dosyalari.objects.create(
                proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = taseron),
                dosya = file,dosya_adi = dosyaadi,
                tarih = tarih,aciklama = aciklama,
                durum = durumu
            )
    return redirect("main:ana_yuklenici_sozlesmler_sayfasi_2",hash)

def ust_yuklenici_sozlesme_duzenle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.ust_yuklenici_duzenleme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        pass
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
                ust_yuklenici_dosyalari.objects.filter(id = id_bilgisi).update(
                    proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = taseron),
                    dosya = file,dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu
                )
            elif silinmedurumu == "2":
                ust_yuklenici_dosyalari.objects.filter(id = id_bilgisi).update(
                    proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = taseron),
                    dosya = file,dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu,silinme_bilgisi = True
                )
            elif silinmedurumu == "1":
                ust_yuklenici_dosyalari.objects.filter(id = id_bilgisi).update(
                    proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = taseron),
                    dosya = file,dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu,silinme_bilgisi = False
                )
        else:

            ust_yuklenici_dosyalari.objects.filter(id = id_bilgisi).update(
                    proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = taseron),
                    dosya = file,dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu
                )
    return redirect("main:ust_yuklenici_sayfasi_2",hash)
#sözleşmeler sil
def ust_yuklenici_silme_sozlesme_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.ust_yuklenici_silme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        pass
    if request.POST:
        buttonId = request.POST.get("buttonId")
        ust_yuklenici_dosyalari.objects.filter(id = buttonId).update(silinme_bilgisi = True)
    return redirect("main:ust_yuklenici_sayfasi_2",hash)

#sözleşmeler sil
#sözleşme olaylari
def sozlesme_ekle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
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
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.sozlesmeler_olusturma:
                        pass
                    else:
                        return redirect("main:yetkisiz")
            else:
                pass
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
    return redirect("main:sozlesmler_sayfasi_2",hash)

def sozlesme_duzenle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.sozlesmeler_duzenleme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        pass
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
    return redirect("main:sozlesmler_sayfasi_2",hash)

#sözleşmeler sil
def sozlesme_silme_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.sozlesmeler_silme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        pass
    if request.POST:
        buttonId = request.POST.get("buttonId")
        taseron_sozlesme_dosyalari.objects.filter(id = buttonId).update(silinme_bilgisi = True)
    return redirect("main:sozlesmler_sayfasi_2",hash)

#sözleşmeler
#sözleşme olaylari
def sozlesmler_sayfasi(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile = taseron_sozlesme_dosyalari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.sozlesmeler_gorme:
                    profile = taseron_sozlesme_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user.kullanicilar_db)
                    #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user.kullanicilar_db,silinme_bilgisi = False)
                    content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user.kullanicilar_db,silinme_bilgisi = False)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = taseron_sozlesme_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user)
            #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
            content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user,silinme_bilgisi = False)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =taseron_sozlesme_dosyalari.objects.filter(Q(taseron_ait_bilgisi__proje_ait_bilgisi__last_name__icontains = search)|Q(taseron_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.sozlesmeler_gorme:
                        profile = taseron_sozlesme_dosyalari.objects.filter(Q(taseron_ait_bilgisi = request.user.kullanicilar_db) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    
    return render(request,"santiye_yonetimi/xxsozlesmler.html",content)
#sözleşme olaylari
#sözleşme olaylari
def ana_yuklenici_sozlesmler_sayfasi(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile = taseron_sozlesme_dosyalari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.ust_yuklenici_gorme:
                    profile = ust_yuklenici_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user.kullanicilar_db)
                    #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user.kullanicilar_db,silinme_bilgisi = False)
                    content["taseronlar"] = ust_yuklenici.objects.filter(taseron_ait_bilgisi= request.user.kullanicilar_db,silinme_bilgisi = False)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = ust_yuklenici_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user)
            #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
            content["taseronlar"] = ust_yuklenici.objects.filter(taseron_ait_bilgisi= request.user,silinme_bilgisi = False)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =ust_yuklenici_dosyalari.objects.filter(Q(taseron_ait_bilgisi__proje_ait_bilgisi__last_name__icontains = search)|Q(taseron_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.sozlesmeler_gorme:
                        profile = ust_yuklenici_dosyalari.objects.filter(Q(taseron_ait_bilgisi = request.user.kullanicilar_db) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                profile = ust_yuklenici_dosyalari.objects.filter(Q(taseron_ait_bilgisi = request.user) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                
           
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    
    return render(request,"santiye_yonetimi/ana_yuklenici_sozlesme.html",content)
#sözleşme olaylari
def ust_yuklenici_sozlesme_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            return redirect("main:sozlesme_ekle_admin",kullanici)
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.ust_yuklenici_olusturma:
                        pass
                    else:
                        return redirect("main:yetkisiz")
            else:
                pass
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
            ust_yuklenici_dosyalari.objects.create(
                proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = taseron),
                dosya = file,dosya_adi = dosyaadi,
                tarih = tarih,aciklama = aciklama,
                durum = durumu
            )
    return redirect("main:ana_yuklenici_sozlesmler_sayfasi")

def ust_yuklenici_sozlesme_duzenle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.ust_yuklenici_duzenleme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        pass
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
                ust_yuklenici_dosyalari.objects.filter(id = id_bilgisi).update(
                    proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = taseron),
                    dosya = file,dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu
                )
            elif silinmedurumu == "2":
                ust_yuklenici_dosyalari.objects.filter(id = id_bilgisi).update(
                    proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = taseron),
                    dosya = file,dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu,silinme_bilgisi = True
                )
            elif silinmedurumu == "1":
                ust_yuklenici_dosyalari.objects.filter(id = id_bilgisi).update(
                    proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = taseron),
                    dosya = file,dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu,silinme_bilgisi = False
                )
        else:

            ust_yuklenici_dosyalari.objects.filter(id = id_bilgisi).update(
                    proje_ait_bilgisi = get_object_or_404(ust_yuklenici,id = taseron),
                    dosya = file,dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    durum = durumu
                )
    return redirect("main:ust_yuklenici_sayfasi")
#sözleşmeler sil
def ust_yuklenici_silme_sozlesme(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.ust_yuklenici_silme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        pass
    if request.POST:
        buttonId = request.POST.get("buttonId")
        ust_yuklenici_dosyalari.objects.filter(id = buttonId).update(silinme_bilgisi = True)
    return redirect("main:ust_yuklenici_sayfasi")

#sözleşmeler sil
#sözleşme olaylari
def sozlesme_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            return redirect("main:sozlesme_ekle_admin",kullanici)
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.sozlesmeler_olusturma:
                        pass
                    else:
                        return redirect("main:yetkisiz")
            else:
                pass
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
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.sozlesmeler_duzenleme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        pass
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
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.sozlesmeler_silme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        pass
    if request.POST:
        buttonId = request.POST.get("buttonId")
        taseron_sozlesme_dosyalari.objects.filter(id = buttonId).update(silinme_bilgisi = True)
    return redirect("main:sozlesmler_sayfasi")

#sözleşmeler sil
#sözleşmeler
#hakedişler

def hakedis_sayfasi_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users

    if super_admin_kontrolu(request):
        profile = taseron_hakedisles.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = taseron_hakedisles.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = users)
        content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi=users,silinme_bilgisi = False)
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.hakedisler_gorme:
                    profile = taseron_hakedisles.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user.kullanicilar_db)
                    content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user.kullanicilar_db,silinme_bilgisi = False)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = taseron_hakedisles.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user)
            content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user,silinme_bilgisi = False)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =taseron_hakedisles.objects.filter(Q(proje_ait_bilgisi__taseron_ait_bilgisi__last_name__icontains = search)|Q(dosya_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.hakedisler_gorme:
                        profile = taseron_hakedisles.objects.filter(Q(proje_ait_bilgisi__taseron_ait_bilgisi = request.user.kullanicilar_db) & Q(proje_ait_bilgisi__taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    
    return render(request,"santiye_yonetimi/hakedis.html",content)

def hakedis_ekle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            if True:
                taseron = request.POST.get("taseron")
                dosyaadi = request.POST.get("yetkili_adi")
                tarih = request.POST.get("tarih_bilgisi")
                aciklama = request.POST.get("aciklama")
                file = request.FILES.get("file")
                fatura_no = request.POST.get("fatura_no")
                
                taseron_hakedisles.objects.create(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                    dosya = file,
                    dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    fatura_numarasi = fatura_no
                )
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.hakedisler_olusturma:
                        taseron = request.POST.get("taseron")
                        dosyaadi = request.POST.get("yetkili_adi")
                        tarih = request.POST.get("tarih_bilgisi")
                        aciklama = request.POST.get("aciklama")
                        file = request.FILES.get("file")
                        fatura_no = request.POST.get("fatura_no")
                       
                        taseron_hakedisles.objects.create(
                            proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                            dosya = file,
                            dosya_adi = dosyaadi,
                            tarih = tarih,aciklama = aciklama,
                            fatura_numarasi = fatura_no
                        )
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                taseron = request.POST.get("taseron")
                dosyaadi = request.POST.get("yetkili_adi")
                tarih = request.POST.get("tarih_bilgisi")
                aciklama = request.POST.get("aciklama")
                file = request.FILES.get("file")
                fatura_no = request.POST.get("fatura_no")
                
                taseron_hakedisles.objects.create(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                    dosya = file,
                    dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    fatura_numarasi = fatura_no
                )
    return redirect("main:hakedis_sayfasi_2",hash)
#hakedisekle
def hakedis_silme_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.hakedisler_silme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        pass
    if request.POST:
        buttonId = request.POST.get("buttonId")
        taseron_hakedisles.objects.filter(id = buttonId).update(silinme_bilgisi = True)
    return redirect("main:hakedis_sayfasi_2",hash)

#hakediş düzenle
def hakedis_duzenle_2(request,hash):
    if request.POST:
        if request.user.is_superuser:
            buttonId = request.POST.get("buttonId")
            taseron = request.POST.get("taseron")
            dosyaadi = request.POST.get("yetkili_adi")
            tarih = request.POST.get("tarih_bilgisi")
            aciklama = request.POST.get("aciklama")
            file = request.FILES.get("file")
            fatura_no = request.POST.get("fatura_no")
            silinmedurumu = request.POST.get("silinmedurumu")
            if silinmedurumu == "3":
                if file:
                    taseron_hakedisles.objects.filter(id=buttonId).update(
                        proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                        dosya = file,
                        dosya_adi = dosyaadi,
                        tarih = tarih,aciklama = aciklama,
                        fatura_numarasi = fatura_no
                    )
                else:
                    taseron_hakedisles.objects.filter(id=buttonId).update(
                        proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                        
                        dosya_adi = dosyaadi,
                        tarih = tarih,aciklama = aciklama,
                        fatura_numarasi = fatura_no
                    )
            elif silinmedurumu == "2":
                if file:
                    taseron_hakedisles.objects.filter(id=buttonId).update(
                        proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                        dosya = file,
                        dosya_adi = dosyaadi,
                        tarih = tarih,aciklama = aciklama,
                        
                        fatura_numarasi = fatura_no,silinme_bilgisi = True
                    )
                else:
                    taseron_hakedisles.objects.filter(id=buttonId).update(
                        proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                        
                        dosya_adi = dosyaadi,
                        tarih = tarih,aciklama = aciklama,
                        
                        fatura_numarasi = fatura_no,silinme_bilgisi = True
                    )
            elif silinmedurumu == "1":
                if file:
                    taseron_hakedisles.objects.filter(id=buttonId).update(
                        proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                        dosya = file,
                        dosya_adi = dosyaadi,
                        tarih = tarih,aciklama = aciklama,
                        fatura_numarasi = fatura_no,silinme_bilgisi = False
                    )
                else:
                    taseron_hakedisles.objects.filter(id=buttonId).update(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                    
                    dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    fatura_numarasi = fatura_no,silinme_bilgisi = False
                )

        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.hakedisler_duzenleme:
                        pass
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")    
            else:
                pass
            buttonId = request.POST.get("buttonId")
            taseron = request.POST.get("taseron")
            dosyaadi = request.POST.get("yetkili_adi")
            tarih = request.POST.get("tarih_bilgisi")
            aciklama = request.POST.get("aciklama")
            file = request.FILES.get("file")
            fatura_no = request.POST.get("fatura_no")
            if file:
                taseron_hakedisles.objects.filter(id=buttonId).update(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                    dosya = file,
                    dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                
                    fatura_numarasi = fatura_no
                )
            else:
                taseron_hakedisles.objects.filter(id=buttonId).update(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),

                    dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                
                    fatura_numarasi = fatura_no
                )
    return redirect("main:hakedis_sayfasi_2",hash)


def hakedis_sayfasi(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile = taseron_hakedisles.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.hakedisler_gorme:
                    profile = taseron_hakedisles.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user.kullanicilar_db)
                    content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user.kullanicilar_db,silinme_bilgisi = False)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = taseron_hakedisles.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user)
            content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user,silinme_bilgisi = False)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =taseron_hakedisles.objects.filter(Q(proje_ait_bilgisi__taseron_ait_bilgisi__last_name__icontains = search)|Q(dosya_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.hakedisler_gorme:
                        profile = taseron_hakedisles.objects.filter(Q(proje_ait_bilgisi__taseron_ait_bilgisi = request.user.kullanicilar_db) & Q(proje_ait_bilgisi__taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    
    return render(request,"santiye_yonetimi/hakedis.html",content)

def hakedis_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            return redirect("main:hakedis_ekle_admin",kullanici)
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.hakedisler_olusturma:
                        taseron = request.POST.get("taseron")
                        dosyaadi = request.POST.get("yetkili_adi")
                        tarih = request.POST.get("tarih_bilgisi")
                        aciklama = request.POST.get("aciklama")
                        file = request.FILES.get("file")
                        fatura_no = request.POST.get("fatura_no")
                       
                        taseron_hakedisles.objects.create(
                            proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                            dosya = file,
                            dosya_adi = dosyaadi,
                            tarih = tarih,aciklama = aciklama,
                            fatura_numarasi = fatura_no
                        )
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                taseron = request.POST.get("taseron")
                dosyaadi = request.POST.get("yetkili_adi")
                tarih = request.POST.get("tarih_bilgisi")
                aciklama = request.POST.get("aciklama")
                file = request.FILES.get("file")
                fatura_no = request.POST.get("fatura_no")
                
                taseron_hakedisles.objects.create(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                    dosya = file,
                    dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    fatura_numarasi = fatura_no
                )
    return redirect("main:hakedis_sayfasi")
#hakedisekle
def hakedis_silme(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.hakedisler_silme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        pass
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
            file = request.FILES.get("file")
            fatura_no = request.POST.get("fatura_no")
            silinmedurumu = request.POST.get("silinmedurumu")
            if silinmedurumu == "3":
                if file:
                    taseron_hakedisles.objects.filter(id=buttonId).update(
                        proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                        dosya = file,
                        dosya_adi = dosyaadi,
                        tarih = tarih,aciklama = aciklama,
                        fatura_numarasi = fatura_no
                    )
                else:
                    taseron_hakedisles.objects.filter(id=buttonId).update(
                        proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                        
                        dosya_adi = dosyaadi,
                        tarih = tarih,aciklama = aciklama,
                        fatura_numarasi = fatura_no
                    )
            elif silinmedurumu == "2":
                if file:
                    taseron_hakedisles.objects.filter(id=buttonId).update(
                        proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                        dosya = file,
                        dosya_adi = dosyaadi,
                        tarih = tarih,aciklama = aciklama,
                        
                        fatura_numarasi = fatura_no,silinme_bilgisi = True
                    )
                else:
                    taseron_hakedisles.objects.filter(id=buttonId).update(
                        proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                        
                        dosya_adi = dosyaadi,
                        tarih = tarih,aciklama = aciklama,
                        
                        fatura_numarasi = fatura_no,silinme_bilgisi = True
                    )
            elif silinmedurumu == "1":
                if file:
                    taseron_hakedisles.objects.filter(id=buttonId).update(
                        proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                        dosya = file,
                        dosya_adi = dosyaadi,
                        tarih = tarih,aciklama = aciklama,
                        fatura_numarasi = fatura_no,silinme_bilgisi = False
                    )
                else:
                    taseron_hakedisles.objects.filter(id=buttonId).update(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                    
                    dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                    fatura_numarasi = fatura_no,silinme_bilgisi = False
                )

        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.hakedisler_duzenleme:
                        pass
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")    
            else:
                pass
            buttonId = request.POST.get("buttonId")
            taseron = request.POST.get("taseron")
            dosyaadi = request.POST.get("yetkili_adi")
            tarih = request.POST.get("tarih_bilgisi")
            aciklama = request.POST.get("aciklama")
            file = request.FILES.get("file")
            fatura_no = request.POST.get("fatura_no")
            if file:
                taseron_hakedisles.objects.filter(id=buttonId).update(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),
                    dosya = file,
                    dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                
                    fatura_numarasi = fatura_no
                )
            else:
                taseron_hakedisles.objects.filter(id=buttonId).update(
                    proje_ait_bilgisi = get_object_or_404(taseronlar,id = taseron),

                    dosya_adi = dosyaadi,
                    tarih = tarih,aciklama = aciklama,
                
                    fatura_numarasi = fatura_no
                )
    return redirect("main:hakedis_sayfasi")


def depolama_sistemim(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile = klasorler.objects.all()

    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dosya_yoneticisi_gorme:
                    profile = klasorler.objects.filter(klasor_adi_db = None).filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = klasorler.objects.filter(klasor_adi_db = None).filter(silinme_bilgisi = False,dosya_sahibi = request.user)

    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(klasor_adi_db = None).filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_gorme:
                        profile = klasorler.objects.filter(klasor_adi_db = None).filter(Q(dosya_sahibi = request.user.kullanicilar_db) & Q(klasor_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/depolama_sistemim.html",content)


def depolama_sistemim_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if super_admin_kontrolu(request):
        #profile = klasorler.objects.all()
        profile = klasorler.objects.filter(klasor_adi_db = None).filter(silinme_bilgisi = False,dosya_sahibi = users)
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dosya_yoneticisi_gorme:
                    profile = klasorler.objects.filter(klasor_adi_db = None).filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = klasorler.objects.filter(klasor_adi_db = None).filter(silinme_bilgisi = False,dosya_sahibi = request.user)

    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(klasor_adi_db = None).filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_gorme:
                        profile = klasorler.objects.filter(klasor_adi_db = None).filter(Q(dosya_sahibi = request.user.kullanicilar_db) & Q(klasor_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/depolama_sistemim.html",content)

def klasor_olustur_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            if True:
                ust_klasor = request.POST.get("ust_klasor")
                if ust_klasor:
                    klasor = request.POST.get("klasor")

                    klasorler.objects.create(
                        dosya_sahibi = users,
                        klasor_adi = klasor,
                        klasor_adi_db = get_object_or_404(klasorler,id =ust_klasor )
                    )
                else:
                    klasor = request.POST.get("klasor")

                    klasorler.objects.create(
                        dosya_sahibi = users,
                        klasor_adi = klasor
                    )
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_olusturma:
                        ust_klasor = request.POST.get("ust_klasor")
                        if ust_klasor:
                            klasor = request.POST.get("klasor")

                            klasorler.objects.create(
                                dosya_sahibi = request.user.kullanicilar_db,
                                klasor_adi = klasor,
                                klasor_adi_db = get_object_or_404(klasorler,id =ust_klasor )
                            )
                        else:
                            klasor = request.POST.get("klasor")

                            klasorler.objects.create(
                                dosya_sahibi = request.user.kullanicilar_db,
                                klasor_adi = klasor
                            )
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    return redirect("main:depolama_sistemim_2",hash)

def klasor__yeniden_adlandir_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            klasor = request.POST.get("klasor")
            idbilgisi = request.POST.get("idbilgisi")
            klasorler.objects.filter(id = idbilgisi).update(
                    dosya_sahibi = users,
                    klasor_adi = klasor
                )
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_duzenleme:
                        klasor = request.POST.get("klasor")
                        idbilgisi = request.POST.get("idbilgisi")
                        klasorler.objects.filter(id = idbilgisi).update(
                            dosya_sahibi = request.user.kullanicilar_db,
                            klasor_adi = klasor
                        )
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                klasor = request.POST.get("klasor")
                idbilgisi = request.POST.get("idbilgisi")
                klasorler.objects.filter(id = idbilgisi).update(
                    dosya_sahibi = request.user,
                    klasor_adi = klasor
                )
    return redirect("main:depolama_sistemim_2",hash)

def klasor_sil_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dosya_yoneticisi_silme:
                    pass
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
    else:
        pass
    if request.POST:
        if request.user.is_superuser:
            idbilgisi = request.POST.get("idbilgisi")
            klasorler.objects.filter(id = idbilgisi).update(
                silinme_bilgisi = True
            )
        else:
            pass
            
    return redirect("main:depolama_sistemim_2",hash)


def klasor_olustur(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_olusturma:
                        ust_klasor = request.POST.get("ust_klasor")
                        if ust_klasor:
                            klasor = request.POST.get("klasor")

                            klasorler.objects.create(
                                dosya_sahibi = request.user.kullanicilar_db,
                                klasor_adi = klasor,
                                klasor_adi_db = get_object_or_404(klasorler,id =ust_klasor )
                            )
                        else:
                            klasor = request.POST.get("klasor")

                            klasorler.objects.create(
                                dosya_sahibi = request.user.kullanicilar_db,
                                klasor_adi = klasor
                            )
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_duzenleme:
                        klasor = request.POST.get("klasor")
                        idbilgisi = request.POST.get("idbilgisi")
                        klasorler.objects.filter(id = idbilgisi).update(
                            dosya_sahibi = request.user.kullanicilar_db,
                            klasor_adi = klasor
                        )
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                klasor = request.POST.get("klasor")
                idbilgisi = request.POST.get("idbilgisi")
                klasorler.objects.filter(id = idbilgisi).update(
                    dosya_sahibi = request.user,
                    klasor_adi = klasor
                )
    return redirect("main:depolama_sistemim")

def klasor_sil(request):
    if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dosya_yoneticisi_silme:
                    pass
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
    else:
        pass
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dosya_yoneticisi_gorme:
                    profile = klasorler.objects.filter(klasor_adi_db__id =id,silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db)
                    dosyalarim = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db,proje_ait_bilgisi__id =id)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
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
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_gorme:
                        profile = klasorler.objects.filter(klasor_adi_db__id =id).filter(Q(dosya_sahibi = request.user.kullanicilar_db) & Q(klasor_adi__icontains = search)& Q(silinme_bilgisi = False))
                        dosyalarim = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db,proje_ait_bilgisi__id =id).filter(__icontains = search)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    content["dosyalarim"] = dosyalarim
    return render(request,"santiye_yonetimi/klasorici.html",content)
#klasöre Gir
#klasöre Gir
def klasore_gir_2(request,id,slug,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    content["id_bilgisi"] = id
    if super_admin_kontrolu(request):
        profile = klasorler.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = klasorler.objects.filter(klasor_adi_db__id =id,silinme_bilgisi = False,dosya_sahibi = users)
        dosyalarim = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = users,proje_ait_bilgisi__id =id)
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dosya_yoneticisi_gorme:
                    profile = klasorler.objects.filter(klasor_adi_db__id =id,silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db)
                    dosyalarim = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db,proje_ait_bilgisi__id =id)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
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
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_gorme:
                        profile = klasorler.objects.filter(klasor_adi_db__id =id).filter(Q(dosya_sahibi = request.user.kullanicilar_db) & Q(klasor_adi__icontains = search)& Q(silinme_bilgisi = False))
                        dosyalarim = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db,proje_ait_bilgisi__id =id).filter(__icontains = search)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
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
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_olusturma:
                        ust_klasor = request.POST.get("ust_klasor")
                        dosya_Adi = request.POST.get("klasor")
                        tarih = request.POST.get("tarih")
                        aciklama = request.POST.get("aciklama")
                        dosya = request.FILES.get("file")

                        klasor_dosyalari.objects.create(
                            dosya_sahibi=request.user.kullanicilar_db,
                            proje_ait_bilgisi=get_object_or_404(klasorler, id=ust_klasor),
                            dosya=dosya,
                            dosya_adi=dosya_Adi,
                            tarih=tarih,
                            aciklama=aciklama
                        )
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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

def dosya_ekle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            if True:
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
            z = "control/storage/mydir/"+str(ust_klasor)+"/"+str(get_object_or_404(klasorler,id = ust_klasor).klasor_adi)+"/"+hash
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_olusturma:
                        ust_klasor = request.POST.get("ust_klasor")
                        dosya_Adi = request.POST.get("klasor")
                        tarih = request.POST.get("tarih")
                        aciklama = request.POST.get("aciklama")
                        dosya = request.FILES.get("file")

                        klasor_dosyalari.objects.create(
                            dosya_sahibi=request.user.kullanicilar_db,
                            proje_ait_bilgisi=get_object_or_404(klasorler, id=ust_klasor),
                            dosya=dosya,
                            dosya_adi=dosya_Adi,
                            tarih=tarih,
                            aciklama=aciklama
                        )
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
def dosya_sil_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            if True:
                ust_klasor = request.POST.get("ust_klasor")
                dosya_Adi = request.POST.get("klasor")

                klasor_dosyalari.objects.filter(id = dosya_Adi).update(silinme_bilgisi = True)
            if ust_klasor:
                z = "control/storage/mydir/"+str(ust_klasor)+"/"+str(get_object_or_404(klasorler,id = ust_klasor).klasor_adi)+"/"+hash
                return redirect(z)
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_silme:
                        pass
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                pass
            ust_klasor = request.POST.get("ust_klasor")
            dosya_Adi = request.POST.get("klasor")

            klasor_dosyalari.objects.filter(id = dosya_Adi).update(silinme_bilgisi = True)
    if ust_klasor:
        z = "/storage/mydir/"+str(ust_klasor)+"/"+str(get_object_or_404(klasorler,id = ust_klasor).klasor_adi)+"/"
        return redirect(z)
    else:
        return redirect("main:depolama_sistemim_2",hash)

#dosya_ sil
def dosya_sil(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_silme:
                        pass
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                pass
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
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_duzenleme:
                        pass
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                pass
            ust_klasor = request.POST.get("ust_klasor")
            dosya_Adi = request.POST.get("klasor")

            klasor_dosyalari.objects.filter(id = dosya_Adi).update(silinme_bilgisi = False)
    return redirect("main:silinen_dosyalari")
def dosya_geri_getir_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            ust_klasor = request.POST.get("ust_klasor")
            dosya_Adi = request.POST.get("klasor")

            klasor_dosyalari.objects.filter(id = dosya_Adi).update(silinme_bilgisi = False)
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_duzenleme:
                        pass
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                pass
            ust_klasor = request.POST.get("ust_klasor")
            dosya_Adi = request.POST.get("klasor")

            klasor_dosyalari.objects.filter(id = dosya_Adi).update(silinme_bilgisi = False)
    return redirect("main:silinen_dosyalari_2",hash)
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dosya_yoneticisi_gorme:
                    profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db).filter(reduce(operator.or_, (Q(dosya__icontains = x) for x in dosya_turu)))
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user).filter(reduce(operator.or_, (Q(dosya__icontains = x) for x in dosya_turu)))
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_gorme:
                        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db).filter(__icontains = search)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/dokuman.html",content)
def dokumanlar_2(request,hash):
    dosya_turu = [".xlsx",".pdf",".xlx",".txt",".docx",".doc",".ppt",".pptx"]
    content = sozluk_yapisi()
    content["id_bilgisi"] = id
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if super_admin_kontrolu(request):
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = users).filter(reduce(operator.or_, (Q(dosya__icontains = x) for x in dosya_turu)))
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dosya_yoneticisi_gorme:
                    profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db).filter(reduce(operator.or_, (Q(dosya__icontains = x) for x in dosya_turu)))
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user).filter(reduce(operator.or_, (Q(dosya__icontains = x) for x in dosya_turu)))
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_gorme:
                        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db).filter(__icontains = search)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/dokuman.html",content)

#dokumanlari_gosterme
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dosya_yoneticisi_gorme:
                    profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db).filter(reduce(operator.or_, (Q(dosya__icontains = x) for x in dosya_turu)))
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user).filter(reduce(operator.or_, (Q(dosya__icontains = x) for x in dosya_turu)))
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_gorme:
                        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db).filter(__icontains = search)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/dokuman.html",content)

#media
def media_dosyalari_2(request,hash):
    dosya_turu = [".jpg",".jpeg",".png",".ico",".css",".JFIF",".GIF",".WEBP"]
    content = sozluk_yapisi()
    content["id_bilgisi"] = id
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if super_admin_kontrolu(request):
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = users).filter(reduce(operator.or_, (Q(dosya__icontains = x) for x in dosya_turu)))
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dosya_yoneticisi_gorme:
                    profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db).filter(reduce(operator.or_, (Q(dosya__icontains = x) for x in dosya_turu)))
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user).filter(reduce(operator.or_, (Q(dosya__icontains = x) for x in dosya_turu)))
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_gorme:
                        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db).filter(__icontains = search)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dosya_yoneticisi_gorme:
                    profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db).order_by("-id")
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user).order_by("-id")
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_gorme:
                        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db).filter(__icontains = search)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/dokuman.html",content)
def zamana_dosyalari_2(request,hash):

    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    content["id_bilgisi"] = id
    if super_admin_kontrolu(request):
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = users).order_by("-id")
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dosya_yoneticisi_gorme:
                    profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db).order_by("-id")
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user).order_by("-id")
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_gorme:
                        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = False,dosya_sahibi = request.user.kullanicilar_db).filter(__icontains = search)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dosya_yoneticisi_gorme:
                    profile = klasor_dosyalari.objects.filter(silinme_bilgisi = True,dosya_sahibi = request.user.kullanicilar_db).order_by("-id")
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = klasor_dosyalari.objects.filter(silinme_bilgisi = True,dosya_sahibi = request.user).order_by("-id")
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_gorme:
                        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = True,dosya_sahibi = request.user.kullanicilar_db).filter(__icontains = search)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/dokuman.html",content)
#zamana göre

def silinen_dosyalari_2(request,hash):
    content = sozluk_yapisi()
    content["id_bilgisi"] = id
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if super_admin_kontrolu(request):
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = True,dosya_sahibi = users).order_by("-id")
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.dosya_yoneticisi_gorme:
                    profile = klasor_dosyalari.objects.filter(silinme_bilgisi = True,dosya_sahibi = request.user.kullanicilar_db).order_by("-id")
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = klasor_dosyalari.objects.filter(silinme_bilgisi = True,dosya_sahibi = request.user).order_by("-id")
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =klasorler.objects.filter(Q(dosya_sahibi__last_name__icontains = search)|Q(klasor_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.dosya_yoneticisi_gorme:
                        profile = klasor_dosyalari.objects.filter(silinme_bilgisi = True,dosya_sahibi = request.user.kullanicilar_db).filter(__icontains = search)
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"santiye_yonetimi/dokuman.html",content)

#sözleşme olaylari
def sozlesmler_depolamam_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if super_admin_kontrolu(request):
        profile = taseron_sozlesme_dosyalari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = taseron_sozlesme_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = users)
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.sozlesmeler_gorme:
                    profile = taseron_sozlesme_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user.kullanicilar_db)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = taseron_sozlesme_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user)

    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =taseron_sozlesme_dosyalari.objects.filter(Q(taseron_ait_bilgisi__proje_ait_bilgisi__last_name__icontains = search)|Q(taseron_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.sozlesmeler_gorme:
                        profile = taseron_sozlesme_dosyalari.objects.filter(Q(taseron_ait_bilgisi = request.user.kullanicilar_db) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user,silinme_bilgisi = False)
    return render(request,"santiye_yonetimi/sozlesmeler_depo.html",content)
def hakedis_depolamam_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if super_admin_kontrolu(request):
        profile = taseron_hakedisles.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = taseron_hakedisles.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = users)
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.hakedisler_gorme:
                    profile = taseron_hakedisles.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user.kullanicilar_db)
                    content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user.kullanicilar_db,silinme_bilgisi = False)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user,silinme_bilgisi = False)
            profile = taseron_hakedisles.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user)

    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =taseron_hakedisles.objects.filter(Q(proje_ait_bilgisi__taseron_ait_bilgisi__last_name__icontains = search)|Q(dosya_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.hakedisler_gorme:
                        profile = taseron_hakedisles.objects.filter(Q(proje_ait_bilgisi__taseron_ait_bilgisi = request.user.kullanicilar_db) & Q(proje_ait_bilgisi__taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user,silinme_bilgisi = False)
    return render(request,"santiye_yonetimi/hakedis_depo.html",content)

#admin
#sözleşme olaylari
def sozlesmler_depolamam(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile = taseron_sozlesme_dosyalari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.sozlesmeler_gorme:
                    profile = taseron_sozlesme_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user.kullanicilar_db)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = taseron_sozlesme_dosyalari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user)

    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =taseron_sozlesme_dosyalari.objects.filter(Q(taseron_ait_bilgisi__proje_ait_bilgisi__last_name__icontains = search)|Q(taseron_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.sozlesmeler_gorme:
                        profile = taseron_sozlesme_dosyalari.objects.filter(Q(taseron_ait_bilgisi = request.user.kullanicilar_db) & Q(taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user,silinme_bilgisi = False)
    return render(request,"santiye_yonetimi/sozlesmeler_depo.html",content)
def hakedis_depolamam(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile = taseron_hakedisles.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.hakedisler_gorme:
                    profile = taseron_hakedisles.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user.kullanicilar_db)
                    content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user.kullanicilar_db,silinme_bilgisi = False)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user,silinme_bilgisi = False)
            profile = taseron_hakedisles.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi__taseron_ait_bilgisi = request.user)

    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =taseron_hakedisles.objects.filter(Q(proje_ait_bilgisi__taseron_ait_bilgisi__last_name__icontains = search)|Q(dosya_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.hakedisler_gorme:
                        profile = taseron_hakedisles.objects.filter(Q(proje_ait_bilgisi__taseron_ait_bilgisi = request.user.kullanicilar_db) & Q(proje_ait_bilgisi__taseron_adi__icontains = search)& Q(silinme_bilgisi = False))
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = page_obj
    #content["blog_bilgisi"]  =projeler.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    content["taseronlar"] = taseronlar.objects.filter(taseron_ait_bilgisi= request.user,silinme_bilgisi = False)
    return render(request,"santiye_yonetimi/hakedis_depo.html",content)

#sözleşme olaylari
#dokumanlari_gosterme
def yapilacaklar_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if super_admin_kontrolu(request):
        profile = IsplaniPlanlari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        content["blog_bilgisi"]  =CustomUser.objects.filter(kullanicilar_db = users,kullanici_silme_bilgisi = False,is_active = True)
        profile = IsplaniPlanlari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = users)
        content["katmanlar"] = katman.objects.filter(proje_ait_bilgisi = users ,silinme_bilgisi = False)
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.yapilacaklar_gorme:
                    profile = IsplaniPlanlari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user.kullanicilar_db)
                    if a.izinler.yapilacaklar_olusturma:
                        content["blog_bilgisi"]  =CustomUser.objects.filter(kullanicilar_db = request.user.kullanicilar_db,kullanici_silme_bilgisi = False,is_active = True)
                        content["katmanlar"] = katman.objects.filter(proje_ait_bilgisi = request.user.kullanicilar_db,silinme_bilgisi = False)
    
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            content["blog_bilgisi"]  =CustomUser.objects.filter(kullanicilar_db = request.user,kullanici_silme_bilgisi = False,is_active = True)
            profile = IsplaniPlanlari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)
            content["katmanlar"] = katman.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = profile
    
    return render(request,"santiye_yonetimi/yapilacaklar.html",content)
#yapilacakalr
def yapilacaklar(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile = IsplaniPlanlari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.yapilacaklar_gorme:
                    profile = IsplaniPlanlari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user.kullanicilar_db)
                    if a.izinler.yapilacaklar_olusturma:
                        content["blog_bilgisi"]  =CustomUser.objects.filter(kullanicilar_db = request.user.kullanicilar_db,kullanici_silme_bilgisi = False,is_active = True)
                        content["katmanlar"] = katman.objects.filter(proje_ait_bilgisi = request.user.kullanicilar_db,silinme_bilgisi = False)
    
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            content["blog_bilgisi"]  =CustomUser.objects.filter(kullanicilar_db = request.user,kullanici_silme_bilgisi = False,is_active = True)
            profile = IsplaniPlanlari.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)
            content["katmanlar"] = katman.objects.filter(proje_ait_bilgisi = request.user,silinme_bilgisi = False)
    
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = profile
    
    return render(request,"santiye_yonetimi/yapilacaklar.html",content)
#yapilacakalr
def yapilacak_gonder_json(request,id):
    
    
    a = get_object_or_404(IsplaniPlanlari, id = id)
    sonuc = {}

    # title varsa ekle
    
    sonuc["id"] = id
    if hasattr(a, 'title'):
        sonuc["title"] = a.title

    # aciklama varsa ekle
    if hasattr(a, 'aciklama'):
        sonuc["aciklama"] = a.aciklama

    # teslim_tarihi varsa ekle
    if hasattr(a, 'teslim_tarihi'):
        sonuc["teslim_tarihi"] = a.teslim_tarihi

    # status varsa ekle
    if hasattr(a, 'status'):
        sonuc["status"] = a.status

    # oncelik_durumu varsa ekle
    if hasattr(a, 'oncelik_durumu'):
        sonuc["oncelik_durumu"] = a.oncelik_durumu

    # katman_id varsa ekle
    if hasattr(a, 'katman') and hasattr(a.katman, 'id'):
        sonuc["katman_id"] = a.katman.id
    
        
    
    # blok_id varsa ekle
    if hasattr(a, 'blok') and hasattr(a.blok, 'id'):
        sonuc["blok_id"] = a.blok.id
    if hasattr(a, 'locasyonx') :
        sonuc["locasyonx"] = a.locasyonx
    if hasattr(a, 'locasyony') :
        sonuc["locasyony"] = a.locasyony
    # katman varsa ekle
    if hasattr(a, 'katman') and hasattr(a.katman, 'katman_adi'):
        sonuc["katman"] = a.katman.katman_adi
    if hasattr(a, 'katman') and hasattr(a.katman, 'katman_dosyasi'):
        sonuc["katman_dosyasi"] = a.katman.katman_dosyasi.url

    # blok varsa ekle
    if hasattr(a, 'blok') and hasattr(a.blok, 'blog_adi'):
        sonuc["blok"] = a.blok.blog_adi

    # kat varsa ekle
    if hasattr(a, 'kat'):
        sonuc["kat"] = a.kat
    try:
        sonuc["isaretli"] = IsplaniDosyalari.objects.filter(proje_ait_bilgisi = a,pin = "pin").last().dosya.url
    except:
        sonuc["isaretli"] =""
    print(sonuc)
    return JsonResponse(sonuc)
import base64
from django.core.files.base import ContentFile
def yapilacalar_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.yapilacaklar_olusturma:
                        baslik = request.POST.get("baslik")
                        durum = request.POST.get("durum")
                        aciliyet =request.POST.get("aciliyet")
                        teslim_tarihi = request.POST.get("teslim_tarihi")
                        blogbilgisi = request.POST.getlist("blogbilgisi")
                        aciklama = request.POST.get("aciklama")
                        katman_bilgisi = request.POST.get("katman")
                        yapi_gonder = request.POST.get("yapi_gonder")
                        kat = request.POST.get("kat")
                        base64_image = request.POST.get('base_64_format', '')
                        pin_lokasyunuxd = request.POST.get("pin_lokasyunux") 
                        pin_lokasyunuyd = request.POST.get("pin_lokasyunuy") 
                        if base64_image !="" .startswith('data:image/png;base64,'):
                            base64_image = base64_image.replace('data:image/png;base64,', '')
                            file_extension = 'png'
                        elif base64_image !="" .startswith('data:image/jpeg;base64,'):
                            base64_image = base64_image.replace('data:image/jpeg;base64,', '')
                            file_extension = 'jpeg'
                        
                        if base64_image !=""  :
                            image_data = base64.b64decode(base64_image)
                            image_file = ContentFile(image_data, name=f'image.{file_extension}')
                        if kat== None or kat  == ""  :
                            kat = 0

                        new_project = IsplaniPlanlari(
                            proje_ait_bilgisi = request.user.kullanicilar_db,
                            title = baslik,
                            status = durum,
                            aciklama = aciklama,
                            oncelik_durumu =aciliyet,
                            teslim_tarihi = teslim_tarihi,silinme_bilgisi = False,
                            blok = get_object_or_none(bloglar,id = yapi_gonder),
                            katman = get_object_or_none(katman,id = katman_bilgisi),
                            kat = kat,locasyonx = pin_lokasyunuxd,locasyony = pin_lokasyunuyd
                        )
                        new_project.save()
                        bloglar_bilgisi = []
                        for i in blogbilgisi:
                            bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
                        new_project.yapacaklar.add(*bloglar_bilgisi)
                        images = request.FILES.getlist('file')
                        print(images)
                        isim = 1
                        for images in images:
                            IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user.kullanicilar_db,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                            isim = isim+1
                        if base64_image !="" :
                            IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user.kullanicilar_db,dosya=image_file,pin="pin")
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                baslik = request.POST.get("baslik")
                durum = request.POST.get("durum")
                aciliyet =request.POST.get("aciliyet")
                teslim_tarihi = request.POST.get("teslim_tarihi")
                blogbilgisi = request.POST.getlist("blogbilgisi")
                aciklama = request.POST.get("aciklama")
                katman_bilgisi = request.POST.get("katman")
                yapi_gonder = request.POST.get("yapi_gonder")
                kat = request.POST.get("kat")
                base64_image = request.POST.get('base_64_format', '')
                pin_lokasyunuxd = request.POST.get("pin_lokasyunux") 
                pin_lokasyunuyd = request.POST.get("pin_lokasyunuy")
                if base64_image !="" .startswith('data:image/png;base64,'):
                    base64_image = base64_image.replace('data:image/png;base64,', '')
                    file_extension = 'png'
                elif base64_image !="" .startswith('data:image/jpeg;base64,'):
                    base64_image = base64_image.replace('data:image/jpeg;base64,', '')
                    file_extension = 'jpeg'
                if kat == None or kat  == ""  :
                    kat = 0
                print(kat)
                new_project = IsplaniPlanlari(
                    proje_ait_bilgisi = request.user,
                    title = baslik,
                    status = durum,
                    aciklama = aciklama,
                    oncelik_durumu =aciliyet,
                    teslim_tarihi = teslim_tarihi,silinme_bilgisi = False,
                    blok = get_object_or_none(bloglar,id = yapi_gonder),
                    katman = get_object_or_none(katman,id = katman_bilgisi),
                    kat = kat,locasyonx = pin_lokasyunuxd,locasyony = pin_lokasyunuyd
                )
                new_project.save()
                bloglar_bilgisi = []
                for i in blogbilgisi:
                    bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
                new_project.yapacaklar.add(*bloglar_bilgisi)
                images = request.FILES.getlist('file')
                print(images)
                isim = 1
                for images in images:
                    IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                    isim = isim+1
                if base64_image !=""  :
                    image_data = base64.b64decode(base64_image)
                    image_file = ContentFile(image_data, name=f'image.{file_extension}')
                if base64_image !="" :
                    IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user,dosya=image_file,pin="pin")
    return redirect("main:yapilacaklar")
#
def yapilacalar_ekle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            if True:
                baslik = request.POST.get("baslik")
                durum = request.POST.get("durum")
                aciliyet =request.POST.get("aciliyet")
                teslim_tarihi = request.POST.get("teslim_tarihi")
                blogbilgisi = request.POST.getlist("blogbilgisi")
                aciklama = request.POST.get("aciklama")
                katman_bilgisi = request.POST.get("katman")
                yapi_gonder = request.POST.get("yapi_gonder")
                kat = request.POST.get("kat")
                base64_image = request.POST.get('base_64_format', '')
                pin_lokasyunuxd = request.POST.get("pin_lokasyunux") 
                pin_lokasyunuyd = request.POST.get("pin_lokasyunuy")
                if base64_image !="" .startswith('data:image/png;base64,'):
                    base64_image = base64_image.replace('data:image/png;base64,', '')
                    file_extension = 'png'
                elif base64_image !="" .startswith('data:image/jpeg;base64,'):
                    base64_image = base64_image.replace('data:image/jpeg;base64,', '')
                    file_extension = 'jpeg'
                if kat == None or kat  == ""  :
                    kat = 0
                print(kat)
                new_project = IsplaniPlanlari(
                    proje_ait_bilgisi = users,
                    title = baslik,
                    status = durum,
                    aciklama = aciklama,
                    oncelik_durumu =aciliyet,
                    teslim_tarihi = teslim_tarihi,silinme_bilgisi = False,
                    blok = get_object_or_none(bloglar,id = yapi_gonder),
                    katman = get_object_or_none(katman,id = katman_bilgisi),
                    kat = kat,locasyonx = pin_lokasyunuxd,locasyony = pin_lokasyunuyd
                )
                new_project.save()
                bloglar_bilgisi = []
                for i in blogbilgisi:
                    bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
                new_project.yapacaklar.add(*bloglar_bilgisi)
                images = request.FILES.getlist('file')
                print(images)
                isim = 1
                for images in images:
                    IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = users,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                    isim = isim+1
                if base64_image !=""  :
                    image_data = base64.b64decode(base64_image)
                    image_file = ContentFile(image_data, name=f'image.{file_extension}')
                if base64_image !="" :
                    IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = users,dosya=image_file,pin="pin")
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.yapilacaklar_olusturma:
                        baslik = request.POST.get("baslik")
                        durum = request.POST.get("durum")
                        aciliyet =request.POST.get("aciliyet")
                        teslim_tarihi = request.POST.get("teslim_tarihi")
                        blogbilgisi = request.POST.getlist("blogbilgisi")
                        aciklama = request.POST.get("aciklama")
                        katman_bilgisi = request.POST.get("katman")
                        yapi_gonder = request.POST.get("yapi_gonder")
                        kat = request.POST.get("kat")
                        base64_image = request.POST.get('base_64_format', '')
                        pin_lokasyunuxd = request.POST.get("pin_lokasyunux") 
                        pin_lokasyunuyd = request.POST.get("pin_lokasyunuy") 
                        if base64_image !="" .startswith('data:image/png;base64,'):
                            base64_image = base64_image.replace('data:image/png;base64,', '')
                            file_extension = 'png'
                        elif base64_image !="" .startswith('data:image/jpeg;base64,'):
                            base64_image = base64_image.replace('data:image/jpeg;base64,', '')
                            file_extension = 'jpeg'
                        
                        if base64_image !=""  :
                            image_data = base64.b64decode(base64_image)
                            image_file = ContentFile(image_data, name=f'image.{file_extension}')
                        if kat== None or kat  == ""  :
                            kat = 0

                        new_project = IsplaniPlanlari(
                            proje_ait_bilgisi = request.user.kullanicilar_db,
                            title = baslik,
                            status = durum,
                            aciklama = aciklama,
                            oncelik_durumu =aciliyet,
                            teslim_tarihi = teslim_tarihi,silinme_bilgisi = False,
                            blok = get_object_or_none(bloglar,id = yapi_gonder),
                            katman = get_object_or_none(katman,id = katman_bilgisi),
                            kat = kat,locasyonx = pin_lokasyunuxd,locasyony = pin_lokasyunuyd
                        )
                        new_project.save()
                        bloglar_bilgisi = []
                        for i in blogbilgisi:
                            bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
                        new_project.yapacaklar.add(*bloglar_bilgisi)
                        images = request.FILES.getlist('file')
                        print(images)
                        isim = 1
                        for images in images:
                            IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user.kullanicilar_db,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                            isim = isim+1
                        if base64_image !="" :
                            IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user.kullanicilar_db,dosya=image_file,pin="pin")
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                baslik = request.POST.get("baslik")
                durum = request.POST.get("durum")
                aciliyet =request.POST.get("aciliyet")
                teslim_tarihi = request.POST.get("teslim_tarihi")
                blogbilgisi = request.POST.getlist("blogbilgisi")
                aciklama = request.POST.get("aciklama")
                katman_bilgisi = request.POST.get("katman")
                yapi_gonder = request.POST.get("yapi_gonder")
                kat = request.POST.get("kat")
                base64_image = request.POST.get('base_64_format', '')
                pin_lokasyunuxd = request.POST.get("pin_lokasyunux") 
                pin_lokasyunuyd = request.POST.get("pin_lokasyunuy")
                if base64_image !="" .startswith('data:image/png;base64,'):
                    base64_image = base64_image.replace('data:image/png;base64,', '')
                    file_extension = 'png'
                elif base64_image !="" .startswith('data:image/jpeg;base64,'):
                    base64_image = base64_image.replace('data:image/jpeg;base64,', '')
                    file_extension = 'jpeg'
                if kat == None or kat  == ""  :
                    kat = 0
                print(kat)
                new_project = IsplaniPlanlari(
                    proje_ait_bilgisi = request.user,
                    title = baslik,
                    status = durum,
                    aciklama = aciklama,
                    oncelik_durumu =aciliyet,
                    teslim_tarihi = teslim_tarihi,silinme_bilgisi = False,
                    blok = get_object_or_none(bloglar,id = yapi_gonder),
                    katman = get_object_or_none(katman,id = katman_bilgisi),
                    kat = kat,locasyonx = pin_lokasyunuxd,locasyony = pin_lokasyunuyd
                )
                new_project.save()
                bloglar_bilgisi = []
                for i in blogbilgisi:
                    bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
                new_project.yapacaklar.add(*bloglar_bilgisi)
                images = request.FILES.getlist('file')
                print(images)
                isim = 1
                for images in images:
                    IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                    isim = isim+1
                if base64_image !=""  :
                    image_data = base64.b64decode(base64_image)
                    image_file = ContentFile(image_data, name=f'image.{file_extension}')
                if base64_image !="" :
                    IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user,dosya=image_file,pin="pin")
    return redirect("main:yapilacaklar_2",hash)
#
def yapilacalar_ekle_duzenleme(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.yapilacaklar_olusturma:
                        id = request.POST.get("id")
                        baslik = request.POST.get("baslik")
                        durum = request.POST.get("durum")
                        aciliyet =request.POST.get("aciliyet")
                        teslim_tarihi = request.POST.get("teslim_tarihi")
                        blogbilgisi = request.POST.getlist("blogbilgisi")
                        aciklama = request.POST.get("aciklama")
                        katman_bilgisi = request.POST.get("katman")
                        yapi_gonder = request.POST.get("yapi_gonder")
                        kat = request.POST.get("kat")
                        base64_image = request.POST.get('base_64_format', '')
                        pin_lokasyunuxd = request.POST.get("pin_lokasyunuxd") 
                        pin_lokasyunuyd = request.POST.get("pin_lokasyunuyd")
                        if kat == None or kat  == ""  :
                            kat = 0
                        if base64_image !="" .startswith('data:image/png;base64,'):
                            base64_image = base64_image.replace('data:image/png;base64,', '')
                            file_extension = 'png'
                        elif base64_image !="" .startswith('data:image/jpeg;base64,'):
                            base64_image = base64_image.replace('data:image/jpeg;base64,', '')
                            file_extension = 'jpeg'
                        
                        image_data = base64.b64decode(base64_image)
                        image_file = ContentFile(image_data, name=f'image.{file_extension}')
                        IsplaniPlanlari.objects.filter(id = id).update(
                            proje_ait_bilgisi = request.user.kullanicilar_db,
                            title = baslik,
                            status = durum,
                            aciklama = aciklama,
                            oncelik_durumu =aciliyet,
                            teslim_tarihi = teslim_tarihi,silinme_bilgisi = False,
                            blok = get_object_or_none(bloglar,id = yapi_gonder),
                            katman = get_object_or_none(katman,id = katman_bilgisi),
                            kat = kat,locasyonx = pin_lokasyunuxd,locasyony = pin_lokasyunuyd
                        )
                        new_project = get_object_or_none(IsplaniPlanlari,id = id)
                        new_project.save()
                        bloglar_bilgisi = []
                        for i in blogbilgisi:
                            bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
                        new_project.yapacaklar.add(*bloglar_bilgisi)
                        images = request.FILES.getlist('file')
                        print(images)
                        isim = 1
                        for images in images:
                            IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user.kullanicilar_db,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                            isim = isim+1
                        if base64_image !="" :
                            IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user.kullanicilar_db,dosya=image_file,pin="pin")
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                id = request.POST.get("id")
                baslik = request.POST.get("baslik")
                durum = request.POST.get("durum")
                aciliyet =request.POST.get("aciliyet")
                teslim_tarihi = request.POST.get("teslim_tarihi")
                blogbilgisi = request.POST.getlist("blogbilgisi")
                aciklama = request.POST.get("aciklama")
                katman_bilgisi = request.POST.get("katman")
                yapi_gonder = request.POST.get("yapi_gonder")
                kat = request.POST.get("kat")
                base64_image = request.POST.get('base_64_format', '')
                pin_lokasyunuxd = request.POST.get("pin_lokasyunuxd") 
                pin_lokasyunuyd = request.POST.get("pin_lokasyunuyd") 
                if kat == None or kat  == ""  :
                    kat = 0
                if base64_image !="" .startswith('data:image/png;base64,'):
                    base64_image = base64_image.replace('data:image/png;base64,', '')
                    file_extension = 'png'
                elif base64_image !="" .startswith('data:image/jpeg;base64,'):
                    base64_image = base64_image.replace('data:image/jpeg;base64,', '')
                    file_extension = 'jpeg'
                        
                image_data = base64.b64decode(base64_image)
                image_file = ContentFile(image_data, name=f'image.{file_extension}')
                IsplaniPlanlari.objects.filter(id = id).update(
                    proje_ait_bilgisi = request.user,
                    title = baslik,
                    status = durum,
                    aciklama = aciklama,
                    oncelik_durumu =aciliyet,
                    teslim_tarihi = teslim_tarihi,silinme_bilgisi = False,
                    blok = get_object_or_none(bloglar,id = yapi_gonder),
                    katman = get_object_or_none(katman,id = katman_bilgisi),
                    kat = kat,locasyonx = pin_lokasyunuxd,locasyony = pin_lokasyunuyd
                )
                new_project = get_object_or_none(IsplaniPlanlari,id = id)
                new_project.save()
                bloglar_bilgisi = []
                for i in blogbilgisi:
                    bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
                new_project.yapacaklar.add(*bloglar_bilgisi)
                images = request.FILES.getlist('file')
                print(images)
                isim = 1
                for images in images:
                    IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                    isim = isim+1
                if base64_image !="" :
                    IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user,dosya=image_file,pin="pin")
    return redirect("main:yapilacaklar")
#
def yapilacalar_ekle_duzenleme_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            if True:
                id = request.POST.get("id")
                baslik = request.POST.get("baslik")
                durum = request.POST.get("durum")
                aciliyet =request.POST.get("aciliyet")
                teslim_tarihi = request.POST.get("teslim_tarihi")
                blogbilgisi = request.POST.getlist("blogbilgisi")
                aciklama = request.POST.get("aciklama")
                katman_bilgisi = request.POST.get("katman")
                yapi_gonder = request.POST.get("yapi_gonder")
                kat = request.POST.get("kat")
                base64_image = request.POST.get('base_64_format', '')
                pin_lokasyunuxd = request.POST.get("pin_lokasyunuxd") 
                pin_lokasyunuyd = request.POST.get("pin_lokasyunuyd") 
                if kat == None or kat  == ""  :
                    kat = 0
                if base64_image !="" .startswith('data:image/png;base64,'):
                    base64_image = base64_image.replace('data:image/png;base64,', '')
                    file_extension = 'png'
                elif base64_image !="" .startswith('data:image/jpeg;base64,'):
                    base64_image = base64_image.replace('data:image/jpeg;base64,', '')
                    file_extension = 'jpeg'
                        
                image_data = base64.b64decode(base64_image)
                image_file = ContentFile(image_data, name=f'image.{file_extension}')
                IsplaniPlanlari.objects.filter(id = id).update(
                    proje_ait_bilgisi = users,
                    title = baslik,
                    status = durum,
                    aciklama = aciklama,
                    oncelik_durumu =aciliyet,
                    teslim_tarihi = teslim_tarihi,silinme_bilgisi = False,
                    blok = get_object_or_none(bloglar,id = yapi_gonder),
                    katman = get_object_or_none(katman,id = katman_bilgisi),
                    kat = kat,locasyonx = pin_lokasyunuxd,locasyony = pin_lokasyunuyd
                )
                new_project = get_object_or_none(IsplaniPlanlari,id = id)
                new_project.save()
                bloglar_bilgisi = []
                for i in blogbilgisi:
                    bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
                new_project.yapacaklar.add(*bloglar_bilgisi)
                images = request.FILES.getlist('file')
                print(images)
                isim = 1
                for images in images:
                    IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = users,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                    isim = isim+1
                if base64_image !="" :
                    IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = users,dosya=image_file,pin="pin")
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.yapilacaklar_olusturma:
                        id = request.POST.get("id")
                        baslik = request.POST.get("baslik")
                        durum = request.POST.get("durum")
                        aciliyet =request.POST.get("aciliyet")
                        teslim_tarihi = request.POST.get("teslim_tarihi")
                        blogbilgisi = request.POST.getlist("blogbilgisi")
                        aciklama = request.POST.get("aciklama")
                        katman_bilgisi = request.POST.get("katman")
                        yapi_gonder = request.POST.get("yapi_gonder")
                        kat = request.POST.get("kat")
                        base64_image = request.POST.get('base_64_format', '')
                        pin_lokasyunuxd = request.POST.get("pin_lokasyunuxd") 
                        pin_lokasyunuyd = request.POST.get("pin_lokasyunuyd")
                        if kat == None or kat  == ""  :
                            kat = 0
                        if base64_image !="" .startswith('data:image/png;base64,'):
                            base64_image = base64_image.replace('data:image/png;base64,', '')
                            file_extension = 'png'
                        elif base64_image !="" .startswith('data:image/jpeg;base64,'):
                            base64_image = base64_image.replace('data:image/jpeg;base64,', '')
                            file_extension = 'jpeg'
                        
                        image_data = base64.b64decode(base64_image)
                        image_file = ContentFile(image_data, name=f'image.{file_extension}')
                        IsplaniPlanlari.objects.filter(id = id).update(
                            proje_ait_bilgisi = request.user.kullanicilar_db,
                            title = baslik,
                            status = durum,
                            aciklama = aciklama,
                            oncelik_durumu =aciliyet,
                            teslim_tarihi = teslim_tarihi,silinme_bilgisi = False,
                            blok = get_object_or_none(bloglar,id = yapi_gonder),
                            katman = get_object_or_none(katman,id = katman_bilgisi),
                            kat = kat,locasyonx = pin_lokasyunuxd,locasyony = pin_lokasyunuyd
                        )
                        new_project = get_object_or_none(IsplaniPlanlari,id = id)
                        new_project.save()
                        bloglar_bilgisi = []
                        for i in blogbilgisi:
                            bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
                        new_project.yapacaklar.add(*bloglar_bilgisi)
                        images = request.FILES.getlist('file')
                        print(images)
                        isim = 1
                        for images in images:
                            IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user.kullanicilar_db,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                            isim = isim+1
                        if base64_image !="" :
                            IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user.kullanicilar_db,dosya=image_file,pin="pin")
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                id = request.POST.get("id")
                baslik = request.POST.get("baslik")
                durum = request.POST.get("durum")
                aciliyet =request.POST.get("aciliyet")
                teslim_tarihi = request.POST.get("teslim_tarihi")
                blogbilgisi = request.POST.getlist("blogbilgisi")
                aciklama = request.POST.get("aciklama")
                katman_bilgisi = request.POST.get("katman")
                yapi_gonder = request.POST.get("yapi_gonder")
                kat = request.POST.get("kat")
                base64_image = request.POST.get('base_64_format', '')
                pin_lokasyunuxd = request.POST.get("pin_lokasyunuxd") 
                pin_lokasyunuyd = request.POST.get("pin_lokasyunuyd") 
                if kat == None or kat  == ""  :
                    kat = 0
                if base64_image !="" .startswith('data:image/png;base64,'):
                    base64_image = base64_image.replace('data:image/png;base64,', '')
                    file_extension = 'png'
                elif base64_image !="" .startswith('data:image/jpeg;base64,'):
                    base64_image = base64_image.replace('data:image/jpeg;base64,', '')
                    file_extension = 'jpeg'
                        
                image_data = base64.b64decode(base64_image)
                image_file = ContentFile(image_data, name=f'image.{file_extension}')
                IsplaniPlanlari.objects.filter(id = id).update(
                    proje_ait_bilgisi = request.user,
                    title = baslik,
                    status = durum,
                    aciklama = aciklama,
                    oncelik_durumu =aciliyet,
                    teslim_tarihi = teslim_tarihi,silinme_bilgisi = False,
                    blok = get_object_or_none(bloglar,id = yapi_gonder),
                    katman = get_object_or_none(katman,id = katman_bilgisi),
                    kat = kat,locasyonx = pin_lokasyunuxd,locasyony = pin_lokasyunuyd
                )
                new_project = get_object_or_none(IsplaniPlanlari,id = id)
                new_project.save()
                bloglar_bilgisi = []
                for i in blogbilgisi:
                    bloglar_bilgisi.append(CustomUser.objects.get(id=int(i)))
                new_project.yapacaklar.add(*bloglar_bilgisi)
                images = request.FILES.getlist('file')
                print(images)
                isim = 1
                for images in images:
                    IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                    isim = isim+1
                if base64_image !="" :
                    IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user,dosya=image_file,pin="pin")
    return redirect("main:yapilacaklar_2",hash)
#
def yapilacalar_ekle_toplu(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.yapilacaklar_olusturma:
                        baslik = request.POST.get("baslik")
                        durum = request.POST.get("durum")
                        aciliyet =request.POST.get("aciliyet")
                        teslim_tarihi = request.POST.get("teslim_tarihi")
                        blogbilgisi = request.POST.getlist("blogbilgisi")
                        aciklama = request.POST.getlist("aciklama")
                        for i in range(0,len(aciklama)):
                            if aciklama[i]:
                                new_project = IsplaniPlanlari(
                                    proje_ait_bilgisi = request.user.kullanicilar_db,
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
                                print(images,"resim geldi")
                                for images in images:
                                    IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user.kullanicilar_db,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                                    isim = isim+1
                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
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
                        print(images,"resim geldi")
                        for images in images:
                            IsplaniDosyalari.objects.create(proje_ait_bilgisi = get_object_or_404(IsplaniPlanlari,id = new_project.id),dosya_sahibi = request.user,dosya=images)  # Urun_resimleri modeline resimleri kaydet
                            isim = isim+1
    return redirect("main:yapilacaklar")

def yapilacalar_sil_2(request,hash):
    
    if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.yapilacaklar_silme:
                    pass
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
    else:
        pass
    if True:
        content = sozluk_yapisi()
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
        if request.POST:
            id = request.POST.get("id_bilgisi")
            IsplaniPlanlari.objects.filter(id = id).update(silinme_bilgisi = True)
    return redirect("main:yapilacaklar_2",hash)

def yapilacalar_sil(request):
    if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.yapilacaklar_silme:
                    pass
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
    else:
        pass
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
        IsplaniPlanlari.objects.filter(id =yenilenecekeklemeyapilacak).update(status = durum)
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
    content["santiyeler"] = profile
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
    if super_admin_kontrolu(request):
        profile = IsplaniPlanlari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.gant_gorme:
                    content["gant"]  =gantt_olayi.objects.filter(gantt_sahibii = request.user.kullanicilar_db).last()
    
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            content["gant"]  =gantt_olayi.objects.filter(gantt_sahibii = request.user).last()
            
    
    return render(request,"santiye_yonetimi/takvim.html",content)
#takvim
from django.http import JsonResponse
from django.shortcuts import redirect

def gant_kaydet(request):
    if request.method == 'POST':
        gant_verisi = request.POST.get("gant_verisi")
        if not gant_verisi:
            return JsonResponse({'ok': False, 'message': 'Gantt verisi bulunamadı.'})

        if super_admin_kontrolu(request):
            # Super admin işlemleri
            pass
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar, kullanicilar=request.user)
                if a and a.izinler.gant_duzenleme:
                    kullanici = request.user.kullanicilar_db
                else:
                    return JsonResponse({'ok': False, 'message': 'Yetkisiz erişim'}, status=403)
            else:
                kullanici = request.user

        gantt_olayi.objects.create(
            gantt_sahibii=kullanici,
            ganti_degistiren_kisi=request.user,
            gantt_verisi=gant_verisi
        )

        return JsonResponse({'ok': True, 'message': 'Gantt kaydedildi'})
    
    return redirect("main:takvim_olaylari")

def santiye_raporu_2(request,id,hash):
    content = sozluk_yapisi()
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.santiye_raporu_gorme:
                profile =  get_object_or_404(bloglar,proje_ait_bilgisi = request.user.kullanicilar_db,id = id )
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        profile =  get_object_or_404(bloglar,proje_ait_bilgisi = users,id = id )
    content["santiye"] = profile
    return render(request,"santiye_yonetimi/santiye_raporu.html",content)

def santiye_raporu(request,id):
    content = sozluk_yapisi()
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.santiye_raporu_gorme:
                profile =  get_object_or_404(bloglar,proje_ait_bilgisi = request.user.kullanicilar_db,id = id )
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        profile =  get_object_or_404(bloglar,proje_ait_bilgisi = request.user,id = id )
    content["santiye"] = profile
    return render(request,"santiye_yonetimi/santiye_raporu.html",content)

def kullanici_yetkileri(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        pass
    else:
        if request.user.kullanicilar_db:
            return redirect("main:yetkisiz")
        profile = personel_izinleri.objects.filter(izinlerin_sahibi_kullanici = request.user)
        content["izinler"] = profile
    return render(request,"kullanici_yetkileri/yetkiler.html",content)
def kullanici_yetkileri_duzenle(request,id):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        pass
    else:
        if request.user.kullanicilar_db:
            return redirect("main:yetkisiz")
        profile = personel_izinleri.objects.filter(izinlerin_sahibi_kullanici = request.user)
        content["izinler"] = profile
        content["secili_grup"] = get_object_or_404(personel_izinleri,id = id)
    return render(request,"kullanici_yetkileri/yetkiler.html",content)
def kullanici_yetki_olustur(request):
    if request.user.kullanicilar_db:
        return redirect("main:yetkisiz")
    if request.POST:
        grup_adi = request.POST.get("grup_adi")
        personel_izinleri.objects.create(
            isim = grup_adi,
            izinlerin_sahibi_kullanici = request.user
        )
    return redirect("main:kullanici_yetkileri")
def kullanici_yetki_adi_duzenle(request):
    if request.user.kullanicilar_db:
        return redirect("main:yetkisiz")
    if request.POST:
        grup_adi = request.POST.get("grup_adi")
        id  = request.POST.get("id")
        personel_izinleri.objects.filter(id = id).update(
            isim = grup_adi,
            izinlerin_sahibi_kullanici = request.user
        )
    return redirect("main:kullanici_yetkileri")
def kullanici_yetki_sil(request):
    if request.user.kullanicilar_db:
        return redirect("main:yetkisiz")
    if request.POST:
        id  = request.POST.get("id")
        personel_izinleri.objects.filter(id = id,izinlerin_sahibi_kullanici = request.user).delete()
    return redirect("main:kullanici_yetkileri")
def kullanici_yetki_alma(request):
    if request.user.kullanicilar_db:
        return redirect("main:yetkisiz")
    if request.POST:
        guncellenen = request.POST.get("guncellenen")
        izinler = get_object_or_404(personel_izinleri,id = guncellenen) 
        ##
        #izinleri Sıfırla
        izinler.dashboard_gorme = False
        izinler.dashboard_silme = False
        izinler.dashboard_duzenleme = False
        izinler.dashboard_olusturma = False
        #
        izinler.gelir_ozeti_gorme = False
        izinler.gelir_ozeti_olusturma = False
        izinler.gelir_ozeti_duzenleme =False
        izinler.gelir_ozeti_silme = False
        #
        izinler.gider_ozeti_gorme = False
        izinler.gider_ozeti_olusturma = False
        izinler.gider_ozeti_duzenleme = False
        izinler.gider_ozeti_silme = False
        #
        izinler.hesap_ekstra_gorme = False
        izinler.hesap_ekstra_olusturma = False
        izinler.hesap_ekstra_duzenleme = False
        izinler.hesap_ekstra_silme = False
        #
        izinler.ilerleme_takibi_gorme = False
        izinler.ilerleme_takibi_olusturma = False
        izinler.ilerleme_takibi_duzenleme = False
        izinler.ilerleme_takibi_silme = False
        #
        izinler.sozlesmeler_gorme = False
        izinler.sozlesmeler_olusturma = False
        izinler.sozlesmeler_duzenleme = False
        izinler.sozlesmeler_silme = False
        #
        izinler.yapilacaklar_gorme = False
        izinler.yapilacaklar_olusturma = False
        izinler.yapilacaklar_duzenleme = False
        izinler.yapilacaklar_silme = False
        #
        izinler.dosya_yoneticisi_gorme = False
        izinler.dosya_yoneticisi_olusturma = False
        izinler.dosya_yoneticisi_duzenleme = False
        izinler.dosya_yoneticisi_silme = False
        #
        izinler.projeler_gorme = False
        izinler.projeler_olusturma = False
        izinler.projeler_duzenleme = False
        izinler.projeler_silme =False
        #
        izinler.personeller_gorme = False
        izinler.personeller_olusturma = False
        izinler.personeller_duzenleme = False
        izinler.personeller_silme = False
        #
        izinler.gelir_faturasi_gorme_izni = False
        izinler.gelir_faturasi_kesme_izni = False
        izinler.gelir_faturasi_duzenleme_izni = False
        izinler.gelir_faturasi_silme_izni = False
        #
        izinler.gider_faturasi_gorme_izni = False
        izinler.gider_faturasi_kesme_izni = False
        izinler.gider_faturasi_duzenleme_izni = False
        izinler.gider_faturasi_silme_izni = False
        #
        izinler.kasa_virman_olusturma_izni = False
        izinler.kasa_virman_gorme_izni = False
        #
        izinler.kasa_gosterme_izni = False
        izinler.kasa_olusturma_izni = False
        izinler.kasa_guncelleme_izni = False
        izinler.Kasa_silme_izni = False
        #
        izinler.cari_gosterme_izni = False
        izinler.cari_olusturma = False
        izinler.cari_guncelleme_izni = False
        izinler.cari_silme_izni = False
        #
        izinler.personeller_gorme = False
        izinler.personeller_olusturma = False
        izinler.personeller_duzenleme = False
        izinler.personeller_silme = False
        #
        izinler.santiye_olusturma = False
        izinler.santiye_silme = False
        izinler.santiye_gorme = False
        izinler.santiye_duzenleme = False
        #
        izinler.blog_olusturma = False
        izinler.blog_silme = False
        izinler.blog_gorme = False
        izinler.blog_duzenleme = False
        #
        izinler.kalemleri_olusturma = False
        izinler.kalemleri_silme = False
        izinler.kalemleri_gorme = False
        izinler.kalemleri_duzenleme = False
        #
        izinler.santiye_raporu_olusturma = False
        izinler.santiye_raporu_silme = False
        izinler.santiye_raporu_gorme = False
        izinler.santiye_raporu_duzenleme = False
        #
        izinler.taseronlar_gorme = False
        izinler.taseronlar_olusturma = False
        izinler.taseronlar_duzenleme = False
        izinler.taseronlar_silme =False
        #
        izinler.hakedisler_gorme = False
        izinler.hakedisler_olusturma = False
        izinler.hakedisler_duzenleme = False
        izinler.hakedisler_silme = False
        #
        izinler.kasa_detay_izni = False
        izinler.cari_detay_izni = False
        ##
        izinler.gelir_kategorisi_gorme = False
        izinler.gelir_kategorisi_olusturma = False
        izinler.gelir_kategorisi_guncelleme = False
        izinler.gelir_kategorisi_silme = False
        #
        izinler.gider_kategorisi_gorme = False
        izinler.gider_kategorisi_olusturma = False
        izinler.gider_kategorisi_guncelleme = False
        izinler.gider_kategorisi_silme = False
        #
        izinler.gelir_etiketi_gorme = False
        izinler.gelir_etiketi_olusturma = False
        izinler.gelir_etiketi_guncelleme = False
        izinler.gelir_etiketi_silme = False
        #
        izinler.gider_etiketi_gorme = False
        izinler.gider_etiketi_olusturma = False
        izinler.gider_etiketi_guncelleme = False
        izinler.gider_etiketi_silme = False
        #
        izinler.urun_gorme = False
        izinler.urun_olusturma = False
        izinler.urun_guncelleme = False
        izinler.urun_silme = False
        #
        izinler.muhasabe_ayarlari_gorme = False
        izinler.muhasabe_ayarlari_guncelleme = False
        #
        izinler.gelir_faturasi_makbuz_gorme_izni = False
        izinler.gelir_faturasi_makbuz_kesme_izni = False
        izinler.gelir_faturasi_makbuz_duzenleme_izni = False
        izinler.gelir_faturasi_makbuz_silme_izni = False
        #
        izinler.gider_faturasi_makbuz_gorme_izni = False
        izinler.gider_faturasi_makbuz_kesme_izni = False
        izinler.gider_faturasi_makbuz_duzenleme_izni = False
        izinler.gider_faturasi_makbuz_silme_izni = False
        #Puantaj
        izinler.personeller_puantaj_olusturma = False
        izinler.personeller_puantaj_silme = False
        izinler.personeller_puantaj_gorme = False
        izinler.personeller_puantaj_duzenleme = False
        #
        # 
        izinler.personeller_odeme_olusturma = False
        izinler.personeller_odeme_silme = False
        izinler.personeller_odeme_gorme = False
        izinler.personeller_odeme_duzenleme = False
        #
        izinler.katman_olusturma = False
        izinler.katman_silme = False
        izinler.katman_gorme = False
        izinler.katman_duzenleme = False
        izinler.save()
        ##
        personeller_puantaj_olusturma = request.POST.get("personeller_puantaj_olusturma")
        if personeller_puantaj_olusturma:
            izinler.personeller_puantaj_olusturma = True
        personeller_puantaj_silme = request.POST.get("personeller_puantaj_silme")
        if personeller_puantaj_silme:
            izinler.personeller_puantaj_silme = True
        personeller_puantaj_gorme = request.POST.get("personeller_puantaj_gorme")
        if personeller_puantaj_gorme:
            izinler.personeller_puantaj_gorme = True
        personeller_puantaj_duzenleme = request.POST.get("personeller_puantaj_duzenleme")
        if personeller_puantaj_duzenleme:
            izinler.personeller_puantaj_duzenleme = True
        #
        personeller_odeme_olusturma = request.POST.get("personeller_odeme_olusturma")
        if personeller_odeme_olusturma:
            izinler.personeller_odeme_olusturma = True
        personeller_odeme_silme = request.POST.get("personeller_odeme_silme")
        if personeller_odeme_silme:
            izinler.personeller_odeme_silme = True
        personeller_odeme_gorme = request.POST.get("personeller_odeme_gorme")
        if personeller_odeme_gorme:
            izinler.personeller_odeme_gorme = True
        personeller_odeme_duzenleme = request.POST.get("personeller_odeme_duzenleme")
        if personeller_odeme_duzenleme:
            izinler.personeller_odeme_duzenleme = True
        #
        katman_olusturma = request.POST.get("katman_olusturma")
        if katman_olusturma:
            izinler.katman_olusturma = True
        katman_silme = request.POST.get("katman_silme")
        if katman_silme:
            izinler.katman_silme = True
        katman_gorme = request.POST.get("katman_gorme")
        if katman_gorme:
            izinler.katman_gorme = True
        katman_duzenleme = request.POST.get("katman_duzenleme")
        if katman_duzenleme:
            izinler.katman_duzenleme = True
        ##
        dashboard_gorme = request.POST.get("dashboard_gorme")
        if dashboard_gorme:
            izinler.dashboard_gorme = True
        dashboard_silme = request.POST.get("dashboard_silme")
        if dashboard_silme:
            izinler.dashboard_silme = True
        dashboard_duzenleme = request.POST.get("dashboard_duzenleme")
        if dashboard_duzenleme:
            izinler.dashboard_duzenleme = True
        dashboard_olusturma = request.POST.get("dashboard_olusturma")
        if dashboard_olusturma:
            izinler.dashboard_olusturma = True
        #
        gelir_ozeti_gorme = request.POST.get("gelir_ozeti_gorme")
        if gelir_ozeti_gorme:
            izinler.gelir_ozeti_gorme = True
        gelir_ozeti_olusturma = request.POST.get("gelir_ozeti_olusturma")
        if gelir_ozeti_olusturma:
            izinler.gelir_ozeti_olusturma = True
        gelir_ozeti_duzenleme = request.POST.get("gelir_ozeti_duzenleme")
        if gelir_ozeti_duzenleme:
            izinler.gelir_ozeti_duzenleme = True
        gelir_ozeti_silme = request.POST.get("gelir_ozeti_silme")
        if gelir_ozeti_silme:
            izinler.gelir_ozeti_silme = True
        #
        gider_ozeti_gorme = request.POST.get("gider_ozeti_gorme")
        if gider_ozeti_gorme:
            izinler.gider_ozeti_gorme = True
        gider_ozeti_olusturma = request.POST.get("gider_ozeti_olusturma")
        if gider_ozeti_olusturma:
            izinler.gider_ozeti_olusturma = True
        gider_ozeti_duzenleme = request.POST.get("gider_ozeti_duzenleme")
        if gider_ozeti_duzenleme:
            izinler.gider_ozeti_duzenleme = True
        gider_ozeti_silme = request.POST.get("gider_ozeti_silme")
        if gider_ozeti_silme:
            izinler.gider_ozeti_silme = True
        #
        hesap_ekstra_gorme = request.POST.get("hesap_ekstra_gorme")
        if hesap_ekstra_gorme:
            izinler.hesap_ekstra_gorme = True
        hesap_ekstra_olusturma = request.POST.get("hesap_ekstra_olusturma")
        if hesap_ekstra_olusturma:
            izinler.hesap_ekstra_olusturma = True
        hesap_ekstra_duzenleme = request.POST.get("hesap_ekstra_duzenleme")
        if hesap_ekstra_duzenleme:
            izinler.hesap_ekstra_duzenleme = True
        hesap_ekstra_silme = request.POST.get("hesap_ekstra_silme")
        if hesap_ekstra_silme:
            izinler.hesap_ekstra_silme = True
        #
        kasa_virman_olusturma_izni = request.POST.get("kasa_virman_olusturma_izni")
        if kasa_virman_olusturma_izni:
            izinler.kasa_virman_olusturma_izni = True
        kasa_virman_gorme_izni = request.POST.get("kasa_virman_gorme_izni")
        if kasa_virman_gorme_izni:
            izinler.kasa_virman_gorme_izni = True
        #
        ilerleme_takibi_gorme = request.POST.get("ilerleme_takibi_gorme")
        if ilerleme_takibi_gorme:
            izinler.ilerleme_takibi_gorme = True
        ilerleme_takibi_olusturma = request.POST.get("ilerleme_takibi_olusturma")
        if ilerleme_takibi_olusturma:
            izinler.ilerleme_takibi_olusturma = True
        ilerleme_takibi_duzenleme = request.POST.get("ilerleme_takibi_duzenleme")
        if ilerleme_takibi_duzenleme:
            izinler.ilerleme_takibi_duzenleme = True
        ilerleme_takibi_silme = request.POST.get("ilerleme_takibi_silme")
        if ilerleme_takibi_silme:
            izinler.ilerleme_takibi_silme = True
        #
        sozlesmeler_gorme = request.POST.get("sozlesmeler_gorme")
        if sozlesmeler_gorme:
            izinler.sozlesmeler_gorme = True
        sozlesmeler_olusturma = request.POST.get("sozlesmeler_olusturma")
        if sozlesmeler_olusturma:
            izinler.sozlesmeler_olusturma = True
        sozlesmeler_duzenleme = request.POST.get("sozlesmeler_duzenleme")
        if sozlesmeler_duzenleme:
            izinler.sozlesmeler_duzenleme = True
        sozlesmeler_silme = request.POST.get("sozlesmeler_silme")
        if sozlesmeler_silme:
            izinler.sozlesmeler_silme = True
        #
        yapilacaklar_gorme = request.POST.get("yapilacaklar_gorme")
        if yapilacaklar_gorme:
            izinler.yapilacaklar_gorme = True
        yapilacaklar_olusturma = request.POST.get("yapilacaklar_olusturma")
        if yapilacaklar_olusturma:
            izinler.yapilacaklar_olusturma = True
        yapilacaklar_duzenleme = request.POST.get("yapilacaklar_duzenleme")
        if yapilacaklar_duzenleme:
            izinler.yapilacaklar_duzenleme = True
        yapilacaklar_silme = request.POST.get("yapilacaklar_silme")
        if yapilacaklar_silme:
            izinler.yapilacaklar_silme = True
        #
        dosya_yoneticisi_gorme = request.POST.get("dosya_yoneticisi_gorme")
        if dosya_yoneticisi_gorme:
            izinler.dosya_yoneticisi_gorme = True
        dosya_yoneticisi_olusturma = request.POST.get("dosya_yoneticisi_olusturma")
        if dosya_yoneticisi_olusturma:
            izinler.dosya_yoneticisi_olusturma = True
        dosya_yoneticisi_duzenleme = request.POST.get("dosya_yoneticisi_duzenleme")
        if dosya_yoneticisi_duzenleme:
            izinler.dosya_yoneticisi_duzenleme = True
        dosya_yoneticisi_silme = request.POST.get("dosya_yoneticisi_silme")
        if dosya_yoneticisi_silme:
            izinler.dosya_yoneticisi_silme = True
        #
        projeler_gorme = request.POST.get("projeler_gorme")
        if projeler_gorme:
            izinler.projeler_gorme = True
        projeler_olusturma = request.POST.get("projeler_olusturma")
        if projeler_olusturma:
            izinler.projeler_olusturma = True
        projeler_duzenleme = request.POST.get("projeler_duzenleme")
        if projeler_duzenleme:
            izinler.projeler_duzenleme = True
        projeler_silme = request.POST.get("projeler_silme")
        if projeler_silme:
            izinler.projeler_silme = True

        #
        personeller_gorme = request.POST.get("personeller_gorme")
        if personeller_gorme:
            izinler.personeller_gorme = True
        personeller_olusturma = request.POST.get("personeller_olusturma")
        if personeller_olusturma:
            izinler.personeller_olusturma = True
        personeller_duzenleme = request.POST.get("personeller_duzenleme")
        if personeller_duzenleme:
            izinler.personeller_duzenleme = True
        personeller_silme = request.POST.get("personeller_silme")
        if personeller_silme:
            izinler.personeller_silme = True
        #
        gelir_faturasi_gorme_izni = request.POST.get("gelir_faturasi_gorme_izni")
        if gelir_faturasi_gorme_izni:
            izinler.gelir_faturasi_gorme_izni = True
        gelir_faturasi_kesme_izni = request.POST.get("gelir_faturasi_kesme_izni")
        if gelir_faturasi_kesme_izni:
            izinler.gelir_faturasi_kesme_izni = True
        gelir_faturasi_duzenleme_izni = request.POST.get("gelir_faturasi_duzenleme_izni")
        if gelir_faturasi_duzenleme_izni:
            izinler.gelir_faturasi_duzenleme_izni = True
        gelir_faturasi_silme_izni = request.POST.get("gelir_faturasi_silme_izni")
        if gelir_faturasi_silme_izni:
            izinler.gelir_faturasi_silme_izni = True
        #
        gider_faturasi_gorme_izni = request.POST.get("gider_faturasi_gorme_izni")
        if gider_faturasi_gorme_izni:
            izinler.gider_faturasi_gorme_izni = True
        gider_faturasi_kesme_izni = request.POST.get("gider_faturasi_kesme_izni")
        if gider_faturasi_kesme_izni:
            izinler.gider_faturasi_kesme_izni = True
        gider_faturasi_duzenleme_izni = request.POST.get("gider_faturasi_duzenleme_izni")
        if gider_faturasi_duzenleme_izni:
            izinler.gider_faturasi_duzenleme_izni = True
        gider_faturasi_silme_izni = request.POST.get("gider_faturasi_silme_izni")
        if gider_faturasi_silme_izni:
            izinler.gider_faturasi_silme_izni = True
        #
        
        kasa_gosterme_izni = request.POST.get("kasa_gosterme_izni")
        if kasa_gosterme_izni:
            izinler.kasa_gosterme_izni = True
        kasa_olusturma_izni = request.POST.get("kasa_olusturma_izni")
        if kasa_olusturma_izni:
            izinler.kasa_olusturma_izni = True
        kasa_guncelleme_izni = request.POST.get("kasa_guncelleme_izni")
        if kasa_guncelleme_izni:
            izinler.kasa_guncelleme_izni = True
        Kasa_silme_izni = request.POST.get("Kasa_silme_izni")
        if Kasa_silme_izni:
            izinler.Kasa_silme_izni = True
        #
        cari_gosterme_izni = request.POST.get("cari_gosterme_izni")
        if cari_gosterme_izni:
            izinler.cari_gosterme_izni = True
        cari_olusturma = request.POST.get("cari_olusturma")
        if cari_olusturma:
            izinler.cari_olusturma = True
        cari_guncelleme_izni = request.POST.get("cari_guncelleme_izni")
        if cari_guncelleme_izni:
            izinler.cari_guncelleme_izni = True
        cari_silme_izni = request.POST.get("cari_silme_izni")
        if cari_silme_izni:
            izinler.cari_silme_izni = True
        #
        personeller_gorme = request.POST.get("personeller_gorme")
        if personeller_gorme:
            izinler.personeller_gorme = True
        personeller_olusturma = request.POST.get("personeller_olusturma")
        if personeller_olusturma:
            izinler.personeller_olusturma = True
        personeller_duzenleme = request.POST.get("personeller_duzenleme")
        if personeller_duzenleme:
            izinler.personeller_duzenleme = True
        personeller_silme = request.POST.get("personeller_silme")
        if personeller_silme:
            izinler.personeller_silme = True
        #
        santiye_gorme = request.POST.get("santiye_gorme")
        if santiye_gorme:
            izinler.santiye_gorme = True
        santiye_olusturma  = request.POST.get("santiye_olusturma")
        if santiye_olusturma:
            izinler.santiye_olusturma = True
        santiye_duzenleme = request.POST.get("santiye_duzenleme")
        if santiye_duzenleme:
            izinler.santiye_duzenleme = True
        santiye_silme = request.POST.get("santiye_silme")
        if santiye_silme:
            izinler.santiye_silme = True
        #
        blog_gorme = request.POST.get("blog_gorme")
        if blog_gorme:
            izinler.blog_gorme = True
        blog_olusturma  = request.POST.get("blog_olusturma")
        if blog_olusturma:
            izinler.blog_olusturma = True
        blog_duzenleme = request.POST.get("blog_duzenleme")
        if blog_duzenleme:
            izinler.blog_duzenleme = True
        blog_silme = request.POST.get("blog_silme")
        if blog_silme:
            izinler.blog_silme = True
        #
        kalemleri_gorme = request.POST.get("kalemleri_gorme")
        if kalemleri_gorme:
            izinler.kalemleri_gorme = True
        kalemleri_olusturma  = request.POST.get("kalemleri_olusturma")
        if kalemleri_olusturma:
            izinler.kalemleri_olusturma = True
        kalemleri_duzenleme = request.POST.get("kalemleri_duzenleme")
        if kalemleri_duzenleme:
            izinler.kalemleri_duzenleme = True
        kalemleri_silme = request.POST.get("kalemleri_silme")
        if kalemleri_silme:
            izinler.kalemleri_silme = True
        #
        santiye_raporu_gorme = request.POST.get("santiye_raporu_gorme")
        if santiye_raporu_gorme:
            izinler.santiye_raporu_gorme = True
        santiye_raporu_olusturma  = request.POST.get("santiye_raporu_olusturma")
        if santiye_raporu_olusturma:
            izinler.santiye_raporu_olusturma = True
        santiye_raporu_duzenleme = request.POST.get("santiye_raporu_duzenleme")
        if santiye_raporu_duzenleme:
            izinler.santiye_raporu_duzenleme = True
        santiye_raporu_silme = request.POST.get("santiye_raporu_silme")
        if santiye_raporu_silme:
            izinler.santiye_raporu_silme = True
        #
        taseronlar_gorme = request.POST.get("taseronlar_gorme")
        if taseronlar_gorme:
            izinler.taseronlar_gorme = True
        taseronlar_olusturma = request.POST.get("taseronlar_olusturma")
        if taseronlar_olusturma:
            izinler.taseronlar_olusturma = True
        taseronlar_duzenleme = request.POST.get("taseronlar_duzenleme")
        if taseronlar_duzenleme:
            izinler.taseronlar_duzenleme = True
        taseronlar_silme = request.POST.get("taseronlar_silme")
        if taseronlar_silme:
            izinler.taseronlar_silme = True
        #
        hakedisler_gorme = request.POST.get("hakedisler_gorme")
        if hakedisler_gorme:
            izinler.hakedisler_gorme = True
        hakedisler_olusturma = request.POST.get("hakedisler_olusturma")
        if hakedisler_olusturma:
            izinler.hakedisler_olusturma = True
        hakedisler_duzenleme = request.POST.get("hakedisler_duzenleme")
        if hakedisler_duzenleme:
            izinler.hakedisler_duzenleme = True
        hakedisler_silme = request.POST.get("hakedisler_silme")
        if hakedisler_silme:
            izinler.hakedisler_silme = True
        #
        kasa_detay_izni = request.POST.get("kasa_detay_izni")
        if kasa_detay_izni:
            izinler.kasa_detay_izni = True
        cari_detay_izni = request.POST.get("cari_detay_izni")
        if cari_detay_izni:
            izinler.cari_detay_izni = True
        
        #
        gelir_kategorisi_gorme = request.POST.get("gelir_kategorisi_gorme")
        if gelir_kategorisi_gorme:  
            izinler.gelir_kategorisi_gorme = True
        gelir_kategorisi_olusturma = request.POST.get("gelir_kategorisi_olusturma")
        if gelir_kategorisi_olusturma : 
            izinler.gelir_kategorisi_olusturma = True
        gelir_kategorisi_guncelleme = request.POST.get("gelir_kategorisi_guncelleme")
        if gelir_kategorisi_guncelleme : 
            izinler.gelir_kategorisi_guncelleme = True
        gelir_kategorisi_silme = request.POST.get("gelir_kategorisi_silme")
        if gelir_kategorisi_silme : 
            izinler.gelir_kategorisi_silme = True
        
        #
        gider_kategorisi_gorme = request.POST.get("gider_kategorisi_gorme")
        if gider_kategorisi_gorme:  
            izinler.gider_kategorisi_gorme = True
        gider_kategorisi_olusturma = request.POST.get("gider_kategorisi_olusturma")
        if gider_kategorisi_olusturma : 
            izinler.gider_kategorisi_olusturma = True
        gider_kategorisi_guncelleme = request.POST.get("gider_kategorisi_guncelleme")
        if gider_kategorisi_guncelleme : 
            izinler.gider_kategorisi_guncelleme = True
        gider_kategorisi_silme = request.POST.get("gider_kategorisi_silme")
        if gider_kategorisi_silme : 
            izinler.gider_kategorisi_silme = True
        #
        #
        gelir_etiketi_gorme = request.POST.get("gelir_etiketi_gorme")
        if gelir_etiketi_gorme:  
            izinler.gelir_etiketi_gorme = True
        gelir_etiketi_olusturma = request.POST.get("gelir_etiketi_olusturma")
        if gelir_etiketi_olusturma : 
            izinler.gelir_etiketi_olusturma = True
        gelir_etiketi_guncelleme = request.POST.get("gelir_etiketi_guncelleme")
        if gelir_etiketi_guncelleme : 
            izinler.gelir_etiketi_guncelleme = True
        gelir_etiketi_silme = request.POST.get("gelir_etiketi_silme")
        if gelir_etiketi_silme : 
            izinler.gelir_etiketi_silme = True

        #
        gider_etiketi_gorme = request.POST.get("gider_etiketi_gorme")
        if gider_etiketi_gorme:  
            izinler.gider_etiketi_gorme = True
        gider_etiketi_olusturma = request.POST.get("gider_etiketi_olusturma")
        if gider_etiketi_olusturma : 
            izinler.gider_etiketi_olusturma = True
        gider_etiketi_guncelleme = request.POST.get("gider_etiketi_guncelleme")
        if gider_etiketi_guncelleme : 
            izinler.gider_etiketi_guncelleme = True
        gider_etiketi_silme = request.POST.get("gider_etiketi_silme")
        if gider_etiketi_silme : 
            izinler.gider_etiketi_silme = True
        #
        #
        urun_gorme = request.POST.get("urun_gorme")
        if urun_gorme:  
            izinler.urun_gorme = True
        urun_olusturma = request.POST.get("urun_olusturma")
        if urun_olusturma : 
            izinler.urun_olusturma = True
        urun_guncelleme = request.POST.get("urun_guncelleme")
        if urun_guncelleme : 
            izinler.urun_guncelleme = True
        urun_silme = request.POST.get("urun_silme")
        if urun_silme : 
            izinler.urun_silme = True

        #
        muhasabe_ayarlari_gorme = request.POST.get("muhasabe_ayarlari_gorme")
        if muhasabe_ayarlari_gorme : 
            izinler.muhasabe_ayarlari_gorme = True
        muhasabe_ayarlari_guncelleme = request.POST.get("muhasabe_ayarlari_guncelleme")
        if muhasabe_ayarlari_guncelleme : 
            izinler.muhasabe_ayarlari_guncelleme = True

        #
        gelir_faturasi_makbuz_gorme_izni = request.POST.get("gelir_faturasi_makbuz_gorme_izni")
        if gelir_faturasi_makbuz_gorme_izni:  
            izinler.gelir_faturasi_makbuz_gorme_izni = True
        gelir_faturasi_makbuz_kesme_izni = request.POST.get("gelir_faturasi_makbuz_kesme_izni")
        if gelir_faturasi_makbuz_kesme_izni : 
            izinler.gelir_faturasi_makbuz_kesme_izni = True
        gelir_faturasi_makbuz_duzenleme_izni = request.POST.get("gelir_faturasi_makbuz_duzenleme_izni")
        if gelir_faturasi_makbuz_duzenleme_izni : 
            izinler.gelir_faturasi_makbuz_duzenleme_izni = True
        gelir_faturasi_makbuz_silme_izni = request.POST.get("gelir_faturasi_makbuz_silme_izni")
        if gelir_faturasi_makbuz_silme_izni : 
            izinler.gelir_faturasi_makbuz_silme_izni = True
        #
        gider_faturasi_makbuz_gorme_izni = request.POST.get("gider_faturasi_makbuz_gorme_izni")
        if gider_faturasi_makbuz_gorme_izni:  
            izinler.gider_faturasi_makbuz_gorme_izni = True
        gider_faturasi_makbuz_kesme_izni = request.POST.get("gider_faturasi_makbuz_kesme_izni")
        if gider_faturasi_makbuz_kesme_izni : 
            izinler.gider_faturasi_makbuz_kesme_izni = True
        gider_faturasi_makbuz_duzenleme_izni = request.POST.get("gider_faturasi_makbuz_duzenleme_izni")
        if gider_faturasi_makbuz_duzenleme_izni : 
            izinler.gider_faturasi_makbuz_duzenleme_izni = True
        gider_faturasi_makbuz_silme_izni = request.POST.get("gider_faturasi_makbuz_silme_izni")
        if gider_faturasi_makbuz_silme_izni : 
            izinler.gider_faturasi_makbuz_silme_izni = True
        izinler.save()
    return redirect("main:kullanici_yetkileri")

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
    return redirect("main:ana_sayfa")

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
    return redirect("main:ana_sayfa")

def sayfa_denemeleri(request):
    content = sozluk_yapisi()
    return render(request,"xxpuantaj.html",content)
def bildirimler(request):
    content = sozluk_yapisi()
    return render(request,"bildirimler.html",content)

def katman_sayfasi(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =katman.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.katman_gorme:
                    profile = katman.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user.kullanicilar_db)
                    content["insaatlar"] = santiye.objects.filter(proje_ait_bilgisi =  request.user.kullanicilar_db,silinme_bilgisi = False)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = katman.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)
            content["insaatlar"] = santiye.objects.filter(proje_ait_bilgisi =  request.user,silinme_bilgisi = False)
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = profile
    return render(request,"santiye_yonetimi/katman.html",content)

def katman_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            return redirect("main:taseron_ekle_admin",kullanici)
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a.izinler.katman_olusturma:
                    kullanici = request.user.kullanicilar_db
                else:
                    return redirect("main:yetkisiz")
            else:
                kullanici = request.user
        katman_adi = request.POST.get("taseron_adi")
        santiye_al = request.POST.get("blogbilgisi")
        dosya = request.FILES.get("file")
        katman.objects.create(
            proje_ait_bilgisi = kullanici,
            proje_santiye_Ait = get_object_or_none(santiye,id = santiye_al),
            katman_adi  = katman_adi,
            katman_dosyasi = dosya
        )
    return redirect("main:katman_sayfasi")

def katman_sil(request):
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            return redirect("main:taseron_ekle_admin",kullanici)
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a.izinler.katman_silme:
                    buttonIdInput = request.POST.get("buttonId")
                    katman.objects.filter(id = buttonIdInput).update(
                        silinme_bilgisi = True
                    )
                else:
                    return redirect("main:yetkisiz")
            else:
                buttonIdInput = request.POST.get("buttonId")
                katman.objects.filter(id = buttonIdInput).update(
                    silinme_bilgisi = True
                )
        
    return redirect("main:katman_sayfasi")

def katman_duzenle(request):
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            return redirect("main:taseron_ekle_admin",kullanici)
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a.izinler.katman_olusturma:
                    kullanici = request.user.kullanicilar_db
                else:
                    return redirect("main:yetkisiz")
            else:
                kullanici = request.user
        katman_adi = request.POST.get("taseron_adi")
        santiye_al = request.POST.get("blogbilgisi")
        dosya = request.FILES.get("file")
        buttonId = request.POST.get("buttonId")
        if dosya:
            katman.objects.filter(id = buttonId).update(
                proje_ait_bilgisi = kullanici,
                proje_santiye_Ait = get_object_or_none(santiye,id = santiye_al),
                katman_adi  = katman_adi,
                katman_dosyasi = dosya
            )
        else:
            katman.objects.filter(id = buttonId).update(
            proje_ait_bilgisi = kullanici,
            proje_santiye_Ait = get_object_or_none(santiye,id = santiye_al),
            katman_adi  = katman_adi
        )
    return redirect("main:katman_sayfasi")


def get_yapi(request, santiye_id):
    yapilar = bloglar.objects.filter(proje_santiye_Ait__id=santiye_id).values('id', 'blog_adi',"kat_sayisi")
    yapilar_list = list(yapilar)
    return JsonResponse({'yapilar': yapilar_list})
######################################3


def kullanici_yetkileri_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if super_admin_kontrolu(request):
        profile = personel_izinleri.objects.filter(izinlerin_sahibi_kullanici = users)
        content["izinler"] = profile
    else:
        if request.user.kullanicilar_db:
            return redirect("main:yetkisiz")
        profile = personel_izinleri.objects.filter(izinlerin_sahibi_kullanici = request.user)
        content["izinler"] = profile
    return render(request,"kullanici_yetkileri/yetkiler.html",content)
def kullanici_yetkileri_duzenle_2(request,id,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if super_admin_kontrolu(request):
        profile = personel_izinleri.objects.filter(izinlerin_sahibi_kullanici = users)
        content["izinler"] = profile
        content["secili_grup"] = get_object_or_404(personel_izinleri,id = id)
    else:
        if request.user.kullanicilar_db:
            return redirect("main:yetkisiz")
        profile = personel_izinleri.objects.filter(izinlerin_sahibi_kullanici = request.user)
        content["izinler"] = profile
        content["secili_grup"] = get_object_or_404(personel_izinleri,id = id)
    return render(request,"kullanici_yetkileri/yetkiler.html",content)
def kullanici_yetki_olustur_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.kullanicilar_db:
        return redirect("main:yetkisiz")
    if request.POST:
        grup_adi = request.POST.get("grup_adi")
        personel_izinleri.objects.create(
            isim = grup_adi,
            izinlerin_sahibi_kullanici = users
        )
    return redirect("main:kullanici_yetkileri_2",hash)
def kullanici_yetki_adi_duzenle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.kullanicilar_db:
        return redirect("main:yetkisiz")
    if request.POST:
        grup_adi = request.POST.get("grup_adi")
        id  = request.POST.get("id")
        personel_izinleri.objects.filter(id = id).update(
            isim = grup_adi,
            izinlerin_sahibi_kullanici = users
        )
    return redirect("main:kullanici_yetkileri_2",hash)
def kullanici_yetki_sil_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.kullanicilar_db:
        return redirect("main:yetkisiz")
    if request.POST:
        id  = request.POST.get("id")
        personel_izinleri.objects.filter(id = id,izinlerin_sahibi_kullanici = users).delete()
    return redirect("main:kullanici_yetkileri_2",hash)
def kullanici_yetki_alma_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.kullanicilar_db:
        return redirect("main:yetkisiz")
    if request.POST:
        guncellenen = request.POST.get("guncellenen")
        izinler = get_object_or_404(personel_izinleri,id = guncellenen) 
        ##
        #izinleri Sıfırla
        izinler.dashboard_gorme = False
        izinler.dashboard_silme = False
        izinler.dashboard_duzenleme = False
        izinler.dashboard_olusturma = False
        #
        izinler.gelir_ozeti_gorme = False
        izinler.gelir_ozeti_olusturma = False
        izinler.gelir_ozeti_duzenleme =False
        izinler.gelir_ozeti_silme = False
        #
        izinler.gider_ozeti_gorme = False
        izinler.gider_ozeti_olusturma = False
        izinler.gider_ozeti_duzenleme = False
        izinler.gider_ozeti_silme = False
        #
        izinler.hesap_ekstra_gorme = False
        izinler.hesap_ekstra_olusturma = False
        izinler.hesap_ekstra_duzenleme = False
        izinler.hesap_ekstra_silme = False
        #
        izinler.ilerleme_takibi_gorme = False
        izinler.ilerleme_takibi_olusturma = False
        izinler.ilerleme_takibi_duzenleme = False
        izinler.ilerleme_takibi_silme = False
        #
        izinler.sozlesmeler_gorme = False
        izinler.sozlesmeler_olusturma = False
        izinler.sozlesmeler_duzenleme = False
        izinler.sozlesmeler_silme = False
        #
        izinler.yapilacaklar_gorme = False
        izinler.yapilacaklar_olusturma = False
        izinler.yapilacaklar_duzenleme = False
        izinler.yapilacaklar_silme = False
        #
        izinler.dosya_yoneticisi_gorme = False
        izinler.dosya_yoneticisi_olusturma = False
        izinler.dosya_yoneticisi_duzenleme = False
        izinler.dosya_yoneticisi_silme = False
        #
        izinler.projeler_gorme = False
        izinler.projeler_olusturma = False
        izinler.projeler_duzenleme = False
        izinler.projeler_silme =False
        #
        izinler.personeller_gorme = False
        izinler.personeller_olusturma = False
        izinler.personeller_duzenleme = False
        izinler.personeller_silme = False
        #
        izinler.gelir_faturasi_gorme_izni = False
        izinler.gelir_faturasi_kesme_izni = False
        izinler.gelir_faturasi_duzenleme_izni = False
        izinler.gelir_faturasi_silme_izni = False
        #
        izinler.gider_faturasi_gorme_izni = False
        izinler.gider_faturasi_kesme_izni = False
        izinler.gider_faturasi_duzenleme_izni = False
        izinler.gider_faturasi_silme_izni = False
        #
        izinler.kasa_virman_olusturma_izni = False
        izinler.kasa_virman_gorme_izni = False
        #
        izinler.kasa_gosterme_izni = False
        izinler.kasa_olusturma_izni = False
        izinler.kasa_guncelleme_izni = False
        izinler.Kasa_silme_izni = False
        #
        izinler.cari_gosterme_izni = False
        izinler.cari_olusturma = False
        izinler.cari_guncelleme_izni = False
        izinler.cari_silme_izni = False
        #
        izinler.personeller_gorme = False
        izinler.personeller_olusturma = False
        izinler.personeller_duzenleme = False
        izinler.personeller_silme = False
        #
        izinler.santiye_olusturma = False
        izinler.santiye_silme = False
        izinler.santiye_gorme = False
        izinler.santiye_duzenleme = False
        #
        izinler.blog_olusturma = False
        izinler.blog_silme = False
        izinler.blog_gorme = False
        izinler.blog_duzenleme = False
        #
        izinler.kalemleri_olusturma = False
        izinler.kalemleri_silme = False
        izinler.kalemleri_gorme = False
        izinler.kalemleri_duzenleme = False
        #
        izinler.santiye_raporu_olusturma = False
        izinler.santiye_raporu_silme = False
        izinler.santiye_raporu_gorme = False
        izinler.santiye_raporu_duzenleme = False
        #
        izinler.taseronlar_gorme = False
        izinler.taseronlar_olusturma = False
        izinler.taseronlar_duzenleme = False
        izinler.taseronlar_silme =False
        #
        izinler.hakedisler_gorme = False
        izinler.hakedisler_olusturma = False
        izinler.hakedisler_duzenleme = False
        izinler.hakedisler_silme = False
        #
        izinler.kasa_detay_izni = False
        izinler.cari_detay_izni = False
        ##
        izinler.gelir_kategorisi_gorme = False
        izinler.gelir_kategorisi_olusturma = False
        izinler.gelir_kategorisi_guncelleme = False
        izinler.gelir_kategorisi_silme = False
        #
        izinler.gider_kategorisi_gorme = False
        izinler.gider_kategorisi_olusturma = False
        izinler.gider_kategorisi_guncelleme = False
        izinler.gider_kategorisi_silme = False
        #
        izinler.gelir_etiketi_gorme = False
        izinler.gelir_etiketi_olusturma = False
        izinler.gelir_etiketi_guncelleme = False
        izinler.gelir_etiketi_silme = False
        #
        izinler.gider_etiketi_gorme = False
        izinler.gider_etiketi_olusturma = False
        izinler.gider_etiketi_guncelleme = False
        izinler.gider_etiketi_silme = False
        #
        izinler.urun_gorme = False
        izinler.urun_olusturma = False
        izinler.urun_guncelleme = False
        izinler.urun_silme = False
        #
        izinler.muhasabe_ayarlari_gorme = False
        izinler.muhasabe_ayarlari_guncelleme = False
        #
        izinler.gelir_faturasi_makbuz_gorme_izni = False
        izinler.gelir_faturasi_makbuz_kesme_izni = False
        izinler.gelir_faturasi_makbuz_duzenleme_izni = False
        izinler.gelir_faturasi_makbuz_silme_izni = False
        #
        izinler.gider_faturasi_makbuz_gorme_izni = False
        izinler.gider_faturasi_makbuz_kesme_izni = False
        izinler.gider_faturasi_makbuz_duzenleme_izni = False
        izinler.gider_faturasi_makbuz_silme_izni = False
        #Puantaj
        izinler.personeller_puantaj_olusturma = False
        izinler.personeller_puantaj_silme = False
        izinler.personeller_puantaj_gorme = False
        izinler.personeller_puantaj_duzenleme = False
        #
        # 
        izinler.personeller_odeme_olusturma = False
        izinler.personeller_odeme_silme = False
        izinler.personeller_odeme_gorme = False
        izinler.personeller_odeme_duzenleme = False
        #
        izinler.katman_olusturma = False
        izinler.katman_silme = False
        izinler.katman_gorme = False
        izinler.katman_duzenleme = False
        izinler.save()
        ##
        personeller_puantaj_olusturma = request.POST.get("personeller_puantaj_olusturma")
        if personeller_puantaj_olusturma:
            izinler.personeller_puantaj_olusturma = True
        personeller_puantaj_silme = request.POST.get("personeller_puantaj_silme")
        if personeller_puantaj_silme:
            izinler.personeller_puantaj_silme = True
        personeller_puantaj_gorme = request.POST.get("personeller_puantaj_gorme")
        if personeller_puantaj_gorme:
            izinler.personeller_puantaj_gorme = True
        personeller_puantaj_duzenleme = request.POST.get("personeller_puantaj_duzenleme")
        if personeller_puantaj_duzenleme:
            izinler.personeller_puantaj_duzenleme = True
        #
        personeller_odeme_olusturma = request.POST.get("personeller_odeme_olusturma")
        if personeller_odeme_olusturma:
            izinler.personeller_odeme_olusturma = True
        personeller_odeme_silme = request.POST.get("personeller_odeme_silme")
        if personeller_odeme_silme:
            izinler.personeller_odeme_silme = True
        personeller_odeme_gorme = request.POST.get("personeller_odeme_gorme")
        if personeller_odeme_gorme:
            izinler.personeller_odeme_gorme = True
        personeller_odeme_duzenleme = request.POST.get("personeller_odeme_duzenleme")
        if personeller_odeme_duzenleme:
            izinler.personeller_odeme_duzenleme = True
        #
        katman_olusturma = request.POST.get("katman_olusturma")
        if katman_olusturma:
            izinler.katman_olusturma = True
        katman_silme = request.POST.get("katman_silme")
        if katman_silme:
            izinler.katman_silme = True
        katman_gorme = request.POST.get("katman_gorme")
        if katman_gorme:
            izinler.katman_gorme = True
        katman_duzenleme = request.POST.get("katman_duzenleme")
        if katman_duzenleme:
            izinler.katman_duzenleme = True
        ##
        dashboard_gorme = request.POST.get("dashboard_gorme")
        if dashboard_gorme:
            izinler.dashboard_gorme = True
        dashboard_silme = request.POST.get("dashboard_silme")
        if dashboard_silme:
            izinler.dashboard_silme = True
        dashboard_duzenleme = request.POST.get("dashboard_duzenleme")
        if dashboard_duzenleme:
            izinler.dashboard_duzenleme = True
        dashboard_olusturma = request.POST.get("dashboard_olusturma")
        if dashboard_olusturma:
            izinler.dashboard_olusturma = True
        #
        gelir_ozeti_gorme = request.POST.get("gelir_ozeti_gorme")
        if gelir_ozeti_gorme:
            izinler.gelir_ozeti_gorme = True
        gelir_ozeti_olusturma = request.POST.get("gelir_ozeti_olusturma")
        if gelir_ozeti_olusturma:
            izinler.gelir_ozeti_olusturma = True
        gelir_ozeti_duzenleme = request.POST.get("gelir_ozeti_duzenleme")
        if gelir_ozeti_duzenleme:
            izinler.gelir_ozeti_duzenleme = True
        gelir_ozeti_silme = request.POST.get("gelir_ozeti_silme")
        if gelir_ozeti_silme:
            izinler.gelir_ozeti_silme = True
        #
        gider_ozeti_gorme = request.POST.get("gider_ozeti_gorme")
        if gider_ozeti_gorme:
            izinler.gider_ozeti_gorme = True
        gider_ozeti_olusturma = request.POST.get("gider_ozeti_olusturma")
        if gider_ozeti_olusturma:
            izinler.gider_ozeti_olusturma = True
        gider_ozeti_duzenleme = request.POST.get("gider_ozeti_duzenleme")
        if gider_ozeti_duzenleme:
            izinler.gider_ozeti_duzenleme = True
        gider_ozeti_silme = request.POST.get("gider_ozeti_silme")
        if gider_ozeti_silme:
            izinler.gider_ozeti_silme = True
        #
        hesap_ekstra_gorme = request.POST.get("hesap_ekstra_gorme")
        if hesap_ekstra_gorme:
            izinler.hesap_ekstra_gorme = True
        hesap_ekstra_olusturma = request.POST.get("hesap_ekstra_olusturma")
        if hesap_ekstra_olusturma:
            izinler.hesap_ekstra_olusturma = True
        hesap_ekstra_duzenleme = request.POST.get("hesap_ekstra_duzenleme")
        if hesap_ekstra_duzenleme:
            izinler.hesap_ekstra_duzenleme = True
        hesap_ekstra_silme = request.POST.get("hesap_ekstra_silme")
        if hesap_ekstra_silme:
            izinler.hesap_ekstra_silme = True
        #
        kasa_virman_olusturma_izni = request.POST.get("kasa_virman_olusturma_izni")
        if kasa_virman_olusturma_izni:
            izinler.kasa_virman_olusturma_izni = True
        kasa_virman_gorme_izni = request.POST.get("kasa_virman_gorme_izni")
        if kasa_virman_gorme_izni:
            izinler.kasa_virman_gorme_izni = True
        #
        ilerleme_takibi_gorme = request.POST.get("ilerleme_takibi_gorme")
        if ilerleme_takibi_gorme:
            izinler.ilerleme_takibi_gorme = True
        ilerleme_takibi_olusturma = request.POST.get("ilerleme_takibi_olusturma")
        if ilerleme_takibi_olusturma:
            izinler.ilerleme_takibi_olusturma = True
        ilerleme_takibi_duzenleme = request.POST.get("ilerleme_takibi_duzenleme")
        if ilerleme_takibi_duzenleme:
            izinler.ilerleme_takibi_duzenleme = True
        ilerleme_takibi_silme = request.POST.get("ilerleme_takibi_silme")
        if ilerleme_takibi_silme:
            izinler.ilerleme_takibi_silme = True
        #
        sozlesmeler_gorme = request.POST.get("sozlesmeler_gorme")
        if sozlesmeler_gorme:
            izinler.sozlesmeler_gorme = True
        sozlesmeler_olusturma = request.POST.get("sozlesmeler_olusturma")
        if sozlesmeler_olusturma:
            izinler.sozlesmeler_olusturma = True
        sozlesmeler_duzenleme = request.POST.get("sozlesmeler_duzenleme")
        if sozlesmeler_duzenleme:
            izinler.sozlesmeler_duzenleme = True
        sozlesmeler_silme = request.POST.get("sozlesmeler_silme")
        if sozlesmeler_silme:
            izinler.sozlesmeler_silme = True
        #
        yapilacaklar_gorme = request.POST.get("yapilacaklar_gorme")
        if yapilacaklar_gorme:
            izinler.yapilacaklar_gorme = True
        yapilacaklar_olusturma = request.POST.get("yapilacaklar_olusturma")
        if yapilacaklar_olusturma:
            izinler.yapilacaklar_olusturma = True
        yapilacaklar_duzenleme = request.POST.get("yapilacaklar_duzenleme")
        if yapilacaklar_duzenleme:
            izinler.yapilacaklar_duzenleme = True
        yapilacaklar_silme = request.POST.get("yapilacaklar_silme")
        if yapilacaklar_silme:
            izinler.yapilacaklar_silme = True
        #
        dosya_yoneticisi_gorme = request.POST.get("dosya_yoneticisi_gorme")
        if dosya_yoneticisi_gorme:
            izinler.dosya_yoneticisi_gorme = True
        dosya_yoneticisi_olusturma = request.POST.get("dosya_yoneticisi_olusturma")
        if dosya_yoneticisi_olusturma:
            izinler.dosya_yoneticisi_olusturma = True
        dosya_yoneticisi_duzenleme = request.POST.get("dosya_yoneticisi_duzenleme")
        if dosya_yoneticisi_duzenleme:
            izinler.dosya_yoneticisi_duzenleme = True
        dosya_yoneticisi_silme = request.POST.get("dosya_yoneticisi_silme")
        if dosya_yoneticisi_silme:
            izinler.dosya_yoneticisi_silme = True
        #
        projeler_gorme = request.POST.get("projeler_gorme")
        if projeler_gorme:
            izinler.projeler_gorme = True
        projeler_olusturma = request.POST.get("projeler_olusturma")
        if projeler_olusturma:
            izinler.projeler_olusturma = True
        projeler_duzenleme = request.POST.get("projeler_duzenleme")
        if projeler_duzenleme:
            izinler.projeler_duzenleme = True
        projeler_silme = request.POST.get("projeler_silme")
        if projeler_silme:
            izinler.projeler_silme = True

        #
        personeller_gorme = request.POST.get("personeller_gorme")
        if personeller_gorme:
            izinler.personeller_gorme = True
        personeller_olusturma = request.POST.get("personeller_olusturma")
        if personeller_olusturma:
            izinler.personeller_olusturma = True
        personeller_duzenleme = request.POST.get("personeller_duzenleme")
        if personeller_duzenleme:
            izinler.personeller_duzenleme = True
        personeller_silme = request.POST.get("personeller_silme")
        if personeller_silme:
            izinler.personeller_silme = True
        #
        gelir_faturasi_gorme_izni = request.POST.get("gelir_faturasi_gorme_izni")
        if gelir_faturasi_gorme_izni:
            izinler.gelir_faturasi_gorme_izni = True
        gelir_faturasi_kesme_izni = request.POST.get("gelir_faturasi_kesme_izni")
        if gelir_faturasi_kesme_izni:
            izinler.gelir_faturasi_kesme_izni = True
        gelir_faturasi_duzenleme_izni = request.POST.get("gelir_faturasi_duzenleme_izni")
        if gelir_faturasi_duzenleme_izni:
            izinler.gelir_faturasi_duzenleme_izni = True
        gelir_faturasi_silme_izni = request.POST.get("gelir_faturasi_silme_izni")
        if gelir_faturasi_silme_izni:
            izinler.gelir_faturasi_silme_izni = True
        #
        gider_faturasi_gorme_izni = request.POST.get("gider_faturasi_gorme_izni")
        if gider_faturasi_gorme_izni:
            izinler.gider_faturasi_gorme_izni = True
        gider_faturasi_kesme_izni = request.POST.get("gider_faturasi_kesme_izni")
        if gider_faturasi_kesme_izni:
            izinler.gider_faturasi_kesme_izni = True
        gider_faturasi_duzenleme_izni = request.POST.get("gider_faturasi_duzenleme_izni")
        if gider_faturasi_duzenleme_izni:
            izinler.gider_faturasi_duzenleme_izni = True
        gider_faturasi_silme_izni = request.POST.get("gider_faturasi_silme_izni")
        if gider_faturasi_silme_izni:
            izinler.gider_faturasi_silme_izni = True
        #
        
        kasa_gosterme_izni = request.POST.get("kasa_gosterme_izni")
        if kasa_gosterme_izni:
            izinler.kasa_gosterme_izni = True
        kasa_olusturma_izni = request.POST.get("kasa_olusturma_izni")
        if kasa_olusturma_izni:
            izinler.kasa_olusturma_izni = True
        kasa_guncelleme_izni = request.POST.get("kasa_guncelleme_izni")
        if kasa_guncelleme_izni:
            izinler.kasa_guncelleme_izni = True
        Kasa_silme_izni = request.POST.get("Kasa_silme_izni")
        if Kasa_silme_izni:
            izinler.Kasa_silme_izni = True
        #
        cari_gosterme_izni = request.POST.get("cari_gosterme_izni")
        if cari_gosterme_izni:
            izinler.cari_gosterme_izni = True
        cari_olusturma = request.POST.get("cari_olusturma")
        if cari_olusturma:
            izinler.cari_olusturma = True
        cari_guncelleme_izni = request.POST.get("cari_guncelleme_izni")
        if cari_guncelleme_izni:
            izinler.cari_guncelleme_izni = True
        cari_silme_izni = request.POST.get("cari_silme_izni")
        if cari_silme_izni:
            izinler.cari_silme_izni = True
        #
        personeller_gorme = request.POST.get("personeller_gorme")
        if personeller_gorme:
            izinler.personeller_gorme = True
        personeller_olusturma = request.POST.get("personeller_olusturma")
        if personeller_olusturma:
            izinler.personeller_olusturma = True
        personeller_duzenleme = request.POST.get("personeller_duzenleme")
        if personeller_duzenleme:
            izinler.personeller_duzenleme = True
        personeller_silme = request.POST.get("personeller_silme")
        if personeller_silme:
            izinler.personeller_silme = True
        #
        santiye_gorme = request.POST.get("santiye_gorme")
        if santiye_gorme:
            izinler.santiye_gorme = True
        santiye_olusturma  = request.POST.get("santiye_olusturma")
        if santiye_olusturma:
            izinler.santiye_olusturma = True
        santiye_duzenleme = request.POST.get("santiye_duzenleme")
        if santiye_duzenleme:
            izinler.santiye_duzenleme = True
        santiye_silme = request.POST.get("santiye_silme")
        if santiye_silme:
            izinler.santiye_silme = True
        #
        blog_gorme = request.POST.get("blog_gorme")
        if blog_gorme:
            izinler.blog_gorme = True
        blog_olusturma  = request.POST.get("blog_olusturma")
        if blog_olusturma:
            izinler.blog_olusturma = True
        blog_duzenleme = request.POST.get("blog_duzenleme")
        if blog_duzenleme:
            izinler.blog_duzenleme = True
        blog_silme = request.POST.get("blog_silme")
        if blog_silme:
            izinler.blog_silme = True
        #
        kalemleri_gorme = request.POST.get("kalemleri_gorme")
        if kalemleri_gorme:
            izinler.kalemleri_gorme = True
        kalemleri_olusturma  = request.POST.get("kalemleri_olusturma")
        if kalemleri_olusturma:
            izinler.kalemleri_olusturma = True
        kalemleri_duzenleme = request.POST.get("kalemleri_duzenleme")
        if kalemleri_duzenleme:
            izinler.kalemleri_duzenleme = True
        kalemleri_silme = request.POST.get("kalemleri_silme")
        if kalemleri_silme:
            izinler.kalemleri_silme = True
        #
        santiye_raporu_gorme = request.POST.get("santiye_raporu_gorme")
        if santiye_raporu_gorme:
            izinler.santiye_raporu_gorme = True
        santiye_raporu_olusturma  = request.POST.get("santiye_raporu_olusturma")
        if santiye_raporu_olusturma:
            izinler.santiye_raporu_olusturma = True
        santiye_raporu_duzenleme = request.POST.get("santiye_raporu_duzenleme")
        if santiye_raporu_duzenleme:
            izinler.santiye_raporu_duzenleme = True
        santiye_raporu_silme = request.POST.get("santiye_raporu_silme")
        if santiye_raporu_silme:
            izinler.santiye_raporu_silme = True
        #
        taseronlar_gorme = request.POST.get("taseronlar_gorme")
        if taseronlar_gorme:
            izinler.taseronlar_gorme = True
        taseronlar_olusturma = request.POST.get("taseronlar_olusturma")
        if taseronlar_olusturma:
            izinler.taseronlar_olusturma = True
        taseronlar_duzenleme = request.POST.get("taseronlar_duzenleme")
        if taseronlar_duzenleme:
            izinler.taseronlar_duzenleme = True
        taseronlar_silme = request.POST.get("taseronlar_silme")
        if taseronlar_silme:
            izinler.taseronlar_silme = True
        #
        hakedisler_gorme = request.POST.get("hakedisler_gorme")
        if hakedisler_gorme:
            izinler.hakedisler_gorme = True
        hakedisler_olusturma = request.POST.get("hakedisler_olusturma")
        if hakedisler_olusturma:
            izinler.hakedisler_olusturma = True
        hakedisler_duzenleme = request.POST.get("hakedisler_duzenleme")
        if hakedisler_duzenleme:
            izinler.hakedisler_duzenleme = True
        hakedisler_silme = request.POST.get("hakedisler_silme")
        if hakedisler_silme:
            izinler.hakedisler_silme = True
        #
        kasa_detay_izni = request.POST.get("kasa_detay_izni")
        if kasa_detay_izni:
            izinler.kasa_detay_izni = True
        cari_detay_izni = request.POST.get("cari_detay_izni")
        if cari_detay_izni:
            izinler.cari_detay_izni = True
        
        #
        gelir_kategorisi_gorme = request.POST.get("gelir_kategorisi_gorme")
        if gelir_kategorisi_gorme:  
            izinler.gelir_kategorisi_gorme = True
        gelir_kategorisi_olusturma = request.POST.get("gelir_kategorisi_olusturma")
        if gelir_kategorisi_olusturma : 
            izinler.gelir_kategorisi_olusturma = True
        gelir_kategorisi_guncelleme = request.POST.get("gelir_kategorisi_guncelleme")
        if gelir_kategorisi_guncelleme : 
            izinler.gelir_kategorisi_guncelleme = True
        gelir_kategorisi_silme = request.POST.get("gelir_kategorisi_silme")
        if gelir_kategorisi_silme : 
            izinler.gelir_kategorisi_silme = True
        
        #
        gider_kategorisi_gorme = request.POST.get("gider_kategorisi_gorme")
        if gider_kategorisi_gorme:  
            izinler.gider_kategorisi_gorme = True
        gider_kategorisi_olusturma = request.POST.get("gider_kategorisi_olusturma")
        if gider_kategorisi_olusturma : 
            izinler.gider_kategorisi_olusturma = True
        gider_kategorisi_guncelleme = request.POST.get("gider_kategorisi_guncelleme")
        if gider_kategorisi_guncelleme : 
            izinler.gider_kategorisi_guncelleme = True
        gider_kategorisi_silme = request.POST.get("gider_kategorisi_silme")
        if gider_kategorisi_silme : 
            izinler.gider_kategorisi_silme = True
        #
        #
        gelir_etiketi_gorme = request.POST.get("gelir_etiketi_gorme")
        if gelir_etiketi_gorme:  
            izinler.gelir_etiketi_gorme = True
        gelir_etiketi_olusturma = request.POST.get("gelir_etiketi_olusturma")
        if gelir_etiketi_olusturma : 
            izinler.gelir_etiketi_olusturma = True
        gelir_etiketi_guncelleme = request.POST.get("gelir_etiketi_guncelleme")
        if gelir_etiketi_guncelleme : 
            izinler.gelir_etiketi_guncelleme = True
        gelir_etiketi_silme = request.POST.get("gelir_etiketi_silme")
        if gelir_etiketi_silme : 
            izinler.gelir_etiketi_silme = True

        #
        gider_etiketi_gorme = request.POST.get("gider_etiketi_gorme")
        if gider_etiketi_gorme:  
            izinler.gider_etiketi_gorme = True
        gider_etiketi_olusturma = request.POST.get("gider_etiketi_olusturma")
        if gider_etiketi_olusturma : 
            izinler.gider_etiketi_olusturma = True
        gider_etiketi_guncelleme = request.POST.get("gider_etiketi_guncelleme")
        if gider_etiketi_guncelleme : 
            izinler.gider_etiketi_guncelleme = True
        gider_etiketi_silme = request.POST.get("gider_etiketi_silme")
        if gider_etiketi_silme : 
            izinler.gider_etiketi_silme = True
        #
        #
        urun_gorme = request.POST.get("urun_gorme")
        if urun_gorme:  
            izinler.urun_gorme = True
        urun_olusturma = request.POST.get("urun_olusturma")
        if urun_olusturma : 
            izinler.urun_olusturma = True
        urun_guncelleme = request.POST.get("urun_guncelleme")
        if urun_guncelleme : 
            izinler.urun_guncelleme = True
        urun_silme = request.POST.get("urun_silme")
        if urun_silme : 
            izinler.urun_silme = True

        #
        muhasabe_ayarlari_gorme = request.POST.get("muhasabe_ayarlari_gorme")
        if muhasabe_ayarlari_gorme : 
            izinler.muhasabe_ayarlari_gorme = True
        muhasabe_ayarlari_guncelleme = request.POST.get("muhasabe_ayarlari_guncelleme")
        if muhasabe_ayarlari_guncelleme : 
            izinler.muhasabe_ayarlari_guncelleme = True

        #
        gelir_faturasi_makbuz_gorme_izni = request.POST.get("gelir_faturasi_makbuz_gorme_izni")
        if gelir_faturasi_makbuz_gorme_izni:  
            izinler.gelir_faturasi_makbuz_gorme_izni = True
        gelir_faturasi_makbuz_kesme_izni = request.POST.get("gelir_faturasi_makbuz_kesme_izni")
        if gelir_faturasi_makbuz_kesme_izni : 
            izinler.gelir_faturasi_makbuz_kesme_izni = True
        gelir_faturasi_makbuz_duzenleme_izni = request.POST.get("gelir_faturasi_makbuz_duzenleme_izni")
        if gelir_faturasi_makbuz_duzenleme_izni : 
            izinler.gelir_faturasi_makbuz_duzenleme_izni = True
        gelir_faturasi_makbuz_silme_izni = request.POST.get("gelir_faturasi_makbuz_silme_izni")
        if gelir_faturasi_makbuz_silme_izni : 
            izinler.gelir_faturasi_makbuz_silme_izni = True
        #
        gider_faturasi_makbuz_gorme_izni = request.POST.get("gider_faturasi_makbuz_gorme_izni")
        if gider_faturasi_makbuz_gorme_izni:  
            izinler.gider_faturasi_makbuz_gorme_izni = True
        gider_faturasi_makbuz_kesme_izni = request.POST.get("gider_faturasi_makbuz_kesme_izni")
        if gider_faturasi_makbuz_kesme_izni : 
            izinler.gider_faturasi_makbuz_kesme_izni = True
        gider_faturasi_makbuz_duzenleme_izni = request.POST.get("gider_faturasi_makbuz_duzenleme_izni")
        if gider_faturasi_makbuz_duzenleme_izni : 
            izinler.gider_faturasi_makbuz_duzenleme_izni = True
        gider_faturasi_makbuz_silme_izni = request.POST.get("gider_faturasi_makbuz_silme_izni")
        if gider_faturasi_makbuz_silme_izni : 
            izinler.gider_faturasi_makbuz_silme_izni = True
        izinler.save()
    return redirect("main:kullanici_yetkileri_2",hash)

def proje_ekleme_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        #yetkili_adi
        if super_admin_kontrolu(request):
            kullanici_bilgisi  = request.POST.get("kullanici")
            proje_tip_adi   = request.POST.get("yetkili_adi")
            proje_tipi.objects.create(proje_ait_bilgisi = users ,Proje_tipi_adi = proje_tip_adi)
        
    return redirect("main:proje_tipi_2",hash)
#Proje Adı Silme
def proje_Adi_sil_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        proje_tipi.objects.filter(id = id).update(silinme_bilgisi = True)
    
    return redirect("main:proje_tipi_2",hash)
#Proje Düzenlme
import folium
def proje_duzenle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        silinmedurumu = request.POST.get("silinmedurumu")
        
        proje_tipi.objects.filter(id = id).update(proje_ait_bilgisi = users ,Proje_tipi_adi = proje_tip_adi )

    
    return redirect("main:proje_tipi_2",hash)
#Şantiye Projesi Ekleme
############################


def santiyeye_kalem_ekle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            if True:
                projetipi = request.POST.getlist("projetipi")
                yetkili_adi = request.POST.get("yetkili_adi")
                santiye_agirligi = request.POST.get("katsayisi")
                finansal_agirlik = request.POST.get("blogsayisi")
                metraj = request.POST.get("metraj")
                tutar = request.POST.get("tutar")
                birim_bilgisi = request.POST.get("birim_bilgisi")
                kata_veya_binaya_daihil = request.POST.get("kata_veya_binaya_daihil")
                id = bloglar.objects.filter(id__in = projetipi).first()
                kalem = santiye_kalemleri.objects.create(
                    proje_ait_bilgisi = users,
                    proje_santiye_Ait =id.proje_santiye_Ait,
                    kalem_adi = yetkili_adi,santiye_agirligi = santiye_agirligi,
                    santiye_finansal_agirligi = finansal_agirlik,
                    birimi = get_object_or_404(birimler,id =birim_bilgisi ),metraj = metraj,
                    tutari = tutar
                )
                if kata_veya_binaya_daihil == "0":
                    blog_lar = bloglar.objects.filter(id__in = projetipi)
                    for i in blog_lar:
                        for j in range(0,int(i.kat_sayisi)):
                            santiye_kalemlerin_dagilisi.objects.create(
                                proje_ait_bilgisi = users,
                                proje_santiye_Ait = id.proje_santiye_Ait,
                                kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =kalem.id ),
                                kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                            )
                elif kata_veya_binaya_daihil == "1":
                    blog_lar = bloglar.objects.filter(id__in = projetipi)
                    for i in blog_lar:
                        for j in range(0,int(i.kat_sayisi)):
                            santiye_kalemlerin_dagilisi.objects.create(
                                proje_ait_bilgisi = users,
                                proje_santiye_Ait = id.proje_santiye_Ait,
                                kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =kalem.id ),
                                kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                            )
                            break
                elif kata_veya_binaya_daihil == "2":
                    blog_lar = bloglar.objects.filter(id__in = projetipi)
                    for i in blog_lar:
                        for j in range(0,4):
                            santiye_kalemlerin_dagilisi.objects.create(
                                proje_ait_bilgisi = users,
                                proje_santiye_Ait = id.proje_santiye_Ait,
                                kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =kalem.id ),
                                kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                            )
                        
    return redirect("main:santiye_projesi_ekle_2",hash)

def blog_ekle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
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
    return redirect("main:santiye_projesi_ekle_2",hash)
def santiye_kalemleri_duzenle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        buttonId = request.POST.get("buttonId")
        santiye_kalemlerin_dagilisi.objects.filter(kalem_bilgisi__id =buttonId).delete()
        yetkili_adi = request.POST.get("yetkili_adi")
        santiye_agirligi = request.POST.get("katsayisi")
        finansal_agirlik = request.POST.get("blogsayisi")
        geri_don = request.POST.get("geri_don")
        metraj = request.POST.get("metraj")
        tutar = request.POST.get("tutar")
        birim_bilgisi = request.POST.get("birim_bilgisi")
        kata_veya_binaya_daihil = request.POST.get("kata_veya_binaya_daihil")
        projetipi = request.POST.getlist("projetipi")
        if request.user.is_superuser:
            
            santiye_kalemleri.objects.filter(id  = buttonId).update(
                            proje_ait_bilgisi = users,
                            kalem_adi = yetkili_adi,santiye_agirligi = santiye_agirligi,
                            santiye_finansal_agirligi = finansal_agirlik,birimi = get_object_or_404(birimler,id =birim_bilgisi ),metraj = metraj,
                        tutari = tutar
                        )
            if True:
                if kata_veya_binaya_daihil == "0":
                    blog_lar = bloglar.objects.filter(id__in = projetipi)
                    for i in blog_lar:
                        for j in range(0,int(i.kat_sayisi)):
                            santiye_kalemlerin_dagilisi.objects.create(
                                proje_ait_bilgisi = users,
                                proje_santiye_Ait_id = geri_don,
                                kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =buttonId ),
                                kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                            )
                elif kata_veya_binaya_daihil == "1":
                    blog_lar = bloglar.objects.filter(id__in = projetipi)
                    for i in blog_lar:
                        for j in range(0,int(i.kat_sayisi)):
                            santiye_kalemlerin_dagilisi.objects.create(
                                proje_ait_bilgisi = users,
                                proje_santiye_Ait_id = geri_don,
                                kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =buttonId),
                                kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                            )
                            break
                elif kata_veya_binaya_daihil == "2":
                    blog_lar = bloglar.objects.filter(id__in = projetipi)
                    for i in blog_lar:
                        for j in range(0,4):
                            santiye_kalemlerin_dagilisi.objects.create(
                                proje_ait_bilgisi = users,
                                proje_santiye_Ait_id = geri_don,
                                kalem_bilgisi = get_object_or_404(santiye_kalemleri,id =buttonId ),
                                kat = j,blog_bilgisi = get_object_or_404(bloglar,id =i.id ),
                            )
    return redirect("main:santiye_projesi_ekle_2",hash)
def kalem_sil_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.kalemleri_silme:
                    buttonId = request.POST.get("buttonId")
                    geri_don = request.POST.get("geri_don")
                    santiye_kalemleri.objects.filter(id = buttonId).update(
                        silinme_bilgisi = True
                    )
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            buttonId = request.POST.get("buttonId")
            geri_don = request.POST.get("geri_don")
            santiye_kalemleri.objects.filter(id = buttonId).update(
                silinme_bilgisi = True
            )
    return redirect("main:santiye_projesi_ekle_2",hash)

def blog_duzenle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.blog_duzenleme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
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
       
    return redirect("main:santiye_projesi_ekle_2",hash)
def blog_sil_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.blog_silme:
                pass
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    if request.POST:
        buttonId = request.POST.get("buttonId")
        geri = request.POST.get("geri")
        blog_bilgisi = get_object_or_404(bloglar,id = buttonId)
        bloglar.objects.filter(id = buttonId).delete()
    return redirect("main:santiye_projesi_ekle_2",hash)

"""
content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
"""
def katman_sayfasi_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if super_admin_kontrolu(request):
        profile =katman.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = katman.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = users)
        content["insaatlar"] = santiye.objects.filter(proje_ait_bilgisi =  users,silinme_bilgisi = False)
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = profile
    return render(request,"santiye_yonetimi/katman.html",content)

def katman_ekle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            kullanici = users
            
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a.izinler.katman_olusturma:
                    kullanici = request.user.kullanicilar_db
                else:
                    return redirect("main:yetkisiz")
            else:
                kullanici = request.user
        katman_adi = request.POST.get("taseron_adi")
        santiye_al = request.POST.get("blogbilgisi")
        dosya = request.FILES.get("file")
        katman.objects.create(
            proje_ait_bilgisi = kullanici,
            proje_santiye_Ait = get_object_or_none(santiye,id = santiye_al),
            katman_adi  = katman_adi,
            katman_dosyasi = dosya
        )
    return redirect("main:katman_sayfasi_2",hash)

def katman_sil_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            buttonIdInput = request.POST.get("buttonId")
            katman.objects.filter(id = buttonIdInput).update(
                    silinme_bilgisi = True
                )
            return redirect("main:katman_sayfasi_2",hash)

    

def katman_duzenle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            
            kullanici = users
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a.izinler.katman_olusturma:
                    kullanici = request.user.kullanicilar_db
                else:
                    return redirect("main:yetkisiz")
            else:
                kullanici = request.user
        katman_adi = request.POST.get("taseron_adi")
        santiye_al = request.POST.get("blogbilgisi")
        dosya = request.FILES.get("file")
        buttonId = request.POST.get("buttonId")
        if dosya:
            katman.objects.filter(id = buttonId).update(
                proje_ait_bilgisi = kullanici,
                proje_santiye_Ait = get_object_or_none(santiye,id = santiye_al),
                katman_adi  = katman_adi,
                katman_dosyasi = dosya
            )
        else:
            katman.objects.filter(id = buttonId).update(
            proje_ait_bilgisi = kullanici,
            proje_santiye_Ait = get_object_or_none(santiye,id = santiye_al),
            katman_adi  = katman_adi
        )
    return redirect("main:katman_sayfasi_2",hash)

