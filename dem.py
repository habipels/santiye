if request.user.kullanicilar_db:
            a = get_object_or_none(bagli_kullanicilar,kullanicilar = request.user)
            if a:
                if a.izinler.blog_olusturma:
                    pass
                else:
                    return redirect("main:yetkisiz")
            else:
                return redirect("main:yetkisiz")
        else: