from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(personel_dosyalari)
admin.site.register(LockScreenStatus)
admin.site.register(faturalardaki_gelir_gider_etiketi_ozel)
admin.site.register(personel_izinleri)
admin.site.register(bagli_kullanicilar)
admin.site.register(calisanlar_kategorisi)
admin.site.register(calisanlar_pozisyonu)
admin.site.register(calisanlar)
admin.site.register(calisan_maas_durumlari)
admin.site.register(calisanlar_calismalari)
