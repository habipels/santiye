from rest_framework import serializers
from muhasebe.models import Gelir_Bilgisi, Gider_Bilgisi, CustomUser, Kasa
from site_info.models import *
class GelirBilgisiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gelir_Bilgisi
        fields = '__all__'  # Veya belirli alanları listeleyin

class GiderBilgisiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gider_Bilgisi
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class KasaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kasa
        fields = '__all__'
class ProjeTipiSerializer(serializers.ModelSerializer):
    class Meta:
        model = proje_tipi
        fields = '__all__'