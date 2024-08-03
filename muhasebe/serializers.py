# serializers.py
from rest_framework import serializers
from .models import Gider_Bilgisi

class FaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gider_Bilgisi
        fields = [
            'id',
            'fatura_no',
            'cari_bilgisi',
            'aciklama',
            'fatura_tarihi',
            'vade_tarihi',
            'toplam_tutar',
            'kalan_tutar',
            'silinme_bilgisi',
            'odeme',
            'gelir_kime_ait_oldugu',
        ]
