import requests

url = "http://localhost:8000/biadago/api/create/sitebloglist/"
token = "2afd5cfac3ca06bbad66500169c69a62e114ed7d"  # Kendi token bilginizi buraya girin

data = {
    "santiye_bilgisi": 6,  # Santiye ID'si
    "blok_adi": "Yeni Blok Adı",
    "kat_sayisi": 25,
    "baslangictarihi": "2024-01-01",
    "bitistarihi": "2024-12-31"
}

headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
    print("Blog başarıyla oluşturuldu:", response.json())
else:
    print("Hata oluştu:", response.status_code, response.text)
