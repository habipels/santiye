from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(cari)
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