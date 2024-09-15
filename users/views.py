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
from main.views import super_admin_kontrolu,dil_bilgisi,translate,sozluk_yapisi,yetki
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from django.db.models.query_utils import Q
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
def personel_bilgisi_axaj(request, id):
    
    if True:
        calisan = get_object_or_none(calisanlar, id = id)
        maasli = calisan_maas_durumlari.objects.filter(calisan = get_object_or_none(calisanlar, id = id)).last()
        cali_belgeleri = calisan_belgeleri.objects.filter(calisan = get_object_or_none(calisanlar, id = id))
        # Sorguları çalıştır
        calismalar = calisanlar_calismalari.objects.filter(
            calisan=get_object_or_none(calisanlar, id=id)
        ).annotate(
            year=ExtractYear('tarihi'),
            month=ExtractMonth('tarihi')
        ).values(
            'year', 'month', 'maas__id', 'calisan__id'  # Maas ID ve ismi ile gruplanıyor
        ).annotate(
            total_normal_calisma_saati=Sum('normal_calisma_saati'),
            total_mesai_calisma_saati=Sum('mesai_calisma_saati')
        ).order_by('year', 'month', 'maas__id')

        odemeler = calisanlar_calismalari_odemeleri.objects.filter(
            calisan=get_object_or_none(calisanlar, id=id)
        ).annotate(
            year=ExtractYear('tarihi'),
            month=ExtractMonth('tarihi')
        ).values(
            'year', 'month', 'calisan__id'  # Maas ID ve ismi ile gruplanıyor
        ).annotate(
            total_tutar=Sum('tutar')
        ).order_by('year', 'month')

        # Ödemeleri bir dict içine yerleştir
        odemeler_dict = {(odeme['year'], odeme['month']): odeme['total_tutar'] for odeme in odemeler}

        # Personel detayını oluştur
        personel_detayi = {
            'id': str(id),
            'calisan_kategori': calisan.calisan_kategori.kategori_isimi,
            'calisan_pozisyonu': calisan.calisan_pozisyonu.kategori_isimi,
            'uyrugu': calisan.uyrugu,
            'pasaport_numarasi': calisan.pasaport_numarasi,
            'isim': calisan.isim,
            'soyisim': calisan.soyisim,
            'profile': calisan.profile.url if calisan.profile else "https://www.pngitem.com/pimgs/m/81-819673_construction-workers-safety-icons-health-and-safety-policy.png",
            'dogum_tarihi': str(calisan.dogum_tarihi.strftime("%d.%m.%Y")),
            'telefon_numarasi': calisan.telefon_numarasi,
            'status': str(calisan.status),
            'maas': str(maasli.maas),
            'yevmiye': str(maasli.yevmiye),
            'durum': "1" if maasli.durum else "0",
            'para_birimi': "1" if maasli.para_birimi else "0",
            'belgeler': [
                {
                    'id': belge.id,
                    'belge_turu': belge.belge_turu,
                    'resim': belge.belge.url if belge.belge else "https://www.pngitem.com/pimgs/m/81-819673_construction-workers-safety-icons-health-and-safety-policy.png",
                } for belge in cali_belgeleri
            ],
            'calismalar': [
                {
                    'tarih': str(calis['year']) + "-" + str(calis['month']),
                    'hakedis_tutari': (calis["total_normal_calisma_saati"] * get_object_or_none(calisan_maas_durumlari, id=calis["maas__id"]).maas) + (calis["total_mesai_calisma_saati"] * get_object_or_none(calisan_maas_durumlari, id=calis["maas__id"]).yevmiye),
                    'odenen': odemeler_dict.get((calis['year'], calis['month']), 0),
                    'kalan': ((calis["total_normal_calisma_saati"] * get_object_or_none(calisan_maas_durumlari, id=calis["maas__id"]).maas) + (calis["total_mesai_calisma_saati"] * get_object_or_none(calisan_maas_durumlari, id=calis["maas__id"]).yevmiye)) - odemeler_dict.get((calis['year'], calis['month']), 0),
                    'bodro': "",  # Bodro ile ilgili ek bir işlem yapılacaksa buraya eklenir.
                } for calis in calismalar
            ]
        }
        
        #print(personel_detayi)
        return JsonResponse(personel_detayi)


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

        return redirect("main:ana_sayfa")

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
        try:
            lock_status = LockScreenStatus.objects.get(user=request.user)
            lock_status.is_locked=False
            lock_status.save()
        except :
            # Kullanıcının LockScreenStatus objesi henüz oluşturulmamışsa, oluşturun.
            lock_status = LockScreenStatus.objects.create(user=request.user, is_locked=False)

        return redirect("main:ana_sayfa")
    return render(request,"account/login.html",context)
