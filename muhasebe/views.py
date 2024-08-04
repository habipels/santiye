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
def get_object_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except :
        return None
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
def a_kasa_viev(request,hash):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
        profile = Kasa.objects.filter(kasa_kart_ait_bilgisi =  users)
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
def kasa_tekli(request,id):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Kasa.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        k_gonder = get_object_or_404(Kasa,id = id)
    else:
        profile = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        k_gonder = get_object_or_404(Kasa,id = id)
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
    content["kasabilgiis_getirme"] = k_gonder
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"muhasebe_page/kasa_hareketleri.html",content)

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
def gelir_kategorisi_tipleri_2(request,hash):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
        #profile = Kasa.objects.filter(kasa_kart_ait_bilgisi =  get_object_or_404(CustomUser,id = post_id))
        profile = gelir_kategorisi.objects.filter(silinme_bilgisi = False,gelir_kategoris_ait_bilgisi = users)
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
#gider Kategorisi
def gider_kategorisi_tipleri_2(request,hash):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
        profile = gider_kategorisi.objects.filter(silinme_bilgisi = False,gider_kategoris_ait_bilgisi = users)
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
    return render(request,"muhasebe_page/cariler.html",content)
def cari_viev_2(request,hash):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
        profile = cari.objects.filter(silinme_bilgisi = False,cari_kart_ait_bilgisi = users)
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
    return render(request,"muhasebe_page/cariler.html",content)
#cari işlemler
#cari işlemler
def cari_views_details(request,id):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =cari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        k_gonder = get_object_or_404(cari,id = id)
    else:
        profile = cari.objects.filter(silinme_bilgisi = False,cari_kart_ait_bilgisi = request.user)
        k_gonder = get_object_or_404(cari,id = id)
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
    content["cari"] = k_gonder
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"muhasebe_page/cari_detay.html",content)

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
def gelir_etiketi_tipleri_2(request,hash):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
        #profile =gelir_etiketi.objects.all()
        profile = gelir_etiketi.objects.filter(silinme_bilgisi = False,gelir_kategoris_ait_bilgisi =users)
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
#

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
def gider_etiketi_tipleri_2(request,hash):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
        #profile =gelir_etiketi.objects.all()
        profile = gider_etiketi.objects.filter(silinme_bilgisi = False,gider_kategoris_ait_bilgisi = users)
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
#
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
        content["kasalar"]  = Kasa.objects.filter(silinme_bilgisi = False)
    else:
        profile = virman.objects.filter(silinme_bilgisi = False,virman_ait_oldugu = request.user)
        content["kasalar"]  = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
    if request.GET:
        gonderen_kasa = request.GET.get("gonderen_kasa")
        alici_kasa = request.GET.get("alici_kasa")
        tarih = request.GET.get("tarih")
        if super_admin_kontrolu(request):
            profile =virman.objects.filter()
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = virman.objects.filter(Q(virman_ait_oldugu = request.user) & Q(silinme_bilgisi = False))
        if gonderen_kasa:
            profile = profile.filter(gonderen_kasa= get_object_or_none(Kasa,id =gonderen_kasa ) )
        if alici_kasa:
            profile = profile.filter(alici_kasa=  get_object_or_none(Kasa,id =alici_kasa ))
        if tarih :
            profile = profile.filter(virman_tarihi = tarih)
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

def virman_gondermeler_2(request,hash):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
        profile = virman.objects.filter(silinme_bilgisi = False,virman_ait_oldugu = users)
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        content["kasalar"]  = Kasa.objects.filter(silinme_bilgisi = False)
    else:
        profile = virman.objects.filter(silinme_bilgisi = False,virman_ait_oldugu = request.user)
        content["kasalar"]  = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
    if request.GET:
        gonderen_kasa = request.GET.get("gonderen_kasa")
        alici_kasa = request.GET.get("alici_kasa")
        tarih = request.GET.get("tarih")
        if super_admin_kontrolu(request):
            d = decode_id(hash)
            content["hashler"] = hash
            users = get_object_or_404(CustomUser,id = d)
            content["hash_bilgi"] = users
            profile = virman.objects.filter(silinme_bilgisi = False,virman_ait_oldugu = users)
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            profile = virman.objects.filter(Q(virman_ait_oldugu = request.user) & Q(silinme_bilgisi = False))
        if gonderen_kasa:
            profile = profile.filter(gonderen_kasa= get_object_or_none(Kasa,id =gonderen_kasa ) )
        if alici_kasa:
            profile = profile.filter(alici_kasa=  get_object_or_none(Kasa,id =alici_kasa ))
        if tarih :
            profile = profile.filter(virman_tarihi = tarih)
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
def urun_viev_2(request,hash):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
        profile = urunler.objects.filter(silinme_bilgisi = False,urun_ait_oldugu = users)
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
        profile =Gelir_Bilgisi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-fatura_tarihi")
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
                profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)| Q(aciklama__icontains = search) | Q(gelir_kategorisi__gelir_kategori_adi__icontains = search))
                content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        if tarih :
            profile = profile.filter(Q(fatura_tarihi__lte  = tarih) & Q(vade_tarihi__gte  = tarih) )
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
def gelirler_sayfasi_2(request,hash):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
        profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = users).order_by("-fatura_tarihi")
        content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = users)
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-fatura_tarihi")
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
                profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)| Q(aciklama__icontains = search) | Q(gelir_kategorisi__gelir_kategori_adi__icontains = search))
                content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        if tarih :
            profile = profile.filter(Q(fatura_tarihi__lte  = tarih) & Q(vade_tarihi__gte  = tarih) )
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
#
def gelir_ekle(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Kasa.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        urunler_bilgisi = ""
        cari_bilgileri = ""
        kategori_bilgisi = ""
        etiketler =  ""
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
#
def gelir_ekle_2(request,hash):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        profile = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = users)
        urunler_bilgisi = urunler.objects.filter(urun_ait_oldugu = users)
        cari_bilgileri = cari.objects.filter(cari_kart_ait_bilgisi = users)
        kategori_bilgisi = gelir_kategorisi.objects.filter(gelir_kategoris_ait_bilgisi = users)
        etiketler = gelir_etiketi.objects.filter(gelir_kategoris_ait_bilgisi = users)
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

def gelir_duzenle(request ,id):
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
        gelir_bilgisi_ver =  get_object_or_none(Gelir_Bilgisi,id = id)
        urunleri = gelir_urun_bilgisi.objects.filter(gider_bilgis = gelir_bilgisi_ver)
    content["gelir_kategoerisi"] = kategori_bilgisi
    content["gelir_etiketi"] = etiketler
    content["kasa"] = profile
    content["urunler"]  = urunler_bilgisi
    content["cari_bilgileri"] = cari_bilgileri
    content["bilgi"] = gelir_bilgisi_ver
    content["urunler"] = urunleri
    return render(request,"muhasebe_page/gelir_faturasi_duzeltme.html",content)
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
def search_2(request,hash):
    term = request.GET.get('term', '')
    d = decode_id(hash)
    user = get_object_or_404(CustomUser,id = d)
    #user = request.user
    results = urunler.objects.filter(urun_adi__icontains=term, urun_ait_oldugu=user)
    suggestions = [{'label': result.urun_adi, 'value': result.urun_fiyati} for result in results]
    print("oldu mu yav")
    return JsonResponse(suggestions, safe=False)
