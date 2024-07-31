import numpy as np
import time
import asyncio
import websockets
import json
from pylsl import StreamInlet, resolve_stream
from DataLoader.EEGDataCache import EEGDataCache

global inlet
global mi, ma

async def send_classification_result(uri, eeg_data_cache):
    async with websockets.connect(uri) as websocket:
        knock_time = time.time()
        while True:
            sample, timestamp = inlet.pull_sample()
            sample = np.array(sample)
            global mi, ma
            mi = min(mi, sample[0])
            ma = max(ma, sample[0])
            eeg_data_cache.add_data(sample, timestamp)
            current_time = time.time()

            knock = eeg_data_cache.check_knock()
            if knock != -1 and current_time - knock_time > 1:
                print(f"Knock on channel {knock}")
                knock_time = current_time
                classification_result = knock
                await websocket.send(json.dumps(classification_result))
                response = await websocket.recv()
                print(f"Received response: {response}")
                continue

            if eeg_data_cache.check_blink() and current_time - knock_time > 1:
                print("Blink")
                classification_result = "blink"
                knock_time = current_time
                await websocket.send(json.dumps(classification_result))
                response = await websocket.recv()
                print(f"Received response: {response}")

def main():
    global inlet, mi, ma
    eeg_data_cache = EEGDataCache(max_size=100)
    uri = "ws://localhost:5000"
    print("Looking for an LSL stream...")
    streams = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streams[0])
    mi = 100
    ma = -100

    asyncio.get_event_loop().run_until_complete(send_classification_result(uri, eeg_data_cache))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped")
        print(f"Min: {mi}, Max: {ma}")
        exit()
    except Exception as e:
        print(e)
        exit()
