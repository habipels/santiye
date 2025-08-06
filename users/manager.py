import socket

def notify_tcp_server(user_id, message, host="127.0.0.1", port=9001):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(str(user_id).encode())  # İlk bağlantı için user_id yolluyoruz
        sock.close()
    except Exception as e:
        print(f"[TCP Notify Error] {e}")
