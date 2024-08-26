import requests

# API URL'sini ve Authorization Token'ını tanımlayın
url = "http://localhost:8000/biadago/api/del/projecttype/"  # URL'yi kendi API yolunuza göre güncelleyin
token = "2afd5cfac3ca06bbad66500169c69a62e114ed7d"  # Kendi token bilginizi buraya girin

# Gönderilecek veriler
data = {
    "id": 5  # Silinecek proje türü ID'sini buraya yazın
}

# Header bilgisi
headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

response = requests.get(url, json=data, headers=headers)

# Yanıtı kontrol et
if response.status_code == 200:
    print("Proje tipi başarıyla silindi:", response.json())
elif response.status_code == 400:
    print("Hata oluştu:", response.json())
else:
    print("Başka bir hata:", response.status_code, response.text)
