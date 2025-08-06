# utils/firebase.py

import os
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, messaging
service={
  "type": "service_account",
  "project_id": "biadago-cloud",
  "private_key_id": "70e24c8bcac3a97b664fb3a14c79322736d59576",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDWvSHVgKNhVZmr\n1tS5q+YmEgguBgrgOMXbvy/yFUArRYkO1i5mIS8tGtuQEsWX3Xytomk7/bKFsrkk\nk42eGAdtNX9PaR70WZBgo2ScEsp9cfnALLR9Qobmgef3SDmGdJpYgTZSc6isCtC/\nOrARC7pQlZjHbafRFzFONRJPfVHHpi67J1LGJaOND9/+CK2+r8qhEWujGBmgKR3i\nQ9pfKTXWmJsabx1d0aaSTBoLUPfWaUa75EP321JFhVRRVWg485L2BF7RceU4J1cK\n3Po7knfOClfzW8lfSWSO7p6OaAgHfz9kn5vxXMgh7DncfJXFw5dJ8++V9kqsS4jw\ntrY13mHJAgMBAAECggEANey51d0fah5uYCYrNlMSEQZfMnuG+KaZHSVGO4MVoagt\nEmI7tZ7os2l2sJfeMdRHbm0GAzAiyAtJDgPVwNkk6EpSZZUu1kq1hGcTqVPYsKbS\nAm3Xh0sRCEqf/0uOUpLufYI5K3xq44U1xYfN1gH9cCYY/x+s0EeENLEEH50HT9yY\nK7v9RfNx69anfflIlrRt3VHm5Ocj+bGKeBzoMQ+YiIC91fNAa85jr+heOdvnObmP\n2ipEQSmhmyze1Z+Fdxz+GBXA74f0c78tLjBU3WiGHBf2EXMSUCtbTSsiuF9DZpyN\nf1/U+cKJ1EDmajUvwpSEj1tDwihXPE1hFuruYwioZwKBgQD0lTQUU16KGbBeLxUT\nKH6GZlQJbl7v6jHAKzHn/8QaZfsfoF2VKw3f4yRaAESS48NdvIOC8rPsEp9yjzNs\nV38jRFyAI5WgFVIhZR3gyIiFHjhyBLKMWQAh024zWBw9GvFwCG8Uc2aNAyPGgjLH\nn/ZWY1RdxLpf8D8eF4+RIvk6swKBgQDgw0no40cHC2CjMBrtLWOOMstxNEeIsYxf\n7+csRwXyWWkIW4JHOyTpKGBQjC+SNic8KvQ7+DywrCS7igz3qcKRIvBhUq9qtt6v\nDtpX8k48MO9VeumcDDHLy/27vchC40ikW92VWa3X5ZE+FQjux0K3cP1do3gUEgE+\nHVbBLcIfkwKBgQDwVQR9zIYjUabahY1B7BKX4klFkyy6tvf4CvnZLJv4DKm8pAoR\nH+NcUohP39+CL0iz/R+FNxPRL2N6YHh5R2josK3sRAss6IZxxjibvrFXjSCN+Uux\nWWsl0eqBjV0CNk10dvUftV3ZxnILB7j6K5cVwDkQgtVYnGyJF0G9rg4UvQKBgAQY\nSr5tdZvRPz953uO3UfsDPeWgGDWLVo1g54tM9/TEYD+Au0zk7PU6gRa2lx9I0Uot\nVinJigGGAV1RVI8mjp7qTgrX4M5G6qOx15SGm5pJIfMivCLVrgqSetryyDU/wtEL\nw2u3KI2oZw8EfxcqljKVYmhUVBm5gkBJdI0scj71AoGBAKkpu+NVy55oql/fYMRv\ngXd7KSAGE5UdR0MYRPe8SJ4o5G1rrDahjW7N9LWwJQwWxek5xHCkFJOndE1g4jP9\nVbjKqD4iqyiyuSi/6wWWdEbOMZrp7t+MTGRPELXns3Fjl/aDmDNd3uyW2QhIgqjl\nqbOmlytGXqUhIS+DW4WU8ALI\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-x8ood@biadago-cloud.iam.gserviceaccount.com",
  "client_id": "118028014141792543512",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-x8ood%40biadago-cloud.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
# Firebase servis hesabı JSON dosyasının yolu
BASE_DIR = Path(__file__).resolve().parent.parent
cred_path = service  # JSON dosyasının adı dosya sistemindeki isme göre değişebilir

# Firebase Admin SDK'yı başlat
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

# Bildirim gönderme fonksiyonu
def send_fcm_notification(token, title, body, data=None):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=token,
            data=data or {},
        )
        response = messaging.send(message)
        return response
    except Exception as e:
        print(f"Bildirim gönderilemedi: {e}")
        return None
