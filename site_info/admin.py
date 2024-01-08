from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(proje_tipi)
admin.site.register(santiye)
admin.site.register(bloglar)
admin.site.register(santiye_kalemleri)
admin.site.register(santiye_kalemlerin_dagilisi)
admin.site.register(projeler)
admin.site.register(proje_dosyalari)
admin.site.register(taseronlar)
admin.site.register(taseron_sozlesme_dosyalari)
admin.site.register(cari_taseron_baglantisi)
admin.site.register(taseron_hakedisles)
admin.site.register(klasorler)
admin.site.register(klasor_dosyalari)
admin.site.register(Event)
admin.site.register(YapilacakPlanlari)
admin.site.register(YapilacakDosyalari)

admin.site.register(IsplaniPlanlari)
admin.site.register(IsplaniDosyalari)