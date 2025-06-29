from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render,get_object_or_404
from .models import *
from .decorators import user_not_authenticated ,lock_screen_required
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from site_info.models import *
from main.views import super_admin_kontrolu,dil_bilgisi,translate,sozluk_yapisi,yetki,get_kayit_tarihi_from_request,get_time_zone_from_country,get_country
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from django.db.models.query_utils import Q
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.core.files.storage import FileSystemStorage
from main.views import decode_id
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.utils.translation  import gettext as _
from django.utils.translation import get_language, activate, gettext
def redirect_with_language(view_name, *args, **kwargs):
    lang = get_language()
    url = reverse(view_name, args=args, kwargs=kwargs)
    return redirect(f'/{lang}{url}')
from collections import defaultdict
from django.http import JsonResponse

def personel_bilgisi_axaj(request, id):
    bilgi = faturalar_icin_bilgiler.objects.filter(
        gelir_kime_ait_oldugu=get_object_or_none(calisanlar, id=id).calisan_kime_ait
    ).last()

    calisan = get_object_or_none(calisanlar, id=id)
    maasli = calisan_maas_durumlari.objects.filter(calisan=calisan).last()
    cali_belgeleri = calisan_belgeleri.objects.filter(calisan=calisan)

    # Calismalar: hepsi tarihiyle çekiliyor
    calismalar_qs = calisanlar_calismalari.objects.filter(calisan=calisan).values(
        'tarihi', 'maas__id'
    ).annotate(
        total_normal_calisma_saati=Sum('normal_calisma_saati'),
        total_mesai_calisma_saati=Sum('mesai_calisma_saati')
    )

    # Ödemeler
    odemeler_qs = calisanlar_calismalari_odemeleri.objects.filter(calisan=calisan).values(
        'tarihi'
    ).annotate(
        total_tutar=Sum('tutar')
    )

    # Calismalari (yil, ay) bazinda grupla
    calismalar_dict = defaultdict(lambda: {'total_normal': 0, 'total_mesai': 0, 'maas_id': None})
    for c in calismalar_qs:
        tarih = c['tarihi']
        if not tarih:
            continue
        year = tarih.year
        month = tarih.month
        key = (year, month)
        calismalar_dict[key]['total_normal'] += c['total_normal_calisma_saati']
        calismalar_dict[key]['total_mesai'] += c['total_mesai_calisma_saati']
        calismalar_dict[key]['maas_id'] = c['maas__id']

    # Odemeleri (yil, ay) bazinda grupla
    odemeler_dict = defaultdict(float)
    for o in odemeler_qs:
        tarih = o['tarihi']
        if not tarih:
            continue
        key = (tarih.year, tarih.month)
        odemeler_dict[key] += o['total_tutar']

    # Calismalari final listeye çevir
    calismalar_list = []
    for (year, month), vals in sorted(calismalar_dict.items()):
        maas_obj = get_object_or_none(calisan_maas_durumlari, id=vals['maas_id'])
        if not maas_obj or not bilgi or not bilgi.gunluk_calisma_saati:
            continue

        hakedis_tutari = (vals['total_normal'] * maas_obj.maas) / bilgi.gunluk_calisma_saati + \
                         (vals['total_mesai'] * maas_obj.yevmiye)
        odenen = odemeler_dict.get((year, month), 0)
        kalan = hakedis_tutari - odenen

        calismalar_list.append({
            'tarih': f"{year}-{month}",
            'hakedis_tutari': hakedis_tutari,
            'odenen': odenen,
            'kalan': kalan,
            'bodro': "",
        })

    personel_detayi = {
        'id': str(id),
        'calisan_kategori': calisan.calisan_kategori.kategori_isimi,
        'calisan_pozisyonu': calisan.calisan_pozisyonu.kategori_isimi,
        'calisan_kategori_id': str(calisan.calisan_kategori.id),
        'calisan_pozisyonu_id': str(calisan.calisan_pozisyonu.id),
        'uyrugu': calisan.uyrugu,
        'pasaport_numarasi': calisan.pasaport_numarasi,
        'isim': calisan.isim,
        'soyisim': calisan.soyisim,
        'profile': calisan.profile.url if calisan.profile else "https://www.pngitem.com/pimgs/m/81-819673_construction-workers-safety-icons-health-and-safety-policy.png",
        'dogum_tarihi': str(calisan.dogum_tarihi),
        'telefon_numarasi': str(calisan.telefon_numarasi),
        'status': str(calisan.status),
        'maas': str(maasli.maas),
        'yevmiye': str(maasli.yevmiye),
        'faza_mesai_orani': str(maasli.fazla_mesai_orani),
        'durum': "1" if maasli.durum else "0",
        'para_birimi': "1" if maasli.para_birimi else "0",
        "gunluk_saatlik_ucret": str(maasli.maas / bilgi.gunluk_calisma_saati),
        'belgeler': [
            {
                'id': belge.id,
                'belge_turu': belge.belge_turu,
                'resim': belge.belge.url if belge.belge else "https://www.pngitem.com/pimgs/m/81-819673_construction-workers-safety-icons-health-and-safety-policy.png",
            } for belge in cali_belgeleri
        ],
        'calismalar': calismalar_list
    }
    print(personel_detayi)
    return JsonResponse(personel_detayi)


def calismalari_cek_2(request,id):
    personel = id
    baslangic = request.GET.get("baslangic")
    bitis = request.GET.get("bitis")
    tarih_baslangic = datetime.strptime(baslangic, "%d.%m.%Y")
    tarih_bitis = datetime.strptime(bitis, "%d.%m.%Y")
    calismalar = calisanlar_calismalari.objects.filter(
        calisan=get_object_or_404(calisanlar, id=personel),
        tarihi__range=[tarih_baslangic, tarih_bitis]
    )
    izin_gunleri = 0
    for i in calismalar:
        if i.normal_calisma_saati <=0:
            izin_gunleri = +1
    if calismalar.exists():
        normal_saat_toplam = sum(c.normal_calisma_saati for c in calismalar)
        mesai_saat_toplam = sum(c.mesai_calisma_saati for c in calismalar)
        return JsonResponse({ 'normal_saat': normal_saat_toplam, 'mesai_saati': mesai_saat_toplam ,"izin_gunleri":izin_gunleri})
    else:
        return JsonResponse({ 'normal_saat': 0, 'mesai_saati': 0,"izin_gunleri" :izin_gunleri })
