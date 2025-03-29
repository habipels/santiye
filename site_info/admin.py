from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(birimler)

admin.site.register(bina_goruntuleri)
admin.site.register(checkdaireleri)
admin.site.register(blog_ortak_alan_ve_cepheleri)
admin.site.register(imalat_daire_balama)
admin.site.register(gantt_olayi)
admin.site.register(check_liste_onaylama_gruplari)
admin.site.register(rfi_sablonlar)
admin.site.register(rfi_kontrol)
admin.site.register(IsplaniPlanlari)
admin.site.register(rapor_bilgisi)