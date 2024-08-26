import requests

# API URL'sini ve Authorization Token'ını tanımlayın
url = "http://localhost:8000/biadago/api/update/projecttype/"  # URL'yi kendi API yolunuza göre güncelleyin
token = "2afd5cfac3ca06bbad66500169c69a62e114ed7d"  # Kendi token bilginizi buraya girin

# Gönderilecek veriler
data = {
    "buttonId": 6,  # Güncellenecek proje türü ID'sini buraya yazın
    "yetkili_adi": "Güncellenmiş Proje Tipi",  # Yeni proje tipi adını buraya yazın
    "silinmedurumu": "1",  # Silinme durumu: "1" False, "2" True
    "kullanici": 2  # Kullanıcı ID'sini buraya yazın (sadece super admin için)
}

# Header bilgisi
headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

# API'ye PATCH isteği gönder
response = requests.patch(url, json=data, headers=headers)

# Yanıtı kontrol et
if response.status_code == 200:
    print("Proje tipi başarıyla güncellendi:", response.json())
elif response.status_code == 400:
    print("Hata oluştu:", response.json())
else:
    print("Başka bir hata:", response.status_code, response.text)
