from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from muhasebe.models import Gelir_Bilgisi, Gider_Bilgisi, Kasa, CustomUser, gider_urun_bilgisi, Gider_odemesi
from site_info.models import *
from django.db.models import Q
from main.views import sozluk_yapisi
from rest_framework import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from muhasebe.models import Gelir_Bilgisi, Gider_Bilgisi, CustomUser, Kasa, gider_urun_bilgisi, Gider_odemesi
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from main.views import super_admin_kontrolu  # varsa, util fonksiyonu
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_exempt
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

@api_view(['GET'])
def proje_tipi_api(request):
    content = {}
    
    # Super admin kontrolü
    if super_admin_kontrolu(request):
        profile = proje_tipi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db=None, is_superuser=False).order_by("-id")
        content["kullanicilar"] = CustomUserSerializer(kullanicilar, many=True).data
    else:
        profile = proje_tipi.objects.filter(silinme_bilgisi=False, proje_ait_bilgisi=request.user)
    
    # Arama işlemi
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile = proje_tipi.objects.filter(
                Q(proje_ait_bilgisi__last_name__icontains=search) | Q(Proje_tipi_adi__icontains=search)
            )
            kullanicilar = CustomUser.objects.filter(kullanicilar_db=None, is_superuser=False).order_by("-id")
            content["kullanicilar"] = CustomUserSerializer(kullanicilar, many=True).data
        else:
            profile = proje_tipi.objects.filter(
                Q(proje_ait_bilgisi=request.user) & Q(Proje_tipi_adi__icontains=search) & Q(silinme_bilgisi=False)
            )
    
    # Sayfalama

    
    content["santiyeler"] = ProjeTipiSerializer(profile, many=True).data


    return Response(content, status=status.HTTP_200_OK)