def get_object_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except :
        return None
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
# Create your views here.
@user_not_authenticated
def register(request):

    form = RegisterForm(request.POST or None)
    context = {

        "form":form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email_address = form.cleaned_data.get("email_address")
        newUser = CustomUser(username =username,email = email_address)
        newUser.set_password(password)

        newUser.save()
        login(request,newUser)
        messages.info(request,"Başarıyla Kayıt Oldunuz...")

        return redirect_with_language("main:ana_sayfa")

    return render(request,"account/register.html",context)


@user_not_authenticated
def loginUser(request):
    form = LoginForm(request.POST or None)

    context = sozluk_yapisi()
    context ["form"] = form

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username,password = password)
        
        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola Hatalı")
            return render(request,"account/login.html",context)
        messages.success(request,"Başarıyla Giriş Yaptınız")
        login(request,user)
        logout_other_sessions(user, request.session.session_key)
        try:
            lock_status = LockScreenStatus.objects.get(user=request.user)
            lock_status.is_locked=False
            lock_status.save()
        except :
            # Kullanıcının LockScreenStatus objesi henüz oluşturulmamışsa, oluşturun.
            lock_status = LockScreenStatus.objects.create(user=request.user, is_locked=False)
        dil = request.user.kullanici_tercih_dili
        return redirect(f"/{dil}/")
    return render(request,"account/login.html",context)
@login_required
def logoutUser(request):

    try:
        lock_status = LockScreenStatus.objects.get(user=request.user)
        lock_status.is_locked=False
        lock_status.save()
    except LockScreenStatus.DoesNotExist:
        # Kullanıcının LockScreenStatus objesi henüz oluşturulmamışsa, oluşturun.
        lock_status = LockScreenStatus.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),user=request.user, is_locked=False)
    logout(request)
    request.session.flush()
    messages.success(request,"Başarıyla Çıkış Yaptınız")
    return redirect_with_language("users:yonlendir")
def yonlendir(request):
    return render(request,"account/logout.html")
def profil_bilgisi (request):
    content = sozluk_yapisi()
    get_client_ip(request)
    return render(request,"account/profile.html",content)

#kullanıcılar
def kullanicilarim(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        profile = taseron_sozlesme_dosyalari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = CustomUser.objects.filter(kullanicilar_db = request.user,kullanici_silme_bilgisi = False).order_by("-id")
        kullanic_izinlerim = personel_izinleri.objects.filter(izinlerin_sahibi_kullanici = request.user)
        content["kullanici_izinlerim"] = kullanic_izinlerim
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =CustomUser.objects.filter(Q(last_name__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = CustomUser.objects.filter(Q(last_name__icontains = search) & Q(kullanici_silme_bilgisi = False))
            kullanic_izinlerim = personel_izinleri.objects.filter(izinlerin_sahibi_kullanici = request.user)
            content["kullanici_izinlerim"] = kullanic_izinlerim
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
    #print(profile)
    return render(request,"account/kullanicilar.html",content)
#kullanıcılar
from django.contrib.auth.hashers import make_password
def kullanici_ekleme(request):
    if request.POST:
        if request.user.is_superuser:
            pass
        else:
            yetkili_adi = request.POST.get("yetkili_adi")
            email = request.POST.get("email")
            gorevi = request.POST.get("gorevi")
            durumu = request.POST.get("durumu")
            parola = request.POST.get("parola")
            file = request.POST.getlist("file")
            izinler = request.POST.get("izinler")
            #yeni_sifre = request.POST.get("sifre")
            if durumu == "1":
                durumu = True
            else:
                durumu = False
            a = CustomUser(
                first_name = request.user.first_name,
                last_name = yetkili_adi,
                username = email,
                email = email,
                gorevi =gorevi,
                kullanicilar_db = request.user,
                is_active = durumu
            )
            a.set_password(parola)

            a.save()
            for images in file:
                personel_dosyalari.objects.create(dosyalari=images,kullanici = get_object_or_404(CustomUser,id = a.id))  # Urun_resimleri modeline resimleri kaydet
            if izinler:
                bagli_kullanicilar.objects.create(izinler = get_object_or_404(personel_izinleri,id = izinler),kullanicilar = get_object_or_404(CustomUser,id = a.id))
        return redirect_with_language("users:kullanicilarim")


def kullanici_silme(request):
    if request.POST:
        buttonIdInput = request.POST.get("buttonId")
        CustomUser.objects.filter(id = buttonIdInput).update(is_active = False,kullanici_silme_bilgisi  = True)
    return redirect_with_language("users:kullanicilarim")

def kullanici_bilgileri_duzenle(request):
    if request.POST:
        if request.user.is_superuser:
            pass  # Superuser için özel işlem varsa buraya eklenmeli
        else:
            buttonId = request.POST.get("buttonId")
            yetkili_adi = request.POST.get("yetkili_adi")
            email = request.POST.get("email")
            gorevi = request.POST.get("gorevi")
            durumu = request.POST.get("durumu")
            file = request.FILES.getlist("file")
            izinler = request.POST.get("izinler")
            yeni_sifre = request.POST.get("sifre")  # 🔐 Şifre alanı

            user = get_object_or_404(CustomUser, id=buttonId)

            bagli_kullanicilar.objects.filter(kullanicilar=user).delete()

            is_active = True if durumu == "1" else False

            # Şifreyi güncelle, sadece doluysa
            if yeni_sifre:
                user.password = make_password(yeni_sifre)

            # Diğer alanları güncelle
            user.first_name = request.user.first_name
            user.last_name = yetkili_adi
            user.username = email
            user.email = email
            user.gorevi = gorevi
            user.kullanicilar_db = request.user
            user.is_active = is_active

            user.save()

            # Dosya ekleme
            if file:
                for images in file:
                    personel_dosyalari.objects.create(
                        kayit_tarihi=get_kayit_tarihi_from_request(request),
                        dosyalari=images,
                        kullanici=user
                    )

            # İzin bağlama
            if izinler:
                bagli_kullanicilar.objects.create(
                    izinler=get_object_or_404(personel_izinleri, id=izinler),
                    kullanicilar=user
                )

        return redirect_with_language("users:kullanicilarim")
######################3
#kullanıcılar
def kullanicilarim_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users

    if super_admin_kontrolu(request):
        profile = taseron_sozlesme_dosyalari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = CustomUser.objects.filter(kullanicilar_db = users,kullanici_silme_bilgisi = False).order_by("-id")
        kullanic_izinlerim = personel_izinleri.objects.filter(izinlerin_sahibi_kullanici = users)
        content["kullanici_izinlerim"] = kullanic_izinlerim
    else:
        profile = CustomUser.objects.filter(kullanicilar_db = request.user,kullanici_silme_bilgisi = False).order_by("-id")
        kullanic_izinlerim = personel_izinleri.objects.filter(izinlerin_sahibi_kullanici = request.user)
        content["kullanici_izinlerim"] = kullanic_izinlerim

    content["santiyeler"] = profile
    return render(request,"account/kullanicilar.html",content)
#kullanıcılar

def kullanici_ekleme_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            yetkili_adi = request.POST.get("yetkili_adi")
            email = request.POST.get("email")
            gorevi = request.POST.get("gorevi")
            durumu = request.POST.get("durumu")
            parola = request.POST.get("parola")
            file = request.POST.getlist("file")
            izinler = request.POST.get("izinler")
            if durumu == "1":
                durumu = True
            else:
                durumu = False
            a = CustomUser(
                first_name = users.first_name,
                last_name = yetkili_adi,
                username = email,
                email = email,
                gorevi =gorevi,
                kullanicilar_db = users,
                is_active = durumu
            )
            a.set_password(parola)

            a.save()
            for images in file:
                personel_dosyalari.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),dosyalari=images,kullanici = get_object_or_404(CustomUser,id = a.id))  # Urun_resimleri modeline resimleri kaydet
            if izinler:
                bagli_kullanicilar.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),izinler = get_object_or_404(personel_izinleri,id = izinler),kullanicilar = get_object_or_404(CustomUser,id = a.id))
        else:
            yetkili_adi = request.POST.get("yetkili_adi")
            email = request.POST.get("email")
            gorevi = request.POST.get("gorevi")
            durumu = request.POST.get("durumu")
            parola = request.POST.get("parola")
            file = request.POST.getlist("file")
            izinler = request.POST.get("izinler")
            if durumu == "1":
                durumu = True
            else:
                durumu = False
            a = CustomUser(
                first_name = request.user.first_name,
                last_name = yetkili_adi,
                username = email,
                email = email,
                gorevi =gorevi,
                kullanicilar_db = request.user,
                is_active = durumu
            )
            a.set_password(parola)

            a.save()
            for images in file:
                personel_dosyalari.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),dosyalari=images,kullanici = get_object_or_404(CustomUser,id = a.id))  # Urun_resimleri modeline resimleri kaydet
            if izinler:
                bagli_kullanicilar.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),izinler = get_object_or_404(personel_izinleri,id = izinler),kullanicilar = get_object_or_404(CustomUser,id = a.id))
        return redirect_with_language("users:kullanicilarim_2",hash)


