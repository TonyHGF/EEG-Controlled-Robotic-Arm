import numpy as np
import time
from pylsl import StreamInlet, resolve_stream

from DataLoader.EEGDataCache import EEGDataCache


global inlet
global inlet2
global mi, ma

def main():
    eeg_data_cache = EEGDataCache(max_size=100)
    uri = "ws://localhost:5000"
    global mi, ma
    print("Looking for an LSL stream...")
    streams = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streams[0])
    # inlet2 = StreamInlet(streams[1])
    mi = 100
    ma = -100
    knock_time = time.time()
    while True:
        sample, timestamp = inlet.pull_sample()
        sample = np.array(sample)
        mi = min(mi, sample[0])
        ma = max(ma, sample[0])
        eeg_data_cache.add_data(sample, timestamp)
        current_time = time.time()

        knock = eeg_data_cache.check_knock()
        if knock != -1 and current_time - knock_time > 1:
            print(f"Knock on channel {knock}")
            knock_time = current_time
            # eeg_data_cache.clear()


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