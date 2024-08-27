import requests

# API URL
url = "http://localhost:8000/biadago/api/create/myfiles/"  # API URL'nizi buraya yazın

# Kullanıcıya ait JWT veya diğer kimlik doğrulama bilgileri
headers = {
    'Authorization': 'Token 2afd5cfac3ca06bbad66500169c69a62e114ed7d',  # Token'ınızı buraya girin
}

# API'ye gönderilecek veriler
data = {
    'ust_klasor': None,  # varsa, üst klasör ID'si
    'klasor': 'Yeni Klasör Adı'
}

# API'ye istek gönderin
response = requests.get(url, data=data, headers=headers)

# Yanıtı kontrol et
if response.status_code == 201:
    print('Klasör başarıyla oluşturuldu!')
    print('Yanıt:', response.json())
else:
    print('Klasör oluşturulamadı.')
    print('Durum Kodu:', response.status_code)
    print('Yanıt:', response.json())