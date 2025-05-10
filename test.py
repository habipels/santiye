def kullanici_yetki_alma(request):
    if request.user.kullanicilar_db:
        return redirect_with_language("main:yetkisiz")
    if request.POST:
        guncellenen = request.POST.get("guncellenen")
        izinler = get_object_or_404(personel_izinleri,id = guncellenen) 
        ##
        #izinleri Sıfırla
        izinler.dashboard_gorme = False
        izinler.dashboard_silme = False
        izinler.dashboard_duzenleme = False
        izinler.dashboard_olusturma = False
        #
        izinler.gelir_ozeti_gorme = False
        izinler.gelir_ozeti_olusturma = False
        izinler.gelir_ozeti_duzenleme =False
        izinler.gelir_ozeti_silme = False
        #
        izinler.gider_ozeti_gorme = False
        izinler.gider_ozeti_olusturma = False
        izinler.gider_ozeti_duzenleme = False
        izinler.gider_ozeti_silme = False
        #
        izinler.hesap_ekstra_gorme = False
        izinler.hesap_ekstra_olusturma = False
        izinler.hesap_ekstra_duzenleme = False
        izinler.hesap_ekstra_silme = False
        #
        izinler.ilerleme_takibi_gorme = False
        izinler.ilerleme_takibi_olusturma = False
        izinler.ilerleme_takibi_duzenleme = False
        izinler.ilerleme_takibi_silme = False
        #
        izinler.sozlesmeler_gorme = False
        izinler.sozlesmeler_olusturma = False
        izinler.sozlesmeler_duzenleme = False
        izinler.sozlesmeler_silme = False
        #
        izinler.yapilacaklar_gorme = False
        izinler.yapilacaklar_olusturma = False
        izinler.yapilacaklar_duzenleme = False
        izinler.yapilacaklar_silme = False
        #
        izinler.dosya_yoneticisi_gorme = False
        izinler.dosya_yoneticisi_olusturma = False
        izinler.dosya_yoneticisi_duzenleme = False
        izinler.dosya_yoneticisi_silme = False
        #
        izinler.projeler_gorme = False
        izinler.projeler_olusturma = False
        izinler.projeler_duzenleme = False
        izinler.projeler_silme =False
        #
        izinler.personeller_gorme = False
        izinler.personeller_olusturma = False
        izinler.personeller_duzenleme = False
        izinler.personeller_silme = False
        #
        izinler.gelir_faturasi_gorme_izni = False
        izinler.gelir_faturasi_kesme_izni = False
        izinler.gelir_faturasi_duzenleme_izni = False
        izinler.gelir_faturasi_silme_izni = False
        #
        izinler.gider_faturasi_gorme_izni = False
        izinler.gider_faturasi_kesme_izni = False
        izinler.gider_faturasi_duzenleme_izni = False
        izinler.gider_faturasi_silme_izni = False
        #
        izinler.kasa_virman_olusturma_izni = False
        izinler.kasa_virman_gorme_izni = False
        #
        izinler.kasa_gosterme_izni = False
        izinler.kasa_olusturma_izni = False
        izinler.kasa_guncelleme_izni = False
        izinler.Kasa_silme_izni = False
        #
        izinler.cari_gosterme_izni = False
        izinler.cari_olusturma = False
        izinler.cari_guncelleme_izni = False
        izinler.cari_silme_izni = False
        #
        izinler.personeller_gorme = False
        izinler.personeller_olusturma = False
        izinler.personeller_duzenleme = False
        izinler.personeller_silme = False
        #
        izinler.santiye_olusturma = False
        izinler.santiye_silme = False
        izinler.santiye_gorme = False
        izinler.santiye_duzenleme = False
        #
        izinler.blog_olusturma = False
        izinler.blog_silme = False
        izinler.blog_gorme = False
        izinler.blog_duzenleme = False
        #
        izinler.kalemleri_olusturma = False
        izinler.kalemleri_silme = False
        izinler.kalemleri_gorme = False
        izinler.kalemleri_duzenleme = False
        #
        izinler.santiye_raporu_olusturma = False
        izinler.santiye_raporu_silme = False
        izinler.santiye_raporu_gorme = False
        izinler.santiye_raporu_duzenleme = False
        #
        izinler.taseronlar_gorme = False
        izinler.taseronlar_olusturma = False
        izinler.taseronlar_duzenleme = False
        izinler.taseronlar_silme =False
        #
        izinler.hakedisler_gorme = False
        izinler.hakedisler_olusturma = False
        izinler.hakedisler_duzenleme = False
        izinler.hakedisler_silme = False
        #
        izinler.kasa_detay_izni = False
        izinler.cari_detay_izni = False
        ##
        izinler.gelir_kategorisi_gorme = False
        izinler.gelir_kategorisi_olusturma = False
        izinler.gelir_kategorisi_guncelleme = False
        izinler.gelir_kategorisi_silme = False
        #
        izinler.gider_kategorisi_gorme = False
        izinler.gider_kategorisi_olusturma = False
        izinler.gider_kategorisi_guncelleme = False
        izinler.gider_kategorisi_silme = False
        #
        izinler.gelir_etiketi_gorme = False
        izinler.gelir_etiketi_olusturma = False
        izinler.gelir_etiketi_guncelleme = False
        izinler.gelir_etiketi_silme = False
        #
        izinler.gider_etiketi_gorme = False
        izinler.gider_etiketi_olusturma = False
        izinler.gider_etiketi_guncelleme = False
        izinler.gider_etiketi_silme = False
        #
        izinler.urun_gorme = False
        izinler.urun_olusturma = False
        izinler.urun_guncelleme = False
        izinler.urun_silme = False
        #
        izinler.muhasabe_ayarlari_gorme = False
        izinler.muhasabe_ayarlari_guncelleme = False
        #
        izinler.gelir_faturasi_makbuz_gorme_izni = False
        izinler.gelir_faturasi_makbuz_kesme_izni = False
        izinler.gelir_faturasi_makbuz_duzenleme_izni = False
        izinler.gelir_faturasi_makbuz_silme_izni = False
        #
        izinler.gider_faturasi_makbuz_gorme_izni = False
        izinler.gider_faturasi_makbuz_kesme_izni = False
        izinler.gider_faturasi_makbuz_duzenleme_izni = False
        izinler.gider_faturasi_makbuz_silme_izni = False
        #Puantaj
        izinler.personeller_puantaj_olusturma = False
        izinler.personeller_puantaj_silme = False
        izinler.personeller_puantaj_gorme = False
        izinler.personeller_puantaj_duzenleme = False
        #
        # 
        izinler.personeller_odeme_olusturma = False
        izinler.personeller_odeme_silme = False
        izinler.personeller_odeme_gorme = False
        izinler.personeller_odeme_duzenleme = False
        #
        izinler.katman_olusturma = False
        izinler.katman_silme = False
        izinler.katman_gorme = False
        izinler.katman_duzenleme = False
        #
        izinler.gant_olusturma = False
        izinler.gant_gorme = False
        izinler.gant_duzenleme = False
        #
        izinler.genel_rapor_olusturma = False
        izinler.genel_rapor_gorme = False
        izinler.genel_rapor_duzenleme = False
        izinler.genel_rapor_silme = False
        izinler.genel_rapor_onaylama = False
        izinler.satin_alma_talebi_olusturma = False
        izinler.satin_alma_talebi_silme = False
        izinler.satin_alma_talebi_gorme = False
        izinler.satin_alma_talebi_duzenleme = False

        izinler.satin_alma_talebi_onaylama_olusturma = False
        izinler.satin_alma_talebi_onaylama_silme = False
        izinler.satin_alma_talebi_onaylama_gorme = False
        izinler.satin_alma_talebi_onaylama_duzenleme = False

        izinler.stok_olusturma = False

        izinler.stok_talebi_onaylama_silme = False
        izinler.stok_talebi_onaylama_gorme = False
        izinler.stok_talebi_onaylama_duzenleme = False

        izinler.zimmet_olusturma = False
        izinler.zimmet_silme = False
        izinler.zimmet_gorme = False

        izinler.rapor_olusturucu_gorme = False
        izinler.rapor_olusturucu_olusturma = False

        izinler.musteri_olusturma = False
        izinler.musteri_gorme = False
        izinler.musteri_duzenleme = False
        izinler.musteri_silme = False
        izinler.crm_musteri_olusturma = False
        izinler.crm_musteri_silme = False
        izinler.crm_musteri_gorme = False
        izinler.crm_musteri_duzenleme = False
        izinler.crm_talep_olusturma = False
        izinler.crm_talep_silme = False
        izinler.crm_talep_gorme = False
        izinler.crm_talep_duzenleme = False
        izinler.crm_teklif_olusturma = False
        izinler.crm_teklif_silme = False
        izinler.crm_teklif_gorme = False
        izinler.crm_teklif_duzenleme = False
        izinler.crm_daire_olusturma = False
        izinler.crm_daire_silme = False
        izinler.crm_daire_gorme = False
        izinler.crm_daire_duzenleme = False
        izinler.crm_evrak_olusturma = False
        izinler.crm_evrak_silme = False
        izinler.crm_evrak_gorme = False
        izinler.crm_evrak_duzenleme = False

        izinler.save()
        ##
        personeller_puantaj_olusturma = request.POST.get("personeller_puantaj_olusturma")
        if personeller_puantaj_olusturma:
            izinler.personeller_puantaj_olusturma = True
        personeller_puantaj_silme = request.POST.get("personeller_puantaj_silme")
        if personeller_puantaj_silme:
            izinler.personeller_puantaj_silme = True
        personeller_puantaj_gorme = request.POST.get("personeller_puantaj_gorme")
        if personeller_puantaj_gorme:
            izinler.personeller_puantaj_gorme = True
        personeller_puantaj_duzenleme = request.POST.get("personeller_puantaj_duzenleme")
        if personeller_puantaj_duzenleme:
            izinler.personeller_puantaj_duzenleme = True
        #
        personeller_odeme_olusturma = request.POST.get("personeller_odeme_olusturma")
        if personeller_odeme_olusturma:
            izinler.personeller_odeme_olusturma = True
        personeller_odeme_silme = request.POST.get("personeller_odeme_silme")
        if personeller_odeme_silme:
            izinler.personeller_odeme_silme = True
        personeller_odeme_gorme = request.POST.get("personeller_odeme_gorme")
        if personeller_odeme_gorme:
            izinler.personeller_odeme_gorme = True
        personeller_odeme_duzenleme = request.POST.get("personeller_odeme_duzenleme")
        if personeller_odeme_duzenleme:
            izinler.personeller_odeme_duzenleme = True
        #
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
        ##
        dashboard_gorme = request.POST.get("dashboard_gorme")
        if dashboard_gorme:
            izinler.dashboard_gorme = True
        dashboard_silme = request.POST.get("dashboard_silme")
        if dashboard_silme:
            izinler.dashboard_silme = True
        dashboard_duzenleme = request.POST.get("dashboard_duzenleme")
        if dashboard_duzenleme:
            izinler.dashboard_duzenleme = True
        dashboard_olusturma = request.POST.get("dashboard_olusturma")
        if dashboard_olusturma:
            izinler.dashboard_olusturma = True
        #
        gelir_ozeti_gorme = request.POST.get("gelir_ozeti_gorme")
        if gelir_ozeti_gorme:
            izinler.gelir_ozeti_gorme = True
        gelir_ozeti_olusturma = request.POST.get("gelir_ozeti_olusturma")
        if gelir_ozeti_olusturma:
            izinler.gelir_ozeti_olusturma = True
        gelir_ozeti_duzenleme = request.POST.get("gelir_ozeti_duzenleme")
        if gelir_ozeti_duzenleme:
            izinler.gelir_ozeti_duzenleme = True
        gelir_ozeti_silme = request.POST.get("gelir_ozeti_silme")
        if gelir_ozeti_silme:
            izinler.gelir_ozeti_silme = True
        #
        gider_ozeti_gorme = request.POST.get("gider_ozeti_gorme")
        if gider_ozeti_gorme:
            izinler.gider_ozeti_gorme = True
        gider_ozeti_olusturma = request.POST.get("gider_ozeti_olusturma")
        if gider_ozeti_olusturma:
            izinler.gider_ozeti_olusturma = True
        gider_ozeti_duzenleme = request.POST.get("gider_ozeti_duzenleme")
        if gider_ozeti_duzenleme:
            izinler.gider_ozeti_duzenleme = True
        gider_ozeti_silme = request.POST.get("gider_ozeti_silme")
        if gider_ozeti_silme:
            izinler.gider_ozeti_silme = True
        #
        hesap_ekstra_gorme = request.POST.get("hesap_ekstra_gorme")
        if hesap_ekstra_gorme:
            izinler.hesap_ekstra_gorme = True
        hesap_ekstra_olusturma = request.POST.get("hesap_ekstra_olusturma")
        if hesap_ekstra_olusturma:
            izinler.hesap_ekstra_olusturma = True
        hesap_ekstra_duzenleme = request.POST.get("hesap_ekstra_duzenleme")
        if hesap_ekstra_duzenleme:
            izinler.hesap_ekstra_duzenleme = True
        hesap_ekstra_silme = request.POST.get("hesap_ekstra_silme")
        if hesap_ekstra_silme:
            izinler.hesap_ekstra_silme = True
        #
        kasa_virman_olusturma_izni = request.POST.get("kasa_virman_olusturma_izni")
        if kasa_virman_olusturma_izni:
            izinler.kasa_virman_olusturma_izni = True
        kasa_virman_gorme_izni = request.POST.get("kasa_virman_gorme_izni")
        if kasa_virman_gorme_izni:
            izinler.kasa_virman_gorme_izni = True
        #
        ilerleme_takibi_gorme = request.POST.get("ilerleme_takibi_gorme")
        if ilerleme_takibi_gorme:
            izinler.ilerleme_takibi_gorme = True
        ilerleme_takibi_olusturma = request.POST.get("ilerleme_takibi_olusturma")
        if ilerleme_takibi_olusturma:
            izinler.ilerleme_takibi_olusturma = True
        ilerleme_takibi_duzenleme = request.POST.get("ilerleme_takibi_duzenleme")
        if ilerleme_takibi_duzenleme:
            izinler.ilerleme_takibi_duzenleme = True
        ilerleme_takibi_silme = request.POST.get("ilerleme_takibi_silme")
        if ilerleme_takibi_silme:
            izinler.ilerleme_takibi_silme = True
        #
        sozlesmeler_gorme = request.POST.get("sozlesmeler_gorme")
        if sozlesmeler_gorme:
            izinler.sozlesmeler_gorme = True
        sozlesmeler_olusturma = request.POST.get("sozlesmeler_olusturma")
        if sozlesmeler_olusturma:
            izinler.sozlesmeler_olusturma = True
        sozlesmeler_duzenleme = request.POST.get("sozlesmeler_duzenleme")
        if sozlesmeler_duzenleme:
            izinler.sozlesmeler_duzenleme = True
        sozlesmeler_silme = request.POST.get("sozlesmeler_silme")
        if sozlesmeler_silme:
            izinler.sozlesmeler_silme = True
        #
        yapilacaklar_gorme = request.POST.get("yapilacaklar_gorme")
        if yapilacaklar_gorme:
            izinler.yapilacaklar_gorme = True
        yapilacaklar_olusturma = request.POST.get("yapilacaklar_olusturma")
        if yapilacaklar_olusturma:
            izinler.yapilacaklar_olusturma = True
        yapilacaklar_duzenleme = request.POST.get("yapilacaklar_duzenleme")
        if yapilacaklar_duzenleme:
            izinler.yapilacaklar_duzenleme = True
        yapilacaklar_silme = request.POST.get("yapilacaklar_silme")
        if yapilacaklar_silme:
            izinler.yapilacaklar_silme = True
        #
        dosya_yoneticisi_gorme = request.POST.get("dosya_yoneticisi_gorme")
        if dosya_yoneticisi_gorme:
            izinler.dosya_yoneticisi_gorme = True
        dosya_yoneticisi_olusturma = request.POST.get("dosya_yoneticisi_olusturma")
        if dosya_yoneticisi_olusturma:
            izinler.dosya_yoneticisi_olusturma = True
        dosya_yoneticisi_duzenleme = request.POST.get("dosya_yoneticisi_duzenleme")
        if dosya_yoneticisi_duzenleme:
            izinler.dosya_yoneticisi_duzenleme = True
        dosya_yoneticisi_silme = request.POST.get("dosya_yoneticisi_silme")
        if dosya_yoneticisi_silme:
            izinler.dosya_yoneticisi_silme = True
        #
        projeler_gorme = request.POST.get("projeler_gorme")
        if projeler_gorme:
            izinler.projeler_gorme = True
        projeler_olusturma = request.POST.get("projeler_olusturma")
        if projeler_olusturma:
            izinler.projeler_olusturma = True
        projeler_duzenleme = request.POST.get("projeler_duzenleme")
        if projeler_duzenleme:
            izinler.projeler_duzenleme = True
        projeler_silme = request.POST.get("projeler_silme")
        if projeler_silme:
            izinler.projeler_silme = True

        #
        personeller_gorme = request.POST.get("personeller_gorme")
        if personeller_gorme:
            izinler.personeller_gorme = True
        personeller_olusturma = request.POST.get("personeller_olusturma")
        if personeller_olusturma:
            izinler.personeller_olusturma = True
        personeller_duzenleme = request.POST.get("personeller_duzenleme")
        if personeller_duzenleme:
            izinler.personeller_duzenleme = True
        personeller_silme = request.POST.get("personeller_silme")
        if personeller_silme:
            izinler.personeller_silme = True
        #
        gelir_faturasi_gorme_izni = request.POST.get("gelir_faturasi_gorme_izni")
        if gelir_faturasi_gorme_izni:
            izinler.gelir_faturasi_gorme_izni = True
        gelir_faturasi_kesme_izni = request.POST.get("gelir_faturasi_kesme_izni")
        if gelir_faturasi_kesme_izni:
            izinler.gelir_faturasi_kesme_izni = True
        gelir_faturasi_duzenleme_izni = request.POST.get("gelir_faturasi_duzenleme_izni")
        if gelir_faturasi_duzenleme_izni:
            izinler.gelir_faturasi_duzenleme_izni = True
        gelir_faturasi_silme_izni = request.POST.get("gelir_faturasi_silme_izni")
        if gelir_faturasi_silme_izni:
            izinler.gelir_faturasi_silme_izni = True
        #
        gider_faturasi_gorme_izni = request.POST.get("gider_faturasi_gorme_izni")
        if gider_faturasi_gorme_izni:
            izinler.gider_faturasi_gorme_izni = True
        gider_faturasi_kesme_izni = request.POST.get("gider_faturasi_kesme_izni")
        if gider_faturasi_kesme_izni:
            izinler.gider_faturasi_kesme_izni = True
        gider_faturasi_duzenleme_izni = request.POST.get("gider_faturasi_duzenleme_izni")
        if gider_faturasi_duzenleme_izni:
            izinler.gider_faturasi_duzenleme_izni = True
        gider_faturasi_silme_izni = request.POST.get("gider_faturasi_silme_izni")
        if gider_faturasi_silme_izni:
            izinler.gider_faturasi_silme_izni = True
        #
        
        kasa_gosterme_izni = request.POST.get("kasa_gosterme_izni")
        if kasa_gosterme_izni:
            izinler.kasa_gosterme_izni = True
        kasa_olusturma_izni = request.POST.get("kasa_olusturma_izni")
        if kasa_olusturma_izni:
            izinler.kasa_olusturma_izni = True
        kasa_guncelleme_izni = request.POST.get("kasa_guncelleme_izni")
        if kasa_guncelleme_izni:
            izinler.kasa_guncelleme_izni = True
        Kasa_silme_izni = request.POST.get("Kasa_silme_izni")
        if Kasa_silme_izni:
            izinler.Kasa_silme_izni = True
        #
        cari_gosterme_izni = request.POST.get("cari_gosterme_izni")
        if cari_gosterme_izni:
            izinler.cari_gosterme_izni = True
        cari_olusturma = request.POST.get("cari_olusturma")
        if cari_olusturma:
            izinler.cari_olusturma = True
        cari_guncelleme_izni = request.POST.get("cari_guncelleme_izni")
        if cari_guncelleme_izni:
            izinler.cari_guncelleme_izni = True
        cari_silme_izni = request.POST.get("cari_silme_izni")
        if cari_silme_izni:
            izinler.cari_silme_izni = True
        #
        personeller_gorme = request.POST.get("personeller_gorme")
        if personeller_gorme:
            izinler.personeller_gorme = True
        personeller_olusturma = request.POST.get("personeller_olusturma")
        if personeller_olusturma:
            izinler.personeller_olusturma = True
        personeller_duzenleme = request.POST.get("personeller_duzenleme")
        if personeller_duzenleme:
            izinler.personeller_duzenleme = True
        personeller_silme = request.POST.get("personeller_silme")
        if personeller_silme:
            izinler.personeller_silme = True
        #
        santiye_gorme = request.POST.get("santiye_gorme")
        if santiye_gorme:
            izinler.santiye_gorme = True
        santiye_olusturma  = request.POST.get("santiye_olusturma")
        if santiye_olusturma:
            izinler.santiye_olusturma = True
        santiye_duzenleme = request.POST.get("santiye_duzenleme")
        if santiye_duzenleme:
            izinler.santiye_duzenleme = True
        santiye_silme = request.POST.get("santiye_silme")
        if santiye_silme:
            izinler.santiye_silme = True
        #
        blog_gorme = request.POST.get("blog_gorme")
        if blog_gorme:
            izinler.blog_gorme = True
        blog_olusturma  = request.POST.get("blog_olusturma")
        if blog_olusturma:
            izinler.blog_olusturma = True
        blog_duzenleme = request.POST.get("blog_duzenleme")
        if blog_duzenleme:
            izinler.blog_duzenleme = True
        blog_silme = request.POST.get("blog_silme")
        if blog_silme:
            izinler.blog_silme = True
        #
        kalemleri_gorme = request.POST.get("kalemleri_gorme")
        if kalemleri_gorme:
            izinler.kalemleri_gorme = True
        kalemleri_olusturma  = request.POST.get("kalemleri_olusturma")
        if kalemleri_olusturma:
            izinler.kalemleri_olusturma = True
        kalemleri_duzenleme = request.POST.get("kalemleri_duzenleme")
        if kalemleri_duzenleme:
            izinler.kalemleri_duzenleme = True
        kalemleri_silme = request.POST.get("kalemleri_silme")
        if kalemleri_silme:
            izinler.kalemleri_silme = True
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
        #
        taseronlar_gorme = request.POST.get("taseronlar_gorme")
        if taseronlar_gorme:
            izinler.taseronlar_gorme = True
        taseronlar_olusturma = request.POST.get("taseronlar_olusturma")
        if taseronlar_olusturma:
            izinler.taseronlar_olusturma = True
        taseronlar_duzenleme = request.POST.get("taseronlar_duzenleme")
        if taseronlar_duzenleme:
            izinler.taseronlar_duzenleme = True
        taseronlar_silme = request.POST.get("taseronlar_silme")
        if taseronlar_silme:
            izinler.taseronlar_silme = True
        #
        hakedisler_gorme = request.POST.get("hakedisler_gorme")
        if hakedisler_gorme:
            izinler.hakedisler_gorme = True
        hakedisler_olusturma = request.POST.get("hakedisler_olusturma")
        if hakedisler_olusturma:
            izinler.hakedisler_olusturma = True
        hakedisler_duzenleme = request.POST.get("hakedisler_duzenleme")
        if hakedisler_duzenleme:
            izinler.hakedisler_duzenleme = True
        hakedisler_silme = request.POST.get("hakedisler_silme")
        if hakedisler_silme:
            izinler.hakedisler_silme = True
        #
        kasa_detay_izni = request.POST.get("kasa_detay_izni")
        if kasa_detay_izni:
            izinler.kasa_detay_izni = True
        cari_detay_izni = request.POST.get("cari_detay_izni")
        if cari_detay_izni:
            izinler.cari_detay_izni = True
        
        #
        gelir_kategorisi_gorme = request.POST.get("gelir_kategorisi_gorme")
        if gelir_kategorisi_gorme:  
            izinler.gelir_kategorisi_gorme = True
        gelir_kategorisi_olusturma = request.POST.get("gelir_kategorisi_olusturma")
        if gelir_kategorisi_olusturma : 
            izinler.gelir_kategorisi_olusturma = True
        gelir_kategorisi_guncelleme = request.POST.get("gelir_kategorisi_guncelleme")
        if gelir_kategorisi_guncelleme : 
            izinler.gelir_kategorisi_guncelleme = True
        gelir_kategorisi_silme = request.POST.get("gelir_kategorisi_silme")
        if gelir_kategorisi_silme : 
            izinler.gelir_kategorisi_silme = True
        
        #
        gider_kategorisi_gorme = request.POST.get("gider_kategorisi_gorme")
        if gider_kategorisi_gorme:  
            izinler.gider_kategorisi_gorme = True
        gider_kategorisi_olusturma = request.POST.get("gider_kategorisi_olusturma")
        if gider_kategorisi_olusturma : 
            izinler.gider_kategorisi_olusturma = True
        gider_kategorisi_guncelleme = request.POST.get("gider_kategorisi_guncelleme")
        if gider_kategorisi_guncelleme : 
            izinler.gider_kategorisi_guncelleme = True
        gider_kategorisi_silme = request.POST.get("gider_kategorisi_silme")
        if gider_kategorisi_silme : 
            izinler.gider_kategorisi_silme = True
        #
        #
        gelir_etiketi_gorme = request.POST.get("gelir_etiketi_gorme")
        if gelir_etiketi_gorme:  
            izinler.gelir_etiketi_gorme = True
        gelir_etiketi_olusturma = request.POST.get("gelir_etiketi_olusturma")
        if gelir_etiketi_olusturma : 
            izinler.gelir_etiketi_olusturma = True
        gelir_etiketi_guncelleme = request.POST.get("gelir_etiketi_guncelleme")
        if gelir_etiketi_guncelleme : 
            izinler.gelir_etiketi_guncelleme = True
        gelir_etiketi_silme = request.POST.get("gelir_etiketi_silme")
        if gelir_etiketi_silme : 
            izinler.gelir_etiketi_silme = True

        #
        gider_etiketi_gorme = request.POST.get("gider_etiketi_gorme")
        if gider_etiketi_gorme:  
            izinler.gider_etiketi_gorme = True
        gider_etiketi_olusturma = request.POST.get("gider_etiketi_olusturma")
        if gider_etiketi_olusturma : 
            izinler.gider_etiketi_olusturma = True
        gider_etiketi_guncelleme = request.POST.get("gider_etiketi_guncelleme")
        if gider_etiketi_guncelleme : 
            izinler.gider_etiketi_guncelleme = True
        gider_etiketi_silme = request.POST.get("gider_etiketi_silme")
        if gider_etiketi_silme : 
            izinler.gider_etiketi_silme = True
        #
        #
        urun_gorme = request.POST.get("urun_gorme")
        if urun_gorme:  
            izinler.urun_gorme = True
        urun_olusturma = request.POST.get("urun_olusturma")
        if urun_olusturma : 
            izinler.urun_olusturma = True
        urun_guncelleme = request.POST.get("urun_guncelleme")
        if urun_guncelleme : 
            izinler.urun_guncelleme = True
        urun_silme = request.POST.get("urun_silme")
        if urun_silme : 
            izinler.urun_silme = True

        #
        muhasabe_ayarlari_gorme = request.POST.get("muhasabe_ayarlari_gorme")
        if muhasabe_ayarlari_gorme : 
            izinler.muhasabe_ayarlari_gorme = True
        muhasabe_ayarlari_guncelleme = request.POST.get("muhasabe_ayarlari_guncelleme")
        if muhasabe_ayarlari_guncelleme : 
            izinler.muhasabe_ayarlari_guncelleme = True

        #
        gelir_faturasi_makbuz_gorme_izni = request.POST.get("gelir_faturasi_makbuz_gorme_izni")
        if gelir_faturasi_makbuz_gorme_izni:  
            izinler.gelir_faturasi_makbuz_gorme_izni = True
        gelir_faturasi_makbuz_kesme_izni = request.POST.get("gelir_faturasi_makbuz_kesme_izni")
        if gelir_faturasi_makbuz_kesme_izni : 
            izinler.gelir_faturasi_makbuz_kesme_izni = True
        gelir_faturasi_makbuz_duzenleme_izni = request.POST.get("gelir_faturasi_makbuz_duzenleme_izni")
        if gelir_faturasi_makbuz_duzenleme_izni : 
            izinler.gelir_faturasi_makbuz_duzenleme_izni = True
        gelir_faturasi_makbuz_silme_izni = request.POST.get("gelir_faturasi_makbuz_silme_izni")
        if gelir_faturasi_makbuz_silme_izni : 
            izinler.gelir_faturasi_makbuz_silme_izni = True
        #
        gider_faturasi_makbuz_gorme_izni = request.POST.get("gider_faturasi_makbuz_gorme_izni")
        if gider_faturasi_makbuz_gorme_izni:  
            izinler.gider_faturasi_makbuz_gorme_izni = True
        gider_faturasi_makbuz_kesme_izni = request.POST.get("gider_faturasi_makbuz_kesme_izni")
        if gider_faturasi_makbuz_kesme_izni : 
            izinler.gider_faturasi_makbuz_kesme_izni = True
        gider_faturasi_makbuz_duzenleme_izni = request.POST.get("gider_faturasi_makbuz_duzenleme_izni")
        if gider_faturasi_makbuz_duzenleme_izni : 
            izinler.gider_faturasi_makbuz_duzenleme_izni = True
        gider_faturasi_makbuz_silme_izni = request.POST.get("gider_faturasi_makbuz_silme_izni")
        if gider_faturasi_makbuz_silme_izni : 
            izinler.gider_faturasi_makbuz_silme_izni = True
        
        #
        gant_olusturma = request.POST.get("gant_olusturma")
        if gant_olusturma:  
            izinler.gant_olusturma = True
        gant_gorme = request.POST.get("gant_gorme")
        if gant_gorme : 
            izinler.gant_gorme = True
        gant_duzenleme = request.POST.get("gant_duzenleme")
        if gant_duzenleme : 
            izinler.gant_duzenleme = True
        #
        genel_rapor_olusturma = request.POST.get("genel_rapor_olusturma")
        if genel_rapor_olusturma:  
            izinler.genel_rapor_olusturma = True
        genel_rapor_gorme = request.POST.get("genel_rapor_gorme")
        if genel_rapor_gorme : 
            izinler.genel_rapor_gorme = True
        genel_rapor_duzenleme = request.POST.get("genel_rapor_duzenleme")
        if genel_rapor_duzenleme : 
            izinler.genel_rapor_duzenleme = True
        genel_rapor_silme = request.POST.get("genel_rapor_silme")
        if genel_rapor_silme : 
            izinler.genel_rapor_silme = True
        genel_rapor_onaylama = request.POST.get("genel_rapor_onaylama")
        if genel_rapor_onaylama : 
            izinler.genel_rapor_onaylama = True
        #stok satın alma 
        satin_alma_talebi_olusturma = request.POST.get("satin_alma_talebi_olusturma")
        if satin_alma_talebi_olusturma:
            izinler.satin_alma_talebi_olusturma = True

        satin_alma_talebi_silme = request.POST.get("satin_alma_talebi_silme")
        if satin_alma_talebi_silme:
            izinler.satin_alma_talebi_silme = True

        satin_alma_talebi_gorme = request.POST.get("satin_alma_talebi_gorme")
        if satin_alma_talebi_gorme:
            izinler.satin_alma_talebi_gorme = True

        satin_alma_talebi_duzenleme = request.POST.get("satin_alma_talebi_duzenleme")
        if satin_alma_talebi_duzenleme:
            izinler.satin_alma_talebi_duzenleme = True

        satin_alma_talebi_onaylama_olusturma = request.POST.get("satin_alma_talebi_onaylama_olusturma")
        if satin_alma_talebi_onaylama_olusturma:
            izinler.satin_alma_talebi_onaylama_olusturma = True

        satin_alma_talebi_onaylama_silme = request.POST.get("satin_alma_talebi_onaylama_silme")
        if satin_alma_talebi_onaylama_silme:
            izinler.satin_alma_talebi_onaylama_silme = True

        satin_alma_talebi_onaylama_gorme = request.POST.get("satin_alma_talebi_onaylama_gorme")
        if satin_alma_talebi_onaylama_gorme:
            izinler.satin_alma_talebi_onaylama_gorme = True

        satin_alma_talebi_onaylama_duzenleme = request.POST.get("satin_alma_talebi_onaylama_duzenleme")
        if satin_alma_talebi_onaylama_duzenleme:
            izinler.satin_alma_talebi_onaylama_duzenleme = True

        stok_olusturma = request.POST.get("stok_olusturma")
        if stok_olusturma:
            izinler.stok_olusturma = True

        stok_talebi_onaylama_silme = request.POST.get("stok_talebi_onaylama_silme")
        if stok_talebi_onaylama_silme:
            izinler.stok_talebi_onaylama_silme = True

        stok_talebi_onaylama_gorme = request.POST.get("stok_talebi_onaylama_gorme")
        if stok_talebi_onaylama_gorme:
            izinler.stok_talebi_onaylama_gorme = True

        stok_talebi_onaylama_duzenleme = request.POST.get("stok_talebi_onaylama_duzenleme")
        if stok_talebi_onaylama_duzenleme:
            izinler.stok_talebi_onaylama_duzenleme = True

        zimmet_olusturma = request.POST.get("zimmet_olusturma")
        if zimmet_olusturma:
            izinler.zimmet_olusturma = True

        zimmet_silme = request.POST.get("zimmet_silme")
        if zimmet_silme:
            izinler.zimmet_silme = True

        zimmet_gorme = request.POST.get("zimmet_gorme")
        if zimmet_gorme:
            izinler.zimmet_gorme = True

        rapor_olusturucu_gorme = request.POST.get("rapor_olusturucu_gorme")
        if rapor_olusturucu_gorme:
            izinler.rapor_olusturucu_gorme = True

        rapor_olusturucu_olusturma = request.POST.get("rapor_olusturucu_olusturma")
        if rapor_olusturucu_olusturma:
            izinler.rapor_olusturucu_olusturma = True

        musteri_olusturma = request.POST.get("musteri_olusturma")
        if musteri_olusturma:
            izinler.musteri_olusturma = True
        musteri_gorme = request.POST.get("musteri_gorme")
        if musteri_gorme:
            izinler.musteri_gorme = True
        musteri_duzenleme = request.POST.get("musteri_duzenleme")
        if musteri_duzenleme:
            izinler.musteri_duzenleme = True
        musteri_silme = request.POST.get("musteri_silme")
        if musteri_silme:
            izinler.musteri_silme = True
        crm_musteri_olusturma = request.POST.get("crm_musteri_olusturma")
        if crm_musteri_olusturma:
            izinler.crm_musteri_olusturma = True
        crm_musteri_silme = request.POST.get("crm_musteri_silme")
        if crm_musteri_silme:
            izinler.crm_musteri_silme = True
        crm_musteri_gorme = request.POST.get("crm_musteri_gorme")
        if crm_musteri_gorme:
            izinler.crm_musteri_gorme = True
        crm_musteri_duzenleme = request.POST.get("crm_musteri_duzenleme")
        if crm_musteri_duzenleme:
            izinler.crm_musteri_duzenleme = True
        crm_talep_olusturma = request.POST.get("crm_talep_olusturma")
        if crm_talep_olusturma:
            izinler.crm_talep_olusturma = True
        crm_talep_silme = request.POST.get("crm_talep_silme")
        if crm_talep_silme:
            izinler.crm_talep_silme = True
        crm_talep_gorme = request.POST.get("crm_talep_gorme")
        if crm_talep_gorme:
            izinler.crm_talep_gorme = True
        crm_talep_duzenleme = request.POST.get("crm_talep_duzenleme")
        if crm_talep_duzenleme:
            izinler.crm_talep_duzenleme = True
        crm_teklif_olusturma = request.POST.get("crm_teklif_olusturma")
        if crm_teklif_olusturma:
            izinler.crm_teklif_olusturma = True
        crm_teklif_silme = request.POST.get("crm_teklif_silme")
        if crm_teklif_silme:
            izinler.crm_teklif_silme = True
        crm_teklif_gorme = request.POST.get("crm_teklif_gorme")
        if crm_teklif_gorme:
            izinler.crm_teklif_gorme = True
        crm_teklif_duzenleme = request.POST.get("crm_teklif_duzenleme")
        if crm_teklif_duzenleme:
            izinler.crm_teklif_duzenleme = True
        crm_daire_olusturma = request.POST.get("crm_daire_olusturma")
        if crm_daire_olusturma:
            izinler.crm_daire_olusturma = True
        crm_daire_silme = request.POST.get("crm_daire_silme")
        if crm_daire_silme:
            izinler.crm_daire_silme = True
        crm_daire_gorme = request.POST.get("crm_daire_gorme")
        if crm_daire_gorme:
            izinler.crm_daire_gorme = True
        crm_daire_duzenleme = request.POST.get("crm_daire_duzenleme")
        if crm_daire_duzenleme:
            izinler.crm_daire_duzenleme = True
        crm_evrak_olusturma = request.POST.get("crm_evrak_olusturma")
        if crm_evrak_olusturma:
            izinler.crm_evrak_olusturma = True
        crm_evrak_silme = request.POST.get("crm_evrak_silme")
        if crm_evrak_silme:
            izinler.crm_evrak_silme = True
        crm_evrak_gorme = request.POST.get("crm_evrak_gorme")
        if crm_evrak_gorme:
            izinler.crm_evrak_gorme = True
        crm_evrak_duzenleme = request.POST.get("crm_evrak_duzenleme")
        if crm_evrak_duzenleme:
            izinler.crm_evrak_duzenleme = True

        izinler.save()
        id_bilgiis = izinler.id
    return redirect_with_language("main:kullanici_yetkileri_duzenle",id_bilgiis)
