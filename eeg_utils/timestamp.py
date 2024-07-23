from pyOpenBCI import OpenBCICyton
import numpy as np
import time
import os
import asyncio
import websockets
import json

class EEGDataCollector:
    def __init__(self, port, save_duration, debug=False):
        self.port = port
        self.eeg_data = []
        self.board = OpenBCICyton(port=self.port, daisy=False)
        self.uVolts_per_count = (4500)/24/(2**23-1)
        self.sample_rate = 250
        self.start_time = time.time()
        self.save_duration = save_duration
        self.cnt = 0
        self.debug = debug
        self.folder = self.make_folder()
        self.loop = asyncio.get_event_loop()
        self.websocket = None

    def make_folder(self):
        folder = "../data"
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    async def connect_to_server(self, uri):
        self.websocket = await websockets.connect(uri)
        print(f"Connected to server at {uri}")

    def collect_data(self):
        print("Start collecting data")
        self.board.start_stream(self.m_callback)

    def m_callback(self, sample):
        current_time = time.time()
        data_with_timestamp = {
            "timestamp": current_time,
            "data": (np.array(sample.channels_data) * self.uVolts_per_count).tolist()
        }
        asyncio.run_coroutine_threadsafe(self.send_to_server(data_with_timestamp), self.loop)

        if self.debug:
            print(data_with_timestamp)      

    async def send_to_server(self, data):
        try:
            data_to_send = json.dumps(data)
            await self.websocket.send(data_to_send)
            response = await self.websocket.recv()
            print("Response from server:", response)
        except Exception as e:
            print("Failed to send data:", e)

    async def start_collecting(self, uri):
        await self.connect_to_server(uri)
        # 在后台运行数据收集任务
        await self.loop.run_in_executor(None, self.collect_data)

    def start(self, uri):
        self.loop.run_until_complete(self.start_collecting(uri))

if __name__ == "__main__":
    port = "COM5"
    uri = "ws://localhost:5000"
    eeg_data_collector = EEGDataCollector(port, save_duration=5, debug=True)
    try:
        eeg_data_collector.start(uri)
    except KeyboardInterrupt:
        eeg_data_collector.board.stop_stream()
        print("Data collection stopped")
        exit()
    except Exception as e:
        print("An error occurred:", e)
        eeg_data_collector.board.stop_stream()
        print("Data collection stopped")
        exit()