def cariler_bilgisi_2(request,hash):
    term = request.GET.get('term', '')
    d = decode_id(hash)
    user = get_object_or_404(CustomUser,id = d)
    results = cari.objects.filter(cari_adi__icontains=term, cari_kart_ait_bilgisi=user)
    suggestions = [{'label': result.cari_adi, 'value':result.aciklama} for result in results]
    return JsonResponse(suggestions, safe=False)

def gelir_faturasi_kaydet(request):
    if request.POST:
        musteri_bilgisi  = request.POST.get("musteri_bilgisi")
        daterange = request.POST.get("daterange")
        gelir_kategorisii = request.POST.get("gelir_kategorisi")
        cari_aciklma = request.POST.get("cari_aciklma")
        etiketler = request.POST.getlist("etiketler")
        faturano = request.POST.get("faturano")
        urunadi = request.POST.getlist("urunadi")
        miktari = request.POST.getlist("miktari")
        bfiyatInput = request.POST.getlist("bfiyatInput")
        indirim = request.POST.getlist("indirim")
        aciklama = request.POST.getlist("aciklama")
        doviz_kuru = request.POST.get("doviz_kuru")

        cari_bilgisi = get_object_or_none(cari,cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = request.user)
        if cari_bilgisi:
            date_range_parts = daterange.split(' - ')

            # Tarihleri ayrı ayrı alma ve uygun formata dönüştürme
            fatura_tarihi_str, vade_tarihi_str = date_range_parts
            fatura_tarihi = datetime.strptime(fatura_tarihi_str, '%m/%d/%Y')
            vade_tarihi = datetime.strptime(vade_tarihi_str, '%m/%d/%Y')

            new_project =Gelir_Bilgisi.objects.create(gelir_kime_ait_oldugu = request.user,
            cari_bilgisi = get_object_or_none(cari,cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = request.user),
            fatura_tarihi=fatura_tarihi,vade_tarihi=vade_tarihi,fatura_no = faturano,
            gelir_kategorisi = get_object_or_none( gelir_kategorisi,id =gelir_kategorisii),doviz = doviz_kuru,aciklama = cari_aciklma
                                         )
            new_project.save()
            gelir_etiketi_sec = []
            for i in etiketler:
                gelir_etiketi_sec.append(gelir_etiketi.objects.get(id=int(i)))
            new_project.gelir_etiketi_sec.add(*gelir_etiketi_sec)
            for i in range(0,len(urunadi)):
                if urunadi[i] != "" and miktari[i] != "" and bfiyatInput[i] != "":
                    urun = get_object_or_none(urunler, urun_ait_oldugu=request.user,urun_adi = urunadi[i])
                    if urun:
                        if indirim[i] == "":
                            a = 0
                        else:
                            a = indirim[i]
                        gelir_urun_bilgisi_bi = gelir_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  request.user,urun_bilgisi = get_object_or_none(urunler, urun_ait_oldugu=request.user,urun_adi = urunadi[i]),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(a),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gelir_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
                    else:
                        urun = urunler.objects.create(urun_ait_oldugu=request.user,urun_adi = urunadi[i],
                                                      urun_fiyati = float(bfiyatInput[i]))
                        gelir_urun_bilgisi_bi = gelir_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  request.user,urun_bilgisi = get_object_or_none(urunler,id = urun.id),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gelir_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )

        else:
            cari_bilgisi = cari.objects.create(cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = request.user,aciklama = cari_aciklma)
            date_range_parts = daterange.split(' - ')

            # Tarihleri ayrı ayrı alma ve uygun formata dönüştürme
            fatura_tarihi_str, vade_tarihi_str = date_range_parts
            fatura_tarihi = datetime.strptime(fatura_tarihi_str, '%m/%d/%Y')
            vade_tarihi = datetime.strptime(vade_tarihi_str, '%m/%d/%Y')

            new_project =Gelir_Bilgisi.objects.create(gelir_kime_ait_oldugu = request.user,
            cari_bilgisi = get_object_or_none(cari,id = cari_bilgisi.id),
            fatura_tarihi=fatura_tarihi,vade_tarihi=vade_tarihi,fatura_no = faturano,
            gelir_kategorisi = get_object_or_none( gelir_kategorisi,id =gelir_kategorisii),doviz = doviz_kuru,aciklama = cari_aciklma
            )
            new_project.save()
            gelir_etiketi_sec = []
            for i in etiketler:
                gelir_etiketi_sec.append(gelir_etiketi.objects.get(id=int(i)))
            new_project.gelir_etiketi_sec.add(*gelir_etiketi_sec)
            for i in range(0,len(urunadi)):
                if urunadi[i] != "" and miktari[i] != "" and bfiyatInput[i] != "":
                    urun = get_object_or_none(urunler, urun_ait_oldugu=request.user,urun_adi = urunadi[i])
                    if urun:
                        gelir_urun_bilgisi_bi = gelir_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  request.user,urun_bilgisi = get_object_or_none(urunler, urun_ait_oldugu=request.user,urun_adi = urunadi[i]),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gelir_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
                    else:
                        urun = urunler.objects.create(urun_ait_oldugu=request.user,urun_adi = urunadi[i],
                                                      urun_fiyati = float(bfiyatInput[i]))
                        gelir_urun_bilgisi_bi = gelir_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  request.user,urun_bilgisi = get_object_or_none(urunler,id = urun.id),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gelir_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
        gelir_qr.objects.create(gelir_kime_ait_oldugu = get_object_or_none(Gelir_Bilgisi,id = new_project.id))
    return redirect("accounting:gelirler_sayfasi")

