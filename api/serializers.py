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

class SantiyeSerializer(serializers.ModelSerializer):
    class Meta:
        model = santiye
        fields = '__all__'

class BloglarSerializer(serializers.ModelSerializer):
    class Meta:
        model = bloglar
        fields = '__all__'

class BirimlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = birimler
        fields = '__all__'
class SantiyeKalemleriSerializer(serializers.ModelSerializer):
    class Meta:
        model = santiye_kalemleri
        fields = '__all__'
class SantiyeKalemlerinDagilisiSerializer(serializers.ModelSerializer):
    class Meta:
        model = santiye_kalemlerin_dagilisi
        fields = '__all__'

class ProjelerSerializer(serializers.ModelSerializer):
    class Meta:
        model = projeler
        fields = '__all__'

class TaseronlarSerializer(serializers.ModelSerializer):
    class Meta:
        model = taseronlar
        fields = '__all__'
class SozlesmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = taseron_sozlesme_dosyalari
        fields = '__all__'
class TaseronHakedislesSerializer(serializers.ModelSerializer):
    class Meta:
        model = taseron_hakedisles
        fields = '__all__'

class KlasorlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = klasorler
        fields = '__all__'  # Veya ihtiyacınıza göre belirli alanları seçin
class KlasorDosyalariSerializer(serializers.ModelSerializer):
    class Meta:
        model = klasor_dosyalari
        fields = '__all__'  # Veya ihtiyacınıza göre belirli alanları seçin

class IsplaniPlanlariSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsplaniPlanlari
        fields = '__all__'  # Veya ihtiyacınıza göre belirli alanları seçin
class IsplaniDosyalariSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsplaniDosyalari
        fields = '__all__'  # Veya ihtiyacınıza göre belirli alanları seçin
class IsplaniIlerlemeDosyalariSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsplaniIlerlemeDosyalari
        fields = '__all__'  # Veya ihtiyacınıza göre belirli alanları seçin

class IsplaniPlanlariIlerlemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsplaniPlanlariIlerleme
        fields = '__all__'  # Veya ihtiyacınıza göre belirli alanları seçin

class YapilacakPlanlariSerializer(serializers.ModelSerializer):
    class Meta:
        model = YapilacakPlanlari
        fields = '__all__'  # Veya ihtiyacınıza göre belirli alanları seçin


from rest_framework import serializers
from users.models import Group, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__' 




class SenderSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'image',
            'telefon_numarasi',
            'gorevi',
            'status',
            'email',
            'online'
        ]

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return "https://cloud.biadago.com/static/go/images/profile.png"

class MessageSerializer(serializers.ModelSerializer):
    sender = SenderSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'group',
            'content',
            'timestamp',
            'file',
            'read',
        ]
