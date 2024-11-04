from django.urls import path
from . import views
app_name = "accounting"
urlpatterns = [
    #kasa işlemleri 
    #get_fatura_gelir
    path('get_fatura_gelir/<int:fatura_id>/', views.get_fatura_gelir, name='get_fatura_gelir'),
    path('get_fatura/<int:fatura_id>/', views.get_fatura_gider, name='get_fatura_gider'),
    path("till", views.kasa_viev, name="kasa"),
    path("control/till/<str:hash>", views.a_kasa_viev, name="a_kasa_viev"),
    path("control/viewstill/<int:id>/<str:hash>", views.kasa_tekli_2, name="kasa_tekli_2"),
    path("control/addtill/<str:hash>", views.kasa_ekle_2, name="kasa_ekle_2"),
    path("control/deltill/<str:hash>", views.kasa_sil_2, name="kasa_sil_2"),
    path("control/settill/<str:hash>", views.kasa_duzenle_2, name="kasa_duzenle_2"),

    path("viewstill/<int:id>", views.kasa_tekli, name="kasa_tekli"),
    path("addtill", views.kasa_ekle, name="kasa_ekle"),
    path("deltill", views.kasa_sil, name="kasa_sil"),
    path("settill", views.kasa_duzenle, name="kasa_duzenle"),
    #kasa işlemleri
    #gelir kategorileri
    path("control/incomecategory/<str:hash>", views.gelir_kategorisi_tipleri_2, name="gelir_kategorisi_tipleri_2"),
    path("incomecategory", views.gelir_kategorisi_tipleri, name="gelir_kategorisi_tipleri"),
    path("addcomecategory", views.gelir_kategorisi_ekleme, name="gelir_kategorisi_ekleme"),
    path("delcomecategory", views.gelir_kategoisi_sil, name="gelir_kategoisi_sil"),
    path("setcomecategory", views.gelir_kategorisi_duzenle, name="gelir_kategorisi_duzenle"),

    path("control/addcomecategory/<str:hash>", views.gelir_kategorisi_ekleme_2, name="gelir_kategorisi_ekleme_2"),
    path("control/delcomecategory/<str:hash>", views.gelir_kategoisi_sil_2, name="gelir_kategoisi_sil_2"),
    path("control/setcomecategory/<str:hash>", views.gelir_kategorisi_duzenle_2, name="gelir_kategorisi_duzenle_2"),
    #gelir kategorileri
    #gider kategorileri}
    path("control/inwcategory/<str:hash>", views.gider_kategorisi_tipleri_2, name="gider_kategorisi_tipleri_2"),
    path("inwcategory", views.gider_kategorisi_tipleri, name="gider_kategorisi_tipleri"),
    path("addwcategory", views.gider_kategorisi_ekleme, name="gider_kategorisi_ekleme"),
    path("delwcategory", views.gider_kategoisi_sil, name="gider_kategoisi_sil"),
    path("setwcategory", views.gider_kategorisi_duzenle, name="gider_kategorisi_duzenle"),

    path("control/addwcategory/<str:hash>", views.gider_kategorisi_ekleme_2, name="gider_kategorisi_ekleme_2"),
    path("control/delwcategory/<str:hash>", views.gider_kategoisi_sil_2, name="gider_kategoisi_sil_2"),
    path("control/setwcategory/<str:hash>", views.gider_kategorisi_duzenle_2, name="gider_kategorisi_duzenle_2"),
    #gider kategorileri
    #cari işlemleri$
    path("control/current/<str:hash>", views.cari_viev_2, name="cari_viev_2"),
    path("control/currentdetails/<int:id>/<str:hash>", views.cari_views_details_2, name="cari_views_details_2"),
    path("control/addcurrent/<str:hash>", views.cari_ekle_2, name="cari_ekle_2"),
    path("control/delcurrent/<str:hash>", views.cari_sil_2, name="cari_sil_2"),
    path("control/setcurrent/<str:hash>", views.cari_duzenle_2, name="cari_duzenle_2"),
    path("current", views.cari_viev, name="cari"),
    path("currentdetails/<int:id>", views.cari_views_details, name="cari_views_details"),
    path("addcurrent", views.cari_ekle, name="cari_ekle"),
    path("delcurrent", views.cari_sil, name="cari_sil"),
    path("setcurrent", views.cari_duzenle, name="cari_duzenle"),

    #cari işlemleri
    #gelir etiket işlemleri
    path("control/incometag/<str:hash>", views.gelir_etiketi_tipleri_2, name="gelir_etiketi_tipleri_2"),
    path("incometag", views.gelir_etiketi_tipleri, name="gelir_etiketi_tipleri"),
    path("addincometag", views.gelir_etiketi_ekleme, name="gelir_etiketi_ekleme"),
    path("delincometag", views.gelir_etiketi_sil, name="gelir_etiketi_sil"),
    path("setincometag", views.gelir_etiketi_duzenle, name="gelir_etiketi_duzenle"),

    path("control/addincometag/<str:hash>", views.gelir_etiketi_ekleme_2, name="gelir_etiketi_ekleme_2"),
    path("control/delincometag/<str:hash>", views.gelir_etiketi_sil_2, name="gelir_etiketi_sil_2"),
    path("control/setincometag/<str:hash>", views.gelir_etiketi_duzenle_2, name="gelir_etiketi_duzenle_2"),
    #gelir etiket işlemleri
    #gider etiketleri #
    path("control/expensetag/<str:hash>", views.gider_etiketi_tipleri_2, name="gider_etiketi_tipleri_2"),
    path("expensetag", views.gider_etiketi_tipleri, name="gider_etiketi_tipleri"),
    path("addexpensetag", views.gider_etiketi_ekleme, name="gider_etiketi_ekleme"),
    path("delexpensetag", views.gider_etiketi_sil, name="gider_etiketi_sil"),
    path("setexpensetag", views.gider_etiketi_duzenle, name="gider_etiketi_duzenle"),
    #gider etiketleri
    #virman olayı #
    path("maketransfer", views.virman_yapma, name="virman_yapma"),
    path("control/maketransfer/<str:hash>", views.virman_yapma_2, name="virman_yapma_2"),
    path("superadmintransfer/<int:id>", views.super_admin_virman, name="super_admin_virman"),
    path("transfer", views.virman_gondermeler, name="virman_gondermeler"),
    path("control/transfer/<str:hash>", views.virman_gondermeler_2, name="virman_gondermeler_2"),
    #virman olayı
    #ürünler olayları
    path("control/products/<str:hash>", views.urun_viev_2, name="urun_viev_2"),
    path("products", views.urun_viev, name="urun_viev"),
    path("addproduct", views.urun_ekle, name="urun_ekle"),
    path("delproduct", views.urun_sil, name="urun_sil"),
    path("setproduct", views.urun_duzenle, name="urun_duzenle"),
    #ürünler olayları
    #gelirler Sayfası#
    path("control/theycome/<str:hash>", views.gelirler_sayfasi_2, name="gelirler_sayfasi_2"),
    path("theycome", views.gelirler_sayfasi, name="gelirler_sayfasi"),
    path("control/addtheycome/<str:hash>", views.gelir_ekle_2, name="gelir_ekle_2"),
    path("addtheycome", views.gelir_ekle, name="gelir_ekle"),
    path("control/addtheycomesave/<str:hash>", views.gelir_faturasi_kaydet_2, name="gelir_faturasi_kaydet_2"),
    path("addtheycomesave", views.gelir_faturasi_kaydet, name="gelir_faturasi_kaydet"),
    path("receivingpayment", views.gelir_odemesi_ekle, name="gelir_odemesi_ekle"),
    path("settheycome/<int:id>", views.gelir_duzenle, name="gelir_duzenle"),
    path("incomesummary", views.gelirler_ozeti, name="gelirler_ozeti"),
    path("control/incomesummary/<str:hash>", views.gelirler_ozeti_2, name="gelirler_ozeti_2"),
    path("viewcome/<int:id>", views.fatura_goster, name="fatura_goster"),
    #gelirler Sayfası#giderler_ozeti_2
    #giderler Sayfası#
    path("control/expenses/<str:hash>", views.giderler_sayfasi_2, name="giderler_sayfasi_2"),
    path("expenses", views.giderler_sayfasi, name="giderler_sayfasi"),
    path("expenseswait", views.giderler_sayfasi_borc, name="giderler_sayfasi_borc"),
    path("control/expenseswait/<str:hash>", views.giderler_sayfasi_borc_2, name="giderler_sayfasi_borc_2"),
    path("control/addexpenses/<str:hash>", views.gider_ekle_2, name="gider_ekle_2"),
    path("addexpenses", views.gider_ekle, name="gider_ekle"),
    path("control/saveaddexpenses/<str:hash>", views.gider_faturasi_kaydet_2, name="gider_faturasi_kaydet_2"),
    path("saveaddexpenses", views.gider_faturasi_kaydet, name="gider_faturasi_kaydet"),
    path("delcomeandexpenses", views.makbuz_sil, name="makbuz_sil"),
    path("savereceivingpayment", views.gider_odemesi_ekle, name="gider_odemesi_ekle"),
    path("setexpenses/<int:id>", views.gider_duzenle, name="gider_duzenle"),
    path("expensessummary", views.giderler_ozeti, name="giderler_ozeti"),
    path("control/expensessummary/<str:hash>", views.giderler_ozeti_2, name="giderler_ozeti_2"),#
    path("viewexpenses/<int:id>", views.fatura_goster2, name="fatura_goster2"),
    path("personnelinvoice/<int:id>", views.personel_gider_faturasi_kesme, name="personel_gider_faturasi_kesme"),
    path("control/personnelinvoice/<int:id>/<str:hash>", views.personel_gider_faturasi_kesme_2, name="personel_gider_faturasi_kesme_2"),
    path("savepersonnelinvoice/", views.gider_faturasi_kaydet_personel, name="gider_faturasi_kaydet_personel"),
    path("control/savepersonnelinvoice/<str:hash>", views.gider_faturasi_kaydet_personel_2, name="gider_faturasi_kaydet_personel_2"),
    #giderler Sayfası #hesap_ekstra_durumu_2
    path('control/search/<str:hash>', views.search_2, name='search_2'),
    path('control/cari/<str:hash>', views.cariler_bilgisi_2, name='cariler_bilgisi_2'),
    path('gelirgiderduzelt', views.gelir_gider_duzelt, name='gelir_gider_duzelt'),
    path('search/', views.search, name='search'),
    path('cari/', views.cariler_bilgisi, name='cariler_bilgisi'),
    path('delivon', views.fatura_sil, name='fatura_sil'),

    #
    path("control/accountingsettings/<str:hash>", views.muhasebe_ayarlari_2, name="muhasebe_ayarlari_2"),
    path("accountingsettings", views.muhasebe_ayarlari, name="muhasebe_ayarlari"),
    path('denme/', views.denme, name='denme'),
    path('kategoriekleme', views.gider_gelir_ekleme, name='gider_gelir_ekleme'),
    path('control/kategoriekleme/<str:hash>', views.gider_gelir_ekleme_2, name='gider_gelir_ekleme_2'),
    path('etiketekleme', views.gider_gelir_etiketekleme, name='gider_gelir_etiketekleme'),
    path('control/etiketeklemee/<str:hash>', views.gider_gelir_etiketekleme_2, name='gider_gelir_etiketekleme_2'),
    path("accountextra", views.hesap_ekstra_durumu, name="hesap_ekstra_durumu"),
    path("control/accountextra/<str:hash>", views.hesap_ekstra_durumu_2, name="hesap_ekstra_durumu_2"),
    path('download-excel/', views.download_excel, name='download_excel'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    #qrfaturasıgöster
    path("viewcomeqr/<int:id>", views.fatura_gosterqr, name="fatura_gosterqr"),
    path("viewexpensesqr/<int:id>", views.fatura_goster2qr, name="fatura_goster2qr"),
    #ürünler KAtegorisi
    path('productscategory/', views.urunler_kategorisi, name='urunler_kategorisi'),
    path('addproductscategory/', views.urunler_kategorisi_ekle, name='urunler_kategorisi_ekle'),
    path('delproductscategory/', views.urunler_kategorisi_sil, name='urunler_kategorisi_sil'),
    path('setproductscategory/', views.urunler_kategorisi_duzenle, name='urunler_kategorisi_duzenle'),

    path('control/productscategory/<str:hash>', views.urunler_kategorisi_2, name='urunler_kategorisi_2'),
    path('control/addproductscategory/<str:hash>', views.urunler_kategorisi_ekle_2, name='urunler_kategorisi_ekle_2'),
    path('control/delproductscategory/<str:hash>', views.urunler_kategorisi_sil_2, name='urunler_kategorisi_sil_2'),
    path('control/setproductscategory/<str:hash>', views.urunler_kategorisi_duzenle_2, name='urunler_kategorisi_duzenle_2'),
    #ürünler KAtegorisi
    #ürünler satin_alma_talabi
    path('purchaserequest/', views.satin_alma_talabi, name='satin_alma_talabi'),
    path('control/purchaserequest/<str:hash>', views.satin_alma_talabi_2, name='satin_alma_talabi_2'),
    path('addpurchaserequest/', views.satin_alma_talebi_ekle, name='satin_alma_talebi_ekle'),
    path('delpurchaserequest/<int:id>/', views.satin_alma_talebi_sil, name='satin_alma_talebi_sil'),
    #ürünler satin_alma_talabi
    path('apleyrequest/', views.satin_alma_talabi_onaylama, name='satin_alma_talabi_onaylama'),
    path('onayapleyrequest/<int:id>/', views.satin_alma_talebi_onayla, name='satin_alma_talebi_onayla'),
    path('redapleyrequest/<int:id>/', views.satin_alma_talebi_red, name='satin_alma_talebi_red'),
    #satın alınma
    path('buyrequest/', views.satin_alma_, name='satin_alma_'),
    path('apleybuyrequest/<int:id>/', views.satin_alma_onayla, name='satin_alma_onayla'),
    path('buyelement/', views.satin_alma_kabuller, name='satin_alma_kabuller'),
    #stoklar
    path('stock/', views.stok, name='stok'),
    path('addstock/', views.stok_girisi_yap, name='stok_girisi_yap'),
    path('zimmetbilgisi/<int:id>/', views.urun_bilgisi, name='urun_bilgisi'),
    #zimmet
    path('debit/', views.zimmetler, name='zimmetler'),
    path('adddebit/', views.zimmet_ekle, name='zimmet_ekle'),
    path('zimmet/<int:id>/', views.zimmet, name='zimmet'),
    path('teslim/<int:id>/<int:iz>/', views.zimmeti_teslim_Al, name='zimmeti_teslim_Al'),
    path('salaryandadvance/', views.avans_maas, name='avans_maas'),
    path('control/salaryandadvance/<str:hash>', views.avans_maas_2, name='avans_maas_2'),
    #########3
    path('control/purchaserequest/<str:hash>', views.satin_alma_talabi_2, name='satin_alma_talabi_2'),
    path('control/addpurchaserequest/<str:hash>', views.satin_alma_talebi_ekle_2, name='satin_alma_talebi_ekle_2'),
    path('control/delpurchaserequest/<int:id>/<str:hash>', views.satin_alma_talebi_sil_2, name='satin_alma_talebi_sil_2'),
    #ürünler satin_alma_talabi
    path('control/apleyrequest/<str:hash>', views.satin_alma_talabi_onaylama_2, name='satin_alma_talabi_onaylama_2'),
    path('control/onayapleyrequest/<int:id>/<str:hash>', views.satin_alma_talebi_onayla_2, name='satin_alma_talebi_onayla_2'),
    path('control/redapleyrequest/<int:id>/<str:hash>', views.satin_alma_talebi_red_2, name='satin_alma_talebi_red_2'),
    #satın alınma
    path('control/buyrequest/<str:hash>', views.satin_alma_2, name='satin_alma_2'),
    path('control/apleybuyrequest/<int:id>/<str:hash>', views.satin_alma_onayla_2, name='satin_alma_onayla_2'),
    path('control/buyelement/<str:hash>', views.satin_alma_kabuller_2, name='satin_alma_kabuller_2'),
    #stoklar
    path('control/stock/<str:hash>', views.stok_2, name='stok_2'),
    path('control/addstock/<str:hash>', views.stok_girisi_yap_2, name='stok_girisi_yap_2'),
    #zimmet
    path('control/debit/<str:hash>', views.zimmetler_2, name='zimmetler_2'),
    path('control/adddebit/<str:hash>', views.zimmet_ekle_2, name='zimmet_ekle_2'),
    path('control/teslim/<int:id>/<int:iz>/<str:hash>', views.zimmeti_teslim_Al_2, name='zimmeti_teslim_Al_2'),
]
#zimmeti_teslim_Al_1
#accounting
#
