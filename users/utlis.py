# utils/firebase.py

import os
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, messaging

# Firebase servis hesabı JSON dosyasının yolu
BASE_DIR = Path(__file__).resolve().parent.parent
cred_path = os.path.join(BASE_DIR, 'biadago_service_account.json')  # JSON dosyasının adı dosya sistemindeki isme göre değişebilir

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
