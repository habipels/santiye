import firebase_admin
from firebase_admin import credentials, messaging

service = {
    # senin verdiğin service_account JSON içeriği burada...
}

if not firebase_admin._apps:
    cred = credentials.Certificate(service)
    firebase_admin.initialize_app(cred)

def send_fcm_notification(token, title, body, platform="android", url=None, screen=None, extra_data=None):
    try:
        data_payload = extra_data or {}

        # Platforma göre uygun ek verileri data payload'a ekle
        if platform == "web" and url:
            data_payload["url"] = url
        elif platform in ["android", "ios"]:
            if screen:
                data_payload["screen"] = screen
            if extra_data:
                data_payload.update(extra_data)

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=token,
            data={k: str(v) for k, v in data_payload.items()},  # Tüm data string olmalı
        )

        response = messaging.send(message)
        return response
    except Exception as e:
        print(f"Bildirim gönderilemedi: {e}")
        return None
