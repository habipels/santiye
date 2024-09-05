from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.


admin.site.register(Kasa)
admin.site.register(gelir_kategorisi)
admin.site.register(gider_kategorisi)
admin.site.register(gelir_etiketi)
admin.site.register(gider_etiketi)
admin.site.register(Gelir_Bilgisi)
admin.site.register(Gider_Bilgisi)
admin.site.register(virman)
admin.site.register(urunler)
admin.site.register(gider_urun_bilgisi)
admin.site.register(gelir_urun_bilgisi)
admin.site.register(Gelir_odemesi)
admin.site.register(Gider_odemesi)
admin.site.register(faturalar_icin_logo)
admin.site.register(gelir_qr)
admin.site.register(gider_qr)
admin.site.register(Gelir_excel_ekleme)
admin.site.register(Gider_excel_ekleme)
admin.site.register(faturalar_icin_bilgiler)
@admin.register(cari)
class CariAdmin(SimpleHistoryAdmin):
    pass