def kullanici_silme_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        buttonIdInput = request.POST.get("buttonId")
        CustomUser.objects.filter(id = buttonIdInput).update(is_active = False,kullanici_silme_bilgisi  = True)
    return redirect_with_language("users:kullanicilarim_2",hash)

def kullanici_bilgileri_duzenle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        if request.user.is_superuser:
            buttonId = request.POST.get("buttonId")
            yetkili_adi = request.POST.get("yetkili_adi")
            email = request.POST.get("email")
            gorevi = request.POST.get("gorevi")
            durumu = request.POST.get("durumu")
            file = request.POST.getlist("file")
            izinler = request.POST.get("izinler")
            bagli_kullanicilar.objects.filter(kullanicilar =get_object_or_404(CustomUser, id = buttonId)).delete()
            if durumu == "1":
                durumu = True
            else:
                durumu = False
            CustomUser.objects.filter(id=buttonId).update(
                first_name = users.first_name,
                last_name = yetkili_adi,
                username = email,
                email = email,
                gorevi =gorevi,
                kullanicilar_db = users,
                is_active = durumu
            )
            if len(file)> 1:
                for images in file:
                    personel_dosyalari.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),dosyalari=images,kullanici = get_object_or_404(CustomUser,id = buttonId))  # Urun_resimleri modeline resimleri kaydet
            if izinler:
                bagli_kullanicilar.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),izinler = get_object_or_404(personel_izinleri,id = izinler),kullanicilar = get_object_or_404(CustomUser, id = buttonId))
        else:
            
            buttonId = request.POST.get("buttonId")
            yetkili_adi = request.POST.get("yetkili_adi")
            email = request.POST.get("email")
            gorevi = request.POST.get("gorevi")
            durumu = request.POST.get("durumu")
            file = request.POST.getlist("file")
            izinler = request.POST.get("izinler")
            bagli_kullanicilar.objects.filter(kullanicilar =get_object_or_404(CustomUser, id = buttonId)).delete()
            if durumu == "1":
                durumu = True
            else:
                durumu = False
            CustomUser.objects.filter(id=buttonId).update(
                first_name = request.user.first_name,
                last_name = yetkili_adi,
                username = email,
                email = email,
                gorevi =gorevi,
                kullanicilar_db = request.user,
                is_active = durumu
            )
            if len(file)> 1:
                for images in file:
                    personel_dosyalari.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),dosyalari=images,kullanici = get_object_or_404(CustomUser,id = buttonId))  # Urun_resimleri modeline resimleri kaydet
            if izinler:
                bagli_kullanicilar.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),izinler = get_object_or_404(personel_izinleri,id = izinler),kullanicilar = get_object_or_404(CustomUser, id = buttonId))
        return redirect_with_language("users:kullanicilarim_2",hash)

######################



@login_required
@lock_screen_required
def lock_screen(request):
    content = sozluk_yapisi()
    try:
        lock_status = LockScreenStatus.objects.get(user=request.user)
        lock_status.is_locked=True
        lock_status.save()
    except LockScreenStatus.DoesNotExist:
        # Kullanıcının LockScreenStatus objesi henüz oluşturulmamışsa, oluşturun.
        lock_status = LockScreenStatus.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),user=request.user, is_locked=True)

    if request.method == 'POST':
        password = request.POST.get('userpassword')
        user = authenticate(request, username=request.user.username, password=password)

        if user is not None:
            # Parola doğru, kullanıcıyı kilidi aç
            lock_status.is_locked = False
            lock_status.save()
            return redirect_with_language('main:homepage')   # Yönlendireceğiniz sayfayı belirtin
        else:
            # Parola doğru değilse hata mesajını gösterin
            error_message = "Parola yanlış. Tekrar deneyin."
            return render(request, 'account/lock_screen.html', {'error_message': error_message})

    return render(request, 'account/lock_screen.html')
#lockscreen

def profile_edit_kismi(request):
    content = sozluk_yapisi()
    
    if request.POST:
        background = request.FILES.get("background_bilgisi")
        profile = request.FILES.get("profile_bilgisi")
        adi_soyadi = request.POST.get("adi_soyadi")
        telefon_numarasi = request.POST.get("telefon_numarasi")
        email_bilgisi = request.POST.get("email_bilgisi")
        aciklama = request.POST.get("aciklama")
        adres = request.POST.get("adres")
        imza = request.POST.get("imza")
        CustomUser.objects.filter(id = request.user.id).update(
            username = email_bilgisi,email = email_bilgisi,
            description = aciklama, last_name = adi_soyadi,
            telefon_numarasi = telefon_numarasi,adrrsi = adres,
            imza_sifresi = imza
        )
        if profile:
            u = CustomUser.objects.get(id = request.user.id)
            u.image = profile
            u.save()

        if background:
            u = CustomUser.objects.get(id = request.user.id)
            u.background_image = background
            u.save()
        return redirect_with_language("users:profile_edit_kismi")
    return render(request,"account/profile_edit.html",content)


def parola_degistime(request):
    if request.POST:
        eski_parola = request.POST.get("eski_parola")
        yeni_parola = request.POST.get("yeni_parola")
        yeni_parola_tekrar = request.POST.get("yeni_parola_tekrar")
        if yeni_parola == yeni_parola_tekrar:
            if request.user.check_password(eski_parola):
                u = CustomUser.objects.get(id = request.user.id)
                u.set_password(yeni_parola)
                u.save()

            else:
                messages.success(request, 'Eski Parolanız hatalı')
        else:
            messages.success(request, 'Parolanız Uyuşmuyor')
    return redirect_with_language("/")