def gelir_faturasi_kaydet_2(request,hash):
    if request.POST:
        musteri_bilgisi  = request.POST.get("musteri_bilgisi")
        daterange = request.POST.get("daterange")
        gelir_kategorisii = request.POST.get("gelir_kategorisi")
        cari_aciklma = request.POST.get("cari_aciklma")
        etiketler = request.POST.getlist("etiketler")
        faturano = request.POST.get("faturano")
        urunadi = request.POST.getlist("urunadi")
        miktari = request.POST.getlist("miktari")
        bfiyatInput = request.POST.getlist("bfiyatInput")
        indirim = request.POST.getlist("indirim")
        aciklama = request.POST.getlist("aciklama")
        doviz_kuru = request.POST.get("doviz_kuru")

        cari_bilgisi = get_object_or_none(cari,cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = request.user)
        if cari_bilgisi:
            date_range_parts = daterange.split(' - ')

            # Tarihleri ayrı ayrı alma ve uygun formata dönüştürme
            fatura_tarihi_str, vade_tarihi_str = date_range_parts
            fatura_tarihi = datetime.strptime(fatura_tarihi_str, '%m/%d/%Y')
            vade_tarihi = datetime.strptime(vade_tarihi_str, '%m/%d/%Y')

            new_project =Gelir_Bilgisi.objects.create(gelir_kime_ait_oldugu = request.user,
            cari_bilgisi = get_object_or_none(cari,cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = request.user),
            fatura_tarihi=fatura_tarihi,vade_tarihi=vade_tarihi,fatura_no = faturano,
            gelir_kategorisi = get_object_or_none( gelir_kategorisi,id =gelir_kategorisii),doviz = doviz_kuru,aciklama = cari_aciklma
                                         )
            new_project.save()
            gelir_etiketi_sec = []
            for i in etiketler:
                gelir_etiketi_sec.append(gelir_etiketi.objects.get(id=int(i)))
            new_project.gelir_etiketi_sec.add(*gelir_etiketi_sec)
            for i in range(0,len(urunadi)):
                if urunadi[i] != "" and miktari[i] != "" and bfiyatInput[i] != "":
                    urun = get_object_or_none(urunler, urun_ait_oldugu=request.user,urun_adi = urunadi[i])
                    if urun:
                        if indirim[i] == "":
                            a = 0
                        else:
                            a = indirim[i]
                        gelir_urun_bilgisi_bi = gelir_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  request.user,urun_bilgisi = get_object_or_none(urunler, urun_ait_oldugu=request.user,urun_adi = urunadi[i]),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(a),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gelir_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
                    else:
                        urun = urunler.objects.create(urun_ait_oldugu=request.user,urun_adi = urunadi[i],
                                                      urun_fiyati = float(bfiyatInput[i]))
                        gelir_urun_bilgisi_bi = gelir_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  request.user,urun_bilgisi = get_object_or_none(urunler,id = urun.id),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gelir_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )

        else:
            cari_bilgisi = cari.objects.create(cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = request.user,aciklama = cari_aciklma)
            date_range_parts = daterange.split(' - ')

            # Tarihleri ayrı ayrı alma ve uygun formata dönüştürme
            fatura_tarihi_str, vade_tarihi_str = date_range_parts
            fatura_tarihi = datetime.strptime(fatura_tarihi_str, '%m/%d/%Y')
            vade_tarihi = datetime.strptime(vade_tarihi_str, '%m/%d/%Y')

            new_project =Gelir_Bilgisi.objects.create(gelir_kime_ait_oldugu = request.user,
            cari_bilgisi = get_object_or_none(cari,id = cari_bilgisi.id),
            fatura_tarihi=fatura_tarihi,vade_tarihi=vade_tarihi,fatura_no = faturano,
            gelir_kategorisi = get_object_or_none( gelir_kategorisi,id =gelir_kategorisii),doviz = doviz_kuru,aciklama = cari_aciklma
            )
            new_project.save()
            gelir_etiketi_sec = []
            for i in etiketler:
                gelir_etiketi_sec.append(gelir_etiketi.objects.get(id=int(i)))
            new_project.gelir_etiketi_sec.add(*gelir_etiketi_sec)
            for i in range(0,len(urunadi)):
                if urunadi[i] != "" and miktari[i] != "" and bfiyatInput[i] != "":
                    urun = get_object_or_none(urunler, urun_ait_oldugu=request.user,urun_adi = urunadi[i])
                    if urun:
                        gelir_urun_bilgisi_bi = gelir_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  request.user,urun_bilgisi = get_object_or_none(urunler, urun_ait_oldugu=request.user,urun_adi = urunadi[i]),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gelir_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
                    else:
                        urun = urunler.objects.create(urun_ait_oldugu=request.user,urun_adi = urunadi[i],
                                                      urun_fiyati = float(bfiyatInput[i]))
                        gelir_urun_bilgisi_bi = gelir_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  request.user,urun_bilgisi = get_object_or_none(urunler,id = urun.id),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gelir_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
        gelir_qr.objects.create(gelir_kime_ait_oldugu = get_object_or_none(Gelir_Bilgisi,id = new_project.id))
    return redirect("accounting:gelirler_sayfasi")


def gelir_odemesi_ekle(request):

    if request.POST:
        faturabilgisi = request.POST.get("faturabilgisi")
        odemeturu = request.POST.get("odemeturu")
        kasabilgisi = request.POST.get("kasabilgisi")
        islemtarihi = request.POST.get("islemtarihi")
        islemtutari = request.POST.get("islemtutari")
        makbuznumarasi = request.POST.get("makbuznumarasi")
        aciklama_bilgisi = request.POST.get("aciklama_bilgisi")
        dosya = request.FILES.get("dosya")
        Gelir_odemesi.objects.create(
            gelir_kime_ait_oldugu =get_object_or_none(Gelir_Bilgisi, id = faturabilgisi),
            gelir_turu = odemeturu,kasa_bilgisi = get_object_or_none(Kasa,id = kasabilgisi),
            tutar  =islemtutari,tarihi = islemtarihi,gelir_makbuzu = dosya,
            makbuz_no = makbuznumarasi,aciklama = aciklama_bilgisi
        )
    return redirect("accounting:gelirler_sayfasi")
def gider_duzenle(request ,id):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Kasa.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        urunler_bilgisi = urunler.objects.filter(urun_ait_oldugu = request.user)
        cari_bilgileri = cari.objects.filter(cari_kart_ait_bilgisi = request.user)
        kategori_bilgisi = gider_kategorisi.objects.filter(gider_kategoris_ait_bilgisi = request.user)
        etiketler = gider_etiketi.objects.filter(gider_kategoris_ait_bilgisi = request.user)
        gelir_bilgisi_ver =  get_object_or_none(Gider_Bilgisi,id = id)
        urunleri = gider_urun_bilgisi.objects.filter(gider_bilgis = gelir_bilgisi_ver)
        content["gelir_kategoerisi"] = kategori_bilgisi
        content["gelir_etiketi"] = etiketler
        content["kasa"] = profile
        content["urunler"]  = urunler_bilgisi
        content["cari_bilgileri"] = cari_bilgileri
        content["bilgi"] = gelir_bilgisi_ver
        content["urunler"] = urunleri
    return render(request,"muhasebe_page/gider_faturasi_duzeltme.html",content)
#Gelirler Sayfası
def makbuz_sil(request):
    if request.POST:
        gelir_gider = request.POST.get("makbuz")
        makbuz_bilgisi = request.POST.get("makbuzidsi")
        if gelir_gider == "0":
            Gelir_odemesi.objects.filter(id = makbuz_bilgisi).delete()
            return redirect("accounting:gelirler_sayfasi")
        elif gelir_gider == "1":
            Gider_odemesi.objects.filter(id = makbuz_bilgisi).delete()

            return redirect("accounting:giderler_sayfasi")
#Gider Sayfası
def giderler_sayfasi(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Gider_Bilgisi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-fatura_tarihi")
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
                profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)|  Q(aciklama__icontains = search) | Q(gelir_kategorisi__gider_kategori_adi__icontains = search))
                content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        if tarih :
            profile = profile.filter(Q(fatura_tarihi__lte  = tarih) & Q(vade_tarihi__gte  = tarih) )
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
    return render(request,"muhasebe_page/deneme_gider.html",content)
#
def giderler_sayfasi_borc(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Gider_Bilgisi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
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
        profile = sonuc
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
                profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)|  Q(aciklama__icontains = search) | Q(gelir_kategorisi__gider_kategori_adi__icontains = search))
                content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        if tarih :
            profile = profile.filter(Q(fatura_tarihi__lte  = tarih) & Q(vade_tarihi__gte  = tarih) )
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
    return render(request,"muhasebe_page/deneme_gider.html",content)
#
def giderler_sayfasi_borc_2(request,hash):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
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
        profile = sonuc
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
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
        profile = sonuc
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
                profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)|  Q(aciklama__icontains = search) | Q(gelir_kategorisi__gider_kategori_adi__icontains = search))
                content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        if tarih :
            profile = profile.filter(Q(fatura_tarihi__lte  = tarih) & Q(vade_tarihi__gte  = tarih) )
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
    return render(request,"muhasebe_page/deneme_gider.html",content)
