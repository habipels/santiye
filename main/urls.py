from django.urls import path
from . import views
app_name = "main"
urlpatterns = [#
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
    #proje tip işlemelri
    #şantiye proje işlemleri
    path("siteprojects", views.santiye_projesi_ekle_, name="santiye_projesi_ekle_"),
    path("control/siteprojects/<str:hash>", views.santiye_projesi_ekle_2, name="santiye_projesi_ekle_2"),
    path("addsite", views.santiye_ekleme_sahibi, name="santiye_ekleme_sahibi"),
    path("addsitesuperadmin/<int:id>", views.santiye_ekleme_super_admin, name="santiye_ekleme_super_admin"),
    path("delsiteproject", views.santiye_projesi_sil, name="santiye_projesi_sil"),
    path("setsiteprojetc", views.santiye_projesi_duzenle, name="santiye_projesi_duzenle"),
    path("siteblog/<int:id>/", views.santiye_projesi_bloklar_ekle_, name="santiye_projesi_bloklar_ekle_"),
    path("addblog", views.blog_ekle, name="blog_ekle"),
    path("delblog", views.blog_sil, name="blog_sil"),
    path("setblog", views.blog_duzenle, name="blog_duzenle"),
    #şantiye proje işlemleri
    #
    path("yetkisiz", views.yetkisiz, name="yetkisiz"),
    #şantiye Kalemleri
    path("buldingsite/<int:id>", views.santtiye_kalemleri, name="santtiye_kalemleri"),
    path("addbuldingsite", views.santiyeye_kalem_ekle, name="santiyeye_kalem_ekle"),
    path("adminaddbuldingsite/<int:id>", views.santiye_kalem_ekle_admin, name="santiye_kalem_ekle_admin"),
    path("addbuldingsiteadmin/<int:id>", views.santiye_kalem_ekle_admin, name="santiye_kalem_ekle_admin"),
    path("editsite", views.santiye_duzelt, name="santiye_duzelt"),
    path("delbuldingsite", views.kalem_sil, name="kalem_sil"),
    path("setbuldingsite", views.santiye_kalemleri_duzenle, name="santiye_kalemleri_duzenle"),
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
    path("saveprogresstracking", views.ilerleme_kaydet, name="ilerleme_kaydet"),
    #
    #ilerleme takibi
    path("santiyeraporu/<int:id>", views.santiye_raporu, name="santiye_raporu"),
#    #taşeron olayları
    path("subcontractor", views.taseron_sayfasi, name="taseron_sayfasi"),
    path("addsubcontractor", views.taseron_ekle, name="taseron_ekle"),
    path("delsubcontractor", views.taseron_silme, name="taseron_silme"),
    path("addsubcontractoradmin/<int:id>", views.taseron_ekle_admin, name="taseron_ekle_admin"),
    path("setsubcontractor", views.taseron_duzelt, name="taseron_duzelt"),
    #
    #Üst Yükleneci olayları
    path("topcontractor", views.ust_yuklenici_sayfasi, name="ust_yuklenici_sayfasi"),
    path("addtopcontractor", views.ust_yuklenici_ekle, name="ust_yuklenici_ekle"),
    path("deltopcontractor", views.ust_yuklenici_silme, name="ust_yuklenici_silme"),
    path("addtopcontractoradmin/<int:id>", views.taseron_ekle_admin, name="taseron_ekle_admin"),
    path("settopcontractor", views.ust_yuklenici_duzelt, name="ust_yuklenici_duzelt"),
    #
    #taşeron olayları
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
    #hakedişler
    path("progresspayment", views.hakedis_sayfasi, name="hakedis_sayfasi"),
    path("addprogresspayment", views.hakedis_ekle, name="hakedis_ekle"),
    path("delprogresspayment", views.hakedis_silme, name="hakedis_silme"),
    path("setprogresspayment", views.hakedis_duzenle, name="hakedis_duzenle"),
    path("adminaddprogresspayment/<int:id>", views.hakedis_ekle_admin, name="hakedis_ekle_admin"),
    #
    #hakedişler
    #depolama sistemim
    path("storage/mydir", views.depolama_sistemim, name="depolama_sistemim"),
    path("storage/addmydir", views.klasor_olustur, name="klasor_olustur"),
    path("storage/setmydir", views.klasor__yeniden_adlandir, name="klasor__yeniden_adlandir"),
    path("storage/delmydir", views.klasor_sil, name="klasor_sil"),
    path("storage/savemydir", views.dosya_geri_getir, name="dosya_geri_getir"),
    path("storage/mydir/<int:id>/<str:slug>/", views.klasore_gir, name="klasore_gir"),
    path("storage/addfile", views.dosya_ekle, name="dosya_ekle"),
    path("storage/delfile", views.dosya_sil, name="dosya_sil"),
    path("storage/mydir/document", views.dokumanlar, name="dokumanlar"),
    path("storage/mydir/media", views.media_dosyalari, name="media_dosyalari"),
    path("storage/mydir/history", views.zamana_dosyalari, name="zamana_dosyalari"),
    path("storage/mydir/contracts", views.sozlesmler_depolamam, name="sozlesmler_depolamam"),
    path("storage/mydir/progresspayment", views.hakedis_depolamam, name="hakedis_depolamam"),
    path("storage/mydir/deletedfile", views.silinen_dosyalari, name="silinen_dosyalari"),
    #depolama sistemim
    #iş planı #
    path("thingstodo", views.yapilacaklar, name="yapilacaklar"),
    path("addthingstodo", views.yapilacalar_ekle, name="yapilacalar_ekle"),
    path("setthingstodo", views.yapilacalar_ekle_duzenleme, name="yapilacalar_ekle_duzenleme"),
    path("delthingstodo", views.yapilacalar_sil, name="yapilacalar_sil"),
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

    #takvim
    path("gantt", views.takvim_olaylari, name="takvim_olaylari"),
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
    path('get_yapi/<int:santiye_id>/', views.get_yapi, name='get_yapi'),
    path('yapilacak/<int:id>/', views.yapilacak_gonder_json, name='yapilacak_gonder_json'),
]
#
