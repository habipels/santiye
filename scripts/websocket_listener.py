import asyncio
import websockets
import json

async def listen_to_group_chat(group_id):
    websocket_url = f"ws://cloud.biadago.com/ws/chat/{group_id}/"  # Replace with your WebSocket URL

    async with websockets.connect(websocket_url) as websocket:
        print(f"Connected to WebSocket for group {group_id}")

        try:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
             
                print(f"New message received:")
                print(f"User: {data['user']}")
                print(f"Message: {data['message']}")
                print(f"Timestamp: {data.get('timestamp', 'N/A')}")  # Handle missing timestamp
        except websockets.ConnectionClosed:
            print("WebSocket connection closed")

if __name__ == "__main__":
    group_id = input("Enter the group ID to listen to: ")
    asyncio.run(listen_to_group_chat(group_id))
