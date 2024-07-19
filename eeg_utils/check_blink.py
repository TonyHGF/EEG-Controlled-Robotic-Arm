import numpy as np
import os
from data_collection import EEGDataCollector
import time
from matplotlib import pyplot as plt


def check_blink(filename, window_size, threshold, step, debug=False):
    signals = np.load(filename)
    signals = signals.transpose()
    # # 假设signals的形状是(8, N)，其中N是每个通道的数据点数
    # num_channels, num_points = signals.shape
    # print(num_channels, num_points)
    # # 计算下采样后每个通道的数据点数
    # downsampled_num_points = num_points // 10
    # # 创建一个新的数组来存储下采样后的数据，形状为(8, downsampled_num_points)
    # downsampled_signals = np.empty((8, downsampled_num_points))

    # 对每个通道进行下采样
    # for i in range(num_channels):
    #     downsampled_signals[i] = signals[i, ::10]

    # 使用downsampled_signals进行后续操作
    # if debug:
    #     print('Downsampled signals shape:', downsampled_signals.shape)

    # print('here', signals.shape)
    print("=========================================")
    # print(time.localtime())
    write_time = time.localtime()
    formatted_time = time.strftime("%Y-%m-%d-%H-%M-%S", write_time)
    print("time: ", formatted_time)
    # for signal in signals:
    # for start_index in range(0, signals.shape[1], window_size):
        # end_index = start_index + window_size
    for channel_num, signal in enumerate(signals):
        if abs(signal.mean()) > 20:
            print(f"skip channel{channel_num}")
            continue
        f = False
        for i in range(0, signals.shape[1] - step, step):
            if abs(np.mean(signal[i:i+step]) - np.mean(signal[i+step:(i+step*2)])) > threshold:
                print(f"Blink detected in channel{channel_num}")
                f = True
                break
        if not f:
            print(f"No blink detected in channel{channel_num}")
    if debug:
        print(signals[0].shape)
        plt.plot(signals[0])
        plt.show()


if __name__ == '__main__':
    port = "COM5"
    # filename = "../data/eeg_data.npy"
    foldername = "G:\\BME1317\\data"
    # eeg_data_collector = EEGDataCollector(port, duration=5, debug=False)

    # try:
    #     eeg_data_collector.collect_data()
    # except KeyboardInterrupt:
    #     eeg_data_collector.board.stop_stream()
    # except Exception as e:
    #     print(e)
    #     eeg_data_collector.board.stop_stream()

    for i in range(0, 100):
        check_blink(os.path.join(foldername, f"eeg_data_{i}.npy"), window_size=250, threshold=0.4, step=25)
        time.sleep(5)