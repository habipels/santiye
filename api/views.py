from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from site_info.models import *
from django.db.models import Q
from main.views import sozluk_yapisi
from rest_framework import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from muhasebe.models import *
from site_info.models import *
from .serializers import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from main.views import super_admin_kontrolu  # varsa, util fonksiyonu
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if user.image:
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                "user_name":user.username,
                "name_sorname":user.last_name,
                "image":user.image.url
            })
        return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                "user_name":user.username,
                "name_sorname":user.last_name,
                "image":False
            })
def super_admin_kontrolu(request):
    if request.user.is_superuser:
            return 1
    else:
        return 0

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
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

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blog_duzenle_api(request):
    try:
        santiye_bilgisi = request.data.get("santiye_bilgisi")
        blog_id = request.data.get("blog")
        blok_adi = request.data.get("blok_adi")
        kat_sayisi = request.data.get("kat_sayisi")
        baslangictarihi = request.data.get("baslangictarihi")
        bitistarihi = request.data.get("bitistarihi")
        
        blog = get_object_or_404(bloglar, id=blog_id)
        santiye_obj = get_object_or_404(santiye, id=santiye_bilgisi)
        
        blog.proje_ait_bilgisi = santiye_obj.proje_ait_bilgisi
        blog.proje_santiye_Ait = santiye_obj
        blog.blog_adi = blok_adi
        blog.kat_sayisi = kat_sayisi
        blog.baslangic_tarihi = baslangictarihi
        blog.bitis_tarihi = bitistarihi
        blog.save()

        serializer = BloglarSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blog_sil_api(request):
    try:
        button_id = request.data.get("buttonId")
        blog = get_object_or_404(bloglar, id=button_id)
        blog.delete()
        
        return Response({"message": "Blog başarıyla silindi"}, status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def santiye_kalemleri_api(request, id):
    content = {}
    
    # Birim bilgilerini al
    birim_bilgisi = birimler.objects.filter(silinme_bilgisi=False)
    content["birim_bilgisi"] = BirimlerSerializer(birim_bilgisi, many=True).data
    
    # Kullanıcı süperuser mı değil mi kontrol et
    if request.user.is_superuser:
        # Süperuser ile ilgili işlemler burada yapılabilir
        pass
    else:
        profile = santiye_kalemleri.objects.filter(
            proje_santiye_Ait=get_object_or_404(santiye, id=id), 
            silinme_bilgisi=False, 
            proje_ait_bilgisi=request.user
        )
        content["santiyeler_bilgileri"] = BloglarSerializer(
            bloglar.objects.filter(proje_ait_bilgisi=request.user, proje_santiye_Ait_id=id), 
            many=True
        ).data

    # Serializing the data
    content["profile"] = SantiyeKalemleriSerializer(profile, many=True).data
    
    return Response(content, status=status.HTTP_200_OK)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def santiyeye_kalem_ekle_api(request):
    if request.user.is_superuser:
        kullanici = request.data.get("kullanici")
        return redirect("main:santiye_kalem_ekle_admin", kullanici)
    else:
        projetipi = request.data.get("projetipi", [])
        yetkili_adi = request.data.get("yetkili_adi")
        santiye_agirligi = request.data.get("katsayisi")
        finansal_agirlik = request.data.get("blogsayisi")
        metraj = request.data.get("metraj")
        tutar = request.data.get("tutar")
        birim_bilgisi = request.data.get("birim_bilgisi")
        kata_veya_binaya_daihil = request.data.get("kata_veya_binaya_daihil")
        id = bloglar.objects.filter(id__in=projetipi).first()
        
        # Yeni kalem oluştur
        kalem = santiye_kalemleri.objects.create(
            proje_ait_bilgisi=request.user,
            proje_santiye_Ait=id.proje_santiye_Ait,
            kalem_adi=yetkili_adi,
            santiye_agirligi=santiye_agirligi,
            santiye_finansal_agirligi=finansal_agirlik,
            birimi=get_object_or_404(birimler, id=birim_bilgisi),
            metraj=metraj,
            tutari=tutar
        )

        blog_lar = bloglar.objects.filter(id__in=projetipi)

        if kata_veya_binaya_daihil == "0":
            for i in blog_lar:
                for j in range(0, int(i.kat_sayisi)):
                    santiye_kalemlerin_dagilisi.objects.create(
                        proje_ait_bilgisi=request.user,
                        proje_santiye_Ait=id.proje_santiye_Ait,
                        kalem_bilgisi=kalem,
                        kat=j,
                        blog_bilgisi=i
                    )
        elif kata_veya_binaya_daihil == "1":
            for i in blog_lar:
                santiye_kalemlerin_dagilisi.objects.create(
                    proje_ait_bilgisi=request.user,
                    proje_santiye_Ait=id.proje_santiye_Ait,
                    kalem_bilgisi=kalem,
                    kat=0,
                    blog_bilgisi=i
                )
        elif kata_veya_binaya_daihil == "2":
            for i in blog_lar:
                for j in range(0, 4):
                    santiye_kalemlerin_dagilisi.objects.create(
                        proje_ait_bilgisi=request.user,
                        proje_santiye_Ait=id.proje_santiye_Ait,
                        kalem_bilgisi=kalem,
                        kat=j,
                        blog_bilgisi=i
                    )

        return Response({"message": "Kalem başarıyla eklendi."}, status=status.HTTP_201_CREATED)

    return Response({"error": "Yetkisiz erişim."}, status=status.HTTP_403_FORBIDDEN)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kalem_sil_api(request, id):
    kalem = get_object_or_404(santiye_kalemleri, id=id)

    # Kullanıcının silme yetkisi olup olmadığını kontrol et
    if request.user != kalem.proje_ait_bilgisi and not request.user.is_superuser:
        return Response({"error": "Yetkisiz erişim."}, status=status.HTTP_403_FORBIDDEN)
    
    kalem.silinme_bilgisi = True
    kalem.save()

    return Response({"message": "Kalem başarıyla silindi."}, status=status.HTTP_200_OK)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def santiye_kalemleri_duzenle_api(request,id):
    try:
        # Verileri al
        yetkili_adi = request.data.get("yetkili_adi")
        santiye_agirligi = request.data.get("katsayisi")
        finansal_agirlik = request.data.get("blogsayisi")
        metraj = request.data.get("metraj")
        tutar = request.data.get("tutar")
        birim_bilgisi = request.data.get("birim_bilgisi")
        silinmedurumu = request.data.get("silinmedurumu")

        # Kalemi al
        kalem = get_object_or_404(santiye_kalemleri, id=id)

        # Verileri güncelle
        if request.user.is_superuser:
            if silinmedurumu == "3":
                kalem.kalem_adi = yetkili_adi
                kalem.santiye_agirligi = santiye_agirligi
                kalem.santiye_finansal_agirligi = finansal_agirlik
                kalem.birimi = get_object_or_404(birimler, id=birim_bilgisi)
                kalem.metraj = metraj
                kalem.tutari = tutar
                kalem.save()

            elif silinmedurumu == "2":
                kalem.kalem_adi = yetkili_adi
                kalem.santiye_agirligi = santiye_agirligi
                kalem.santiye_finansal_agirligi = finansal_agirlik
                kalem.silinme_bilgisi = True
                kalem.birimi = get_object_or_404(birimler, id=birim_bilgisi)
                kalem.metraj = metraj
                kalem.tutari = tutar
                kalem.save()

            elif silinmedurumu == "1":
                kalem.kalem_adi = yetkili_adi
                kalem.santiye_agirligi = santiye_agirligi
                kalem.santiye_finansal_agirligi = finansal_agirlik
                kalem.silinme_bilgisi = False
                kalem.birimi = get_object_or_404(birimler, id=birim_bilgisi)
                kalem.metraj = metraj
                kalem.tutari = tutar
                kalem.save()

        else:
            kalem.proje_ait_bilgisi = request.user
            kalem.kalem_adi = yetkili_adi
            kalem.santiye_agirligi = santiye_agirligi
            kalem.santiye_finansal_agirligi = finansal_agirlik
            kalem.birimi = get_object_or_404(birimler, id=birim_bilgisi)
            kalem.metraj = metraj
            kalem.tutari = tutar
            kalem.save()

        return Response({"message": "Kalem başarıyla güncellendi."}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def kalem_blog_dagilis_sil_api(request, id, ik):
    try:
        # İlgili kayıtları al
        dagilis = get_object_or_404(santiye_kalemlerin_dagilisi, blog_bilgisi__id=id)
        proje_santiye_id = dagilis.proje_santiye_Ait.id

        # Kayıtları sil
        santiye_kalemlerin_dagilisi.objects.filter(kalem_bilgisi__id=ik, blog_bilgisi__id=id).delete()

        return Response({"message": "Kalem ve blog dağılımı başarıyla silindi."}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def santiye_kalem_ve_blog_api(request):
    content = {}
    
    try:
        # Proje tiplerini al
        proje_tipleri = proje_tipi.objects.filter(proje_ait_bilgisi=request.user)
        content["proje_tipleri"] = ProjeTipiSerializer(proje_tipleri, many=True).data
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if request.user.is_superuser:
            profile = bloglar.objects.all()  # Superuser tüm blogları görebilir
        else:
            profile = bloglar.objects.filter(proje_ait_bilgisi=request.user)
        
        content["santiyeler"] = BloglarSerializer(profile, many=True).data
        return Response(content, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blogtan_kaleme_ilerleme_takibi_api(request, id):
    content = {}
    
    try:
        # Blog bilgisi al
        #content["id"] =BloglarSerializer (get_object_or_404(bloglar, id=id),many = True).data
        #content["blog_id"] = id
        
        if request.user.is_authenticated:
            if request.user.is_superuser:
                # Superuser için santiye bilgileri ve kalemler
                pass
            else:
                # Normal kullanıcı için santiye bilgileri ve kalemler
                content["santiyeler_bilgileri"] = SantiyeSerializer(santiye.objects.filter(silinme_bilgisi=False, proje_ait_bilgisi=request.user), many=True).data
                kalemler = santiye_kalemlerin_dagilisi.objects.filter(blog_bilgisi__id=id)
            
            kalem_id = list(set(i.kalem_bilgisi.id for i in kalemler))
            profile =santiye_kalemleri.objects.filter(id__in=kalem_id, silinme_bilgisi=False)  
            content["santiyeler"] = SantiyeKalemleriSerializer(profile, many=True).data
        
        else:
            return Response({"error": "Kullanıcı giriş yapmamış."}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(content, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ilerleme_kaydet_api(request):
    try:
        kalem = request.data.getlist("kalem")
        tumbilgi = request.data.getlist("tumbilgi")
        
        a = []
        for i in tumbilgi:
            k = i.split(",")
            for j in k:
                a.append(j)

        # Seçilen kalemleri tamamlandı olarak işaretle
        for i in kalem:
            a.remove(i)
            dagilis = santiye_kalemlerin_dagilisi.objects.filter(id=int(i)).update(tamamlanma_bilgisi=True)
            # Güncellenen nesneleri serileştir
            updated_item = santiye_kalemlerin_dagilisi.objects.get(id=int(i))
            updated_serializer = SantiyeKalemlerinDagilisiSerializer(updated_item)

        # Seçilmeyen kalemleri tamamlanmadı olarak işaretle
        for i in a:
            if i != "":
                dagilis = santiye_kalemlerin_dagilisi.objects.filter(id=int(i)).update(tamamlanma_bilgisi=False)
                # Güncellenen nesneleri serileştir
                updated_item = santiye_kalemlerin_dagilisi.objects.get(id=int(i))
                updated_serializer = SantiyeKalemlerinDagilisiSerializer(updated_item)

        return Response({
            "success": True,
            "updated_items": updated_serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Eğer bir yönlendirme gerekiyorsa (API olmadığı durumlarda)
    # return redirect("main:blogtan_kaleme_ilerleme_takibi", geri_don, veri_cek)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def projeler_sayfasi_api(request):
    content = {}
    
    try:
        # Superadmin kontrolü
        if request.user.is_superuser:
            pass
        else:
            profile = projeler.objects.filter(silinme_bilgisi=False, proje_ait_bilgisi=request.user)
        content["santiyeler"] = ProjelerSerializer(profile, many=True).data
        content["blog_bilgisi"] = BloglarSerializer(
            bloglar.objects.filter(proje_ait_bilgisi=request.user, proje_santiye_Ait__silinme_bilgisi=False), 
            many=True
        ).data
        
        return Response(content, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def proje_ekle_api(request):
    try:
        if request.user.is_superuser:
            kullanici = request.data.get("kullanici")
            return redirect("main:proje_ekle_admin", id=kullanici)
        else:
            yetkili_adi = request.data.get("yetkili_adi")
            tarih_bilgisi = request.data.get("tarih_bilgisi")
            aciklama = request.data.get("aciklama")
            durumu = request.data.get("durumu")
            durumu = True if durumu == "1" else False
            blogbilgisi = request.data.getlist("blogbilgisi")
            
            # Yeni proje oluşturma
            new_project = projeler(
                proje_ait_bilgisi=request.user,
                proje_Adi=yetkili_adi,
                tarih=tarih_bilgisi,
                aciklama=aciklama,
                durum=durumu,
                silinme_bilgisi=False
            )
            new_project.save()
            
            # Blog bilgilerini ekleme
            bloglar_bilgisi = [get_object_or_404(bloglar, id=int(i)) for i in blogbilgisi]
            new_project.blog_bilgisi.add(*bloglar_bilgisi)
            
            # Resim dosyalarını kaydetme
            images = request.FILES.getlist('file')
            for image in images:
                proje_dosyalari.objects.create(dosya=image, proje_ait_bilgisi=new_project)
            
            return Response({"message": "Proje başarıyla eklendi."}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def proje_silme_api(request):
    try:
        button_id = request.data.get("buttonId")
        
        # Proje ID'sinin mevcut olup olmadığını kontrol et
        proje = get_object_or_404(projeler, id=button_id)
        
        # Projeyi silinmiş olarak işaretle
        proje.silinme_bilgisi = True
        proje.save()
        
        return Response({"message": "Proje başarıyla silindi."}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def proje_duzenle_bilgi_api(request):
    try:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                kullanici = request.data.get("kullanici")
                yetkili_adi = request.data.get("yetkili_adi")
                tarih_bilgisi = request.data.get("tarih_bilgisi")
                aciklama = request.data.get("aciklama")
                durumu = request.data.get("durumu")
                buttonIdInput = request.data.get("buttonId")

                durumu = True if durumu == "1" else False
                blogbilgisi = request.data.getlist("blogbilgisi")

                projeler.objects.filter(id=buttonIdInput).update(
                    proje_ait_bilgisi=get_object_or_404(CustomUser, id=kullanici),
                    proje_Adi=yetkili_adi,
                    tarih=tarih_bilgisi,
                    aciklama=aciklama,
                    durum=durumu,
                    silinme_bilgisi=False
                )
                z = get_object_or_404(projeler, id=buttonIdInput)
                bloglar_bilgisi = [get_object_or_404(bloglar, id=int(i)) for i in blogbilgisi]
                z.blog_bilgisi.set(bloglar_bilgisi)
                
                # Resim dosyalarını işleme
                files = request.FILES.getlist('file')
                for file in files:
                    proje_dosyalari.objects.create(dosya=file, proje_ait_bilgisi=z)
                
            else:
                yetkili_adi = request.data.get("yetkili_adi")
                tarih_bilgisi = request.data.get("tarih_bilgisi")
                aciklama = request.data.get("aciklama")
                durumu = request.data.get("durumu")
                buttonIdInput = request.data.get("buttonId")

                durumu = True if durumu == "1" else False
                blogbilgisi = request.data.getlist("blogbilgisi")

                projeler.objects.filter(id=buttonIdInput).update(
                    proje_Adi=yetkili_adi,
                    tarih=tarih_bilgisi,
                    aciklama=aciklama,
                    durum=durumu,
                    silinme_bilgisi=False
                )
                z = get_object_or_404(projeler, id=buttonIdInput)
                bloglar_bilgisi = [get_object_or_404(bloglar, id=int(i)) for i in blogbilgisi]
                z.blog_bilgisi.set(bloglar_bilgisi)
                
                # Resim dosyalarını işleme
                files = request.FILES.getlist('file')
                for file in files:
                    proje_dosyalari.objects.create(dosya=file, proje_ait_bilgisi=z)

        return Response({"message": "Proje başarıyla güncellendi."}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taseron_sayfasi_api(request):
    content = {}
    
    try:
        # Superadmin kontrolü
        if super_admin_kontrolu(request):
            pass
        else:
            profile = taseronlar.objects.filter(silinme_bilgisi=False, taseron_ait_bilgisi=request.user)
        
        
        content["santiyeler"] = TaseronlarSerializer(profile, many=True).data
        content["blog_bilgisi"] = ProjelerSerializer(projeler.objects.filter(proje_ait_bilgisi=request.user, silinme_bilgisi=False), many=True).data
        
        return Response(content, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taseron_ekle_api(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            kullanici = request.data.get("kullanici")
            return Response({"message": "Redirect to admin page"}, status=status.HTTP_302_FOUND)
        else:
            taseron_adi = request.data.get("taseron_adi")
            telefonnumarasi = request.data.get("telefonnumarasi")
            email_adresi = request.data.get("email_adresi")
            blogbilgisi = request.data.getlist("blogbilgisi")
            aciklama = request.data.get("aciklama")
            
            new_taseron = taseronlar(
                taseron_ait_bilgisi=request.user,
                taseron_adi=taseron_adi,
                email=email_adresi,
                aciklama=aciklama,
                telefon_numarasi=telefonnumarasi,
                silinme_bilgisi=False
            )
            new_taseron.save()
            
            bloglar_bilgisi = [projeler.objects.get(id=int(i)) for i in blogbilgisi]
            new_taseron.proje_bilgisi.add(*bloglar_bilgisi)
            
            # Handle file uploads
            files = request.FILES.getlist('file')
            for idx, file in enumerate(files, start=1):
                taseron_sozlesme_dosyalari.objects.create(
                    aciklama="",
                    dosya_adi=idx,
                    dosya=file,
                    proje_ait_bilgisi=new_taseron
                )
            
            car = cari.objects.create(
                cari_kart_ait_bilgisi=request.user,
                cari_adi=taseron_adi,
                telefon_numarasi=telefonnumarasi,
                aciklama=aciklama
            )
            
            cari_taseron_baglantisi.objects.create(
                gelir_kime_ait_oldugu=new_taseron,
                cari_bilgisi=car
            )
            
            return Response({"message": "Taseron başarıyla eklendi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "Kullanıcı giriş yapmamış."}, status=status.HTTP_401_UNAUTHORIZED)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taseron_silme_api(request):
    try:
        button_id = request.data.get("buttonId")
        
        # Proje ID'sinin mevcut olup olmadığını kontrol et
        proje = get_object_or_404(taseronlar, id=button_id)
        
        # Projeyi silinmiş olarak işaretle
        proje.silinme_bilgisi = True
        proje.save()
        
        return Response({"message": "Taşeron başarıyla silindi."}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taseron_duzelt_api(request):
    try:
        if request.user.is_authenticated:
            id_bilgisi = request.data.get("id_bilgisi")
            taseron_adi = request.data.get("taseron_adi")
            telefonnumarasi = request.data.get("telefonnumarasi")
            email_adresi = request.data.get("email_adresi")
            blogbilgisi = request.data.getlist("blogbilgisi")
            aciklama = request.data.get("aciklama")
            silinmedurumu = request.data.get("silinmedurumu")

            # Silinme durumuna göre güncelleme yap
            if silinmedurumu == "1":
                taseronlar.objects.filter(id=id_bilgisi).update(
                    taseron_adi=taseron_adi,
                    email=email_adresi,
                    aciklama=aciklama,
                    telefon_numarasi=telefonnumarasi,
                    silinme_bilgisi=False
                )
            elif silinmedurumu == "2":
                taseronlar.objects.filter(id=id_bilgisi).update(
                    taseron_adi=taseron_adi,
                    email=email_adresi,
                    aciklama=aciklama,
                    telefon_numarasi=telefonnumarasi,
                    silinme_bilgisi=True
                )
            else:
                taseronlar.objects.filter(id=id_bilgisi).update(
                    taseron_adi=taseron_adi,
                    email=email_adresi,
                    aciklama=aciklama,
                    telefon_numarasi=telefonnumarasi
                )

            # Blog bilgilerini güncelle
            taseron = get_object_or_404(taseronlar, id=id_bilgisi)
            bloglar_bilgisi = [get_object_or_404(projeler, id=int(i)) for i in blogbilgisi]
            taseron.proje_bilgisi.set(bloglar_bilgisi)

            # Dosyaları işleme
            files = request.FILES.getlist('file')
            for i, file in enumerate(files, start=1):
                taseron_sozlesme_dosyalari.objects.create(
                    aciklama="",
                    dosya_adi=i,
                    dosya=file,
                    proje_ait_bilgisi=taseron
                )

            return Response({"message": "Taseron başarıyla güncellendi."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Yetkisiz erişim."}, status=status.HTTP_403_FORBIDDEN)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sozlesmeler_sayfasi_api(request):
    try:
        # Sözlük oluşturma fonksiyonunu çağır
        content = {}

        if super_admin_kontrolu(request):
            pass
        else:
            profile = taseron_sozlesme_dosyalari.objects.filter(silinme_bilgisi=False, proje_ait_bilgisi__taseron_ait_bilgisi=request.user)


        content["santiyeler"] = SozlesmeSerializer(profile, many=True).data
        content["blog_bilgisi"] = ProjelerSerializer( projeler.objects.filter(proje_ait_bilgisi=request.user, silinme_bilgisi=False),many =True).data
        content["taseronlar"] = TaseronlarSerializer(taseronlar.objects.filter(taseron_ait_bilgisi=request.user, silinme_bilgisi=False),many =True).data

        return Response(content, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sozlesme_ekle_api(request):
    try:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                kullanici = request.data.get("kullanici")
                return Response({"message": "Redirect to admin page"}, status=status.HTTP_302_FOUND)
            else:
                taseron = request.data.get("taseron")
                dosyaadi = request.data.get("dosyaadi")
                tarih = request.data.get("tarih")
                aciklama = request.data.get("aciklama")
                durumu = request.data.get("durumu") == "1"
                file = request.FILES.get("file")
                
                taseron_sozlesme_dosyalari.objects.create(
                    proje_ait_bilgisi=get_object_or_404(taseronlar, id=taseron),
                    dosya=file,
                    dosya_adi=dosyaadi,
                    tarih=tarih,
                    aciklama=aciklama,
                    durum=durumu
                )
                return Response({"message": "Sözleşme başarıyla eklendi."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sozlesme_duzenle_api(request):
    try:
        if request.user.is_authenticated:
            id_bilgisi = request.data.get("id_bilgisi")
            taseron = request.data.get("taseron")
            dosyaadi = request.data.get("dosyaadi")
            tarih = request.data.get("tarih")
            aciklama = request.data.get("aciklama")
            durumu = request.data.get("durumu") == "1"
            file = request.FILES.get("file")
            
            if request.user.is_superuser:
                silinmedurumu = request.data.get("silinmedurumu")
                if silinmedurumu == "3":
                    taseron_sozlesme_dosyalari.objects.filter(id=id_bilgisi).update(
                        proje_ait_bilgisi=get_object_or_404(taseronlar, id=taseron),
                        dosya=file,
                        dosya_adi=dosyaadi,
                        tarih=tarih,
                        aciklama=aciklama,
                        durum=durumu
                    )
                elif silinmedurumu == "2":
                    taseron_sozlesme_dosyalari.objects.filter(id=id_bilgisi).update(
                        proje_ait_bilgisi=get_object_or_404(taseronlar, id=taseron),
                        dosya=file,
                        dosya_adi=dosyaadi,
                        tarih=tarih,
                        aciklama=aciklama,
                        durum=durumu,
                        silinme_bilgisi=True
                    )
                elif silinmedurumu == "1":
                    taseron_sozlesme_dosyalari.objects.filter(id=id_bilgisi).update(
                        proje_ait_bilgisi=get_object_or_404(taseronlar, id=taseron),
                        dosya=file,
                        dosya_adi=dosyaadi,
                        tarih=tarih,
                        aciklama=aciklama,
                        durum=durumu,
                        silinme_bilgisi=False
                    )
            else:
                taseron_sozlesme_dosyalari.objects.filter(id=id_bilgisi).update(
                    proje_ait_bilgisi=get_object_or_404(taseronlar, id=taseron),
                    dosya=file,
                    dosya_adi=dosyaadi,
                    tarih=tarih,
                    aciklama=aciklama,
                    durum=durumu
                )
            
            return Response({"message": "Sözleşme başarıyla güncellendi."}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sozlesme_silme_api(request):
    try:
        if request.user.is_authenticated:
            buttonId = request.data.get("buttonId")
            if not buttonId:
                return Response({"error": "Button ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            sozlesme = get_object_or_404(taseron_sozlesme_dosyalari, id=buttonId)
            sozlesme.silinme_bilgisi = True
            sozlesme.save()

            return Response({"message": "Sözleşme başarıyla silindi."}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hakedis_sayfasi_api(request):
    try:
        # Kullanıcı yetkisini kontrol et
        if super_admin_kontrolu(request):
            pass
        else:
            profile = taseron_hakedisles.objects.filter(silinme_bilgisi=False, proje_ait_bilgisi__taseron_ait_bilgisi=request.user)
            content = {}


        # İçeriği hazırlama
        content["santiyeler"] = TaseronHakedislesSerializer(profile,many = True).data
        content["taseronlar"] =TaseronlarSerializer(taseronlar.objects.filter(taseron_ait_bilgisi=request.user, silinme_bilgisi=False),many = True).data

        return Response(content, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hakedis_ekle_api(request):
    try:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                # Superuser için özel işlem
                kullanici = request.data.get("kullanici")
                return Response({"message": "Superuser işlemi yapılacak."}, status=status.HTTP_200_OK)
            else:
                # Normal kullanıcı işlemi
                taseron = request.data.get("taseron")
                dosyaadi = request.data.get("yetkili_adi")
                tarih = request.data.get("tarih_bilgisi")
                aciklama = request.data.get("aciklama")
                durumu = request.data.get("durumu")
                file = request.FILES.get("file")
                tutar = request.data.get("tutar")
                fatura_no = request.data.get("fatura_no")

                durumu = True if durumu == "1" else False

                taseron_hakedisles.objects.create(
                    proje_ait_bilgisi=get_object_or_404(taseronlar, id=taseron),
                    dosya=file,
                    dosya_adi=dosyaadi,
                    tarih=tarih,
                    aciklama=aciklama,
                    durum=durumu,
                    tutar=tutar,
                    fatura_numarasi=fatura_no
                )

                return Response({"message": "Hakediş başarıyla eklendi."}, status=status.HTTP_201_CREATED)

        return Response({"error": "Yetkisiz erişim."}, status=status.HTTP_403_FORBIDDEN)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hakedis_silme_api(request):
    try:
        if request.user.is_authenticated:
            # POST verilerini al
            button_id = request.data.get("buttonId")

            # Kayıtları güncelle
            updated_count = taseron_hakedisles.objects.filter(id=button_id).update(silinme_bilgisi=True)

            if updated_count > 0:
                return Response({"message": "Hakediş başarıyla silindi."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Hakediş bulunamadı."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "Yetkisiz erişim."}, status=status.HTTP_403_FORBIDDEN)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hakedis_duzenle_api(request):
    try:
        if request.user.is_authenticated:
            button_id = request.data.get("buttonId")
            taseron_id = request.data.get("taseron")
            dosya_adi = request.data.get("yetkili_adi")
            tarih = request.data.get("tarih_bilgisi")
            aciklama = request.data.get("aciklama")
            durumu = request.data.get("durumu")
            file = request.FILES.get("file")
            tutar = request.data.get("tutar")
            fatura_no = request.data.get("fatura_no")
            silinme_durumu = request.data.get("silinmedurumu")

            # Durum ve silinme bilgisi ayarları
            durumu = True if durumu == "1" else False
            silinme_durumu = True if silinme_durumu == "2" else False

            # Veritabanı güncellemeleri
            if request.user.is_superuser:
                if silinme_durumu:
                    taseron_hakedisles.objects.filter(id=button_id).update(
                        proje_ait_bilgisi=get_object_or_404(taseronlar, id=taseron_id),
                        dosya=file,
                        dosya_adi=dosya_adi,
                        tarih=tarih,
                        aciklama=aciklama,
                        durum=durumu,
                        tutar=tutar,
                        fatura_numarasi=fatura_no,
                        silinme_bilgisi=silinme_durumu
                    )
                else:
                    taseron_hakedisles.objects.filter(id=button_id).update(
                        proje_ait_bilgisi=get_object_or_404(taseronlar, id=taseron_id),
                        dosya=file,
                        dosya_adi=dosya_adi,
                        tarih=tarih,
                        aciklama=aciklama,
                        durum=durumu,
                        tutar=tutar,
                        fatura_numarasi=fatura_no,
                        silinme_bilgisi=False
                    )
            else:
                taseron_hakedisles.objects.filter(id=button_id).update(
                    proje_ait_bilgisi=get_object_or_404(taseronlar, id=taseron_id),
                    dosya=file,
                    dosya_adi=dosya_adi,
                    tarih=tarih,
                    aciklama=aciklama,
                    durum=durumu,
                    tutar=tutar,
                    fatura_numarasi=fatura_no
                )

            return Response({"message": "Hakediş başarıyla güncellendi."}, status=status.HTTP_200_OK)

        return Response({"error": "Yetkisiz erişim."}, status=status.HTTP_403_FORBIDDEN)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def depolama_sistemim(request):
    if request.user.is_superuser:
        pass
    else:
        profile = klasorler.objects.filter(klasor_adi_db=None, silinme_bilgisi=False, dosya_sahibi=request.user)

    
    content = {}

    
    content.update({
        "santiyeler": KlasorlerSerializer(profile, many=True).data
    })

    return Response(content, status=status.HTTP_200_OK)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def klasor_olustur(request):
    if request.user.is_superuser:
        return Response({"detail": "Superuser cannot create folders."}, status=status.HTTP_403_FORBIDDEN)
    
    ust_klasor = request.data.get("ust_klasor")
    klasor = request.data.get("klasor")
    
    if ust_klasor:
        ust_klasor_instance = get_object_or_404(klasorler, id=ust_klasor)
        new_klasor = klasorler.objects.create(
            dosya_sahibi=request.user,
            klasor_adi=klasor,
            klasor_adi_db=ust_klasor_instance
        )
    else:
        new_klasor = klasorler.objects.create(
            dosya_sahibi=request.user,
            klasor_adi=klasor
        )
    
    serializer = KlasorlerSerializer(new_klasor)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def klasor_yeniden_adlandir_api(request):
    if request.user.is_superuser:
        return Response({"detail": "Superuser yetkisi ile bu işlem yapılamaz."}, status=status.HTTP_403_FORBIDDEN)
    
    klasor = request.data.get("klasor")
    idbilgisi = request.data.get("idbilgisi")

    if not klasor or not idbilgisi:
        return Response({"detail": "Gerekli tüm alanlar doldurulmalıdır."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        klasor_obj = klasorler.objects.filter(id=idbilgisi, dosya_sahibi=request.user).update(
            klasor_adi=klasor
        )
        if klasor_obj:
            return Response({"detail": "Klasör başarıyla yeniden adlandırıldı."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Klasör bulunamadı veya yetkiniz yok."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def klasor_sil_api(request):
    if request.user.is_superuser:
        return Response({"detail": "Superuser yetkisi ile bu işlem yapılamaz."}, status=status.HTTP_403_FORBIDDEN)
    
    idbilgisi = request.data.get("idbilgisi")

    if not idbilgisi:
        return Response({"detail": "ID bilgisi sağlanmalı."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        klasor = klasorler.objects.filter(id=idbilgisi, dosya_sahibi=request.user).update(
            silinme_bilgisi=True
        )
        if klasor:
            return Response({"detail": "Klasör başarıyla silindi."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Klasör bulunamadı veya yetkiniz yok."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def klasore_gir_api(request, id):
    content = {}
    content["id_bilgisi"] = id

    if super_admin_kontrolu(request):
        pass
    else:
        profile = klasorler.objects.filter(klasor_adi_db__id=id, silinme_bilgisi=False, dosya_sahibi=request.user)
        dosyalarim = klasor_dosyalari.objects.filter(silinme_bilgisi=False, dosya_sahibi=request.user, proje_ait_bilgisi__id=id)
    
    content["santiyeler"] = KlasorlerSerializer(profile,many=True).data
    content["dosyalarim"] = KlasorDosyalariSerializer(dosyalarim,many = True).data

    # Verileri JSON formatında döndür
    return Response(content, status=status.HTTP_200_OK)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dosya_ekle_api(request):
    if request.user.is_superuser:
        return Response({"detail": "Superuser has no permission to upload files."}, status=status.HTTP_403_FORBIDDEN)

    ust_klasor = request.data.get("ust_klasor")
    dosya_adi = request.data.get("dosya_adi")
    tarih = request.data.get("tarih")
    aciklama = request.data.get("aciklama")
    dosya = request.FILES.get("file")

    if not ust_klasor or not dosya:
        return Response({"detail": "Ust klasor ID and file are required."}, status=status.HTTP_400_BAD_REQUEST)

    ust_klasor_instance = get_object_or_404(klasorler, id=ust_klasor)

    yeni_dosya = klasor_dosyalari.objects.create(
        dosya_sahibi=request.user,
        proje_ait_bilgisi=ust_klasor_instance,
        dosya=dosya,
        dosya_adi=dosya_adi,
        tarih=tarih,
        aciklama=aciklama
    )



    return Response("Dosya Başarıyla Eklendi", status=status.HTTP_201_CREATED)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['get'])
@permission_classes([IsAuthenticated])
def dosya_sil_api(request):
    if request.user.is_superuser:
        return Response({"detail": "Superuser yetkisi ile bu işlem yapılamaz."}, status=status.HTTP_403_FORBIDDEN)
    
    idbilgisi = request.data.get("klasor")

    if not idbilgisi:
        return Response({"detail": "ID bilgisi sağlanmalı."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        klasor = klasor_dosyalari.objects.filter(id=idbilgisi).update(
            silinme_bilgisi=True
        )
        if klasor:
            return Response({"detail": "Dosya başarıyla silindi."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Dosya bulunamadı veya yetkiniz yok."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['get'])
@permission_classes([IsAuthenticated])
def dosya_geri_getir_api(request):
    if request.user.is_superuser:
        return Response({"detail": "Superuser yetkisi ile bu işlem yapılamaz."}, status=status.HTTP_403_FORBIDDEN)
    
    idbilgisi = request.data.get("klasor")

    if not idbilgisi:
        return Response({"detail": "ID bilgisi sağlanmalı."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        klasor = klasor_dosyalari.objects.filter(id=idbilgisi).update(
            silinme_bilgisi=False
        )
        if klasor:
            return Response({"detail": "Dosya başarıyla Geri Getirildi."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Dosya bulunamadı veya yetkiniz yok."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from functools import reduce
import operator
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dokumanlar_api(request):
    content= {}
    dosya_turu = [".xlsx", ".pdf", ".xlx", ".txt", ".docx", ".doc", ".ppt", ".pptx"]

    if super_admin_kontrolu(request):
        profile = klasor_dosyalari.objects.all()  # Super admin için tüm veriyi getir
    else:
        profile = klasor_dosyalari.objects.filter(
            dosya_sahibi=request.user,silinme_bilgisi = False
        ).filter(reduce(operator.or_, (Q(dosya__icontains=x) for x in dosya_turu)))
    content["santiyeler"]= KlasorDosyalariSerializer(profile, many=True).data
    

    return Response(content, status=status.HTTP_200_OK)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def media_dosyalari_api(request):
    content= {}
    dosya_turu = [".jpg",".jpeg",".png",".ico",".css",".JFIF",".GIF",".WEBP"]

    if super_admin_kontrolu(request):
        profile = klasor_dosyalari.objects.all()  # Super admin için tüm veriyi getir
    else:
        profile = klasor_dosyalari.objects.filter(
            dosya_sahibi=request.user,silinme_bilgisi = False
        ).filter(reduce(operator.or_, (Q(dosya__icontains=x) for x in dosya_turu)))
    content["santiyeler"]= KlasorDosyalariSerializer(profile, many=True).data
    

    return Response(content, status=status.HTTP_200_OK)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def zamana_dosyalari_api(request):
    content= {}
    dosya_turu = [".jpg",".jpeg",".png",".ico",".css",".JFIF",".GIF",".WEBP"]

    if super_admin_kontrolu(request):
        profile = klasor_dosyalari.objects.all()  # Super admin için tüm veriyi getir
    else:
        profile = klasor_dosyalari.objects.filter(
            dosya_sahibi=request.user,silinme_bilgisi = False
        ).order_by("-id")
    content["santiyeler"]= KlasorDosyalariSerializer(profile, many=True).data
    

    return Response(content, status=status.HTTP_200_OK)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def silinen_dosyalari_api(request):
    content= {}
    dosya_turu = [".jpg",".jpeg",".png",".ico",".css",".JFIF",".GIF",".WEBP"]

    if super_admin_kontrolu(request):
        profile = klasor_dosyalari.objects.all()  # Super admin için tüm veriyi getir
    else:
        profile = klasor_dosyalari.objects.filter(
            dosya_sahibi=request.user,silinme_bilgisi = True
        )
    content["santiyeler"]= KlasorDosyalariSerializer(profile, many=True).data
    

    return Response(content, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def yapilacaklar_api(request):
    content = {}
    # Süper admin kontrolü
    if super_admin_kontrolu(request):
        profile = IsplaniPlanlari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db=None, is_superuser=False).order_by("-id")
        content["kullanicilar"] = CustomUserSerializer(kullanicilar, many=True).data
    else:
        profile = IsplaniPlanlari.objects.filter(silinme_bilgisi=False, proje_ait_bilgisi=request.user)
    content["santiyeler"] = IsplaniPlanlariSerializer(profile, many=True).data
    content["isplani_dosyalari"] = IsplaniDosyalariSerializer(IsplaniDosyalari.objects.filter(proje_ait_bilgisi = request.user ), many=True).data
    content["kullanicilari"] =CustomUserSerializer( CustomUser.objects.filter(
        kullanicilar_db=request.user,
        kullanici_silme_bilgisi=False,
        is_active=True
    ),many = True).data
    
    return Response(content, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def yapilacalar_ekle_api(request):
    if request.user.is_superuser:
        return Response({"detail": "Superuser access is restricted for this endpoint."}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = IsplaniPlanlariSerializer(data=request.data)
    
    if serializer.is_valid():
        baslik = request.data.get("baslik")
        durum = request.data.get("durum")
        aciliyet = request.data.get("aciliyet")
        teslim_tarihi = request.data.get("teslim_tarihi")
        blogbilgisi = request.data.getlist("kullanicilari")
        aciklama = request.data.get("aciklama")
        katman_bilgisi = request.data.get("katman_bilgisi")
        yapi_gonder = request.data.get("yapi_gonder")
        kat = request.data.get("kat")
        locasyonx = request.data.get("locasyonx")
        locasyony = request.data.get("locasyony")
        
        new_project = IsplaniPlanlari(
            proje_ait_bilgisi=request.user,
            title=baslik,
            status=durum,
            aciklama=aciklama,
            oncelik_durumu=aciliyet,
            teslim_tarihi=teslim_tarihi,
            silinme_bilgisi=False,
            blok = get_object_or_404(bloglar,id = yapi_gonder),
            katman = get_object_or_404(katman,id = katman_bilgisi),
            kat = kat,locasyonx = locasyonx,locasyony = locasyony
        )
        new_project.save()
        
        bloglar_bilgisi = [CustomUser.objects.get(id=int(i)) for i in blogbilgisi]
        new_project.yapacaklar.add(*bloglar_bilgisi)
        
        files = request.FILES.getlist('file')
        for file in files:
            IsplaniDosyalari.objects.create(
                proje_ait_bilgisi=new_project,
                dosya_sahibi=request.user,
                dosya=file
            )
        
        return Response({"detail": "Task successfully created."}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def yapilacalar_sil(request):
    # id bilgisini al
    id_bilgisi = request.data.get('id_bilgisi')

    if not id_bilgisi:
        return Response({'error': 'ID bilgisi sağlanmalı'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Görevi güncelle
        IsplaniPlanlari.objects.filter(id=id_bilgisi).update(silinme_bilgisi=True)
        return Response({'message': 'Görev başarıyla silindi'}, status=status.HTTP_200_OK)
    except IsplaniPlanlari.DoesNotExist:
        return Response({'error': 'Görev bulunamadı'}, status=status.HTTP_404_NOT_FOUND)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def yapilacak_durumu_yenileme(request):
    # POST verilerini al
    yenilenecek_ekleme_id = request.data.get("yenilenecekeklemeyapilacak")
    aciklama = request.data.get("aciklama")
    durum = request.data.get("durum")
    teslim_tarihi = request.data.get("teslim_tarihi")

    # ID bilgisinin geçerli olup olmadığını kontrol et
    if not yenilenecek_ekleme_id:
        return Response({"error": "ID bilgisi eksik"}, status=status.HTTP_400_BAD_REQUEST)

    # IsplaniPlanlari nesnesini bul
    proje = get_object_or_404(IsplaniPlanlari, id=yenilenecek_ekleme_id)

    # Yeni ilerleme kaydını oluştur
    new_project = IsplaniPlanlariIlerleme(
        proje_ait_bilgisi=proje,
        status=durum,
        aciklama=aciklama,
        teslim_tarihi=teslim_tarihi,
        silinme_bilgisi=False,
        yapan_kisi=request.user
    )
    new_project.save()

    # Dosyaları al ve kaydet
    files = request.FILES.getlist('file')
    for file in files:
        IsplaniIlerlemeDosyalari.objects.create(
            proje_ait_bilgisi=new_project,
            yapan_kisi=request.user,
            dosya=file,
            dosya_sahibi=proje
        )

    return Response({"message": "Durum başarıyla güncellendi"}, status=status.HTTP_200_OK)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def yapilacaklar_durum_bilgisi(request):
    content = {}
    id = request.data.get("id")
    # Süper admin kontrolü
    if super_admin_kontrolu(request):
        profile = IsplaniPlanlariIlerleme.objects.filter(id = id)
        kullanicilar = CustomUser.objects.filter(kullanicilar_db=None, is_superuser=False).order_by("-id")
        content["kullanicilar"] = CustomUserSerializer(kullanicilar, many=True).data
    else:
        profile = IsplaniPlanlariIlerleme.objects.filter(id = id)
    content["santiyeler"] = IsplaniPlanlariIlerlemeSerializer(profile, many=True).data
    content["isplani_dosyalari"] = IsplaniIlerlemeDosyalariSerializer(IsplaniIlerlemeDosyalari.objects.filter(dosya_sahibi__id = id), many=True).data
    content["kullanicilari"] =CustomUserSerializer( CustomUser.objects.filter(
        kullanicilar_db=request.user,
        kullanici_silme_bilgisi=False,
        is_active=True
    ),many = True).data
    
    return Response(content, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['Get'])
@permission_classes([IsAuthenticated])
def yapilacalar_duzenle_api(request):
    if request.user.is_superuser:
        return Response({"error": "Superusers are not allowed to modify tasks."}, status=status.HTTP_403_FORBIDDEN)

    id = request.data.get("id_bilgisi")
    baslik = request.data.get("baslik")
    durum = request.data.get("durum")
    aciliyet = request.data.get("aciliyet")
    teslim_tarihi = request.data.get("teslim_tarihi")
    blogbilgisi = request.data.getlist("kullanicilari")
    aciklama = request.data.get("aciklama")
    katman_bilgisi = request.data.get("katman_bilgisi")
    yapi_gonder = request.data.get("yapi_gonder")
    kat = request.data.get("kat")
    locasyonx = request.data.get("locasyonx")
    locasyony = request.data.get("locasyony")
        
    # Get the task and update
    project = get_object_or_404(IsplaniPlanlari, id=id)
    project.proje_ait_bilgisi = request.user
    project.title = baslik
    project.status = durum
    project.aciklama = aciklama
    project.oncelik_durumu = aciliyet
    project.teslim_tarihi = teslim_tarihi
    project.silinme_bilgisi = False
    project.blok = get_object_or_404(bloglar,id = yapi_gonder)
    project.katman = get_object_or_404(katman,id = katman_bilgisi)
    project.kat = kat
    project.locasyonx = locasyonx
    project.locasyony = locasyony
    project.save()

    # Update the users assigned to the task
    bloglar_bilgisi = [CustomUser.objects.get(id=int(user_id)) for user_id in blogbilgisi]
    project.yapacaklar.set(bloglar_bilgisi)

    # Handle file uploads
    files = request.FILES.getlist('file')
    for file in files:
        IsplaniDosyalari.objects.create(
            proje_ait_bilgisi=project,
            dosya_sahibi=request.user,
            dosya=file
        )

    return Response({"message": "Task başarıyla Güncellendi."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def yapilacaklar_timeline_api(request):
    if super_admin_kontrolu(request):
        profile = YapilacakPlanlari.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db=None, is_superuser=False).order_by("-id")
    else:
        profile = YapilacakPlanlari.objects.filter(silinme_bilgisi=False, proje_ait_bilgisi=request.user).order_by("teslim_tarihi")
    content = {
        "santiyeler": YapilacakPlanlariSerializer(profile, many=True).data,
        "kullanicilarim": CustomUserSerializer(CustomUser.objects.filter(kullanicilar_db=request.user, kullanici_silme_bilgisi=False, is_active=True), many=True).data
    }

    return Response(content, status=status.HTTP_200_OK)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def yapilacalar_time_line_ekle_api(request):
    if request.user.is_superuser:
        return Response({"detail": "Superuser cannot add tasks."}, status=status.HTTP_403_FORBIDDEN)

    serializer = YapilacakPlanlariSerializer(data=request.data)
    if serializer.is_valid():
        baslik = serializer.validated_data.get("baslik")
        durum = serializer.validated_data.get("durum")
        aciliyet = serializer.validated_data.get("aciliyet")
        teslim_tarihi = serializer.validated_data.get("teslim_tarihi")
        aciklama = serializer.validated_data.get("aciklama")
        blogbilgisi = request.data.getlist("kullanicilari")
        images = request.FILES.getlist('file')

        new_project = YapilacakPlanlari(
            proje_ait_bilgisi=request.user,
            title=baslik,
            status=durum,
            aciklama=aciklama,
            oncelik_durumu=aciliyet,
            teslim_tarihi=teslim_tarihi,
            silinme_bilgisi=False
        )
        new_project.save()

        bloglar_bilgisi = [get_object_or_404(CustomUser, id=int(i)) for i in blogbilgisi]
        new_project.yapacaklar.add(*bloglar_bilgisi)

        for image in images:
            YapilacakDosyalari.objects.create(
                proje_ait_bilgisi=new_project,
                dosya_sahibi=request.user,
                dosya=image
            )

        return Response(YapilacakPlanlariSerializer(new_project).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def yapilacalar_time_line_sil_api(request):
    id_bilgisi = request.data.get('id_bilgisi')

    if not id_bilgisi:
        return Response({'error': 'ID bilgisi sağlanmalı'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Görevi güncelle
        YapilacakPlanlari.objects.filter(id=id_bilgisi).update(silinme_bilgisi=True)
        return Response({'message': 'Yapılacak başarıyla silindi'}, status=status.HTTP_200_OK)
    except YapilacakPlanlari.DoesNotExist:
        return Response({'error': 'Yapılacak bulunamadı'}, status=status.HTTP_404_NOT_FOUND)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def yapilacaklar_time_line_duzenle_api(request):
    id = request.data.get("id")
    baslik = request.data.get("baslik")
    durum = request.data.get("durum")
    aciliyet = request.data.get("aciliyet")
    teslim_tarihi = request.data.get("teslim_tarihi")
    aciklama = request.data.get("aciklama")
    blogbilgisi = request.data.get("kullanicilari", [])

    # Belirtilen ID'ye sahip YapilacakPlanlari nesnesini güncelle
    yapilacak = get_object_or_404(YapilacakPlanlari, id=id)

    if not request.user.is_superuser:
        yapilacak.proje_ait_bilgisi = request.user
    
    yapilacak.title = baslik
    yapilacak.status = durum
    yapilacak.aciklama = aciklama
    yapilacak.oncelik_durumu = aciliyet
    yapilacak.teslim_tarihi = teslim_tarihi
    yapilacak.silinme_bilgisi = False
    yapilacak.save()

    # Blog bilgilerini güncelle
    if blogbilgisi:
        bloglar_bilgisi = CustomUser.objects.filter(id__in=blogbilgisi)
        yapilacak.yapacaklar.set(bloglar_bilgisi)

    # Dosyaları ekle
    images = request.FILES.getlist('file')
    for image in images:
        YapilacakDosyalari.objects.create(
            proje_ait_bilgisi=yapilacak,
            dosya_sahibi=request.user,
            dosya=image
        )
    
    return Response({"detail": "Yapılacak plan başarıyla güncellendi."}, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def santiye_raporu_api(request, id):
    try:
        profile = get_object_or_404(bloglar, proje_ait_bilgisi=request.user, id=id)
        content = {
            "santiye": BloglarSerializer(profile).data 
        }
        return Response(content, status=status.HTTP_200_OK)
    except bloglar.DoesNotExist:
        return Response({"detail": "Santiye raporu bulunamadı."}, status=status.HTTP_404_NOT_FOUND)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_katman_ekle(request):
    if request.user.is_superuser:
        kullanici = request.data.get("kullanici")
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_404(bagli_kullanicilar, kullanicilar=request.user)
            if a and a.izinler.katman_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return Response({"detail": "Yetkiniz yok."}, status=status.HTTP_403_FORBIDDEN)
        else:
            kullanici = request.user

    katman_adi = request.data.get("taseron_adi")
    santiye_al = request.data.get("blogbilgisi")
    dosya = request.FILES.get("file")
    
    katman_instance = katman.objects.create(
        proje_ait_bilgisi=kullanici,
        proje_santiye_Ait=get_object_or_404(santiye, id=santiye_al),
        katman_adi=katman_adi,
        katman_dosyasi=dosya
    )
    
    return Response({"detail": "Katman başarıyla eklendi.", "katman_id": katman_instance.id}, status=status.HTTP_201_CREATED)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_katman_sil(request):
    buttonIdInput = request.data.get("buttonId")
    
    if request.user.is_superuser:
        katman.objects.filter(id=buttonIdInput).update(silinme_bilgisi=True)
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_404(bagli_kullanicilar, kullanicilar=request.user)
            if a and a.izinler.katman_silme:
                katman.objects.filter(id=buttonIdInput).update(silinme_bilgisi=True)
            else:
                return Response({"detail": "Yetkiniz yok."}, status=status.HTTP_403_FORBIDDEN)
        else:
            katman.objects.filter(id=buttonIdInput).update(silinme_bilgisi=True)
    
    return Response({"detail": "Katman başarıyla silindi."}, status=status.HTTP_200_OK)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_katman_duzenle(request):
    buttonId = request.data.get("buttonId")
    
    if request.user.is_superuser:
        kullanici = request.data.get("kullanici")
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_404(bagli_kullanicilar, kullanicilar=request.user)
            if a and a.izinler.katman_olusturma:
                kullanici = request.user.kullanicilar_db
            else:
                return Response({"detail": "Yetkiniz yok."}, status=status.HTTP_403_FORBIDDEN)
        else:
            kullanici = request.user
    
    katman_adi = request.data.get("taseron_adi")
    santiye_al = request.data.get("blogbilgisi")
    dosya = request.FILES.get("file")

    update_fields = {
        "proje_ait_bilgisi": kullanici,
        "proje_santiye_Ait": get_object_or_404(santiye, id=santiye_al),
        "katman_adi": katman_adi,
    }
    
    if dosya:
        update_fields["katman_dosyasi"] = dosya

    katman.objects.filter(id=buttonId).update(**update_fields)
    
    return Response({"detail": "Katman başarıyla güncellendi."}, status=status.HTTP_200_OK)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_katman_sayfasi(request):
    content = {}
    
    # Check for super admin
    if request.user.is_superuser:
        content["profile"] = katman.objects.all().values()
        content["kullanicilar"] = CustomUser.objects.filter(kullanicilar_db=None, is_superuser=False).order_by("-id").values()
    else:
        # Regular user with `kullanicilar_db` access level
        if request.user.kullanicilar_db:
            a = get_object_or_404(bagli_kullanicilar, kullanicilar=request.user)
            if a and a.izinler.katman_gorme:
                content["profile"] = katman.objects.filter(silinme_bilgisi=False, proje_ait_bilgisi=request.user.kullanicilar_db).values()
                content["insaatlar"] = santiye.objects.filter(proje_ait_bilgisi=request.user.kullanicilar_db, silinme_bilgisi=False).values()
            else:
                return Response({"detail": "Yetkiniz yok."}, status=status.HTTP_403_FORBIDDEN)
        else:
            content["profile"] = katman.objects.filter(silinme_bilgisi=False, proje_ait_bilgisi=request.user).values()
            content["insaatlar"] = santiye.objects.filter(proje_ait_bilgisi=request.user, silinme_bilgisi=False).values()

    content["santiyeler"] = content.get("profile", [])
    content["top"] = content.get("profile", [])
    content["medya"] = content.get("profile", [])

    return Response(content, status=status.HTTP_200_OK)

