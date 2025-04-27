from django.urls import path
from . import views
app_name = "main"
urlpatterns = [#
    path('get-country/', views.get_country, name='get-country'),
    path("get-csrf-token/", views.get_csrf_token, name="get_csrf_token"),
    path("", views.homepage, name="homepage"),
    path("home", views.ana_sayfa, name="ana_sayfa"),
    path("control/<str:hash>", views.homepage_2, name="homepage_2"),
    path("logs", views.loglar, name="loglar"),
    #site ayarları
    path("websitesettings", views.site_ayarlari, name="site_ayarlari"),
    path("savesitesettings", views.site_ayari_kaydet, name="site_ayari_kaydet"),
    #
    #site ayarları
    #şantiye işlemelri
    path("addingsite", views.santiye_ekle, name="santiye_ekle"),
    path("sitesettings", views.santiye_listele, name="santiye_listele"),
    path("delsite", views.santiye_sil, name="santiye_sil"),
    path("editsite", views.santiye_duzelt, name="santiye_duzelt"),
    #şantiye işlemelri
    #dil ayarları
    path("langsettings", views.dil_ayari_listele, name="dil_ayari_listele"),
    path("addlang", views.dil_ekle, name="dil_ekle"),
    path("setlang", views.dil_duzelt, name="dil_duzelt"),
    path("dellang", views.dil_sil, name="dil_sil"),
    #dil ayarları
    #proje tip işlemelri
    path("projectstype", views.proje_tipi_, name="proje_tipi_"),
    path("addprojectstype", views.proje_ekleme, name="proje_ekleme"),
    path("delprojectstype", views.proje_Adi_sil, name="proje_Adi_sil"),
    path("setprojecttype", views.proje_duzenle, name="proje_duzenle"),
    path("control/projectstypes/<str:hash>", views.proje_tipi_2, name="proje_tipi_2"),
    path("control/addprojectstype/<str:hash>", views.proje_ekleme_2, name="proje_ekleme_2"),
    path("control/delprojectstype/<str:hash>", views.proje_Adi_sil_2, name="proje_Adi_sil_2"),
    path("control/setprojecttype/<str:hash>", views.proje_duzenle_2, name="proje_duzenle_2"),
    #proje tip işlemelri
    #şantiye proje işlemleri
    path("siteprojects", views.santiye_projesi_ekle_, name="santiye_projesi_ekle_"),
    path("control/siteprojects/<str:hash>", views.santiye_projesi_ekle_2, name="santiye_projesi_ekle_2"),
    path("addsite", views.santiye_ekleme_sahibi, name="santiye_ekleme_sahibi"),
    path("control/addsite/<str:hash>", views.santiye_ekleme_sahibi_2, name="santiye_ekleme_sahibi_2"),
    path("addsitesuperadmin/<int:id>", views.santiye_ekleme_super_admin, name="santiye_ekleme_super_admin"),
    path("delsiteproject", views.santiye_projesi_sil, name="santiye_projesi_sil"),
    path("setsiteprojetc", views.santiye_projesi_duzenle, name="santiye_projesi_duzenle"),
    path("siteblog/<int:id>/", views.santiye_projesi_bloklar_ekle_, name="santiye_projesi_bloklar_ekle_"),
    path("addblog", views.blog_ekle, name="blog_ekle"),
    path("delblog", views.blog_sil, name="blog_sil"),
    path("setblog", views.blog_duzenle, name="blog_duzenle"),
    path("control/addblog/<str:hash>", views.blog_ekle_2, name="blog_ekle_2"),
    path("control/delblog/<str:hash>", views.blog_sil_2, name="blog_sil_2"),
    path("control/setblog/<str:hash>", views.blog_duzenle_2, name="blog_duzenle_2"),
    #şantiye proje işlemleri
    #
    path("yetkisiz", views.yetkisiz, name="yetkisiz"),
    #şantiye Kalemleri
    path("buldingsite/<int:id>", views.santtiye_kalemleri, name="santtiye_kalemleri"),
    path("addbuldingsite", views.santiyeye_kalem_ekle, name="santiyeye_kalem_ekle"),
    path("control/addbuldingsite/<str:hash>", views.santiyeye_kalem_ekle_2, name="santiyeye_kalem_ekle_2"),
    path("adminaddbuldingsite/<int:id>", views.santiye_kalem_ekle_admin, name="santiye_kalem_ekle_admin"),
    path("addbuldingsiteadmin/<int:id>", views.santiye_kalem_ekle_admin, name="santiye_kalem_ekle_admin"),
    path("editsite", views.santiye_duzelt, name="santiye_duzelt"),
    path("delbuldingsite", views.kalem_sil, name="kalem_sil"),
     path("control/delbuldingsite/<str:hash>", views.kalem_sil_2, name="kalem_sil_2"),
    path("setbuldingsite", views.santiye_kalemleri_duzenle, name="santiye_kalemleri_duzenle"),
    path("control/setbuldingsite/<str:hash>", views.santiye_kalemleri_duzenle_2, name="santiye_kalemleri_duzenle_2"),
    path("delbuldingsites/<int:id>/<int:ik>", views.kalem_blog_dagilis_sil, name="kalem_blog_dagilis_sil"),
    #
    #şantiye Kalemleri
    #proje
    path("prjectspage", views.projeler_sayfasi, name="projeler_sayfasi"),
    path("addprjects", views.proje_ekle, name="proje_ekle"),
    path("addprjects/<int:id>", views.proje_ekle_admin, name="proje_ekle_admin"),
    path("delprjects", views.proje_silme, name="proje_silme"),
    path("setprojects", views.proje_duzenle_bilgi, name="proje_duzenle_bilgi"),
    #proje
    #ilerleme takibi
    path("progresstracking", views.santiye_kalem_ve_blog, name="santiye_kalem_ve_blog"),
    path("control/progresstracking/<str:hash>", views.santiye_kalem_ve_blog_2, name="santiye_kalem_ve_blog_2"),
    path("progresstracking/progress/<int:id>/<str:slug>", views.blogtan_kaleme_ilerleme_takibi, name="blogtan_kaleme_ilerleme_takibi"),
    path("control/progresstracking/progress/<int:id>/<str:slug>/<str:hash>", views.blogtan_kaleme_ilerleme_takibi_hash, name="blogtan_kaleme_ilerleme_takibi_hash"),
    path("saveprogresstracking", views.ilerleme_kaydet, name="ilerleme_kaydet"),
    path("control/saveprogresstracking/<str:hash>", views.ilerleme_kaydet_2, name="ilerleme_kaydet_2"),
    #
    #ilerleme takibi#
    path("santiyeraporu/<int:id>", views.santiye_raporu, name="santiye_raporu"),
    path("santiyeraporuu/<int:id>", views.santiye_raporu_rapor_gonderme, name="santiye_raporu_rapor_gonderme"),
    path("control/santiyeraporu/<int:id>/<str:hash>", views.santiye_raporu_2, name="santiye_raporu_2"),
#    #taşeron olayları#
    path("subcontractor", views.taseron_sayfasi, name="taseron_sayfasi"),
    path("control/subcontractor/<str:hash>", views.taseron_sayfasi_2, name="taseron_sayfasi_2"),
    path("control/addsubcontractor/<str:hash>", views.taseron_ekle_2, name="taseron_ekle_2"),
    path("control/delsubcontractor/<str:hash>", views.taseron_silme_2, name="taseron_silme_2"),
    path("control/setsubcontractor/<str:hash>", views.taseron_duzelt_2, name="taseron_duzelt_2"),
    path("addsubcontractor", views.taseron_ekle, name="taseron_ekle"),
    path("delsubcontractor", views.taseron_silme, name="taseron_silme"),
    path("addsubcontractoradmin/<int:id>", views.taseron_ekle_admin, name="taseron_ekle_admin"),
    path("setsubcontractor", views.taseron_duzelt, name="taseron_duzelt"),
    #
    #Üst Yükleneci olayları
    path("control/topcontractor/<str:hash>", views.ust_yuklenici_sayfasi_2, name="ust_yuklenici_sayfasi_2"),
    path("control/addtopcontractor/<str:hash>", views.ust_yuklenici_ekle_2, name="ust_yuklenici_ekle_2"),
    path("control/deltopcontractor/<str:hash>", views.ust_yuklenici_silme_2, name="ust_yuklenici_silme_2"),
    path("control/settopcontractor/<str:hash>", views.ust_yuklenici_duzelt_2, name="ust_yuklenici_duzelt_2"),

    path("topcontractor", views.ust_yuklenici_sayfasi, name="ust_yuklenici_sayfasi"),
    path("addtopcontractor", views.ust_yuklenici_ekle, name="ust_yuklenici_ekle"),
    path("deltopcontractor", views.ust_yuklenici_silme, name="ust_yuklenici_silme"),
    path("addtopcontractoradmin/<int:id>", views.taseron_ekle_admin, name="taseron_ekle_admin"),
    path("settopcontractor", views.ust_yuklenici_duzelt, name="ust_yuklenici_duzelt"),
    #
    #taşeron olayları
    path("control/contracts/<str:hash>", views.sozlesmler_sayfasi_2, name="sozlesmler_sayfasi_2"),
    path("control/addcontract/<str:hash>", views.sozlesme_ekle_2, name="sozlesme_ekle_2"),
    path("control/delcontract/<str:hash>", views.sozlesme_silme_2, name="sozlesme_silme_2"),
    path("control/setcontracts/<str:hash>", views.sozlesme_duzenle_2, name="sozlesme_duzenle_2"),

    path("control/topcontractss/<str:hash>", views.ana_yuklenici_sozlesmler_sayfasi_2, name="ana_yuklenici_sozlesmler_sayfasi_2"),
    path("control/topaddcontracts/<str:hash>", views.ust_yuklenici_sozlesme_ekle_2, name="ust_yuklenici_sozlesme_ekle_2"),
    path("control/topdelcontracts/<str:hash>", views.ust_yuklenici_silme_sozlesme_2, name="ust_yuklenici_silme_sozlesme_2"),
    path("control/topsetcontractss/<str:hash>", views.ust_yuklenici_sozlesme_duzenle_2, name="ust_yuklenici_sozlesme_duzenle_2"),
    #sözleşmeler olayları
    path("contracts", views.sozlesmler_sayfasi, name="sozlesmler_sayfasi"),
    path("addcontract", views.sozlesme_ekle, name="sozlesme_ekle"),
    path("delcontract", views.sozlesme_silme, name="sozlesme_silme"),
    path("adminaddcontracts/<int:id>", views.sozlesme_ekle_admin, name="sozlesme_ekle_admin"),
    path("setcontracts", views.sozlesme_duzenle, name="sozlesme_duzenle"),
    #
    path("topcontracts", views.ana_yuklenici_sozlesmler_sayfasi, name="ana_yuklenici_sozlesmler_sayfasi"),
    path("topaddcontract", views.ust_yuklenici_sozlesme_ekle, name="ust_yuklenici_sozlesme_ekle"),
    path("topdelcontract", views.ust_yuklenici_silme_sozlesme, name="ust_yuklenici_silme_sozlesme"),
    path("topadminaddcontracts/<int:id>", views.sozlesme_ekle_admin, name="sozlesme_ekle_admin"),
    path("topsetcontracts", views.ust_yuklenici_sozlesme_duzenle, name="ust_yuklenici_sozlesme_duzenle"),

    #
    #sözleşmeler olayları
    path("control/progresspayment/<str:hash>", views.hakedis_sayfasi_2, name="hakedis_sayfasi_2"),
    path("control/addprogresspayment/<str:hash>", views.hakedis_ekle_2, name="hakedis_ekle_2"),
    path("control/delprogresspayment/<str:hash>", views.hakedis_silme_2, name="hakedis_silme_2"),
    path("control/setprogresspayment/<str:hash>", views.hakedis_duzenle_2, name="hakedis_duzenle_2"),
    #hakedişler
    path("progresspayment", views.hakedis_sayfasi, name="hakedis_sayfasi"),
    path("addprogresspayment", views.hakedis_ekle, name="hakedis_ekle"),
    path("delprogresspayment", views.hakedis_silme, name="hakedis_silme"),
    path("setprogresspayment", views.hakedis_duzenle, name="hakedis_duzenle"),
    path("adminaddprogresspayment/<int:id>", views.hakedis_ekle_admin, name="hakedis_ekle_admin"),
    #
    #hakedişler#
    #depolama sistemim
    path("storage/mydir", views.depolama_sistemim, name="depolama_sistemim"),
    path("control/storage/mydir/<str:hash>", views.depolama_sistemim_2, name="depolama_sistemim_2"),
    path("storage/addmydir", views.klasor_olustur, name="klasor_olustur"),
    path("control/storage/addmydir/<str:hash>", views.klasor_olustur_2, name="klasor_olustur_2"),
    path("storage/setmydir", views.klasor__yeniden_adlandir, name="klasor__yeniden_adlandir"),
    path("control/storage/setmydir/<str:hash>", views.klasor__yeniden_adlandir_2, name="klasor__yeniden_adlandir_2"),
    path("storage/delmydir", views.klasor_sil, name="klasor_sil"),
    path("control/storage/delmydir/<str:hash>", views.klasor_sil_2, name="klasor_sil_2"),
    path("storage/savemydir", views.dosya_geri_getir, name="dosya_geri_getir"),
    path("control/storage/savemydir/<str:hash>", views.dosya_geri_getir_2, name="dosya_geri_getir_2"),
    #
    path("storage/mydir/files/<int:id>/<str:slug>/", views.klasore_gir, name="klasore_gir"),
    path("control/storage/mydir/<int:id>/<str:slug>/<str:hash>", views.klasore_gir_2, name="klasore_gir_2"),
    path("storage/addfile", views.dosya_ekle, name="dosya_ekle"),
    path("control/storage/addfile/<str:hash>", views.dosya_ekle_2, name="dosya_ekle_2"),
    path("storage/delfile", views.dosya_sil, name="dosya_sil"),
    path("control/storage/delfile/<str:hash>", views.dosya_sil_2, name="dosya_sil_2"),
    path("storage/mydir/document", views.dokumanlar, name="dokumanlar"),
    path("control/storage/mydir/document/<str:hash>", views.dokumanlar_2, name="dokumanlar_2"),
    path("storage/mydir/media", views.media_dosyalari, name="media_dosyalari"),
    path("control/storage/mydir/media/<str:hash>", views.media_dosyalari_2, name="media_dosyalari_2"),
    path("storage/mydir/history", views.zamana_dosyalari, name="zamana_dosyalari"),
    path("control/storage/mydir/history/<str:hash>", views.zamana_dosyalari_2, name="zamana_dosyalari_2"),
    path("storage/mydir/contracts", views.sozlesmler_depolamam, name="sozlesmler_depolamam"),
    path("control/storage/mydir/progresspayment/<str:hash>", views.hakedis_depolamam_2, name="hakedis_depolamam_2"),
    path("control/storage/mydir/contracts/<str:hash>", views.sozlesmler_depolamam_2, name="sozlesmler_depolamam_2"),
    path("storage/mydir/progresspayment", views.hakedis_depolamam, name="hakedis_depolamam"),
    path("storage/mydir/deletedfile", views.silinen_dosyalari, name="silinen_dosyalari"),
    path("control/storage/mydir/deletedfile/<str:hash>", views.silinen_dosyalari_2, name="silinen_dosyalari_2"),
    #depolama sistemim
    #iş planı #
    path("thingstodo", views.yapilacaklar, name="yapilacaklar"),
    path("control/thingstodo/<str:hash>", views.yapilacaklar_2, name="yapilacaklar_2"),
    path("addthingstodo", views.yapilacalar_ekle, name="yapilacalar_ekle"),
    path("control/addthingstodo/<str:hash>", views.yapilacalar_ekle_2, name="yapilacalar_ekle_2"),
    path("setthingstodo", views.yapilacalar_ekle_duzenleme, name="yapilacalar_ekle_duzenleme"),
    path("control/setthingstodo/<str:hash>", views.yapilacalar_ekle_duzenleme_2, name="yapilacalar_ekle_duzenleme_2"),
    path("delthingstodo", views.yapilacalar_sil, name="yapilacalar_sil"),
    path("control/delthingstodo/<str:hash>", views.yapilacalar_sil_2, name="yapilacalar_sil_2"),
    path("setthingstodo", views.yapilacalar_duzenle, name="yapilacalar_duzenle"),
    path("allthingstodo", views.yapilacalar_ekle_toplu, name="yapilacalar_ekle_toplu"),
    path("statusthingstodo", views.yapilacak_durumu_yenileme, name="yapilacak_durumu_yenileme"),
    #
    #iş planı
    #yapilacaklar
    path("todo", views.yapilacaklar_timeline, name="yapilacaklar_timeline"),
    path("addtodo", views.yapilacalar_time_line_ekle, name="yapilacalar_time_line_ekle"),
    path("deltodo", views.yapilacalar_time_line_sil, name="yapilacalar_time_line_sil"),
    path("settodo", views.yapilacalar_time_line_duzenle, name="yapilacalar_time_line_duzenle"),
    #yapilacaklar
    # 
    #takvim
    path("generalreporttake/<int:rapor_id>", views.rapor_gonder, name="rapor_gonder"),
    path("generalreport", views.genel_rapor_sayfasi, name="genel_rapor_sayfasi"),
    path("rapor_onaylama", views.rapor_onaylama, name="rapor_onaylama"),
    path("applygeneralreport/<int:id>", views.genel_rapor_onaylama, name="genel_rapor_onaylama"),
    path("delgeneralreport", views.rapor_sil, name="rapor_sil"),
    path("creategeneralreport", views.genel_rapor_olustur, name="genel_rapor_olustur"),
    path("gantt", views.takvim_olaylari, name="takvim_olaylari"),
    path('gantt-kaydet/', views.gant_kaydet, name='gant_kaydet'),
    path("userauthorizations", views.kullanici_yetkileri, name="kullanici_yetkileri"),
    path("kullaniciyetkiolustur", views.kullanici_yetki_olustur, name="kullanici_yetki_olustur"),
    path("kullaniciyetkiadiduzenle", views.kullanici_yetki_adi_duzenle, name="kullanici_yetki_adi_duzenle"),
    path("kullaniciyetkisil", views.kullanici_yetki_sil, name="kullanici_yetki_sil"),
    path("userauthorizationsset/<int:id>/", views.kullanici_yetkileri_duzenle, name="kullanici_yetkileri_duzenle"),
    path("kullaniciyetkialma", views.kullanici_yetki_alma, name="kullanici_yetki_alma"),

    path("deneme/<int:cari_id>", views.cari_history_view, name="cari_history_view"),
    #takvim
    path("yukleme/<int:id>", views.giderleri_excelden_ekle, name="giderleri_excelden_ekle"),
    path("yukleme2/<int:id>", views.gelirleri_excelden_ekle, name="gelirleri_excelden_ekle"),
    path("pageshow", views.sayfa_denemeleri, name="sayfa_denemeleri"),
    path("notifications", views.bildirimler, name="bildirimler"),
    #katmanlar
    path("layer", views.katman_sayfasi, name="katman_sayfasi"),
    path("savelayer", views.katman_ekle, name="katman_ekle"),
    path("dellayer", views.katman_sil, name="katman_sil"),
    path("setlayer", views.katman_duzenle, name="katman_duzenle"),
    path("control/layer/<str:hash>", views.katman_sayfasi_2, name="katman_sayfasi_2"),
    path("control/savelayer/<str:hash>", views.katman_ekle_2, name="katman_ekle_2"),
    path("control/dellayer/<str:hash>", views.katman_sil_2, name="katman_sil_2"),
    path("control/setlayer/<str:hash>", views.katman_duzenle_2, name="katman_duzenle_2"),
    path('get_yapi/<int:santiye_id>/', views.get_yapi, name='get_yapi'),
    path('yapilacak/<int:id>/', views.yapilacak_gonder_json, name='yapilacak_gonder_json'),
    path("control/userauthorizations/<str:hash>", views.kullanici_yetkileri_2, name="kullanici_yetkileri_2"),
    path("control/kullaniciyetkiolustur/<str:hash>", views.kullanici_yetki_olustur_2, name="kullanici_yetki_olustur_2"),
    path("control/kullaniciyetkiadiduzenle/<str:hash>", views.kullanici_yetki_adi_duzenle_2, name="kullanici_yetki_adi_duzenle_2"),
    path("control/kullaniciyetkisil/<str:hash>", views.kullanici_yetki_sil_2, name="kullanici_yetki_sil_2"),
    path("control/userauthorizationsset/<int:id>/<str:hash>", views.kullanici_yetkileri_duzenle_2, name="kullanici_yetkileri_duzenle_2"),
    path("control/kullaniciyetkialma/<str:hash>", views.kullanici_yetki_alma_2, name="kullanici_yetki_alma_2"),
    #şantiye Kontrol
    #
    path("checklist/<int:id>/", views.santiye_onay_listesi_kontrol, name="santiye_onay_listesi_kontrol"),
    path("site_control_save/", views.kontrolculeri_kaydet, name="kontrolculeri_kaydet"),
    path("site_control_add/<int:id>/<str:slug>", views.santiye_kontrolculeri_ekle, name="santiye_kontrolculeri_ekle"),
    path("site_control/<int:id>/", views.santiye_kontrolculeri_isle, name="santiye_kontrolculeri_isle"),
    path("viewsitedetail/<int:id>/", views.santiye_kontrol_detayi_ust_yoneticii, name="santiye_kontrol_detayi_ust_yoneticii"),
    path("onaylama_islemi/", views.daire_imalat_checklist_onaylama, name="daire_imalat_checklist_onaylama"),
    path("mansitedetail/<int:id>/", views.santiye_kontrol_detayi_ust_yonetici, name="santiye_kontrol_detayi_ust_yonetici"),
    path("sitedetail/<int:id>/", views.santiye_kontrol_detayi, name="santiye_kontrol_detayi"),
    path("blockprojects/<int:id>", views.santiye_projeleri, name="santiye_projeleri"),
    path("siteprojectslist/", views.santiye_onay_listesi, name="santiye_onay_listesi"),
    path("siteprojectsablone/<int:id>/", views.santiye_sablonu, name="santiye_sablonu"),
    path("setsiteprojectsablone/<int:id>/", views.santiye_sablonu_duzenle, name="santiye_sablonu_duzenle"),
    path("createsiteprojectsablone/", views.save_template, name="save_template"),
    path("setcreatesiteprojectsablone/", views.save_template_duzenle, name="save_template_duzenle"),
    path("mysiteprojects/", views.santiyelerim, name="santiyelerim"),

 path("savemystructures/", views.santiye_proje_olustur, name="santiye_proje_olustur"),

path("mystructures/<int:id>", views.yapilarim, name="yapilarim"),
path("check/", views.daire_imalat_checklist, name="daire_imalat_checklist"),
path("myhouse/<int:id>", views.daireleri_gor, name="daireleri_gor"),
path("level/<int:id>", views.katlara_gore_gor, name="katlara_gore_gor"),
path("levelhouse/<int:id>/<int:kat>/", views.kat_daire_bilgisi, name="kat_daire_bilgisi"),


#rfi
path("saat/", views.get_kayit_tarihi_from_request, name="get_kayit_tarihi_from_request"),
path("rfi_create/", views.rfi_Olustur, name="rfi_Olustur"),
path("rfi_list/", views.rfi_listesi, name="rfi_listesi"),
path("rfi_template/", views.rfi_template, name="rfi_template"),
path("rfi_detail/<int:id>", views.rfi_detail, name="rfi_detail"),
path("rfi_duzenleme/<int:id>", views.rfi_duzenleme, name="rfi_duzenleme"),
path("rfi_reject/", views.rfi_reject, name="rfi_reject"),
path("rfi_approve/", views.rfi_approve, name="rfi_approve"),
path("rfi_show/<int:id>", views.rfi_show, name="rfi_show"),
path("create_report/", views.rapor_olusturma, name="rapor_olusturma"),
path("report_list/", views.raporlari_gor_sayfasi, name="raporlari_gor_sayfasi"),
path("rapor_kaydedici/", views.rapor_kaydedici, name="rapor_kaydedici"),
]

#
