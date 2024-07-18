from pyOpenBCI import OpenBCICyton
import numpy as np
import time
import os
import asyncio
import websockets
import json

class EEGDataCollector:
    def __init__(self, port):
        self.port = port
        self.eeg_data = []
        self.board = OpenBCICyton(port=self.port, daisy=False)
        self.uVolts_per_count = (4500)/24/(2**23-1)
        self.start_time = time.time()

    def collect_data(self):
        self.board.start_stream(self.debug)

    def debug(self, sample):
        duration = time.time() - self.start_time
        if duration < 20:
            # print(duration)
            self.eeg_data.append(np.array(sample.channels_data) * self.uVolts_per_count)
        else:
            self.board.stop_stream()
            self.save_data("../data/eeg_data.npy")
            print("Data saved to", os.path.abspath("../data/eeg_data.npy"))

    async def send_to_server(self, websocket, path):
        while True:
            if self.eeg_data:
                data_to_send = json.dumps(self.eeg_data[-1].tolist())
                await websocket.send(data_to_send)
            await asyncio.sleep(0.1)

    def save_data(self, filename):
        self.eeg_data = np.array(self.eeg_data)
        np.save(filename, self.eeg_data)

def main():
    port = "COM5"
    filename = "../data/eeg_data.npy"
    eeg_data_collector = EEGDataCollector(port)

    # Start collecting data
    eeg_data_collector.collect_data()

    # Start WebSocket server
    start_server = websockets.serve(eeg_data_collector.send_to_server, "localhost", 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        eeg_data_collector.board.stop_stream()
    except Exception as e:
        print(e)
        eeg_data_collector.board.stop_stream()

if __name__ == '__main__':
    main()
