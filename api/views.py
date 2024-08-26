from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from muhasebe.models import Gelir_Bilgisi, Gider_Bilgisi, Kasa, CustomUser, gider_urun_bilgisi, Gider_odemesi
from django.db.models import Q
from main.views import sozluk_yapisi
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
def super_admin_kontrolu(request):
    if request.user.is_superuser:
            return 1
    else:
        return 0

from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from muhasebe.models import Gelir_Bilgisi, Gider_Bilgisi, CustomUser, Kasa, gider_urun_bilgisi, Gider_odemesi
from .serializers import GelirBilgisiSerializer, GiderBilgisiSerializer, CustomUserSerializer, KasaSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

@api_view(['GET'])
def homepage_api(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    content = {}

    # Gelir bilgileri
    if super_admin_kontrolu(request):
        profile = Gelir_Bilgisi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db=None, is_superuser=False).order_by("-id")
        content["kullanicilar"] = CustomUserSerializer(kullanicilar, many=True).data
    else:
        profile = Gelir_Bilgisi.objects.filter(gelir_kime_ait_oldugu=request.user).order_by("-id")
        content["kasa"] = KasaSerializer(Kasa.objects.filter(silinme_bilgisi=False, kasa_kart_ait_bilgisi=request.user), many=True).data

    content["santiyeler"] = GelirBilgisiSerializer(profile, many=True).data

    # Gider bilgileri
    if super_admin_kontrolu(request):
        gider_profile = Gider_Bilgisi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db=None, is_superuser=False).order_by("-id")
        content["kullanicilar"] = CustomUserSerializer(kullanicilar, many=True).data
    else:
        gider_profile = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu=request.user).order_by("-id")

    bilgi_ver = Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu=request.user).order_by("-fatura_tarihi")
    sonuc = []
    for i in bilgi_ver:
        urun_tutari = sum(float(j.urun_adeti) * float(j.urun_fiyati) for j in gider_urun_bilgisi.objects.filter(gider_bilgis=i))
        odeme_tutari = sum(float(j.tutar) for j in Gider_odemesi.objects.filter(gelir_kime_ait_oldugu=i))
        if urun_tutari > odeme_tutari:
            sonuc.append(i)
        if len(sonuc) >= 5:
            break
    content["gider"] = GiderBilgisiSerializer(sonuc, many=True).data
    content["bilgi"] = GiderBilgisiSerializer(Gider_Bilgisi.objects.filter(gelir_kime_ait_oldugu=request.user).order_by("-id")[:5], many=True).data

    return Response(content)
