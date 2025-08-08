import asyncio
import websockets
import json

# WebSocket sunucu adresin, domain veya localhost olabilir
WS_SERVER_URL = "wss://cloud.biadago.com/ws/global/"  # Django Channels sunucun burada çalışıyor olmalı

async def listen_to_global_chat():
    async with websockets.connect(WS_SERVER_URL) as websocket:
        print("[WS] Global chat bağlantısı kuruldu.")

        try:
            while True:
                message = await websocket.recv()
                data = json.loads(message)

                if data.get("type") == "global_message":
                    print(f"[GLOBAL MESAJ] {data}")
                else:
                    print(f"[Diğer Veri] {data}")
        except websockets.ConnectionClosed:
            print("[WS] Bağlantı kapandı.")
        except Exception as e:
            print(f"[HATA] {e}")

if __name__ == "__main__":
    asyncio.run(listen_to_global_chat())