def personeller_sayfasi(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        pass
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.personeller_gorme:
                    kullanici = request.user.kullanicilar_db
                    
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            kullanici = request.user
        content["departmanlar"] = calisanlar_kategorisi.objects.filter(kategori_kime_ait = kullanici)
        content["pozisyonlari"] = calisanlar_pozisyonu.objects.filter(kategori_kime_ait = kullanici)
        content["personeller"] = calisanlar.objects.filter(status = "0",calisan_kime_ait = kullanici)
        bilgi = faturalar_icin_bilgiler.objects.filter(gelir_kime_ait_oldugu  = kullanici).last()
        if bilgi:
            pass
            if bilgi.gunluk_calisma_saati:
                pass
            else:
                return redirect_with_language("accounting:muhasebe_ayarlari")
        else:
            return redirect_with_language("accounting:muhasebe_ayarlari")
    return render(request,"personel/personeller.html",content)
#

def personeller_sayfasi_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users

    if super_admin_kontrolu(request):
        kullanici = users
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.personeller_gorme:
                    kullanici = request.user.kullanicilar_db
                    
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            kullanici = request.user
    content["departmanlar"] = calisanlar_kategorisi.objects.filter(kategori_kime_ait = kullanici)
    content["pozisyonlari"] = calisanlar_pozisyonu.objects.filter(kategori_kime_ait = kullanici)
    content["personeller"] = calisanlar.objects.filter(status = "0",calisan_kime_ait = kullanici,silinme_bilgisi = False)
    return render(request,"personel/personeller.html",content)
#
def personeller_ekle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.personeller_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else:
        kullanici = request.user
    if request.POST:
        profilePicture = request.FILES.get("profilePicture")
        passportNo = request.POST.get("passportNo")
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        dogum_tarihi = request.POST.get("dob")
        nationality = request.POST.get("nationality")
        phoneNumber = request.POST.get("phoneNumber")
        department = request.POST.get("department")
        position = request.POST.get("position")
        salaryType = request.POST.get("salaryType")
        dailyWage = request.POST.get("dailyWage")
        fazla_mesai_orani = request.POST.get("fazla_mesai_orani")
        hourlyWage = request.POST.get("hourlyWage")
        currency = request.POST.get("currency")
        belgeler = request.POST.getlist("belgeler")
        documents = request.FILES.getlist("ekler")
        for i in range(1):
            #print(belgeler,documents)
            if profilePicture:
                pass
            else:
                profilePicture =None
            if salaryType == "maas":
                salaryType = True
            else:
                salaryType = False
            if currency == "USD":
                currency = True
            else:
                currency = False
            for i in range(21):
                bilgi = calisanlar.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),calisan_kime_ait = kullanici,calisan_kategori = get_object_or_none(calisanlar_kategorisi , id =department),
                calisan_pozisyonu = get_object_or_none(calisanlar_pozisyonu , id =position),uyrugu  = nationality,pasaport_numarasi = passportNo,
                isim = firstName,soyisim = lastName,profile = profilePicture,dogum_tarihi =dogum_tarihi,telefon_numarasi = phoneNumber  )
                calisan_maas_durumlari.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),calisan = get_object_or_none(calisanlar,id =bilgi.id ),maas = dailyWage,
                yevmiye = hourlyWage,durum =salaryType,para_birimi = currency,fazla_mesai_orani =fazla_mesai_orani  )
                for i in documents:
                    calisan_belgeleri.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),calisan = get_object_or_none(calisanlar,id =bilgi.id ) ,belge = i )
    return redirect_with_language("user:personeller_sayfasi")
def personeller_ekle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.user.is_superuser:
        kullanici = users
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.personeller_olusturma:
                    kullanici = request.user.kullanicilar_db
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            kullanici = request.user
    if request.POST:
        profilePicture = request.FILES.get("profilePicture")
        passportNo = request.POST.get("passportNo")
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        dogum_tarihi = request.POST.get("dob")
        nationality = request.POST.get("nationality")
        phoneNumber = request.POST.get("phoneNumber")
        department = request.POST.get("department")
        position = request.POST.get("position")
        salaryType = request.POST.get("salaryType")
        dailyWage = request.POST.get("dailyWage")
        hourlyWage = request.POST.get("hourlyWage")
        fazla_mesai_orani = request.POST.get("fazla_mesai_orani")
        currency = request.POST.get("currency")
        belgeler = request.POST.getlist("belgeler")
        documents = request.FILES.getlist("ekler")
        for i in range(1):
            #print(belgeler,documents)
            if profilePicture:
                pass
            else:
                profilePicture =None
            if salaryType == "maas":
                salaryType = True
            else:
                salaryType = False
            if currency == "USD":
                currency = True
            else:
                currency = False
            bilgi = calisanlar.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),calisan_kime_ait = kullanici,calisan_kategori = get_object_or_none(calisanlar_kategorisi , id =department),
            calisan_pozisyonu = get_object_or_none(calisanlar_pozisyonu , id =position),uyrugu  = nationality,pasaport_numarasi = passportNo,
            isim = firstName,soyisim = lastName,profile = profilePicture,dogum_tarihi =dogum_tarihi,telefon_numarasi = phoneNumber  )
            calisan_maas_durumlari.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),calisan = get_object_or_none(calisanlar,id =bilgi.id ),maas = dailyWage,
            yevmiye = hourlyWage,durum =salaryType,para_birimi = currency,fazla_mesai_orani =fazla_mesai_orani  )
            for i in documents:
                calisan_belgeleri.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),calisan = get_object_or_none(calisanlar,id =bilgi.id ) ,belge = i )
    return redirect_with_language("user:personeller_sayfasi_2",hash)
def personeller_sil_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        id = request.POST.get("idbilgisi")
        calisanlar.objects.filter(id =id).update(silinme_bilgisi = True)
    return redirect_with_language("user:personeller_sayfasi_2",hash)
