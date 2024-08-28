import requests

# API URL
url = "http://localhost:8000/biadago/api/report/16"  # API URL'nizi buraya yazın

# Kullanıcıya ait JWT veya diğer kimlik doğrulama bilgileri
headers = {
    'Authorization': 'Token 2afd5cfac3ca06bbad66500169c69a62e114ed7d',  # Token'ınızı buraya girin
}
# API'ye gönderilecek veri
# Gönderilecek veri
data = {
    'id': 1,  # Güncellenmek istenen YapilacakPlanlari nesnesinin ID'si
    'baslik': 'Yeni Başlık',
    'durum': 'Tamamlandı',
    'aciliyet': 'Yüksek',
    'teslim_tarihi': '2024-09-01',
    'aciklama': 'Güncellenmiş açıklama',
    'kullanicilari': [14],  # İlgili kullanıcı ID'leri
}

# Dosyalar
files = {
    'file': open(r"C:\Users\habip\Downloads\belge.pdf", 'rb')  # Gönderilecek dosyayı belirtin
}



# POST isteği gönder
response = requests.get(url, headers=headers)

# Yanıtı kontrol et
if response.status_code == 201:
    print("Görev başarıyla oluşturuldu.")
elif response.status_code == 403:
    print("Erişim reddedildi.")
else:
    print(f"Hata oluştu: {response.status_code}")
    print(response.json())
