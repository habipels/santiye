katman_olusturma = request.POST.get("katman_olusturma")
        if katman_olusturma:
            izinler.katman_olusturma = True
        katman_silme = request.POST.get("katman_silme")
        if katman_silme:
            izinler.katman_silme = True
        katman_gorme = request.POST.get("katman_gorme")
        if katman_gorme:
            izinler.katman_gorme = True
        katman_duzenleme = request.POST.get("katman_duzenleme")
        if katman_duzenleme:
            izinler.katman_duzenleme = True