@login_required
def logoutUser(request):

    try:
        lock_status = LockScreenStatus.objects.get(user=request.user)
        lock_status.is_locked=False
        lock_status.save()
    except LockScreenStatus.DoesNotExist:
        # Kullanıcının LockScreenStatus objesi henüz oluşturulmamışsa, oluşturun.
        lock_status = LockScreenStatus.objects.create(user=request.user, is_locked=False)
    logout(request)
    messages.success(request,"Başarıyla Çıkış Yaptınız")
    return redirect("users:yonlendir")
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
    print(profile)
    return render(request,"account/kullanicilar.html",content)
#kullanıcılar

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
        return redirect("users:kullanicilarim")


def kullanici_silme(request):
    if request.POST:
        buttonIdInput = request.POST.get("buttonId")
        CustomUser.objects.filter(id = buttonIdInput).update(is_active = False,kullanici_silme_bilgisi  = True)
    return redirect("users:kullanicilarim")

def kullanici_bilgileri_duzenle(request):
    if request.POST:
        if request.user.is_superuser:
            pass
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
                    personel_dosyalari.objects.create(dosyalari=images,kullanici = get_object_or_404(CustomUser,id = buttonId))  # Urun_resimleri modeline resimleri kaydet
            if izinler:
                bagli_kullanicilar.objects.create(izinler = get_object_or_404(personel_izinleri,id = izinler),kullanicilar = get_object_or_404(CustomUser, id = buttonId))
        return redirect("users:kullanicilarim")

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
        lock_status = LockScreenStatus.objects.create(user=request.user, is_locked=True)

    if request.method == 'POST':
        password = request.POST.get('userpassword')
        user = authenticate(request, username=request.user.username, password=password)

        if user is not None:
            # Parola doğru, kullanıcıyı kilidi aç
            lock_status.is_locked = False
            lock_status.save()
            return redirect('/')   # Yönlendireceğiniz sayfayı belirtin
        else:
            # Parola doğru değilse hata mesajını gösterin
            error_message = "Parola yanlış. Tekrar deneyin."
            return render(request, 'account/lock_screen.html', {'error_message': error_message})

    return render(request, 'account/lock_screen.html')
#lockscreen
from django.core.files.storage import FileSystemStorage

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
        CustomUser.objects.filter(id = request.user.id).update(
            username = email_bilgisi,email = email_bilgisi,
            description = aciklama, last_name = adi_soyadi,
            telefon_numarasi = telefon_numarasi,adrrsi = adres
        )
        if profile:
            u = CustomUser.objects.get(id = request.user.id)
            u.image = profile
            u.save()

        if background:
            u = CustomUser.objects.get(id = request.user.id)
            u.background_image = background
            u.save()
        return redirect("users:profile_edit_kismi")
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
    return redirect("users:logout")



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
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            kullanici = request.user
        content["departmanlar"] = calisanlar_kategorisi.objects.filter(kategori_kime_ait = kullanici)
        content["pozisyonlari"] = calisanlar_pozisyonu.objects.filter(kategori_kime_ait = kullanici)
        content["personeller"] = calisanlar.objects.filter(status = "0",calisan_kime_ait = kullanici)
    return render(request,"personel/personeller.html",content)
