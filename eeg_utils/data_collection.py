from pyOpenBCI import OpenBCICyton
import numpy as np
import time
import os
import asyncio
import websockets
import json

class EEGDataCollector:
    def __init__(self, port, duration, debug):
        self.port = port
        self.eeg_data = []
        self.board = OpenBCICyton(port=self.port, daisy=False)
        self.uVolts_per_count = (4500)/24/(2**23-1)
        self.start_time = time.time()
        self.duration = duration
        self.cnt = 0
        self.debug = debug
        self.folder = self.make_folder()


    def make_folder(self):
        write_time = time.localtime()
        formatted_time = time.strftime("%Y-%m-%d-%H-%M-%S", write_time)
        folder = os.path.join('../data/', f'{self.start_time}')
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    def collect_data(self):
        if self.debug:
            self.board.start_stream(self.debug)
        else:
            self.board.start_stream(self.fun)


    def fun(self, sample):
        current_time = time.time()
        if current_time - self.start_time < self.duration:
            print(current_time - self.start_time)
            self.eeg_data.append(np.array(sample.channels_data) * self.uVolts_per_count)
        else:
            # write_time = time.localtime()
            # formatted_time = time.strftime("%Y-%m-%d-%H-%M-%S", write_time)
            # filename = os.path.join('../data/', f"{formatted_time}")
            filename = os.path.join(self.folder, f"eeg_data_{self.cnt}")

            self.cnt += 1
            self.save_data(filename)
            print('save to:', os.path.abspath(filename))
            self.start_time = current_time
            self.eeg_data.clear()


    def debug(self, sample):
        duration = time.time() - self.start_time
        if duration < 20:
            print(duration)
            self.eeg_data.append(np.array(sample.channels_data) * self.uVolts_per_count)
        else:
            # self.board.stop_stream()
            self.save_data("../data/eeg_data.npy")
            print("Data saved to", os.path.abspath("../data/eeg_data.npy"))
            start_server = websockets.serve(self.send_to_server, "localhost", 5000)
            asyncio.get_event_loop().run_until_complete(start_server)
            # self.board.stop_stream()
            try:
                asyncio.get_event_loop().run_forever()
            except KeyboardInterrupt:
                self.board.stop_stream()
            except Exception as e:
                print(e)
                self.board.stop_stream()

    async def send_to_server(self, websocket, path):
        print("send to server")
        while True:
            if self.eeg_data:
                data_to_send = json.dumps(self.eeg_data[-1].tolist())
                await websocket.send(data_to_send)
            await asyncio.sleep(0.1)

    def save_data(self, filename):
        save_data = np.array(self.eeg_data)
        np.save(filename, save_data)


def main():
    port = "COM5"
    filename = "../data/eeg_data.npy"
    eeg_data_collector = EEGDataCollector(port, duration=5, debug=False)

    # Start collecting data
    eeg_data_collector.collect_data()

    exit()
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
