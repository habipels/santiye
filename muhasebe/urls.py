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
    #gelir kategorileri
    #gider kategorileri}
    path("control/inwcategory/<str:hash>", views.gider_kategorisi_tipleri_2, name="gider_kategorisi_tipleri_2"),
    path("inwcategory", views.gider_kategorisi_tipleri, name="gider_kategorisi_tipleri"),
    path("addwcategory", views.gider_kategorisi_ekleme, name="gider_kategorisi_ekleme"),
    path("delwcategory", views.gider_kategoisi_sil, name="gider_kategoisi_sil"),
    path("setwcategory", views.gider_kategorisi_duzenle, name="gider_kategorisi_duzenle"),
    #gider kategorileri
    #cari işlemleri$
    path("control/current/<str:hash>", views.cari_viev_2, name="cari_viev_2"),
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
    path("viewcome/<int:id>", views.fatura_goster, name="fatura_goster"),
    #gelirler Sayfası#
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
    path("viewexpenses/<int:id>", views.fatura_goster2, name="fatura_goster2"),
    #giderler Sayfası
    path('control/search/<str:hash>', views.search_2, name='search_2'),
    path('control/cari/<str:hash>', views.cariler_bilgisi_2, name='cariler_bilgisi_2'),
    path('gelirgiderduzelt', views.gelir_gider_duzelt, name='gelir_gider_duzelt'),
    path('search/', views.search, name='search'),
    path('cari/', views.cariler_bilgisi, name='cariler_bilgisi'),
    path('delivon', views.fatura_sil, name='fatura_sil'),

    #
    path("accountingsettings/<str:hash>", views.muhasebe_ayarlari_2, name="muhasebe_ayarlari_2"),
    path("accountingsettings", views.muhasebe_ayarlari, name="muhasebe_ayarlari"),
    path('denme/', views.denme, name='denme'),
    path('kategoriekleme', views.gider_gelir_ekleme, name='gider_gelir_ekleme'),
    path('etiketekleme', views.gider_gelir_etiketekleme, name='gider_gelir_etiketekleme'),
    path("accountextra", views.hesap_ekstra_durumu, name="hesap_ekstra_durumu"),
    path('download-excel/', views.download_excel, name='download_excel'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    #qrfaturasıgöster
    path("viewcomeqr/<int:id>", views.fatura_gosterqr, name="fatura_gosterqr"),
    path("viewexpensesqr/<int:id>", views.fatura_goster2qr, name="fatura_goster2qr"),
]
#

