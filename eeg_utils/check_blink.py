import numpy as np

from data_collection import EEGDataCollector


def check_blink(filename, window_size, threshold):
    signals = np.load(filename)
    print(signals.shape)
    # for i in range(len(signals[:1]) - window_size):
    for i in range(0, 1000, window_size):
        for signal in signals:
            window = signal[i:i+window_size]
            if np.max(window) - np.min(window) > threshold:
                print("blink")
            else:
                print("no blink")


if __name__ == '__main__':
    port = "COM5"
    filename = "../data/eeg_data.npy"
    print('here')
    eeg_data_collector = EEGDataCollector(port)

    
    try:
        eeg_data_collector.collect_data()
    except KeyboardInterrupt:
        eeg_data_collector.board.stop_stream()
    except Exception as e:
        print(e)
        eeg_data_collector.board.stop_stream()

    check_blink(filename=filename, window_size=100, threshold=1000)