from django import template
from site_info.models import *
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
register = template.Library()

#@register.filter
@register.simple_tag
def to_int(veri):
    return int(veri)

@register.simple_tag
def bloglar_getir(veri):
    deger = bloglar.objects.filter(proje_santiye_Ait = veri)
    veri_esiti = ""
    for i in  deger:
        veri_esiti = veri_esiti + str(i.blog_adi)+str(i.blog_numarasi)+" ,"
    return str(veri_esiti)


