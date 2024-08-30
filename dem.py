#
        santiye_raporu_gorme = request.POST.get("santiye_raporu_gorme")
        if santiye_raporu_gorme:
            izinler.santiye_raporu_gorme = True
        santiye_raporu_olusturma  = request.POST.get("santiye_raporu_olusturma")
        if santiye_raporu_olusturma:
            izinler.santiye_raporu_olusturma = True
        santiye_raporu_duzenleme = request.POST.get("santiye_raporu_duzenleme")
        if santiye_raporu_duzenleme:
            izinler.santiye_raporu_duzenleme = True
        santiye_raporu_silme = request.POST.get("santiye_raporu_silme")
        if santiye_raporu_silme:
            izinler.santiye_raporu_silme = True