import requests

# API URL
url = "http://localhost:8000/biadago/api/progresspayment/"  # API URL'nizi buraya yazın

# Kullanıcıya ait JWT veya diğer kimlik doğrulama bilgileri
headers = {
    'Authorization': 'Token 2afd5cfac3ca06bbad66500169c69a62e114ed7d',  # Token'ınızı buraya girin
}


# API'ye GET isteği gönder
response = requests.get(url, headers=headers)

# Yanıtı kontrol etme
if response.status_code == 200:
    print("Veriler başarıyla alındı:", response.json())
else:
    print("Hata:", response.status_code, response.text)