def personeller_odenmeye_maaslar(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        pass
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.personeller_gorme:
                    kullanici = request.user.kullanicilar_db
                    
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            kullanici = request.user
        content["departmanlar"] = calisanlar_kategorisi.objects.filter(kategori_kime_ait = kullanici)
        content["pozisyonlari"] = calisanlar_pozisyonu.objects.filter(kategori_kime_ait = kullanici)
        content["personeller"] = calisanlar.objects.filter(status = "0",calisan_kime_ait = kullanici)
    return render(request,"personel/odenmeyen_maaslar.html",content)

def personeller_odenmeye_maaslar_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users

    if super_admin_kontrolu(request):
        kullanici = users
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.personeller_gorme:
                    kullanici = request.user.kullanicilar_db
                    
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            kullanici = request.user
    content["departmanlar"] = calisanlar_kategorisi.objects.filter(kategori_kime_ait = kullanici)
    content["pozisyonlari"] = calisanlar_pozisyonu.objects.filter(kategori_kime_ait = kullanici)
    content["personeller"] = calisanlar.objects.filter(status = "0",calisan_kime_ait = kullanici,silinme_bilgisi = False)
    return render(request,"personel/odenmeyen_maaslar.html",content)
def bodro(request,tarih,id):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        pass
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.personeller_gorme:
                    kullanici = request.user.kullanicilar_db
                    
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            kullanici = request.user
        content["departmanlar"] = calisanlar_kategorisi.objects.filter(kategori_kime_ait = kullanici)
        content["pozisyonlari"] = calisanlar_pozisyonu.objects.filter(kategori_kime_ait = kullanici)
        content["personel"] = get_object_or_404(calisanlar,status = "0",calisan_kime_ait = kullanici,id = id) 
        content["istenen_tarih_araligi"] =tarih
    return render(request,"personel/bodro.html",content)
def personeller_sil(request):
    if request.POST:
        id = request.POST.get("idbilgisi")
        calisanlar.objects.filter(id =id).update(silinme_bilgisi = True)
    return redirect_with_language("user:personeller_sayfasi")
def personelleri_düzenle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.personeller_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            return redirect_with_language("main:yetkisiz")
    else:
        kullanici = request.user
    if request.POST:
        idbilgisi = request.POST.get("idbilgisi")
        profilePicture = request.FILES.get("profilePicture")
        passportNo = request.POST.get("passportNo")
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        dogum_tarihi = request.POST.get("dob")
        nationality = request.POST.get("nationality")
        phoneNumber = request.POST.get("phoneNumber")
        department = request.POST.get("department")
        position = request.POST.get("position")
        salaryType = request.POST.get("salaryType")
        dailyWage = request.POST.get("dailyWage")
        hourlyWage = request.POST.get("hourlyWage")
        currency = request.POST.get("currency")
        belgeler = request.POST.getlist("belgeler")
        documents = request.FILES.getlist("ekler")
        for i in range(1):
            #print(belgeler,documents)
            if profilePicture:
                duzenle = calisanlar.objects.get(id = idbilgisi)
                duzenle.profile = profilePicture
                duzenle.save()
            else:
                profilePicture =None
            if salaryType == "maas":
                salaryType = True
            else:
                salaryType = False
            if currency == "USD":
                currency = True
            else:
                currency = False
            bilgi = calisanlar.objects.filter(id = idbilgisi).update(calisan_kime_ait = kullanici,calisan_kategori = get_object_or_none(calisanlar_kategorisi , id =department),
            calisan_pozisyonu = get_object_or_none(calisanlar_pozisyonu , id =position),uyrugu  = nationality,pasaport_numarasi = passportNo,
            isim = firstName,soyisim = lastName,dogum_tarihi =dogum_tarihi,telefon_numarasi = phoneNumber  )
            calisan_maas_durumlari.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),calisan = get_object_or_none(calisanlar,id =idbilgisi),maas = dailyWage,
            yevmiye = hourlyWage,durum =salaryType,para_birimi = currency )
            for i in documents:
                calisan_belgeleri.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),calisan = get_object_or_none(calisanlar,id =idbilgisi ) ,belge = i )
        return redirect_with_language("user:personeller_sayfasi")
#######################################################3
#Pozisyonlar
def personeller_kategori_sayfalari_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users

    if super_admin_kontrolu(request):
        kullanici = users
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.personeller_gorme:
                    kullanici = request.user.kullanicilar_db
                    
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            kullanici = request.user
        #content["departmanlar"] = calisanlar_kategorisi.objects.filter(kategori_kime_ait = kullanici)
    content["santiyeler"] = calisanlar_pozisyonu.objects.filter(kategori_kime_ait = kullanici)
        #content["personeller"] = calisanlar.objects.filter(status = "0",calisan_kime_ait = kullanici)
    return render(request,"personel/pozisyonlar.html",content)
def personeller_kategori_ekle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        pozsiyon = request.POST.get("yetkili_adi")
        if super_admin_kontrolu(request):
            kullanici = users
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.personeller_olusturma:
                        kullanici = request.user.kullanicilar_db
                        
                    else:
                        return redirect_with_language("main:yetkisiz")
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                kullanici = request.user
    calisanlar_pozisyonu.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),kategori_kime_ait =kullanici,kategori_isimi = pozsiyon )
        
    return redirect_with_language("users:personeller_kategori_sayfalari_2",hash)   
def personeller_kategori_sil_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        pozsiyon = request.POST.get("buttonId")
        if super_admin_kontrolu(request):
            kullanici = users
        
        calisanlar_pozisyonu.objects.filter(kategori_kime_ait =kullanici,id = pozsiyon ).delete()
        
    return redirect_with_language("users:personeller_kategori_sayfalari_2",hash)   
def personelleri_kategori_düzenle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        buton = request.POST.get("buttonId")
        pozsiyon = request.POST.get("yetkili_adi")
        if super_admin_kontrolu(request):
            kullanici = users
        
        calisanlar_pozisyonu.objects.filter(kategori_kime_ait =kullanici,id =buton ).update(kategori_isimi = pozsiyon )
        
    return redirect_with_language("users:personeller_kategori_sayfalari_2",hash)

#
def personeller_depertman_sayfalari_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users

    if super_admin_kontrolu(request):
        kullanici = users
    
        content["santiyeler"] = calisanlar_kategorisi.objects.filter(kategori_kime_ait = kullanici)
        #content["santiyeler"] = calisanlar_pozisyonu.objects.filter(kategori_kime_ait = kullanici)
        #content["personeller"] = calisanlar.objects.filter(status = "0",calisan_kime_ait = kullanici)
    return render(request,"personel/departmanlar.html",content)
def personeller_departman_ekle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        pozsiyon = request.POST.get("yetkili_adi")
        if super_admin_kontrolu(request):
            kullanici = users
        calisanlar_kategorisi.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),kategori_kime_ait =kullanici,kategori_isimi = pozsiyon )
        
    return redirect_with_language("users:personeller_depertman_sayfalari_2",hash)   
def personeller_departman_sil_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        pozsiyon = request.POST.get("buttonId")
        if super_admin_kontrolu(request):
            kullanici = users
        
        calisanlar_kategorisi.objects.filter(kategori_kime_ait =kullanici,id = pozsiyon ).delete()
        
    return redirect_with_language("users:personeller_depertman_sayfalari_2",hash)   
def personelleri_departman_düzenle_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        buton = request.POST.get("buttonId")
        pozsiyon = request.POST.get("yetkili_adi")
        if super_admin_kontrolu(request):
            kullanici = users
        
        calisanlar_kategorisi.objects.filter(kategori_kime_ait =kullanici,id =buton ).update(kategori_isimi = pozsiyon )
        
    return redirect_with_language("users:personeller_depertman_sayfalari_2",hash)






