import requests

# API URL'sini tanımlayın
url = "http://127.0.0.1:8000/biadago/api/statusthingstodo/"  # Güncel URL'inizi buraya yazın
token = "2afd5cfac3ca06bbad66500169c69a62e114ed7d"  # Geçerli token'inizi buraya yazın

# Header bilgisi
headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}
data={
    "id" : 64
}
# API'ye GET isteği gönder
response = requests.post(url,json=data, headers=headers)

# Yanıtı kontrol et
if response.status_code == 200:
    print("Veriler başarıyla alındı:", response.json())
elif response.status_code == 401:
    print("Yetkisiz erişim. Token geçersiz veya sağlanmadı.")
else:
    print("Başka bir hata:", response.status_code)
