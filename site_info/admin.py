from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(birimler)

admin.site.register(bina_goruntuleri)
admin.site.register(santiye_sablonlari)
admin.site.register(sanytiye_sablon_bolumleri)
admin.site.register(santiye_imalat_kalemleri)
admin.site.register(imalat_kalemleri_imalat_detaylari)