#####################################################
#Pozisyonlar
def personeller_kategori_sayfalari(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        pass
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.personeller_gorme:
                    kullanici = request.user.kullanicilar_db
                    
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            kullanici = request.user
        #content["departmanlar"] = calisanlar_kategorisi.objects.filter(kategori_kime_ait = kullanici)
        content["santiyeler"] = calisanlar_pozisyonu.objects.filter(kategori_kime_ait = kullanici)
        #content["personeller"] = calisanlar.objects.filter(status = "0",calisan_kime_ait = kullanici)
    return render(request,"personel/pozisyonlar.html",content)
def personeller_kategori_ekle(request):
    if request.POST:
        pozsiyon = request.POST.get("yetkili_adi")
        if super_admin_kontrolu(request):
            pass
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.personeller_olusturma:
                        kullanici = request.user.kullanicilar_db
                        
                    else:
                        return redirect_with_language("main:yetkisiz")
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                kullanici = request.user
        calisanlar_pozisyonu.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),kategori_kime_ait =kullanici,kategori_isimi = pozsiyon )
        
    return redirect_with_language("users:personeller_kategori_sayfalari")   
def personeller_kategori_sil(request):
    if request.POST:
        pozsiyon = request.POST.get("buttonId")
        if super_admin_kontrolu(request):
            pass
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.personeller_silme:
                        kullanici = request.user.kullanicilar_db
                        
                    else:
                        return redirect_with_language("main:yetkisiz")
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                kullanici = request.user
        calisanlar_pozisyonu.objects.filter(kategori_kime_ait =kullanici,id = pozsiyon ).delete()
        
    return redirect_with_language("users:personeller_kategori_sayfalari")   
def personelleri_kategori_düzenle(request):
    if request.POST:
        buton = request.POST.get("buttonId")
        pozsiyon = request.POST.get("yetkili_adi")
        if super_admin_kontrolu(request):
            pass
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.personeller_olusturma:
                        kullanici = request.user.kullanicilar_db
                        
                    else:
                        return redirect_with_language("main:yetkisiz")
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                kullanici = request.user
        calisanlar_pozisyonu.objects.filter(kategori_kime_ait =kullanici,id =buton ).update(kategori_isimi = pozsiyon )
        
    return redirect_with_language("users:personeller_kategori_sayfalari")

#
def personeller_depertman_sayfalari(request):
    content = sozluk_yapisi()

    if super_admin_kontrolu(request):
        pass
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.personeller_gorme:
                    kullanici = request.user.kullanicilar_db
                    
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            kullanici = request.user
        content["santiyeler"] = calisanlar_kategorisi.objects.filter(kategori_kime_ait = kullanici)
        #content["santiyeler"] = calisanlar_pozisyonu.objects.filter(kategori_kime_ait = kullanici)
        #content["personeller"] = calisanlar.objects.filter(status = "0",calisan_kime_ait = kullanici)
    return render(request,"personel/departmanlar.html",content)
def personeller_departman_ekle(request):
    if request.POST:
        pozsiyon = request.POST.get("yetkili_adi")
        if super_admin_kontrolu(request):
            pass
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.personeller_olusturma:
                        kullanici = request.user.kullanicilar_db
                        
                    else:
                        return redirect_with_language("main:yetkisiz")
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                kullanici = request.user
        calisanlar_kategorisi.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),kategori_kime_ait =kullanici,kategori_isimi = pozsiyon )
        
    return redirect_with_language("users:personeller_depertman_sayfalari")   
def personeller_departman_sil(request):
    if request.POST:
        pozsiyon = request.POST.get("buttonId")
        if super_admin_kontrolu(request):
            pass
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.personeller_silme:
                        kullanici = request.user.kullanicilar_db
                        
                    else:
                        return redirect_with_language("main:yetkisiz")
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                kullanici = request.user
        calisanlar_kategorisi.objects.filter(kategori_kime_ait =kullanici,id = pozsiyon ).delete()
        
    return redirect_with_language("users:personeller_depertman_sayfalari")   
def personelleri_departman_düzenle(request):
    if request.POST:
        buton = request.POST.get("buttonId")
        pozsiyon = request.POST.get("yetkili_adi")
        if super_admin_kontrolu(request):
            pass
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.personeller_olusturma:
                        kullanici = request.user.kullanicilar_db
                        
                    else:
                        return redirect_with_language("main:yetkisiz")
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                kullanici = request.user
        calisanlar_kategorisi.objects.filter(kategori_kime_ait =kullanici,id =buton ).update(kategori_isimi = pozsiyon )
        
    return redirect_with_language("users:personeller_depertman_sayfalari")
import calendar
from datetime import datetime
def personeller_puantaj_sayfasi(request):
    content = sozluk_yapisi()
    
    if super_admin_kontrolu(request):
        pass
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.personeller_gorme:
                    kullanici = request.user.kullanicilar_db
                    
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            kullanici = request.user
        person = calisanlar.objects.filter(status = "0",calisan_kime_ait = kullanici,silinme_bilgisi = False)
        if request.GET:
            month_filter = request.GET.get("monthFilter")
            jobTypeFilter = request.GET.get("jobTypeFilter")
            personelID = request.GET.get("personelID")
            days_in_month = 0
            days_list =[]
            hafta_bazinda = {}
            hafta1 = []
            hafta2 = []
            hafta3 = []
            hafta4 = []
            if month_filter:
                year, month = map(int, month_filter.split('-'))  # Yıl ve ayı alıyoruz
                _, num_days = calendar.monthrange(year, month)   # O ayın gün sayısını buluyoruz
                days_list = [day for day in range(1, num_days + 1)] 
            for i in days_list:
                if 7 >= i >= 1:
                    hafta1.append(i)
                    
                if 14 >= i > 7:
                    hafta2.append(i)
                if 21 >= i > 14:
                    hafta3.append(i)
                if i > 21:
                    hafta4.append(i)

            hafta_bazinda["hafta1"] = hafta1
            hafta_bazinda["hafta2"] = hafta2
            hafta_bazinda["hafta3"] = hafta3
            hafta_bazinda["hafta4"] = hafta4
            content["haftalik"] = hafta_bazinda
            content["gun"] =days_list
            if jobTypeFilter :
                person = person.filter(calisan_kategori = get_object_or_none(calisanlar_kategorisi , id = jobTypeFilter))
            if personelID:
                person = person.filter(id = personelID)
        content["departmanlar"] = calisanlar_kategorisi.objects.filter(kategori_kime_ait = kullanici)
        content["pozisyonlari"] = calisanlar_pozisyonu.objects.filter(kategori_kime_ait = kullanici)
        content["personeller"] = person
    return render(request,"personel/puantaj2.html",content)
