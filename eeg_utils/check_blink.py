import numpy as np

from data_collection import EEGDataCollector


def check_blink(filename, window_size, threshold):
    signals = np.load(filename)
    print(signals.shape)
    


if __name__ == '__main__':
    port = "COM5"
    filename = "../data/eeg_data.npy"
    eeg_data_collector = EEGDataCollector(port)

    try:
        eeg_data_collector.collect_data()
    except KeyboardInterrupt:
        eeg_data_collector.board.stop_stream()
    except Exception as e:
        print(e)
        eeg_data_collector.board.stop_stream()

    check_blink(filename=filename, window_size=100, threshold=1000)