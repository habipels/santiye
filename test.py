import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def save_template(request):
    if request.user.kullanicilar_db:
        a = get_object_or_none(bagli_kullanicilar, kullanicilar=request.user)
        if a:
            if a.izinler.santiye_kontrol:
                kullanici = request.user.kullanicilar_db
            else:
                return redirect("main:yetkisiz")
        else:
            return redirect("main:yetkisiz")
    else:
        kullanici = request.user

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Şablonu oluştur
            sablon = santiye_sablonlari.objects.create(
                proje_ait_bilgisi=kullanici,
                sablon_adi=data.get('name', 'Unnamed Template'),
                sablon_durumu=data.get('projectType', 'Unknown'),
                proje_santiye_Ait=get_object_or_none(santiye, id=data.get('santiyeId', 'Unknown'))
            )

            for section_data in data.get('sections', []):
                sablon_bolumleri = sanytiye_sablon_bolumleri.objects.create(
                    proje_ait_bilgisi=kullanici,
                    proje_santiye_Ait=get_object_or_none(santiye, id=data.get('santiyeId', 'Unknown')),
                    sablon_adi=get_object_or_none(santiye_sablonlari, id=sablon.id),
                    bolum=section_data.get('type', 'Unknown')
                )
                for category_data in section_data.get('categories', []):
                    sablon_imalat_olayi = santiye_imalat_kalemleri.objects.create(
                        proje_ait_bilgisi=kullanici,
                        proje_santiye_Ait=get_object_or_none(santiye, id=data.get('santiyeId', 'Unknown')),
                        detay=get_object_or_none(sanytiye_sablon_bolumleri, id=sablon_bolumleri.id),
                        icerik=category_data.get('name', 'Unnamed Category'),
                        is_grubu=category_data.get('workGroup', 'Unknown Work Group')
                    )
                    for item_name in category_data.get('checklistItems', []):
                        imalat_kalemleri_imalat_detaylari.objects.create(
                            proje_ait_bilgisi=kullanici,
                            proje_santiye_Ait=get_object_or_none(santiye, id=data.get('santiyeId', 'Unknown')),
                            icerik=get_object_or_none(santiye_imalat_kalemleri, id=sablon_imalat_olayi.id),
                            imalat_detayi=item_name
                        )
            return JsonResponse({"status": "success", "message": "Şablon başarıyla kaydedildi."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