def personeller_puantaj_sayfasi_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    
    if super_admin_kontrolu(request):
        kullanici = users
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.personeller_gorme:
                    kullanici = request.user.kullanicilar_db
                    
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                return redirect_with_language("main:yetkisiz")
        else:
            kullanici = request.user
    if kullanici:
        person = calisanlar.objects.filter(status = "0",calisan_kime_ait = kullanici,silinme_bilgisi = False)
        if request.GET:
            month_filter = request.GET.get("monthFilter")
            jobTypeFilter = request.GET.get("jobTypeFilter")
            personelID = request.GET.get("personelID")
            days_in_month = 0
            days_list =[]
            hafta_bazinda = {}
            hafta1 = []
            hafta2 = []
            hafta3 = []
            hafta4 = []
            if month_filter:
                year, month = map(int, month_filter.split('-'))  # Yıl ve ayı alıyoruz
                _, num_days = calendar.monthrange(year, month)   # O ayın gün sayısını buluyoruz
                days_list = [day for day in range(1, num_days + 1)] 
            for i in days_list:
                if 7 >= i >= 1:
                    hafta1.append(i)
                    
                if 14 >= i > 7:
                    hafta2.append(i)
                if 21 >= i > 14:
                    hafta3.append(i)
                if i > 21:
                    hafta4.append(i)

            hafta_bazinda["hafta1"] = hafta1
            hafta_bazinda["hafta2"] = hafta2
            hafta_bazinda["hafta3"] = hafta3
            hafta_bazinda["hafta4"] = hafta4
            content["haftalik"] = hafta_bazinda
            content["gun"] =days_list
            if jobTypeFilter :
                person = person.filter(calisan_kategori = get_object_or_none(calisanlar_kategorisi , id = jobTypeFilter))
            if personelID:
                person = person.filter(id = personelID)
        content["departmanlar"] = calisanlar_kategorisi.objects.filter(kategori_kime_ait = kullanici)
        content["pozisyonlari"] = calisanlar_pozisyonu.objects.filter(kategori_kime_ait = kullanici)
        content["personeller"] = person
    return render(request,"personel/puantaj2.html",content)

from django.http import JsonResponse
import json

def save_attendance(request):
    from datetime import datetime
    if request.method == 'POST':
        data = json.loads(request.body)  # JSON veriyi al
        tarih = data[0]
        tarih = str(tarih).split("-")
        yil  = tarih[0]
        ay = tarih[1]
        veriler = data[1]
        for entry in veriler:     
            person_id = entry.get('person')
            day = entry.get('day')
            work_type = entry.get('type')
            hours_value = entry.get('value')
            date_obj = datetime(int(yil), int(ay), int(day))
            if work_type == "normal":
                if get_object_or_none(calisanlar_calismalari,calisan = get_object_or_none(calisanlar,id =person_id ),tarihi = date_obj):
                    calisanlar_calismalari.objects.filter(calisan = get_object_or_none(calisanlar,id =person_id ),tarihi = date_obj
                    ).update(normal_calisma_saati =float(hours_value))
                else:
                    calisanlar_calismalari.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),calisan = get_object_or_none(calisanlar,id =person_id )
                    ,tarihi = date_obj,maas = calisan_maas_durumlari.objects.filter(calisan = get_object_or_none(calisanlar,id =person_id )).last(),
                    normal_calisma_saati =float(hours_value) )
            elif work_type == "overtime":
                calisanlar_calismalari.objects.filter(calisan = get_object_or_none(calisanlar,id =person_id ),tarihi = date_obj
                    ).update(mesai_calisma_saati =float(hours_value))
            # Her bir kayıttaki verilerle istediğiniz işlemi yapabilirsiniz
            
        return JsonResponse({'status': 'success'})
def calismalari_cek(request):
    from datetime import datetime
    if request.method == 'POST':
        data = json.loads(request.body)
        for entry in data: 
            personel = entry.get('personel')
            gun = entry.get('gun_gonder')
            tarih = entry.get('tarih_gonder')
            tarih  = str(tarih).split("-")
            yil  = tarih[0]
            ay = tarih[1]
            date_obj = datetime(int(yil), int(ay), int(gun))
            sonuc  = get_object_or_none(calisanlar_calismalari,calisan = get_object_or_none(calisanlar,id =personel ),tarihi = date_obj)
            if sonuc:
                return JsonResponse({'sonuc': 'veri_var',"normal_saat":sonuc.normal_calisma_saati,"mesai_saati":sonuc.mesai_calisma_saati})   
            else:
                return JsonResponse({'sonuc': 'veri_yok'})   
    return JsonResponse({'sonuc': 'veri_yok'})

from muhasebe.models import calisanlar_calismalari_odemeleri
def calisan_odemeleri_kaydet(request):
    if request.POST:
        odeme_turu = request.POST.get("odeme_turu")
        users_id = request.POST.get("users_id")
        maas_ayi = request.POST.get("maas_ayi")
        odeme_tarihi = request.POST.get("odeme_tarihi")
        tutar = request.POST.get("tutar")
        aciklama = request.POST.get("aciklama")
        file = request.FILES.get("file")
        kur = request.POST.get("kur")
        if kur:
            pass
        else:
            kur = 0
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.blog_olusturma:
                    kullanici = request.user.kullanicilar_db
                else:
                    return redirect_with_language("main:yetkisiz")
            else:
                return redirect_with_language("main:yetkisiz")
        elif super_admin_kontrolu(request):
            return redirect_with_language("/")
        else:
            kullanici = request.user
        year, month = map(int, maas_ayi.split('-'))
    
        # Ayın ilk günü ile Date nesnesini oluştur
        date_obj = datetime(year, month, 1)
        if odeme_turu:
            calisanlar_calismalari_odemeleri.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),
                calisan = get_object_or_none(calisanlar,id =users_id,calisan_kime_ait =  kullanici),
                tutar = tutar,kur = kur,tarihi = date_obj,odeme_tarihi = odeme_tarihi,
                odeme_turu = True,aciklama = aciklama,dosya = file
            )
        else:
            calisanlar_calismalari_odemeleri.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),
                calisan = get_object_or_none(calisanlar,id =users_id,calisan_kime_ait =  kullanici),
                tutar = tutar,kur = kur,tarihi = date_obj,odeme_tarihi = odeme_tarihi,
                odeme_turu = False,aciklama = aciklama,dosya = file
            )
    return redirect_with_language("users:personeller_sayfasi")
def calisan_odemeleri_kaydet_2(request,hash):
    content = sozluk_yapisi()
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        odeme_turu = request.POST.get("odeme_turu")
        users_id = request.POST.get("users_id")
        maas_ayi = request.POST.get("maas_ayi")
        odeme_tarihi = request.POST.get("odeme_tarihi")
        tutar = request.POST.get("tutar")
        aciklama = request.POST.get("aciklama")
        file = request.FILES.get("file")
        kur = request.POST.get("kur")
        if kur:
            pass
        else:
            kur = 0
        if request.user.is_superuser:
            kullanici = users
        year, month = map(int, maas_ayi.split('-'))
    
        # Ayın ilk günü ile Date nesnesini oluştur
        date_obj = datetime(year, month, 1)
        if odeme_turu:
            calisanlar_calismalari_odemeleri.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),
                calisan = get_object_or_none(calisanlar,id =users_id,calisan_kime_ait =  kullanici),
                tutar = tutar,kur = kur,tarihi = date_obj,odeme_tarihi = odeme_tarihi,
                odeme_turu = True,aciklama = aciklama,dosya = file
            )
        else:
            calisanlar_calismalari_odemeleri.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),
                calisan = get_object_or_none(calisanlar,id =users_id,calisan_kime_ait =  kullanici),
                tutar = tutar,kur = kur,tarihi = date_obj,odeme_tarihi = odeme_tarihi,
                odeme_turu = False,aciklama = aciklama,dosya = file
            )
    return redirect_with_language("users:personeller_sayfasi_2",hash)