#
def giderler_sayfasi_2(request,hash):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
        profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = users).order_by("-fatura_tarihi")
        content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = users)
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-fatura_tarihi")
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
                profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)|  Q(aciklama__icontains = search) | Q(gelir_kategorisi__gider_kategori_adi__icontains = search))
                content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        if tarih :
            profile = profile.filter(Q(fatura_tarihi__lte  = tarih) & Q(vade_tarihi__gte  = tarih) )
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
    return render(request,"muhasebe_page/deneme_gider.html",content)

def gider_ekle(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Kasa.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        urunler_bilgisi = ""
        cari_bilgileri = ""
        kategori_bilgisi =""
        etiketler =  ""

    else:
        profile = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        urunler_bilgisi = urunler.objects.filter(urun_ait_oldugu = request.user)
        cari_bilgileri = cari.objects.filter(cari_kart_ait_bilgisi = request.user)
        kategori_bilgisi = gider_kategorisi.objects.filter(gider_kategoris_ait_bilgisi = request.user)
        etiketler = gider_etiketi.objects.filter(gider_kategoris_ait_bilgisi = request.user)
    content["gelir_kategoerisi"] = kategori_bilgisi
    content["gelir_etiketi"] = etiketler
    content["kasa"] = profile
    content["urunler"]  = urunler_bilgisi
    content["cari_bilgileri"] = cari_bilgileri
    return render(request,"muhasebe_page/gider_faturasi.html",content)
#
def gider_ekle_2(request,hash):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        d = decode_id(hash)
        content["hashler"] = hash
        users = get_object_or_404(CustomUser,id = d)
        content["hash_bilgi"] = users
        profile = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = users)
        urunler_bilgisi = urunler.objects.filter(urun_ait_oldugu = users)
        cari_bilgileri = cari.objects.filter(cari_kart_ait_bilgisi = users)
        kategori_bilgisi = gider_kategorisi.objects.filter(gider_kategoris_ait_bilgisi = users)
        etiketler = gider_etiketi.objects.filter(gider_kategoris_ait_bilgisi = users)
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        

    else:
        profile = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        urunler_bilgisi = urunler.objects.filter(urun_ait_oldugu = request.user)
        cari_bilgileri = cari.objects.filter(cari_kart_ait_bilgisi = request.user)
        kategori_bilgisi = gider_kategorisi.objects.filter(gider_kategoris_ait_bilgisi = request.user)
        etiketler = gider_etiketi.objects.filter(gider_kategoris_ait_bilgisi = request.user)
    content["gelir_kategoerisi"] = kategori_bilgisi
    content["gelir_etiketi"] = etiketler
    content["kasa"] = profile
    content["urunler"]  = urunler_bilgisi
    content["cari_bilgileri"] = cari_bilgileri
    return render(request,"muhasebe_page/gider_faturasi.html",content)
#
def gider_faturasi_kaydet(request):
    print("kayıt")
    if request.POST:
        musteri_bilgisi  = request.POST.get("musteri_bilgisi")
        daterange = request.POST.get("daterange")
        gelir_kategorisii = request.POST.get("gelir_kategorisi")
        cari_aciklma = request.POST.get("cari_aciklma")
        etiketler = request.POST.getlist("etiketler")
        faturano = request.POST.get("faturano")
        urunadi = request.POST.getlist("urunadi")
        miktari = request.POST.getlist("miktari")
        bfiyatInput = request.POST.getlist("bfiyatInput")
        indirim = request.POST.getlist("indirim")
        aciklama = request.POST.getlist("aciklama")
        aciklama_id = request.POST.getlist('aciklama_id')
        doviz_kuru = request.POST.get("doviz_kuru")
        cari_bilgisi = get_object_or_none(cari,cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = request.user)
        if cari_bilgisi:
            date_range_parts = daterange.split(' - ')

            # Tarihleri ayrı ayrı alma ve uygun formata dönüştürme
            fatura_tarihi_str, vade_tarihi_str = date_range_parts
            fatura_tarihi = datetime.strptime(fatura_tarihi_str, '%m/%d/%Y')
            vade_tarihi = datetime.strptime(vade_tarihi_str, '%m/%d/%Y')

            new_project =Gider_Bilgisi.objects.create(gelir_kime_ait_oldugu = request.user,
            cari_bilgisi = get_object_or_none(cari,cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = request.user),
            fatura_tarihi=fatura_tarihi,vade_tarihi=vade_tarihi,fatura_no = faturano,
            gelir_kategorisi = get_object_or_none( gelir_kategorisi,id =gelir_kategorisii),doviz = doviz_kuru,aciklama = cari_aciklma
                                         )
            new_project.save()
            gelir_etiketi_sec = []
            for i in etiketler:
                gelir_etiketi_sec.append(gider_etiketi.objects.get(id=int(i)))
            new_project.gelir_etiketi_sec.add(*gelir_etiketi_sec)
            for i in range(0,len(urunadi)):
                if urunadi[i] != "" and miktari[i] != "" and bfiyatInput[i] != "":
                    urun = get_object_or_none(urunler, urun_ait_oldugu=request.user,urun_adi = urunadi[i])
                    if urun:
                        gelir_urun_bilgisi_bi = gider_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  request.user,urun_bilgisi = get_object_or_none(urunler, urun_ait_oldugu=request.user,urun_adi = urunadi[i]),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gider_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
                    else:
                        urun = urunler.objects.create(urun_ait_oldugu=request.user,urun_adi = urunadi[i],
                                                      urun_fiyati = float(bfiyatInput[i]))
                        gelir_urun_bilgisi_bi = gider_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  request.user,urun_bilgisi = get_object_or_none(urunler,id = urun.id),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gider_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )

        else:
            cari_bilgisi = cari.objects.create(cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = request.user,aciklama = cari_aciklma)
            date_range_parts = daterange.split(' - ')

            # Tarihleri ayrı ayrı alma ve uygun formata dönüştürme
            fatura_tarihi_str, vade_tarihi_str = date_range_parts
            fatura_tarihi = datetime.strptime(fatura_tarihi_str, '%m/%d/%Y')
            vade_tarihi = datetime.strptime(vade_tarihi_str, '%m/%d/%Y')

            new_project =Gider_Bilgisi.objects.create(gelir_kime_ait_oldugu = request.user,
            cari_bilgisi = get_object_or_none(cari,id = cari_bilgisi.id),
            fatura_tarihi=fatura_tarihi,vade_tarihi=vade_tarihi,fatura_no = faturano,
            gelir_kategorisi = get_object_or_none( gelir_kategorisi,id =gelir_kategorisii),doviz = doviz_kuru,aciklama = cari_aciklma
                                         )
            new_project.save()
            gelir_etiketi_sec = []
            for i in etiketler:
                gelir_etiketi_sec.append(gider_etiketi.objects.get(id=int(i)))
            new_project.gelir_etiketi_sec.add(*gelir_etiketi_sec)
            for i in range(0,len(urunadi)):
                if urunadi[i] != "" and miktari[i] != "" and bfiyatInput[i] != "":
                    urun = get_object_or_none(urunler, urun_ait_oldugu=request.user,urun_adi = urunadi[i])
                    if urun:
                        gelir_urun_bilgisi_bi = gider_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  request.user,urun_bilgisi = get_object_or_none(urunler, urun_ait_oldugu=request.user,urun_adi = urunadi[i]),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gider_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
                    else:
                        urun = urunler.objects.create(urun_ait_oldugu=request.user,urun_adi = urunadi[i],
                                                      urun_fiyati = float(bfiyatInput[i]))
                        gelir_urun_bilgisi_bi = gider_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  request.user,urun_bilgisi = get_object_or_none(urunler,id = urun.id),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gider_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
        gider_qr.objects.create(gelir_kime_ait_oldugu = get_object_or_none(Gider_Bilgisi,id = new_project.id))
        print(aciklama_id,"gelen id")

    return redirect("accounting:giderler_sayfasi")
