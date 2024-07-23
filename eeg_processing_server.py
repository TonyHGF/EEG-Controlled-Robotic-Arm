import asyncio
import websockets
import json
import numpy as np

WS_PORT = 5000
DATA_FILE = "data_cache.json"

data_cache = {"timestamps": [], "channels": [[] for _ in range(8)]}
buffer_size = 1000  # 缓存大小，调整以适应你的需求

async def process_signal(data):
    # 这里可以添加任何信号处理逻辑
    return data

async def ws_handler(websocket, path):
    print("WebSocket connection established")
    try:
        async for message in websocket:
            data = json.loads(message)
            print("Received data via WebSocket:", data)

            # 添加数据到缓存
            timestamp = data["timestamp"]
            channels = data["data"]
            data_cache["timestamps"].append(timestamp)
            for i in range(8):
                data_cache["channels"][i].append(channels[i])

            # 维护缓存大小
            if len(data_cache["timestamps"]) > buffer_size:
                data_cache["timestamps"] = data_cache["timestamps"][-buffer_size:]
                for i in range(8):
                    data_cache["channels"][i] = data_cache["channels"][i][-buffer_size:]

            # 将数据写入文件
            with open(DATA_FILE, 'w') as f:
                json.dump(data_cache, f)

            # 处理接收到的数据
            processed_data = await process_signal(data)

            # 发送响应
            response = "Message received"
            await websocket.send(response)
            print(f"Sent response: {response}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        print("WebSocket connection closed")

async def main():
    async with websockets.serve(ws_handler, "localhost", WS_PORT):
        print(f"Serving WebSocket on port {WS_PORT}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    
    asyncio.run(main())
