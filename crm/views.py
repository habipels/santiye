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
from main.views import sozluk_yapisi
def crm_dashboard(request):
    content = sozluk_yapisi()
    return render(request,"crm/crm-dashboard.html",content)

def crm_dairedetayi(request):
    content = sozluk_yapisi()
    return render(request,"crm/crm-daire-detay.html",content)

def crm_daireyonetimi(request):
    content = sozluk_yapisi()
    return render(request,"crm/crm-daire-yonetimi.html",content)

def crm_evr(request):
    content = sozluk_yapisi()
    return render(request,"crm/crm-evrak-ve-dokuman-detay.html",content)
def crm_evrak_dokuman(request):
    content = sozluk_yapisi()
    return render(request,"crm/crm-evrak-ve-dokuman.html",content)

def crm_musteri_detayi(request):
    content = sozluk_yapisi()
    return render(request,"crm/musteri-detay.html",content)

def crm_musteri_yonetimi(request):
    content = sozluk_yapisi()
    return render(request,"crm/musteri-yonetimi.html",content)


def crm_talepler_sikayetler(request):
    content = sozluk_yapisi()
    return render(request,"crm/talep-ve-sikayetler.html",content)

def crm_teklif_olustur(request):
    content = sozluk_yapisi()
    return render(request,"crm/teklif-olustur.html",content)

def crm_teklif_yonetimi(request):
    content = sozluk_yapisi()
    return render(request,"crm/teklif-yonetimi.html",content)