def gider_faturasi_kaydet_2(request,hash):
    print("kayıt")
    content = {}
    d = decode_id(hash)
    content["hashler"] = hash
    users = get_object_or_404(CustomUser,id = d)
    content["hash_bilgi"] = users
    if request.POST:
        musteri_bilgisi  = request.POST.get("musteri_bilgisi")
        daterange = request.POST.get("daterange")
        gelir_kategorisii = request.POST.get("gelir_kategorisi")
        cari_aciklma = request.POST.get("cari_aciklma")
        etiketler = request.POST.getlist("etiketler")
        faturano = request.POST.get("faturano")
        urunadi = request.POST.getlist("urunadi")
        miktari = request.POST.getlist("miktari")
        bfiyatInput = request.POST.getlist("bfiyatInput")
        indirim = request.POST.getlist("indirim")
        aciklama = request.POST.getlist("aciklama")
        aciklama_id = request.POST.getlist('aciklama_id')
        doviz_kuru = request.POST.get("doviz_kuru")
        cari_bilgisi = get_object_or_none(cari,cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = users)
        if cari_bilgisi:
            date_range_parts = daterange.split(' - ')

            # Tarihleri ayrı ayrı alma ve uygun formata dönüştürme
            fatura_tarihi_str, vade_tarihi_str = date_range_parts
            fatura_tarihi = datetime.strptime(fatura_tarihi_str, '%m/%d/%Y')
            vade_tarihi = datetime.strptime(vade_tarihi_str, '%m/%d/%Y')

            new_project =Gider_Bilgisi.objects.create(gelir_kime_ait_oldugu = users,
            cari_bilgisi = get_object_or_none(cari,cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = users),
            fatura_tarihi=fatura_tarihi,vade_tarihi=vade_tarihi,fatura_no = faturano,
            gelir_kategorisi = get_object_or_none( gelir_kategorisi,id =gelir_kategorisii),doviz = doviz_kuru,aciklama = cari_aciklma
                                         )
            new_project.save()
            gelir_etiketi_sec = []
            for i in etiketler:
                gelir_etiketi_sec.append(gider_etiketi.objects.get(id=int(i)))
            new_project.gelir_etiketi_sec.add(*gelir_etiketi_sec)
            for i in range(0,len(urunadi)):
                if urunadi[i] != "" and miktari[i] != "" and bfiyatInput[i] != "":
                    urun = get_object_or_none(urunler, urun_ait_oldugu=users,urun_adi = urunadi[i])
                    if urun:
                        gelir_urun_bilgisi_bi = gider_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  users,urun_bilgisi = get_object_or_none(urunler, urun_ait_oldugu=users,urun_adi = urunadi[i]),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gider_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
                    else:
                        urun = urunler.objects.create(urun_ait_oldugu=users,urun_adi = urunadi[i],
                                                      urun_fiyati = float(bfiyatInput[i]))
                        gelir_urun_bilgisi_bi = gider_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  users,urun_bilgisi = get_object_or_none(urunler,id = urun.id),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gider_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )

        else:
            cari_bilgisi = cari.objects.create(cari_adi = musteri_bilgisi,cari_kart_ait_bilgisi = users,aciklama = cari_aciklma)
            date_range_parts = daterange.split(' - ')

            # Tarihleri ayrı ayrı alma ve uygun formata dönüştürme
            fatura_tarihi_str, vade_tarihi_str = date_range_parts
            fatura_tarihi = datetime.strptime(fatura_tarihi_str, '%m/%d/%Y')
            vade_tarihi = datetime.strptime(vade_tarihi_str, '%m/%d/%Y')

            new_project =Gider_Bilgisi.objects.create(gelir_kime_ait_oldugu = users,
            cari_bilgisi = get_object_or_none(cari,id = cari_bilgisi.id),
            fatura_tarihi=fatura_tarihi,vade_tarihi=vade_tarihi,fatura_no = faturano,
            gelir_kategorisi = get_object_or_none( gelir_kategorisi,id =gelir_kategorisii),doviz = doviz_kuru,aciklama = cari_aciklma
                                         )
            new_project.save()
            gelir_etiketi_sec = []
            for i in etiketler:
                gelir_etiketi_sec.append(gider_etiketi.objects.get(id=int(i)))
            new_project.gelir_etiketi_sec.add(*gelir_etiketi_sec)
            for i in range(0,len(urunadi)):
                if urunadi[i] != "" and miktari[i] != "" and bfiyatInput[i] != "":
                    urun = get_object_or_none(urunler, urun_ait_oldugu=users,urun_adi = urunadi[i])
                    if urun:
                        gelir_urun_bilgisi_bi = gider_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  users,urun_bilgisi = get_object_or_none(urunler, urun_ait_oldugu=users,urun_adi = urunadi[i]),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gider_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
                    else:
                        urun = urunler.objects.create(urun_ait_oldugu=users,urun_adi = urunadi[i],
                                                      urun_fiyati = float(bfiyatInput[i]))
                        gelir_urun_bilgisi_bi = gider_urun_bilgisi.objects.create(
                            urun_ait_oldugu =  users,urun_bilgisi = get_object_or_none(urunler,id = urun.id),
                            urun_fiyati = bfiyatInput[i],urun_indirimi = float(indirim[i]),urun_adeti = int(miktari[i]),
                            gider_bilgis =  get_object_or_none(Gider_Bilgisi,id = new_project.id),
                            aciklama = aciklama[i]
                        )
        gider_qr.objects.create(gelir_kime_ait_oldugu = get_object_or_none(Gider_Bilgisi,id = new_project.id))
        print(aciklama_id,"gelen id")

    return redirect("accounting:giderler_sayfasi")
#
def gider_odemesi_ekle(request):

    if request.POST:
        faturabilgisi = request.POST.get("faturabilgisi")
        odemeturu = request.POST.get("odemeturu")
        kasabilgisi = request.POST.get("kasabilgisi")
        islemtarihi = request.POST.get("islemtarihi")
        islemtutari = request.POST.get("islemtutari")
        makbuznumarasi = request.POST.get("makbuznumarasi")
        aciklama_bilgisi = request.POST.get("aciklama_bilgisi")
        dosya = request.FILES.get("dosya")
        Gider_odemesi.objects.create(
            gelir_kime_ait_oldugu =get_object_or_none(Gider_Bilgisi, id = faturabilgisi),
            gelir_turu = odemeturu,kasa_bilgisi = get_object_or_none(Kasa,id = kasabilgisi),
            tutar  =islemtutari,tarihi = islemtarihi,gelir_makbuzu = dosya,
            makbuz_no = makbuznumarasi,aciklama = aciklama_bilgisi
        )
    return redirect("accounting:giderler_sayfasi")


