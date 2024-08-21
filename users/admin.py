from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(personel_dosyalari)
admin.site.register(LockScreenStatus)
admin.site.register(faturalardaki_gelir_gider_etiketi_ozel)