import requests
from django.shortcuts import render



def get_client_ip(request):
    """Kullanıcının IP adresini alır"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def weather_view(request):
    weather_data = None
    ip_info = None
    
    # Kullanıcının IP adresini alıyoruz
    ip ="85.110.71.229"  #get_client_ip(request) #
    
    # ipinfo.io API'sini kullanarak IP'ye göre konum alıyoruz
    ipinfo_api_url = f"http://ipinfo.io/{ip}/json"
    ip_response = requests.get(ipinfo_api_url)
    #print(ip_response.json())
    if ip_response.status_code == 200:
        ip_info = ip_response.json()
        loc = ip_info.get('loc')
        
        if loc:  # Eğer 'loc' None değilse
            #print(loc)
            location = loc.split(',')
            lat, lon = location[0], location[1]
            
            # OpenWeatherMap API'yi kullanarak hava durumu alıyoruz
            api_key = 'dee0661903df4f2c76ccfd8afab8be69'
            weather_api_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}'
            
            weather_response = requests.get(weather_api_url)
            #print(weather_response)
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
            a = weather_data["weather"][0]
            icon = a["icon"] 
    return render(request, 'weather.html', {'weather_data': weather_data, 'ip_info': ip_info,"icon":icon})
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Group, Message

@login_required
def group_chat(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    messages = Message.objects.filter(group=group).order_by('timestamp')
    members = group.members.all()
    for member in members:
        member.is_online = member.is_online()  # Update the is_online status for each member

    context = {
        'group': group,
        'messages': messages,
        'members': members,
    }
    return render(request, 'chat/group_chat.html', context)
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Group, Message
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def user_list(request):
    content = sozluk_yapisi()
    if request.user.kullanicilar_db:
        users = User.objects.filter(Q(kullanicilar_db = request.user.kullanicilar_db) | Q(id = request.user.kullanicilar_db.id) ).exclude(id=request.user.id)
    else:
        users = User.objects.filter(kullanicilar_db = request.user ).exclude(id=request.user.id)
    groups = Group.objects.filter(members=request.user)
    content["users"] = users
    content["groups"] = groups
    return render(request, 'chat/chat.html', {'users': users})

@login_required
def user_chat(request, user_id):
    if True:
        recipient = get_object_or_404(User, id=user_id)
        group, created = Group.objects.get_or_create(name=f"{request.user.username}-{recipient.username}")
        if created:
            group.members.set([request.user, recipient])
            group.save()
        #Message.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),sender=request.user, group=group, content=content)
    return redirect_with_language('users:group_chat', group_id=group.id)
    #return render(request, 'chat/user_chat.html', context)
@login_required
def create_group(request):
    if request.method == "POST":
        group_name = request.POST.get('group_name')
        member_ids = request.POST.getlist('members')
        image = request.FILES.get("image")
        if image:
            group, created = Group.objects.get_or_create(name=group_name,image = image)
        else:
            group, created = Group.objects.get_or_create(name=group_name)
        
        if created:
            group.members.set(member_ids + [request.user.id])
            group.save()
        
        return redirect_with_language('users:group_chat', group_id=group.id)
    
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'chat/create_group.html', {'users': users})

@login_required
def group_chat(request, group_id):
    context = sozluk_yapisi()
    group = get_object_or_404(Group, id=group_id)
    messages = Message.objects.filter(group=group)
    messages = messages.order_by('timestamp')[:100]
    for message in messages:
        if message.sender != request.user:
            message.read = True
            message.save()
    if request.user.kullanicilar_db:
        users = User.objects.filter(kullanicilar_db = request.user.kullanicilar_db ).exclude(id=request.user.id)
    else:
        users = User.objects.filter(kullanicilar_db = request.user ).exclude(id=request.user.id)
    groups = Group.objects.filter(members=request.user)
    context["messages"] = messages
    context["users"] = users
    context["groups"] = groups
    context["group"] = group
    context["group_id"] = group_id  # Add group_id to context
    if request.method == "POST":
        content = request.POST.get('content')
        Message.objects.create(kayit_tarihi=get_kayit_tarihi_from_request(request),sender=request.user, group=group, content=content)
    
    return render(request, 'chat/group_chat.html', context)
@login_required
def group_list(request):
    context = sozluk_yapisi()
    
    if request.user.kullanicilar_db:
        users = User.objects.filter(kullanicilar_db = request.user.kullanicilar_db ).exclude(id=request.user.id)
    else:
        users = User.objects.filter(kullanicilar_db = request.user ).exclude(id=request.user.id)
    groups = Group.objects.filter(members=request.user)
    context["messages"] = messages
    context["users"] = users
    context["groups"] = groups
    
    return render(request, 'chat/group_chat.html', context)

#chat denemesi 
import requests

SENDBIRD_APP_ID = '9CAC1C16-4C39-4E56-BB2E-C37A9703C88C'
API_TOKEN = 'b90e79fa06974b6b945e349e'

def create_sendbird_user(user_id, nickname):
    url = f"https://api-9CAC1C16-4C39-4E56-BB2E-C37A9703C88C.sendbird.com/v3/users"
    headers = {
        "Content-Type": "application/json, charset=utf8",
        "Api-Token": API_TOKEN
    }
    data = {
        "user_id": user_id,
        "nickname": nickname
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
def create_group_channel(user_ids, name):
    url = f"https://api-9CAC1C16-4C39-4E56-BB2E-C37A9703C88C.sendbird.com/v3/group_channels"
    headers = {
        "Content-Type": "application/json, charset=utf8",
        "Api-Token": API_TOKEN
    }
    data = {
        "user_ids": user_ids,  # ['user1', 'user2', ...]
        "name": name,
        "is_distinct": True  # Aynı kullanıcılarla yeni bir kanal oluşturmaktan kaçınmak için
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('channel_url')  # Kanal URL'sini döndürür
    else:
        #print("Kanal oluşturulamadı:", response.json())
        return None

def is_user_online(user):
    last_login = user.last_login
    if last_login:
        now = timezone.now()
        return now - last_login < timedelta(minutes=5)
    return False

@login_required
def online_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return JsonResponse({'is_online': is_user_online(user)})

from django.contrib.sessions.models import Session
from django.utils import timezone

def logout_other_sessions(user, current_session_key):
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(user.id) and session.session_key != current_session_key:
            session.delete()
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_device_token(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token is required'}, status=400)

    DeviceToken.objects.update_or_create(
        user=request.user,
        defaults={'token': token}
    )

    return Response({'status': 'ok'})