def fatura_sil(request):
    if request.POST:
        gelir_gider = request.POST.get("gelir_gider")
        id_bilgisi  = request.POST.get("idbilgisicek")
        if gelir_gider == "0":
            Gelir_Bilgisi.objects.filter(id = id_bilgisi).update(silinme_bilgisi = True)
            Gelir_odemesi.objects.filter(gelir_kime_ait_oldugu =get_object_or_404(Gelir_Bilgisi,id =id_bilgisi )).update(silinme_bilgisi = True)
            return redirect("accounting:gelirler_sayfasi")

        elif gelir_gider == "1":
            Gider_Bilgisi.objects.filter(id = id_bilgisi).update(silinme_bilgisi = True)
            Gider_odemesi.objects.filter(gelir_kime_ait_oldugu=get_object_or_404(Gider_Bilgisi,id =id_bilgisi )).update(silinme_bilgisi = True)
            return redirect("accounting:giderler_sayfasi")
#Gider Sayfası
from django.shortcuts import get_object_or_404

def gelir_gider_duzelt(request):
    if request.POST:
        bilgi = request.POST.get("bilgi")
        degisen = request.POST.get("degisen")
        musteri_bilgisi = request.POST.get("musteri_bilgisi")
        daterange = request.POST.get("daterange")
        gelir_kategorisii = request.POST.get("gelir_kategorisi")
        cari_aciklma = request.POST.get("cari_aciklma")
        etiketler = request.POST.getlist("etiketler")
        faturano = request.POST.get("faturano")
        urunadi = request.POST.getlist("urunadi")
        miktari = request.POST.getlist("miktari")
        bfiyatInput = request.POST.getlist("bfiyatInput")
        indirim = request.POST.getlist("indirim")
        aciklama = request.POST.getlist("aciklama")
        doviz_kuru = request.POST.get("doviz_kuru")

        if bilgi == "0":
            gelir_bilgisi = get_object_or_404(Gelir_Bilgisi, id=degisen)
            gelir_bilgisi.gelir_kime_ait_oldugu = request.user
            cari_bilgisi = get_object_or_none(cari, cari_adi=musteri_bilgisi, cari_kart_ait_bilgisi=request.user)
            if not cari_bilgisi:
                cari_bilgisi = cari.objects.create(cari_adi=musteri_bilgisi, cari_kart_ait_bilgisi=request.user, aciklama=cari_aciklma)
            date_range_parts = daterange.split(' - ')
            fatura_tarihi_str, vade_tarihi_str = date_range_parts
            fatura_tarihi = datetime.strptime(fatura_tarihi_str, '%m/%d/%Y')
            vade_tarihi = datetime.strptime(vade_tarihi_str, '%m/%d/%Y')

            gelir_bilgisi.fatura_tarihi = fatura_tarihi
            gelir_bilgisi.vade_tarihi = vade_tarihi
            gelir_bilgisi.fatura_no = faturano
            gelir_bilgisi.gelir_kategorisi = get_object_or_none(gelir_kategorisi, id=gelir_kategorisii)
            gelir_bilgisi.save()

            gelir_etiketi_sec = gelir_etiketi.objects.filter(id__in=etiketler)
            gelir_bilgisi.gelir_etiketi_sec.set(gelir_etiketi_sec)
            gelir_urun_bilgisi.objects.filter(gider_bilgis = get_object_or_404(Gelir_Bilgisi, id=degisen)).delete()
            for i in range(len(urunadi)):
                if urunadi[i] and miktari[i] and bfiyatInput[i]:
                    urun = get_object_or_none(urunler, urun_ait_oldugu=request.user, urun_adi=urunadi[i])
                    if not urun:
                        urun = urunler.objects.create(urun_ait_oldugu=request.user, urun_adi=urunadi[i], urun_fiyati=float(bfiyatInput[i]))

                    gelir_urun_bilgisi.objects.create(
                        urun_ait_oldugu=request.user,
                        urun_bilgisi=urun,
                        urun_fiyati=bfiyatInput[i],
                        urun_indirimi=float(indirim[i]),
                        urun_adeti=int(miktari[i]),
                        gider_bilgis=gelir_bilgisi,
                        aciklama=aciklama[i]
                    )

            return redirect("accounting:gelirler_sayfasi")

        elif bilgi == "1":
            gider_bilgisi = get_object_or_404(Gider_Bilgisi, id=degisen)
            gider_bilgisi.gelir_kime_ait_oldugu = request.user
            cari_bilgisi = get_object_or_none(cari, cari_adi=musteri_bilgisi, cari_kart_ait_bilgisi=request.user)
            if not cari_bilgisi:
                cari_bilgisi = cari.objects.create(cari_adi=musteri_bilgisi, cari_kart_ait_bilgisi=request.user, aciklama=cari_aciklma)
            date_range_parts = daterange.split(' - ')
            fatura_tarihi_str, vade_tarihi_str = date_range_parts
            fatura_tarihi = datetime.strptime(fatura_tarihi_str, '%m/%d/%Y')
            vade_tarihi = datetime.strptime(vade_tarihi_str, '%m/%d/%Y')

            gider_bilgisi.fatura_tarihi = fatura_tarihi
            gider_bilgisi.vade_tarihi = vade_tarihi
            gider_bilgisi.fatura_no = faturano
            gider_bilgisi.gelir_kategorisi = get_object_or_none(gider_kategorisi, id=gelir_kategorisii)
            gider_bilgisi.doviz = doviz_kuru
            gider_bilgisi.save()

            gelir_etiketi_sec = gider_etiketi.objects.filter(id__in=etiketler)
            gider_bilgisi.gelir_etiketi_sec.set(gelir_etiketi_sec)
            gider_urun_bilgisi.objects.filter(gider_bilgis = get_object_or_404(Gider_Bilgisi, id=degisen)).delete()
            for i in range(len(urunadi)):
                if urunadi[i] and miktari[i] and bfiyatInput[i]:
                    urun = get_object_or_none(urunler, urun_ait_oldugu=request.user, urun_adi=urunadi[i])
                    if not urun:
                        urun = urunler.objects.create(urun_ait_oldugu=request.user, urun_adi=urunadi[i], urun_fiyati=float(bfiyatInput[i]))

                    gider_urun_bilgisi.objects.create(
                        urun_ait_oldugu=request.user,
                        urun_bilgisi=urun,
                        urun_fiyati=bfiyatInput[i],
                        urun_indirimi=float(indirim[i]),
                        urun_adeti=int(miktari[i]),
                        gider_bilgis=gider_bilgisi,
                        aciklama=aciklama[i]
                    )

            return redirect("accounting:giderler_sayfasi")

    return redirect("accounting:giderler_sayfasi")

def gider_gelir_ekleme(request):
    user = request.user
    tur = request.POST.get("tur")
    adi = request.POST.get("adi")
    aciklama= request.POST.get("aciklama")
    renk = request.POST.get("renk")
    print("selam")
    if tur == "0":
        gelir_kategorisi.objects.create(
            gelir_kategoris_ait_bilgisi = user,
            gelir_kategori_adi = adi,
            gelir_kategorisi_renk = renk,
            aciklama = aciklama
        )
        return redirect("accounting:gelir_ekle")
    elif tur == "1":
        gider_kategorisi.objects.create(
            gider_kategoris_ait_bilgisi = user,
            gider_kategori_adi = adi,
            gider_kategorisi_renk = renk,
            aciklama = aciklama
        )
        return redirect("accounting:gider_ekle")
