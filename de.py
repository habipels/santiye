import requests

url = "http://localhost:8000/biadago/api/constructionsite/6/"
token = "2afd5cfac3ca06bbad66500169c69a62e114ed7d"  # Kendi token bilginizi buraya girin

headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
print(response.json())
if response.status_code == 204:
    print("Blog başarıyla silindi.")
    # Yönlendirme URL'sini alıp, işleminiz için kullanabilirsiniz
    print("Başarıyla Silindi:", response.json())
else:
    print("Hata oluştu:", response.status_code)