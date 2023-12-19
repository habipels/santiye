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
        proje_tip_adi   = request.POST.get("yetkili_adi")
        konumu = request.POST.get("konumu")
        Kasa.objects.filter(kasa_kart_ait_bilgisi = request.user,id = id).update(kasa_adi = proje_tip_adi                                                                 
                ,aciklama = konumu)
    return redirect("accounting:kasa")