def gider_gelir_ekleme_2(request,hash):
    d = decode_id(hash)
    user = get_object_or_404(CustomUser,id = d)
    tur = request.POST.get("tur")
    adi = request.POST.get("adi")
    aciklama= request.POST.get("aciklama")
    renk = request.POST.get("renk")
    print("selam")
    if tur == "0":
        gelir_kategorisi.objects.create(
            gelir_kategoris_ait_bilgisi = user,
            gelir_kategori_adi = adi,
            gelir_kategorisi_renk = renk,
            aciklama = aciklama
        )
        return redirect("accounting:gelir_ekle")
    elif tur == "1":
        gider_kategorisi.objects.create(
            gider_kategoris_ait_bilgisi = user,
            gider_kategori_adi = adi,
            gider_kategorisi_renk = renk,
            aciklama = aciklama
        )
        return redirect("accounting:gider_ekle")

from django.utils import timezone
def gider_gelir_etiketekleme(request):
    print("sela")
    user = request.user
    tur = request.POST.get("tur2")
    adi = request.POST.get("adi2")

    if tur == "0":
        gelir_etiketi.objects.create(
            gelir_kategoris_ait_bilgisi = user,
            gelir_etiketi_adi = adi,kayit_tarihi = timezone.now()
        )
        return redirect("accounting:gelir_ekle")
    elif tur == "1":
        gider_etiketi.objects.create(
            gider_kategoris_ait_bilgisi = user,
            gider_etiketi_adi = adi,kayit_tarihi = timezone.now()
        )
        return redirect("accounting:gider_ekle")

def gider_gelir_etiketekleme_2(request,hash):
    d = decode_id(hash)
    user = get_object_or_404(CustomUser,id = d)
    user = request.user
    tur = request.POST.get("tur2")
    adi = request.POST.get("adi2")

    if tur == "0":
        gelir_etiketi.objects.create(
            gelir_kategoris_ait_bilgisi = user,
            gelir_etiketi_adi = adi,kayit_tarihi = timezone.now()
        )
        return redirect("accounting:gelir_ekle")
    elif tur == "1":
        gider_etiketi.objects.create(
            gider_kategoris_ait_bilgisi = user,
            gider_etiketi_adi = adi,kayit_tarihi = timezone.now()
        )
        return redirect("accounting:gider_ekle")


#Gelirler özeti
def gelirler_ozeti(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Gelir_Bilgisi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-fatura_tarihi")
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
                profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)| Q(aciklama__icontains = search) | Q(gelir_kategorisi__gelir_kategori_adi__icontains = search))
                content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        if tarih :
            profile = profile.filter(Q(fatura_tarihi__lte  = tarih) & Q(vade_tarihi__gte  = tarih) )
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
    return render(request,"muhasebe_page/gelir_ozeti.html",content)
#Gider Sayfası
def giderler_ozeti(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Gider_Bilgisi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).order_by("-fatura_tarihi")
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
                profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)|  Q(aciklama__icontains = search) | Q(gelir_kategorisi__gider_kategori_adi__icontains = search))
                content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        if tarih :
            profile = profile.filter(Q(fatura_tarihi__lte  = tarih) & Q(vade_tarihi__gte  = tarih) )
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
    return render(request,"muhasebe_page/gider_ozeti.html",content)

#Hesapğ eksta
def hesap_ekstra_durumu(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Gider_Bilgisi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        profile = list(Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user))+list(Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user))
        profile.sort(key=lambda x: x.kayit_tarihi)
        content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
    if request.GET:
        search = request.GET.get("search")
        tarih = request.GET.get("tarih")
        if search:
            if super_admin_kontrolu(request):
                profile =Gider_Bilgisi.objects.filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)|  Q(aciklama__icontains = search) | Q(gelir_kategorisi__gider_kategori_adi__icontains = search))
                kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
                content["kullanicilar"] =kullanicilar
            else:
                profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user).filter(Q(fatura_no__icontains = search)|Q(cari_bilgisi__cari_adi__icontains = search)|  Q(aciklama__icontains = search) | Q(gelir_kategorisi__gider_kategori_adi__icontains = search))
                content["kasa"] = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        if tarih :
            profile = profile.filter(fatura_tarihi  =tarih)
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
    return render(request,"muhasebe_page/hesap_eksta.html",content)

def fatura_goster(request,id):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Kasa.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        gelir_bilgisi_ver =  get_object_or_none(Gelir_Bilgisi,id = id)
        urunleri = gelir_urun_bilgisi.objects.filter(gider_bilgis = gelir_bilgisi_ver)
    else:
        profile = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        urunler_bilgisi = urunler.objects.filter(urun_ait_oldugu = request.user)
        cari_bilgileri = cari.objects.filter(cari_kart_ait_bilgisi = request.user)
        kategori_bilgisi = gelir_kategorisi.objects.filter(gelir_kategoris_ait_bilgisi = request.user)
        etiketler = gelir_etiketi.objects.filter(gelir_kategoris_ait_bilgisi = request.user)
        gelir_bilgisi_ver =  get_object_or_none(Gelir_Bilgisi,id = id)
        urunleri = gelir_urun_bilgisi.objects.filter(gider_bilgis = gelir_bilgisi_ver)


    content["bilgi"] = gelir_bilgisi_ver
    content["urunler"] = urunleri
    return render(request,"muhasebe_page/gelir_faturasi_goster.html",content)
def fatura_goster2(request,id):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Kasa.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        gelir_bilgisi_ver =  get_object_or_none(Gider_Bilgisi,id = id)
        urunleri = gider_urun_bilgisi.objects.filter(gider_bilgis = gelir_bilgisi_ver)
    else:
        profile = Kasa.objects.filter(silinme_bilgisi = False,kasa_kart_ait_bilgisi = request.user)
        urunler_bilgisi = urunler.objects.filter(urun_ait_oldugu = request.user)
        cari_bilgileri = cari.objects.filter(cari_kart_ait_bilgisi = request.user)
        kategori_bilgisi = gider_kategorisi.objects.filter(gider_kategoris_ait_bilgisi = request.user)
        etiketler = gider_etiketi.objects.filter(gider_kategoris_ait_bilgisi = request.user)
        gelir_bilgisi_ver =  get_object_or_none(Gider_Bilgisi,id = id)
        urunleri = gider_urun_bilgisi.objects.filter(gider_bilgis = gelir_bilgisi_ver)

    content["bilgi"] = gelir_bilgisi_ver
    content["urunler"] = urunleri
    return render(request,"muhasebe_page/gider_faturasi_goster.html",content)
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Border, Side, GradientFill, Alignment
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def toplam_odenme_tutar(id):
    a = Gelir_odemesi.objects.filter(gelir_kime_ait_oldugu=id)
    topla = 0
    for i in a:
        topla += i.tutar
    return topla

def toplam_tutar_cikarma(id):
    a = gelir_urun_bilgisi.objects.filter(gider_bilgis=id)
    topla = 0
    for i in a:
        topla += (i.urun_fiyati * i.urun_adeti) - i.urun_indirimi
    return topla
def toplam_tutar_cikarmai(id):
    a = gider_urun_bilgisi.objects.filter(gider_bilgis = id)
    topla = 0
    for i in a:
        topla = topla + ((i.urun_fiyati*i.urun_adeti)-i.urun_indirimi)
    return topla
