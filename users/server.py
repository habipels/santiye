import socket
import threading

active_users = {}  # user_id: socket objesi

def handle_client(client_socket, addr):
    try:
        user_id = client_socket.recv(1024).decode().strip()
        print(f"[TCP] Kullanıcı {user_id} bağlandı: {addr}")

        active_users[user_id] = client_socket

        while True:
            # TCP açık olduğu sürece dinle ama veri beklenmiyor
            data = client_socket.recv(1024)
            if not data:
                break

    except Exception as e:
        print(f"[TCP] Hata: {e}")
    finally:
        print(f"[TCP] Bağlantı sonlandı: {addr}")
        if user_id in active_users:
            del active_users[user_id]
        client_socket.close()

def run_server(host="127.0.0.1", port=9001):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(10)
    print(f"[TCP] Dinleniyor: {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

def send_message_to_user(user_id, message):
    socket_conn = active_users.get(str(user_id))
    if socket_conn:
        try:
            socket_conn.send(message.encode())
            print(f"[TCP] Mesaj gönderildi -> user_id {user_id}: {message}")
        except:
            print(f"[TCP] Kullanıcıya mesaj gönderilemedi: {user_id}")

# Bu modül doğrudan çalıştırıldığında server başlasın
if __name__ == "__main__":
    run_server()
