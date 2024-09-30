import requests

# Giriş URL'si (bu URL, API'deki CustomAuthToken view'e gider)
url = "http://127.0.0.1:8000/biadago/api/api-token-auth/"

# Giriş bilgileri
data = {
    "username": "habipelis65@gmail.com",
    "password": "Habip6565."
}

# İstek gönderme
response = requests.post(url, data=data)

# Yanıtı kontrol etme
if response.status_code == 200:
    try:
        # Başarılı ise token alınıyor
        token = response.json().get('token')
        print(f"Giriş başarılı! Token: {token}")
    except ValueError:
        # JSON formatında bir yanıt yoksa yanıtı ham haliyle yazdır
        print("Yanıt JSON formatında değil!")
        print(response.text)
else:
    # Hatalı ise hata mesajı ve yanıtı gösteriliyor
    print(f"Giriş başarısız! Status kodu: {response.status_code}")
    print("Yanıt içeriği:")
    print(response.text)
