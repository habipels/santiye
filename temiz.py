import requests

# API URL'sini tanımlayın
url = "http://localhost:8000/biadago/api/siteprojectlist/"  # Güncel URL'inizi buraya yazın
token = "728799007d33d1be1ab3f4d03e9dc183d5f8f8d1"  # Geçerli token'inizi buraya yazın

# Header bilgisi
headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

# API'ye GET isteği gönder
response = requests.get(url, headers=headers)

# Yanıtı kontrol et
if response.status_code == 200:
    print("Veriler başarıyla alındı:", response.json())
elif response.status_code == 401:
    print("Yetkisiz erişim. Token geçersiz veya sağlanmadı.")
else:
    print("Başka bir hata:", response.status_code, response.text)
