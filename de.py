import requests

url = "http://localhost:8000/biadago/api/progresstracking/14/"
token = "2afd5cfac3ca06bbad66500169c69a62e114ed7d"  # Kendi token bilginizi buraya girin

headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}



# PUT isteği gönderme
response = requests.get(url, headers=headers)

# Yanıtı kontrol etme
if response.status_code == 200:
    print("Kalem başarıyla güncellendi:", response.json())
else:
    print("Hata oluştu:", response.status_code)