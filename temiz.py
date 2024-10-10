
def katman_sayfasi(request):
    content = sozluk_yapisi()
    if super_admin_kontrolu(request):
        profile =proje_tipi.objects.all()
        kullanicilar = CustomUser.objects.filter(kullanicilar_db = None,is_superuser = False).order_by("-id")
        content["kullanicilar"] =kullanicilar
    else:
        if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.projeler_gorme:
                    profile = proje_tipi.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user.kullanicilar_db)
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else:
            profile = proje_tipi.objects.filter(silinme_bilgisi = False,proje_ait_bilgisi = request.user)
    if request.GET.get("search"):
        search = request.GET.get("search")
        if super_admin_kontrolu(request):
            profile =proje_tipi.objects.filter(Q(proje_ait_bilgisi__last_name__icontains = search)|Q(Proje_tipi_adi__icontains = search))
            kullanicilar = CustomUser.objects.filter( kullanicilar_db = None,is_superuser = False).order_by("-id")
            content["kullanicilar"] =kullanicilar
        else:
            if request.user.kullanicilar_db:
                a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
                if a:
                    if a.izinler.projeler_gorme:
                        profile = proje_tipi.objects.filter(Q(proje_ait_bilgisi = request.user.kullanicilar_db) & Q(Proje_tipi_adi__icontains = search)& Q(silinme_bilgisi = False))

                    else:
                        return redirect("main:yetkisiz")
                else:
                    return redirect("main:yetkisiz")
            else:
                profile = proje_tipi.objects.filter(Q(proje_ait_bilgisi = request.user) & Q(Proje_tipi_adi__icontains = search)& Q(silinme_bilgisi = False))
    
    content["santiyeler"] = profile
    content["top"]  = profile
    content["medya"] = profile
    return render(request,"santiye_yonetimi/katman.html",content)