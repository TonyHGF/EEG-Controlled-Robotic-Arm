from pyOpenBCI import OpenBCICyton
import numpy as np
import time

uVolts_per_count = (4500)/24/(2**23-1) #mV/count

def print_raw(sample):
    # print(str(sample))
    # print(sample.__dict__)
    channels = sample.channels_data
    channels = np.array(channels) * uVolts_per_count
    print(channels)
    # exit()


def main():
    board = OpenBCICyton(port='COM5', daisy=False)
    try:
        board.start_stream(print_raw)
        # time.sleep(1)
        # print('aaaaa')
    except KeyboardInterrupt:
        # eeg_data_collector.board.stop_stream()
        board.stop_stream()

if __name__ == '__main__':
    main()



