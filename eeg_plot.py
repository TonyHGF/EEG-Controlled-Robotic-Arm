import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

DATA_FILE = "data_cache.json"
buffer_size = 1000  # 缓存大小，调整以适应你的需求

class RealtimePlot(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.axs = plt.subplots(8, 1, figsize=(10, 15))
        super().__init__(fig)
        self.setParent(parent)
        self.data_cache = {"timestamps": [], "channels": [[] for _ in range(8)]}
        self.lines = [ax.plot([], [])[0] for ax in self.axs]

    def update_plot(self):
        try:
            with open(DATA_FILE, 'r') as f:
                self.data_cache = json.load(f)
        except FileNotFoundError:
            pass  # 文件可能还未创建
        for i, line in enumerate(self.lines):
            line.set_data(self.data_cache["timestamps"], self.data_cache["channels"][i])
            self.axs[i].relim()
            self.axs[i].autoscale_view()
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Realtime EEG Data Plot")
        self.plot_widget = RealtimePlot(self)
        self.setCentralWidget(self.plot_widget)
        self.show()

        # 设置一个定时器，每隔500毫秒刷新一次图像
        self.timer = QTimer()
        self.timer.timeout.connect(self.plot_widget.update_plot)
        self.timer.start(500)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
