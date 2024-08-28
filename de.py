import requests

# API URL
url = "http://localhost:8000/biadago/api/update/thingstodo/"  # API URL'nizi buraya yazın

# Kullanıcıya ait JWT veya diğer kimlik doğrulama bilgileri
headers = {
    'Authorization': 'Token 2afd5cfac3ca06bbad66500169c69a62e114ed7d',  # Token'ınızı buraya girin
}
# API'ye gönderilecek veri
# Gönderilecek veri
data = {
    'id_bilgisi': 1,  # Güncellenecek proje ID'si
    'baslik': 'Yeni Başlık',
    'durum': 'Tamamlandı',
    'aciliyet': 'Yüksek',
    'teslim_tarihi': '2024-09-01',
    'kullanicilari': [14],  # Atanacak kullanıcı ID'leri
    'aciklama': 'Yeni açıklama'
}

# Dosyalar
files = {
    'file': open(r"C:\Users\habip\Downloads\belge.pdf", 'rb')  # Gönderilecek dosyayı belirtin
}



# POST isteği gönder
response = requests.get(url, data=data, files=files, headers=headers)

# Yanıtı kontrol et
if response.status_code == 201:
    print("Görev başarıyla oluşturuldu.")
elif response.status_code == 403:
    print("Erişim reddedildi.")
else:
    print(f"Hata oluştu: {response.status_code}")
    print(response.json())
