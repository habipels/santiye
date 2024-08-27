import requests

url = "http://localhost:8000/biadago/api/del/sitebloglist/"
token = "2afd5cfac3ca06bbad66500169c69a62e114ed7d"  # Kendi token bilginizi buraya girin

data = {
    "buttonId": 15,  # Silinecek Blog ID'si
}

headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers, json=data)

if response.status_code == 204:
    print("Blog başarıyla silindi.")
    # Yönlendirme URL'sini alıp, işleminiz için kullanabilirsiniz
    print("Başarıyla Silindi:", response.status_code)
else:
    print("Hata oluştu:", response.status_code)