@api_view(['GET'])
def proje_ekleme_api(request):
    if request.method == 'GET':
        if super_admin_kontrolu(request):
            kullanici_bilgisi = request.data.get("kullanici")
            if kullanici_bilgisi:
                try:
                    kullanici = CustomUser.objects.get(id=kullanici_bilgisi)
                except CustomUser.DoesNotExist:
                    return Response({'error': 'Kullanıcı bulunamadı'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Kullanıcı ID\'si gerekli'}, status=status.HTTP_400_BAD_REQUEST)

            proje_tip_adi = request.data.get("yetkili_adi")
            proje_tipi.objects.create(proje_ait_bilgisi=kullanici, Proje_tipi_adi=proje_tip_adi)
        else:
            proje_tip_adi = request.data.get("yetkili_adi")
            proje_tipi.objects.create(proje_ait_bilgisi=request.user, Proje_tipi_adi=proje_tip_adi)
    
    return Response({'success': 'Proje tipi başarıyla oluşturuldu'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def proje_adi_sil(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    id = request.data.get("id")
    
    if not id:
        return Response({'detail': 'ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        proje = proje_tipi.objects.get(id=id)
    except proje_tipi.DoesNotExist:
        return Response({'detail': 'Project type not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if super_admin_kontrolu(request):
        proje.silinme_bilgisi = True
        proje.save()
        return Response({'status': 'Project type marked as deleted.'}, status=status.HTTP_200_OK)
    else:
        if proje.proje_ait_bilgisi!= request.user:
            return Response({'detail': f'{proje.proje_ait_bilgisi}'}, status=status.HTTP_403_FORBIDDEN)
        
        proje.silinme_bilgisi = True
        proje.save()
        return Response({'status': 'Project type marked as deleted.'}, status=status.HTTP_200_OK)
@api_view(['PATCH'])
def proje_duzenle(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    id = request.data.get("buttonId")
    if not id:
        return Response({'detail': 'ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        proje = proje_tipi.objects.get(id=id)
    except proje_tipi.DoesNotExist:
        return Response({'detail': 'Project type not found.'}, status=status.HTTP_404_NOT_FOUND)

    if super_admin_kontrolu(request):
        kullanici_bilgisi = request.data.get("kullanici")
        proje_tip_adi = request.data.get("yetkili_adi")
        silinmedurumu = request.data.get("silinmedurumu")
        
        if silinmedurumu == "1":
            silinmedurumu = False
        elif silinmedurumu == "2":
            silinmedurumu = True
        else:
            return Response({'detail': 'Invalid silinmedurumu value.'}, status=status.HTTP_400_BAD_REQUEST)
        
        proje.proje_ait_bilgisi = get_object_or_404(CustomUser, id=kullanici_bilgisi)
        proje.Proje_tipi_adi = proje_tip_adi
        proje.silinme_bilgisi = silinmedurumu
        proje.save()

        return Response({'status': 'Project type updated successfully.'}, status=status.HTTP_200_OK)
    else:
        proje_tip_adi = request.data.get("yetkili_adi")
        if proje.proje_ait_bilgisi != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        proje.Proje_tipi_adi = proje_tip_adi
        proje.save()
        
        return Response({'status': 'Project type updated successfully.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def santiye_projesi_liste(request):
    content = {}

    if super_admin_kontrolu(request):
        profile = santiye.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db=None, is_superuser=False).order_by("-id")
        content["kullanicilar"] = CustomUserSerializer(kullanicilar, many=True).data
    else:
        profile = santiye.objects.filter(silinme_bilgisi=False, proje_ait_bilgisi=request.user)
        content["proje_tipleri"] = ProjeTipiSerializer(proje_tipi.objects.filter(proje_ait_bilgisi=request.user), many=True).data

    content["santiyeler"] = SantiyeSerializer(profile, many=True).data
    content["top"] = profile.count()

    return Response(content, status=status.HTTP_200_OK)

from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def santiye_ekleme_api(request):
    if request.method == 'GET':    
        projetipi = request.data.get("projetipi")
        proje_adi = request.data.get("yetkili_adi")

        santiye.objects.create(
            proje_ait_bilgisi=request.user,
            proje_tipi=get_object_or_404(proje_tipi, id=projetipi),
            proje_adi=proje_adi
        )
        return Response({"message": "Santiye başarıyla eklendi."}, status=status.HTTP_201_CREATED)

    return Response({"error": "Geçersiz istek."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def santiye_projesi_sil_api(request):
    if request.method == 'POST':
        id = request.data.get("id")

        if super_admin_kontrolu(request):
            santiye.objects.filter(id=id).update(silinme_bilgisi=True)
        else:
            santiye.objects.filter(proje_ait_bilgisi=request.user, id=id).update(silinme_bilgisi=True)

        return Response({"message": "Şantiye başarıyla silindi."}, status=status.HTTP_200_OK)

    return Response({"error": "Geçersiz istek."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def santiye_projesi_duzenle_api(request):
    if request.method == 'GET':
        id = request.data.get("buttonId")

        if super_admin_kontrolu(request):
            proje_tip_adi = request.data.get("yetkili_adi")
            silinmedurumu = request.data.get("silinmedurumu")

            if silinmedurumu == "1":
                silinmedurumu = False
                santiye.objects.filter(id=id).update(proje_adi=proje_tip_adi, silinme_bilgisi=silinmedurumu)
            elif silinmedurumu == "2":
                silinmedurumu = True
                santiye.objects.filter(id=id).update(proje_adi=proje_tip_adi, silinme_bilgisi=silinmedurumu)
        else:
            proje_tip_adi = request.data.get("yetkili_adi")
            santiye.objects.filter(proje_ait_bilgisi=request.user, id=id).update(proje_adi=proje_tip_adi)

        return Response({"message": "Şantiye başarıyla güncellendi."}, status=status.HTTP_200_OK)

    return Response({"error": "Geçersiz istek."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def santiye_projesi_bloklar_ekle_api(request, id):
    try:
        if super_admin_kontrolu(request):
            pass
        else:
            profile = bloglar.objects.filter(proje_santiye_Ait__id=id)
            content = {
                "id_bilgisi": id,
                "proje_tipleri": ProjeTipiSerializer(proje_tipi.objects.filter(proje_ait_bilgisi=request.user), many=True).data,
            }
        content["santiyeler"] = BloglarSerializer(profile, many=True).data
        return Response(content, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blog_ekle_api(request):
    try:
        santiye_bilgisi = request.data.get("santiye_bilgisi")
        blok_adi = request.data.get("blok_adi")
        kat_sayisi = request.data.get("kat_sayisi")
        baslangictarihi = request.data.get("baslangictarihi")
        bitistarihi = request.data.get("bitistarihi")
        
        if not santiye_bilgisi or not blok_adi:
            return Response({"error": "Eksik bilgi"}, status=status.HTTP_400_BAD_REQUEST)

        santiye_obj = get_object_or_404(santiye, id=santiye_bilgisi)
        blog = bloglar.objects.create(
            proje_ait_bilgisi=santiye_obj.proje_ait_bilgisi,
            proje_santiye_Ait=santiye_obj,
            blog_adi=blok_adi,
            kat_sayisi=kat_sayisi,
            baslangic_tarihi=baslangictarihi,
            bitis_tarihi=bitistarihi
        )
        
        serializer = BloglarSerializer(blog)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