def personeller_ekle(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
        if a:
            if a.izinler.personeller_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
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
        currency = request.POST.get("currency")
        belgeler = request.POST.getlist("belgeler")
        documents = request.FILES.getlist("documents")
        for i in range(50):
            print(belgeler,documents)
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
            bilgi = calisanlar.objects.create(calisan_kime_ait = kullanici,calisan_kategori = get_object_or_none(calisanlar_kategorisi , id =department),
            calisan_pozisyonu = get_object_or_none(calisanlar_pozisyonu , id =position),uyrugu  = nationality,pasaport_numarasi = passportNo,
            isim = firstName+str(i),soyisim = lastName,profile = profilePicture,dogum_tarihi =dogum_tarihi,telefon_numarasi = phoneNumber  )
            calisan_maas_durumlari.objects.create(calisan = get_object_or_none(calisanlar,id =bilgi.id ),maas = dailyWage,
            yevmiye = hourlyWage,durum =salaryType,para_birimi = currency )
    return redirect("user:personeller_sayfasi")
def personeller_sil(request):
    pass
def personelleri_düzenle(request):
    pass

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
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
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
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                kullanici = request.user
        calisanlar_pozisyonu.objects.create(kategori_kime_ait =kullanici,kategori_isimi = pozsiyon )
        
    return redirect("users:personeller_kategori_sayfalari")   
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
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                kullanici = request.user
        calisanlar_pozisyonu.objects.filter(kategori_kime_ait =kullanici,id = pozsiyon ).delete()
        
    return redirect("users:personeller_kategori_sayfalari")   
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
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                kullanici = request.user
        calisanlar_pozisyonu.objects.filter(kategori_kime_ait =kullanici,id =buton ).update(kategori_isimi = pozsiyon )
        
    return redirect("users:personeller_kategori_sayfalari")

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
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
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
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                kullanici = request.user
        calisanlar_kategorisi.objects.create(kategori_kime_ait =kullanici,kategori_isimi = pozsiyon )
        
    return redirect("users:personeller_depertman_sayfalari")   
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
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                kullanici = request.user
        calisanlar_kategorisi.objects.filter(kategori_kime_ait =kullanici,id = pozsiyon ).delete()
        
    return redirect("users:personeller_depertman_sayfalari")   
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
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                kullanici = request.user
        calisanlar_kategorisi.objects.filter(kategori_kime_ait =kullanici,id =buton ).update(kategori_isimi = pozsiyon )
        
    return redirect("users:personeller_depertman_sayfalari")
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
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            kullanici = request.user
        person = calisanlar.objects.filter(status = "0",calisan_kime_ait = kullanici)
        if request.GET:
            month_filter = request.GET.get("monthFilter")
            jobTypeFilter = request.GET.get("jobTypeFilter")
            personelID = request.GET.get("personelID")
            days_in_month = 0
            days_list =[]
            if month_filter:
                year, month = map(int, month_filter.split('-'))  # Yıl ve ayı alıyoruz
                _, num_days = calendar.monthrange(year, month)   # O ayın gün sayısını buluyoruz
                days_list = [day for day in range(1, num_days + 1)] 
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
                    calisanlar_calismalari.objects.create(calisan = get_object_or_none(calisanlar,id =person_id )
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
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.blog_olusturma:
                    kullanici = request.user.kullanicilar_db
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        elif super_admin_kontrolu(request):
            return redirect("/")
        else:
            kullanici = request.user
        year, month = map(int, maas_ayi.split('-'))
    
        # Ayın ilk günü ile Date nesnesini oluştur
        date_obj = datetime(year, month, 1)
        if odeme_turu:
            calisanlar_calismalari_odemeleri.objects.create(
                calisan = get_object_or_none(calisanlar,id =users_id,calisan_kime_ait =  kullanici),
                tutar = tutar,kur = kur,tarihi = date_obj,odeme_tarihi = odeme_tarihi,
                odeme_turu = True,aciklama = aciklama,dosya = file
            )
        else:
            calisanlar_calismalari_odemeleri.objects.create(
                calisan = get_object_or_none(calisanlar,id =users_id,calisan_kime_ait =  kullanici),
                tutar = tutar,kur = kur,tarihi = date_obj,odeme_tarihi = odeme_tarihi,
                odeme_turu = False,aciklama = aciklama,dosya = file
            )
    return redirect("users:personeller_sayfasi")

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
    return render(request, 'weather.html', {'weather_data': weather_data, 'ip_info': ip_info,"icon":icon})
