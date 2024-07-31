import asyncio
import websockets
import json

connected_clients = set()

async def process_signal(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            classification_data = json.loads(message)
            print(f"Received classification data: {classification_data}")
            arm_command = convert_to_arm_command(classification_data)
            response = json.dumps({"status": "received", "command": arm_command})
            await websocket.send(response)
    finally:
        connected_clients.remove(websocket)

def convert_to_arm_command(classification_data):
    return classification_data

async def send_to_arm_control(arm_command):
    async with websockets.connect("ws://localhost:5000") as websocket:
        await websocket.send(json.dumps(arm_command))
        response = await websocket.recv()
        print(f"Response from arm control client: {response}")

start_server = websockets.serve(process_signal, "localhost", 5000)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
