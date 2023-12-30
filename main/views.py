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
    return sozluk

#superadmin Kontrol
def yetki(request):
    if request.user.is_superuser:
        
        pass
    else:

        return redirect("main:yetkisiz")
# Create your views here,
# Anasayfa
def homepage(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect("/users/login/")

    return render(request,"index.html",sozluk_yapisi())

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
#Proje Ekleme
def proje_ekle(request):
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

def santiye_ekleme_sahibi(request):
    if request.POST:
        if super_admin_kontrolu(request):
            kullanici = request.POST.get("kullanici")
            link = "/addsitesuperadmin/"+kullanici
            return redirect(link)
        
        projetipi = request.POST.get("projetipi")
        proje_adi = request.POST.get("yetkili_adi")
        katsayisi = int(request.POST.get("katsayisi"))
        blogsayisi = int(request.POST.get("blogsayisi"))
        blogadi = request.POST.get("blogadi")
        a = santiye.objects.create(proje_ait_bilgisi = request.user,proje_tipi = get_object_or_404(proje_tipi,id = projetipi),
                               proje_adi = proje_adi,kat_sayisi = katsayisi,
                               blog_sayisi = blogsayisi,blog_adi = blogadi
                               )
        for i in range(1,blogsayisi+1):
            bloglar.objects.create(proje_ait_bilgisi =request.user,
                                   proje_santiye_Ait = get_object_or_404(santiye,id = a.id),
                                    blog_adi = blogadi,blog_numarasi = i )
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
        katsayisi = int(request.POST.get("katsayisi"))
        blogsayisi = int(request.POST.get("blogsayisi"))
        blogadi = request.POST.get("blogadi")
        a = santiye.objects.create(proje_ait_bilgisi = get_object_or_404(CustomUser,id = id),proje_tipi = get_object_or_404(proje_tipi,id = projetipi),
                               proje_adi = proje_adi,kat_sayisi = katsayisi,
                               blog_sayisi = blogsayisi,blog_adi = blogadi
                               )
        for i in range(1,blogsayisi+1):
            bloglar.objects.create(proje_ait_bilgisi =get_object_or_404(CustomUser,id = id),
                                   proje_santiye_Ait = get_object_or_404(santiye,id = a.id),
                                    blog_adi = blogadi,blog_numarasi = i )
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
    if request.user.is_authenticated:
        if request.user.is_superuser:
            kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
            
        else:
            content["santiyeler_bilgileri"] = santiye.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)
            profile = santiye_kalemleri.objects.filter(proje_santiye_Ait = get_object_or_404(santiye,id = id) ,silinme_bilgisi = False,proje_ait_bilgisi = request.user)
            if request.GET.get("search"):
                search = request.GET.get("search")
                if search:
                    profile = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).filter(Q(last_name__icontains = search)|Q(first_name__icontains = search)|Q(email__icontains = search) ).order_by("-id")
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
    return render(request,"santiye_yonetimi\santiye_kalemleri.html",content)

def santiyeye_kalem_ekle(request):
    if request.POST:
        if request.user.is_superuser:
            kullanici = request.POST.get("kullanici")
            z = "/addbuldingsiteadmin/"+kullanici
            return redirect("")
        else:
            projetipi = request.POST.get("projetipi")
            yetkili_adi = request.POST.get("yetkili_adi")
            santiye_agirligi = request.POST.get("katsayisi")
            finansal_agirlik = request.POST.get("blogsayisi")
            santiye_kalemleri.objects.create(
                proje_ait_bilgisi = request.user,
                proje_santiye_Ait = get_object_or_404(santiye,id =projetipi ),
                kalem_adi = yetkili_adi,santiye_agirligi = santiye_agirligi,
                santiye_finansal_agirligi = finansal_agirlik
            )
    return redirect("main:santiye_projesi_ekle_")

def santiye_kalem_ekle_admin(redirect,id):
    return 0
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
            profile = projeler.objects.filter(Q(proje_ait_bilgisi = request.user) & Q(Proje_tipi_adi__icontains = search)& Q(silinme_bilgisi = False))
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
            buttonIdInput = request.POST.get("buttonIdInput")
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
            buttonIdInput = request.POST.get("buttonIdInput")
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


