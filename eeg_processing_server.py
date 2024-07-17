# signal_processing_server.py
import asyncio
import websockets
import json
import random

async def send_classification(websocket, path):
    # while True:
        
        # signal_data = {"eeg_data": random.choice([1, 2, 3])}  # 模拟信号数据
        # signal_data = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])  # 模拟信号数据
    for i in range(10):
        signal_data = i
        # classification_result = classify_signal(signal_data)
        # await websocket.send(json.dumps(classification_result))
        await websocket.send(json.dumps(signal_data))
        await asyncio.sleep(3)  # 模拟信号处理和分类间隔

def classify_signal(signal_data):
    if signal_data["eeg_data"] == 1:
        return {"classification": "move_up"}
    elif signal_data["eeg_data"] == 2:
        return {"classification": "move_down"}
    elif signal_data["eeg_data"] == 3:
        return {"classification": "move_left"}
    return {"classification": "unknown"}

def run_server():
    start_server = websockets.serve(send_classification, "localhost", 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    run_server()
