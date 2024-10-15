import requests

# API URL
url = "https://cloud.biadago.com/biadago/api/thingstodo/"  # API URL'nizi buraya yazın

# Kullanıcıya ait JWT veya diğer kimlik doğrulama bilgileri
headers = {
    'Authorization': 'Token 728799007d33d1be1ab3f4d03e9dc183d5f8f8d1',  # Token'ınızı buraya girin
}

# API'ye istek gönderin
response = requests.get(url, headers=headers)
print(response.json())
# Yanıtı kontrol et
if response.status_code == 201 or response.status_code == 200:
    print('Yanıt:')
else:
    print('Durum Kodu:', response.status_code)
