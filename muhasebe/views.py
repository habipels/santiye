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
from main.views import super_admin_kontrolu,dil_bilgisi,translate,sozluk_yapisi,yetki
from .models import *
# Create your views here.
def kasa_viev(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Kasa.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =Kasa.objects.filter(Q(kasa_kart_ait_bilgisi__first_name__icontains = search)|Q(kasa_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = Kasa.objects.filter(Q(kasa_kart_ait_bilgisi = request.user) & Q(kasa_adi__icontains = search)& Q(silinme_bilgisi = False))
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
    return render(request,"muhasebe_page/muhasebe_index.html",content)

#kasa ekleme
def kasa_ekle(request):
    if request.POST:
        #yetkili_adi
        if super_admin_kontrolu(request):
            kullanici_bilgisi  = request.POST.get("kullanici")
            kasa_Adi   = request.POST.get("kasaadi")
            bakiye = request.POST.get("bakiye")
            konumu = request.POST.get("konumu")
            Kasa.objects.create(kasa_kart_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) 
                                ,kasa_adi = kasa_Adi,aciklama = konumu,bakiye = bakiye
                                
                                )
        else:
            kasa_Adi   = request.POST.get("kasaadi")
            bakiye = request.POST.get("bakiye")
            konumu = request.POST.get("konumu")
            Kasa.objects.create(kasa_kart_ait_bilgisi = request.user
                ,kasa_adi = kasa_Adi,aciklama = konumu,bakiye = bakiye)
    
    return redirect("accounting:kasa")

#kasa silme
def kasa_sil(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        Kasa.objects.filter(id = id).update(silinme_bilgisi = True)
    else:
        Kasa.objects.filter(kasa_kart_ait_bilgisi = request.user,id = id).update(silinme_bilgisi = True)
    return redirect("accounting:kasa")


#kasa düzenle
def kasa_duzenle(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        silinmedurumu = request.POST.get("silinmedurumu")
        konumu = request.POST.get("konumu")
        if silinmedurumu == "1":
            silinmedurumu = False
            Kasa.objects.filter(id = id).update(kasa_kart_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,kasa_adi = proje_tip_adi,aciklama = konumu,silinme_bilgisi = silinmedurumu)
        elif silinmedurumu == "2":
            silinmedurumu = True
            Kasa.objects.filter(id = id).update(kasa_kart_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,kasa_adi = proje_tip_adi,aciklama = konumu,silinme_bilgisi = silinmedurumu)
        else:
            Kasa.objects.filter(id = id).update(kasa_kart_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,kasa_adi = proje_tip_adi,aciklama = konumu)
    else:
        proje_tip_adi   = request.POST.get("yetkili_adi")
        konumu = request.POST.get("konumu")
        Kasa.objects.filter(kasa_kart_ait_bilgisi = request.user,id = id).update(kasa_adi = proje_tip_adi                                                                 
                ,aciklama = konumu)
    return redirect("accounting:kasa")

#Gelir Kategorisi
def gelir_kategorisi_tipleri(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =gelir_kategorisi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = gelir_kategorisi.objects.filter(silinme_bilgisi = False,gelir_kategoris_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =gelir_kategorisi.objects.filter(Q(gelir_kategoris_ait_bilgisi__last_name__icontains = search)|Q(gelir_kategori_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = gelir_kategorisi.objects.filter(Q(gelir_kategoris_ait_bilgisi = request.user) & Q(gelir_kategori_adi__icontains = search)& Q(silinme_bilgisi = False))
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
    return render(request,"muhasebe_page/gelir_kategorisi.html",content)
#gelir KAtegorisi Ekleme
def gelir_kategorisi_ekleme(request):
    if request.POST:
        #yetkili_adi
        if super_admin_kontrolu(request):
            kullanici_bilgisi  = request.POST.get("kullanici")
            proje_tip_adi   = request.POST.get("yetkili_adi")
            aciklama = request.POST.get("aciklama")
            renk = request.POST.get("renk")
            
            gelir_kategorisi.objects.create(gelir_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gelir_kategori_adi = proje_tip_adi,gelir_kategorisi_renk = renk,aciklama = aciklama)
        else:
            proje_tip_adi   = request.POST.get("yetkili_adi")
            aciklama = request.POST.get("aciklama")
            renk = request.POST.get("renk")
            gelir_kategorisi.objects.create(gelir_kategoris_ait_bilgisi = request.user,gelir_kategori_adi = proje_tip_adi,gelir_kategorisi_renk = renk,aciklama = aciklama)
    return redirect("accounting:gelir_kategorisi_tipleri")

#gelir Kategorisi Silme

def gelir_kategoisi_sil(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        gelir_kategorisi.objects.filter(id = id).update(silinme_bilgisi = True)
    else:
        gelir_kategorisi.objects.filter(gelir_kategoris_ait_bilgisi = request.user,id = id).update(silinme_bilgisi = True)
    return redirect("accounting:gelir_kategorisi_tipleri")
#gelir düzenleme
def gelir_kategorisi_duzenle(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        aciklama = request.POST.get("aciklama")
        renk = request.POST.get("renk")
        silinmedurumu = request.POST.get("silinmedurumu")
        if silinmedurumu == "1":
            silinmedurumu = False
            gelir_kategorisi.objects.filter(id = id).update(gelir_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gelir_kategori_adi = proje_tip_adi,gelir_kategorisi_renk = renk,aciklama = aciklama,silinme_bilgisi = silinmedurumu)
        elif silinmedurumu == "2":
            silinmedurumu = True
            gelir_kategorisi.objects.filter(id = id).update(gelir_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gelir_kategori_adi = proje_tip_adi,gelir_kategorisi_renk = renk,aciklama = aciklama,silinme_bilgisi = silinmedurumu)
        else:
            gelir_kategorisi.objects.filter(id = id).update(gelir_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gelir_kategori_adi = proje_tip_adi,gelir_kategorisi_renk = renk,aciklama = aciklama)
    else:
        proje_tip_adi   = request.POST.get("yetkili_adi")
        aciklama = request.POST.get("aciklama")
        renk = request.POST.get("renk")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        gelir_kategorisi.objects.filter(gelir_kategoris_ait_bilgisi = request.user,id = id).update(gelir_kategori_adi = proje_tip_adi,gelir_kategorisi_renk = renk,aciklama = aciklama)
    return redirect("accounting:gelir_kategorisi_tipleri")


#gider_kategorisi.html

#gider Kategorisi
def gider_kategorisi_tipleri(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =gider_kategorisi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = gider_kategorisi.objects.filter(silinme_bilgisi = False,gider_kategoris_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =gider_kategorisi.objects.filter(Q(gider_kategoris_ait_bilgisi__last_name__icontains = search)|Q(gider_kategori_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = gider_kategorisi.objects.filter(Q(gider_kategoris_ait_bilgisi = request.user) & Q(gider_kategori_adi__icontains = search)& Q(silinme_bilgisi = False))
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
    return render(request,"muhasebe_page/gider_kategorisi.html",content)
#gider KAtegorisi Ekleme
def gider_kategorisi_ekleme(request):
    if request.POST:
        #yetkili_adi
        if super_admin_kontrolu(request):
            kullanici_bilgisi  = request.POST.get("kullanici")
            proje_tip_adi   = request.POST.get("yetkili_adi")
            aciklama = request.POST.get("aciklama")
            renk = request.POST.get("renk")
            
            gider_kategorisi.objects.create(gider_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gider_kategori_adi = proje_tip_adi,gider_kategorisi_renk = renk,aciklama = aciklama)
        else:
            proje_tip_adi   = request.POST.get("yetkili_adi")
            aciklama = request.POST.get("aciklama")
            renk = request.POST.get("renk")
            gider_kategorisi.objects.create(gider_kategoris_ait_bilgisi = request.user,gider_kategori_adi = proje_tip_adi,gider_kategorisi_renk = renk,aciklama = aciklama)
    return redirect("accounting:gider_kategorisi_tipleri")

#gider Kategorisi Silme

def gider_kategoisi_sil(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        gider_kategorisi.objects.filter(id = id).update(silinme_bilgisi = True)
    else:
        gider_kategorisi.objects.filter(gider_kategoris_ait_bilgisi = request.user,id = id).update(silinme_bilgisi = True)
    return redirect("accounting:gider_kategorisi_tipleri")
#gider düzenleme
def gider_kategorisi_duzenle(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        aciklama = request.POST.get("aciklama")
        renk = request.POST.get("renk")
        silinmedurumu = request.POST.get("silinmedurumu")
        if silinmedurumu == "1":
            silinmedurumu = False
            gider_kategorisi.objects.filter(id = id).update(gider_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gider_kategori_adi = proje_tip_adi,gider_kategorisi_renk = renk,aciklama = aciklama,silinme_bilgisi = silinmedurumu)
        elif silinmedurumu == "2":
            silinmedurumu = True
            gider_kategorisi.objects.filter(id = id).update(gider_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gider_kategori_adi = proje_tip_adi,gider_kategorisi_renk = renk,aciklama = aciklama,silinme_bilgisi = silinmedurumu)
        else:
            gider_kategorisi.objects.filter(id = id).update(gider_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gider_kategori_adi = proje_tip_adi,gider_kategorisi_renk = renk,aciklama = aciklama)
    else:
        proje_tip_adi   = request.POST.get("yetkili_adi")
        aciklama = request.POST.get("aciklama")
        renk = request.POST.get("renk")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        gider_kategorisi.objects.filter(gider_kategoris_ait_bilgisi = request.user,id = id).update(gider_kategori_adi = proje_tip_adi,gider_kategorisi_renk = renk,aciklama = aciklama)
    return redirect("accounting:gider_kategorisi_tipleri")


#cari işlemler
def cari_viev(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =cari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = cari.objects.filter(silinme_bilgisi = False,cari_kart_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =cari.objects.filter(Q(cari_kart_ait_bilgisi__first_name__icontains = search)|Q(cari_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = cari.objects.filter(Q(cari_kart_ait_bilgisi = request.user) & Q(cari_adi__icontains = search)& Q(silinme_bilgisi = False))
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
    return render(request,"muhasebe_page/cari.html",content)

#cari ekleme
def cari_ekle(request):
    if request.POST:
        #yetkili_adi
        if super_admin_kontrolu(request):
            kullanici_bilgisi  = request.POST.get("kullanici")
            cari_Adi   = request.POST.get("cariadi")
            bakiye = request.POST.get("bakiye")
            konumu = request.POST.get("konumu")
            cari.objects.create(cari_kart_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) 
                                ,cari_adi = cari_Adi,aciklama = konumu,telefon_numarasi = bakiye
                                
                                )
        else:
            cari_Adi   = request.POST.get("cariadi")
            bakiye = request.POST.get("bakiye")
            konumu = request.POST.get("konumu")
            cari.objects.create(cari_kart_ait_bilgisi = request.user
                ,cari_adi = cari_Adi,aciklama = konumu,telefon_numarasi = bakiye)
    
    return redirect("accounting:cari")

#cari silme
def cari_sil(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        cari.objects.filter(id = id).update(silinme_bilgisi = True)
    else:
        cari.objects.filter(cari_kart_ait_bilgisi = request.user,id = id).update(silinme_bilgisi = True)
    return redirect("accounting:cari")


#cari düzenle
def cari_duzenle(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        silinmedurumu = request.POST.get("silinmedurumu")
        konumu = request.POST.get("konumu")
        if silinmedurumu == "1":
            silinmedurumu = False
            cari.objects.filter(id = id).update(cari_kart_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,cari_adi = proje_tip_adi,aciklama = konumu,silinme_bilgisi = silinmedurumu)
        elif silinmedurumu == "2":
            silinmedurumu = True
            cari.objects.filter(id = id).update(cari_kart_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,cari_adi = proje_tip_adi,aciklama = konumu,silinme_bilgisi = silinmedurumu)
        else:
            cari.objects.filter(id = id).update(cari_kart_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,cari_adi = proje_tip_adi,aciklama = konumu)
    else:
        proje_tip_adi   = request.POST.get("yetkili_adi")
        konumu = request.POST.get("konumu")
        cari.objects.filter(cari_kart_ait_bilgisi = request.user,id = id).update(cari_adi = proje_tip_adi                                                                 
                ,aciklama = konumu)
    return redirect("accounting:cari")
#cari işlemler

#gelir Etiketleri
def gelir_etiketi_tipleri(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =gelir_etiketi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = gelir_etiketi.objects.filter(silinme_bilgisi = False,gelir_kategoris_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =gelir_etiketi.objects.filter(Q(gelir_kategoris_ait_bilgisi__last_name__icontains = search)|Q(gelir_kategori_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = gelir_etiketi.objects.filter(Q(gelir_kategoris_ait_bilgisi = request.user) & Q(gelir_kategori_adi__icontains = search)& Q(silinme_bilgisi = False))
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
    return render(request,"muhasebe_page/gelir_etiketi.html",content)
def gelir_etiketi_ekleme(request):
    if request.POST:
        #yetkili_adi
        if super_admin_kontrolu(request):
            kullanici_bilgisi  = request.POST.get("kullanici")
            proje_tip_adi   = request.POST.get("yetkili_adi")
            
            gelir_etiketi.objects.create(gelir_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gelir_etiketi_adi = proje_tip_adi)
        else:
            proje_tip_adi   = request.POST.get("yetkili_adi")
            gelir_etiketi.objects.create(gelir_kategoris_ait_bilgisi = request.user,gelir_etiketi_adi = proje_tip_adi)
    return redirect("accounting:gelir_etiketi_tipleri")

def gelir_etiketi_sil(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        gelir_etiketi.objects.filter(id = id).update(silinme_bilgisi = True)
    else:
        gelir_etiketi.objects.filter(gelir_kategoris_ait_bilgisi = request.user,id = id).update(silinme_bilgisi = True)
    return redirect("accounting:gelir_etiketi_tipleri")
def gelir_etiketi_duzenle(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        
        silinmedurumu = request.POST.get("silinmedurumu")
        if silinmedurumu == "1":
            silinmedurumu = False
            gelir_etiketi.objects.filter(id = id).update(gelir_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gelir_etiketi_adi = proje_tip_adi,silinme_bilgisi = silinmedurumu)
        elif silinmedurumu == "2":
            silinmedurumu = True
            gelir_etiketi.objects.filter(id = id).update(gelir_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gelir_etiketi_adi = proje_tip_adi,silinme_bilgisi = silinmedurumu)
        else:
           gelir_etiketi.objects.filter(id = id).update(gelir_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gelir_etiketi_adi = proje_tip_adi) 
    else:
        proje_tip_adi   = request.POST.get("yetkili_adi")
        
        proje_tip_adi   = request.POST.get("yetkili_adi")
        gelir_etiketi.objects.filter(gelir_kategoris_ait_bilgisi = request.user,id = id).update(gelir_etiketi_adi = proje_tip_adi)
    return redirect("accounting:gelir_etiketi_tipleri")
#gelir Etiketleri

#gider etiketi


#gider Etiketleri
def gider_etiketi_tipleri(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =gider_etiketi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = gider_etiketi.objects.filter(silinme_bilgisi = False,gider_kategoris_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =gider_etiketi.objects.filter(Q(gider_kategoris_ait_bilgisi__last_name__icontains = search)|Q(gider_kategori_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = gider_etiketi.objects.filter(Q(gider_kategoris_ait_bilgisi = request.user) & Q(gider_kategori_adi__icontains = search)& Q(silinme_bilgisi = False))
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
    return render(request,"muhasebe_page/gider_etiketi.html",content)
def gider_etiketi_ekleme(request):
    if request.POST:
        #yetkili_adi
        if super_admin_kontrolu(request):
            kullanici_bilgisi  = request.POST.get("kullanici")
            proje_tip_adi   = request.POST.get("yetkili_adi")
            
            gider_etiketi.objects.create(gider_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gider_etiketi_adi = proje_tip_adi)
        else:
            proje_tip_adi   = request.POST.get("yetkili_adi")
            gider_etiketi.objects.create(gider_kategoris_ait_bilgisi = request.user,gider_etiketi_adi = proje_tip_adi)
    return redirect("accounting:gider_etiketi_tipleri")

def gider_etiketi_sil(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        gider_etiketi.objects.filter(id = id).update(silinme_bilgisi = True)
    else:
        gider_etiketi.objects.filter(gider_kategoris_ait_bilgisi = request.user,id = id).update(silinme_bilgisi = True)
    return redirect("accounting:gider_etiketi_tipleri")
def gider_etiketi_duzenle(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        
        silinmedurumu = request.POST.get("silinmedurumu")
        if silinmedurumu == "1":
            silinmedurumu = False
            gider_etiketi.objects.filter(id = id).update(gider_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gider_etiketi_adi = proje_tip_adi,silinme_bilgisi = silinmedurumu)
        elif silinmedurumu == "2":
            silinmedurumu = True
            gider_etiketi.objects.filter(id = id).update(gider_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gider_etiketi_adi = proje_tip_adi,silinme_bilgisi = silinmedurumu)
        else:
            gider_etiketi.objects.filter(id = id).update(gider_kategoris_ait_bilgisi = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,gider_etiketi_adi = proje_tip_adi)
    else:
        proje_tip_adi   = request.POST.get("yetkili_adi")
        
        proje_tip_adi   = request.POST.get("yetkili_adi")
        gider_etiketi.objects.filter(gider_kategoris_ait_bilgisi = request.user,id = id).update(gider_etiketi_adi = proje_tip_adi)
    return redirect("accounting:gider_etiketi_tipleri")
#gider Etiketleri
#gider etiketi

#virman olayları
def virman_yapma(request):
    if request.POST:
        #yetkili_adi
        if super_admin_kontrolu(request):
            kullanici_bilgisi  = request.POST.get("kullanici")
            proje_tip_adi   = request.POST.get("yetkili_adi")
            z = "/accounting/superadmintransfer/"+kullanici_bilgisi
            return redirect(z)
        else:
            gonderen = request.POST.get("gonderen")
            alici = request.POST.get("alici")
            islemtarihi = request.POST.get("islemtarihi")
            tutar = float(str(request.POST.get("tutar")).replace(",","."))
            aciklama = request.POST.get("aciklama")
            virman.objects.create(virman_ait_oldugu = request.user,
                virman_tarihi = islemtarihi,gonderen_kasa = get_object_or_404(Kasa,id = gonderen)
                ,alici_kasa = get_object_or_404(Kasa,id = alici),tutar = tutar,
                aciklama = aciklama
                )
            bakiye_dusme = get_object_or_404(Kasa,id = gonderen).bakiye
            bakiye_yukseltme = get_object_or_404(Kasa,id = alici).bakiye
            bakiye_dusme = bakiye_dusme - float(tutar)
            bakiye_yukseltme = bakiye_yukseltme + float(tutar)
            Kasa.objects.filter(id = gonderen).update(bakiye = bakiye_dusme)
            Kasa.objects.filter(id = alici).update(bakiye = bakiye_yukseltme)

    return redirect("accounting:kasa")


def super_admin_virman(request,id):
    content = sozluk_yapisi()
    content["proje_tipleri"] = proje_tipi.objects.filter(proje_ait_bilgisi =  get_object_or_404(CustomUser,id = id))
    yetki(request)
    profile = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = get_object_or_404(CustomUser,id = id))
    content["santiyeler"] = profile
    if request.POST:    
            gonderen = request.POST.get("gonderen")
            alici = request.POST.get("alici")
            islemtarihi = request.POST.get("islemtarihi")
            tutar = float(str(request.POST.get("tutar")).replace(",","."))
            aciklama = request.POST.get("aciklama")
            virman.objects.create(virman_ait_oldugu = get_object_or_404(CustomUser,id = id),
                virman_tarihi = islemtarihi,gonderen_kasa = get_object_or_404(Kasa,id = gonderen)
                ,alici_kasa = get_object_or_404(Kasa,id = alici),tutar = tutar,
                aciklama = aciklama
                )
            bakiye_dusme = get_object_or_404(Kasa,id = gonderen).bakiye
            bakiye_yukseltme = get_object_or_404(Kasa,id = alici).bakiye
            bakiye_dusme = bakiye_dusme - float(tutar)
            bakiye_yukseltme = bakiye_yukseltme + float(tutar)
            Kasa.objects.filter(id = gonderen).update(bakiye = bakiye_dusme)
            Kasa.objects.filter(id = alici).update(bakiye = bakiye_yukseltme)
            return redirect("accounting:kasa")
    return render(request,"muhasebe_page/super_admin_virman.html",content)


def virman_gondermeler(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =virman.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = virman.objects.filter(silinme_bilgisi = False,virman_ait_oldugu = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =virman.objects.filter(Q(kasa_kart_ait_bilgisi__first_name__icontains = search)|Q(kasa_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = virman.objects.filter(Q(virman_ait_oldugu = request.user) & Q(kasa_adi__icontains = search)& Q(silinme_bilgisi = False))
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
    return render(request,"muhasebe_page/virman_raporu.html",content)
#virman olayları
#ürünler olayları
def urun_viev(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =urunler.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = urunler.objects.filter(silinme_bilgisi = False,urun_ait_oldugu = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =urunler.objects.filter(Q(urun_ait_oldugu__first_name__icontains = search)|Q(urun_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = urunler.objects.filter(Q(urun_ait_oldugu = request.user) & Q(urun_adi__icontains = search)& Q(silinme_bilgisi = False))
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
    return render(request,"muhasebe_page/urunler.html",content)

#Ürün ekleme
def urun_ekle(request):
    if request.POST:
        #yetkili_adi
        if super_admin_kontrolu(request):
            kullanici_bilgisi  = request.POST.get("kullanici")
            kasa_Adi   = request.POST.get("kasaadi")
            bakiye = request.POST.get("bakiye")
            urunler.objects.create(urun_ait_oldugu = get_object_or_404(CustomUser,id = kullanici_bilgisi ) 
                                ,urun_adi = kasa_Adi,urun_fiyati = bakiye
                                
                                )
        else:
            kasa_Adi   = request.POST.get("kasaadi")
            bakiye = request.POST.get("bakiye")
            
            urunler.objects.create(urun_ait_oldugu = request.user
                ,urun_adi = kasa_Adi,urun_fiyati = bakiye)
    
    return redirect("accounting:urun_viev")

#ürün ekle
#ürün_sil
def urun_sil(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("yetkili_adi")
        urunler.objects.filter(id = id).update(silinme_bilgisi = True)
    else:
        urunler.objects.filter(urun_ait_oldugu = request.user,id = id).update(silinme_bilgisi = True)
    return redirect("accounting:urun_viev")


#ürün Sil
 
#ürün Düzenle
#kasa düzenle
def urun_duzenle(request):
    content = {}
    if request.POST:
        id = request.POST.get("buttonId")
    if super_admin_kontrolu(request):
        kullanici_bilgisi  = request.POST.get("kullanici")
        proje_tip_adi   = request.POST.get("kasaadi")
        silinmedurumu = request.POST.get("silinmedurumu")
        bakiye = request.POST.get("bakiye")
        if silinmedurumu == "1":
            silinmedurumu = False
            urunler.objects.filter(id = id).update(urun_ait_oldugu = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,urun_adi = proje_tip_adi,urun_fiyati = bakiye,silinme_bilgisi = silinmedurumu)
        elif silinmedurumu == "2":
            silinmedurumu = True
            urunler.objects.filter(id = id).update(urun_ait_oldugu = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,urun_adi = proje_tip_adi,urun_fiyati = bakiye,silinme_bilgisi = silinmedurumu)
        else:
            urunler.objects.filter(id = id).update(urun_ait_oldugu = get_object_or_404(CustomUser,id = kullanici_bilgisi ) ,urun_adi = proje_tip_adi,urun_fiyati = bakiye)
    else:
        proje_tip_adi   = request.POST.get("kasaadi")
        bakiye = request.POST.get("bakiye")
        urunler.objects.filter(urun_ait_oldugu = request.user,id = id).update(urun_adi = proje_tip_adi                                                                 
                ,urun_fiyati = bakiye)
    return redirect("accounting:urun_viev")

#ürün Düzenle
#ürünler olayları

#Gelirler Sayfası
def gelirler_sayfasi(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Kasa.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =Kasa.objects.filter(Q(kasa_kart_ait_bilgisi__first_name__icontains = search)|Q(kasa_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = Kasa.objects.filter(Q(kasa_kart_ait_bilgisi = request.user) & Q(kasa_adi__icontains = search)& Q(silinme_bilgisi = False))
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
    return render(request,"muhasebe_page/gelir.html",content)
def gelir_ekle(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Kasa.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        urunler_bilgisi = urunler.objects.filter(urun_ait_oldugu = request.user)
        cari_bilgileri = cari.objects.filter(cari_kart_ait_bilgisi = request.user)
        kategori_bilgisi = gelir_kategorisi.objects.filter(gelir_kategoris_ait_bilgisi = request.user)
        etiketler = gelir_etiketi.objects.filter(gelir_kategoris_ait_bilgisi = request.user)
    content["gelir_kategoerisi"] = kategori_bilgisi
    content["gelir_etiketi"] = etiketler
    content["kasa"] = profile
    content["urunler"]  = urunler_bilgisi
    content["cari_bilgileri"] = cari_bilgileri
    return render(request,"muhasebe_page/gelir_faturasi.html",content)
def denme(request):
    return render(request,"a.html")
from django.http import JsonResponse
def search(request):
    term = request.GET.get('term', '')
    user = request.user
    results = urunler.objects.filter(urun_adi__icontains=term, urun_ait_oldugu=user)
    suggestions = [{'label': result.urun_adi, 'value': result.urun_fiyati} for result in results]
    print("oldu mu yav")
    return JsonResponse(suggestions, safe=False)
def cariler_bilgisi(request):
    term = request.GET.get('term', '')
    user = request.user
    results = cari.objects.filter(cari_adi__icontains=term, cari_kart_ait_bilgisi=user)
    suggestions = [{'label': result.cari_adi, 'value':result.aciklama} for result in results]
    return JsonResponse(suggestions, safe=False)
def gelir_faturasi_kaydet(request):
    if request.POST:
        musteri_bilgisi  = request.POST.get("musteri_bilgisi")
        daterange = request.POST.get("daterange")
        gelir_kategorisi = request.POST.get("gelir_kategorisi")
        cari_aciklma = request.POST.get("cari_aciklma")
        etiketler = request.POST.getlist("etiketler")
        faturano = request.POST.get("faturano")
        urunadi = request.POST.getlist("urunadi")
        miktari = request.POST.getlist("miktari")
        bfiyatInput = request.POST.getlist("bfiyatInput")
        indirim = request.POST.getlist("indirim")
        aciklama = request.POST.getlist("aciklama")
        
    return redirect("accounting:gelirler_sayfasi")

#Gelirler Sayfası

#Gider Sayfası
def giderler_sayfasi(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Kasa.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =Kasa.objects.filter(Q(kasa_kart_ait_bilgisi__first_name__icontains = search)|Q(kasa_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = Kasa.objects.filter(Q(kasa_kart_ait_bilgisi = request.user) & Q(kasa_adi__icontains = search)& Q(silinme_bilgisi = False))
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
    return render(request,"muhasebe_page/gelir.html",content)
#Gider Sayfası