def toplam_odenme_tutari(id):
    a = Gider_odemesi.objects.filter(gelir_kime_ait_oldugu = id)
    topla = 0
    for i in a:
        topla = topla + i.tutar
    return topla
def ekstra(id,k):
    bilgi =  faturalardaki_gelir_gider_etiketi.objects.last()
    if bilgi.gelir_etiketi in k:
        a = gelir_urun_bilgisi.objects.filter(gider_bilgis = id)
        topla = 0
        for i in a:
            topla = topla + ((i.urun_fiyati*i.urun_adeti)-i.urun_indirimi)
        return topla
    else:
        a = gider_urun_bilgisi.objects.filter(gider_bilgis = id)
        topla = 0
        for i in a:
            topla = topla + ((i.urun_fiyati*i.urun_adeti)-i.urun_indirimi)
        return topla

def ekstra_odeme(id,k):
    bilgi =  faturalardaki_gelir_gider_etiketi.objects.last()
    if bilgi.gelir_etiketi in k:
        a = Gelir_odemesi.objects.filter(gelir_kime_ait_oldugu = id)
        topla = 0
        for i in a:
            topla = topla +  i.tutar
        return topla
    else:
        a = Gider_odemesi.objects.filter(gelir_kime_ait_oldugu = id)
        topla = 0
        for i in a:
            topla = topla +  i.tutar
        return topla
def download_excel(request):
    tablo = []
    if request.POST:
        a = request.POST.get("sonuc_cek")
        if a == "0":
            islem = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu=request.user)
            for i in islem:
                tablo.append([
                    str(i.fatura_no),
                    str(i.cari_bilgisi.cari_adi),
                    str(i.aciklama),
                    str(i.fatura_tarihi.strftime("%d.%m.%Y")),
                    str(round(float(toplam_tutar_cikarma(i.id)),2)),
                    str(round(float(toplam_odenme_tutar(i.id)),2))
                ])
        elif a == "1":
            islem = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu=request.user)
            for i in islem:
                tablo.append([
                    str(i.fatura_no),
                    str(i.cari_bilgisi.cari_adi),
                    str(i.aciklama),
                    str(i.fatura_tarihi.strftime("%d.%m.%Y")),
                    str(round(float(toplam_tutar_cikarmai(i.id)),2)),
                    str(round(float(toplam_odenme_tutari(i.id)),2))
                ])
        elif a == "2":
            profile = list(Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user))+list(Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user))
            profile.sort(key=lambda x: x.kayit_tarihi)
            for i in profile:
                tablo.append([
                    str(i.fatura_no),
                    str(i.cari_bilgisi.cari_adi),
                    str(i.aciklama),
                    str(i.fatura_tarihi.strftime("%d.%m.%Y")),
                    str(round(float(ekstra(i,i.fatura_no)),2)),
                    str(round(float(ekstra_odeme(i,i.fatura_no)),2))
                ])

    wb = Workbook()
    ws = wb.active

    # Başlık satırını ekle
    ws.append(['Fatura No', 'Müşteri', 'Açıklama', 'Tarih', 'Tutar', 'Ödeme Tutarı'])

    # İçerik satırlarını ekle
    for row in tablo:
        ws.append(row)

    # Stil düzenlemeleri (opsiyonel)
    for cell in ws["1:1"]:
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

    # Excel dosyasını bir BytesIO nesnesine yaz
    excel_data = BytesIO()
    wb.save(excel_data)
    excel_data.seek(0)

    # HttpResponse ile dosyayı indirme bağlantısı olarak sun
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if a == "0":
        response['Content-Disposition'] = 'attachment; filename=incomesummary.xlsx'
    if a == "1":
        response['Content-Disposition'] = 'attachment; filename=expensesummary.xlsx'
    if a == "2":
        response['Content-Disposition'] = 'attachment; filename=accountsummary.xlsx'
    response.write(excel_data.getvalue())
    return response



def download_pdf(request):
    a = request.POST.get("sonuc_cek")
    # PDF dosyasını oluştur
    response = HttpResponse(content_type='application/pdf')
    if a == "0":
        response['Content-Disposition'] = 'attachment; filename=incomesummary.pdf'
    if a == "1":
        response['Content-Disposition'] = 'attachment; filename=expensesummary.pdf'
    if a == "2":
        response['Content-Disposition'] = 'attachment; filename=accountsummary.pdf'


    # PDF içeriği oluştur
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    data = [['Fatura No', 'Müşteri', 'Açıklama', 'Tarih', 'Tutar', 'Ödeme Tutarı']]

    if request.POST:
        a = request.POST.get("sonuc_cek")
        if a == "0":
            islem = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu=request.user)
            for i in islem:
                data.append([
                    str(i.fatura_no),
                    str(i.cari_bilgisi.cari_adi),
                    str(i.aciklama),
                    str(i.fatura_tarihi.strftime("%d.%m.%Y")),
                    str(round(float(toplam_tutar_cikarma(i.id)),2)),
                    str(round(float(toplam_odenme_tutar(i.id)),2))
                ])
        elif a == "1":
            islem = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu=request.user)
            for i in islem:
                data.append([
                    str(i.fatura_no),
                    str(i.cari_bilgisi.cari_adi),
                    str(i.aciklama),
                    str(i.fatura_tarihi.strftime("%d.%m.%Y")),
                    str(round(float(toplam_tutar_cikarmai(i.id)),2)),
                    str(round(float(toplam_odenme_tutari(i.id)),2))
                ])
        elif a == "2":
            profile = list(Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user))+list(Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu = request.user))
            profile.sort(key=lambda x: x.kayit_tarihi)
            for i in profile:
                data.append([
                    str(i.fatura_no),
                    str(i.cari_bilgisi.cari_adi),
                    str(i.aciklama),
                    str(i.fatura_tarihi.strftime("%d.%m.%Y")),
                    str(round(float(ekstra(i,i.fatura_no)),2)),
                    str(round(float(ekstra_odeme(i,i.fatura_no)),2))
                ])

    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # PDF'e tabloyu ekle
    elements.append(table)
    pdf.build(elements)
    return response
    #return redirect("/")
def fatura_gosterqr(request,id):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Kasa.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        gelir_bilgisi_ver =  get_object_or_none(Gelir_Bilgisi,id = id)
        urunleri = gelir_urun_bilgisi.objects.filter(gider_bilgis = gelir_bilgisi_ver)
    else:
        gelir_bilgisi_ver =  get_object_or_none(Gelir_Bilgisi,id = id)
        urunleri = gelir_urun_bilgisi.objects.filter(gider_bilgis = gelir_bilgisi_ver)

    content["bilgi"] = gelir_bilgisi_ver
    content["urunler"] = urunleri
    return render(request,"muhasebe_page/faturalari_goster_gelir.html",content)
def fatura_goster2qr(request,id):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =Kasa.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
        gelir_bilgisi_ver =  get_object_or_none(Gider_Bilgisi,id = id)
        urunleri = gider_urun_bilgisi.objects.filter(gider_bilgis = gelir_bilgisi_ver)
    else:

        gelir_bilgisi_ver =  get_object_or_none(Gider_Bilgisi,id = id)
        urunleri = gider_urun_bilgisi.objects.filter(gider_bilgis = gelir_bilgisi_ver)

    content["bilgi"] = gelir_bilgisi_ver
    content["urunler"] = urunleri
    return render(request,"muhasebe_page/faturalari_goster_gider.html",content)