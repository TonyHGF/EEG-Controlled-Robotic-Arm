import numpy as np

class EEGDataCache:
    def __init__(self, max_size=1000):
        self.data = np.zeros((max_size, 8))
        self.timestamps = np.zeros((max_size, 1))
        self.max_size = max_size
        self.current_size = 0

    def add_data(self, data, timestamp):
        if self.current_size < self.max_size:
            self.data[self.current_size] = data
            self.timestamps[self.current_size] = timestamp
            self.current_size += 1
        else:
            self.data = np.roll(self.data, -1, axis=0)
            self.timestamps = np.roll(self.timestamps, -1, axis=0)
            self.data[-1] = data
            self.timestamps[-1] = timestamp

    def get_data(self):
        return self.data

    def get_timestamps(self):
        return self.timestamps

    def get_current_size(self):
        return self.current_size

    def clear(self):
        self.data = np.zeros((self.max_size, 8))
        self.timestamps = np.zeros((self.max_size, 1))
        self.current_size = 0

    def __str__(self):
        return f"EEGDataCache(max_size={self.max_size}, current_size={self.current_size})"
    
    def __dict__(self):
        return {
            "data": self.data,
            "timestamps": self.timestamps,
            "max_size": self.max_size,
            "current_size": self.current_size
        }
    
    def check_blink(self):
        return False
        if self.data[self.current_size - 1][0] > 100 and self.data[self.current_size - 1][1] > 100:
            return True

    def check_channel_1(self, signal, timestamp):
        with open ("blink.txt", "w") as f:
            if signal > 50:
                f.write("blink", timestamp)

    def get_diff(self):
        return self.data[self.current_size - 1] - self.data[self.current_size - 2]
    
    def check_knock(self):
        return -1
        max_value = -100000
        max_channel = -1
        for i in range(8):
            if self.data[self.current_size - 1][i] > max_value:
                max_value = self.data[self.current_size - 1][i]
                max_channel = i

        if np.mean(self.data[self.current_size - 1]) >= 600:
            return -1

        # if 4 <= max_channel <= 7:
        #     return -1   

        if max_value > 600:
            return max_channel
        else:
            return -1