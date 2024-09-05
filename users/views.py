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
    pass
def personeller_ekle(request):
    pass
def personeller_sil(request):
    pass
def personelleri_düzenle(request):
    pass

#
def personeller_kategori_ekle(request):
    pass
def personeller_kategori_sil(request):
    pass
def personelleri_kategori_düzenle(request):
    pass
