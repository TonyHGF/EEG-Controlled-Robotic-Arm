# import asyncio
# import websockets
# import json
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# import numpy as np

# # 全局变量用于存储接收到的数据
# eeg_data = []

# async def receive_data():
#     uri = "ws://localhost:5000"
#     async with websockets.connect(uri) as websocket:
#         while True:
#             data = await websocket.recv()
#             data = json.loads(data)
#             print(f"Received data: {data}")
#             eeg_data.append(data)
#             if len(eeg_data) > 100:  # 只保留最近的100个数据点
#                 eeg_data.pop(0)

# def update_plot(frame):
#     print(eeg_data)
#     if eeg_data:
#         plt.cla()  # 清除当前图形
#         plt.plot(eeg_data[-100:])  # 绘制最近的100个数据点
#         plt.xlabel('Time')
#         plt.ylabel('EEG Data (uV)')
#         plt.title('Real-time EEG Data')

# def main():
#     # 启动WebSocket客户端以接收数据
#     loop = asyncio.get_event_loop()
#     loop.create_task(receive_data())

#     # 设置Matplotlib的绘图
#     fig = plt.figure()
#     ani = FuncAnimation(fig, update_plot, interval=500)  # 每100毫秒更新一次图像

#     plt.show()

#     # 运行事件循环
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         loop.close()

# if __name__ == '__main__':
#     main()


import asyncio
import websockets
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# 全局变量用于存储接收到的数据
eeg_data = []

async def receive_data():
    uri = "ws://localhost:5000"
    print('here')
    async with websockets.connect(uri) as websocket:
        print("Connected to server")
        while True:
            try:
                data = await websocket.recv()
                data = json.loads(data)
                print(f"Received data: {data}")  # 调试信息
                eeg_data.append(data)
                if len(eeg_data) > 100:  # 只保留最近的100个数据点
                    eeg_data.pop(0)
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break


def update_plot(frame):
    if eeg_data:
        plt.cla()  # 清除当前图形
        plt.plot(eeg_data[-100:])  # 只绘制最近的100个数据点
        plt.xlabel('Time')
        plt.ylabel('EEG Data (mV)')
        plt.title('Real-time EEG Data')


def main():
    # 启动WebSocket客户端以接收数据
    loop = asyncio.get_event_loop()
    loop.create_task(receive_data())

    # 设置Matplotlib的绘图
    fig = plt.figure()
    ani = FuncAnimation(fig, update_plot, interval=100)  # 每100毫秒更新一次图像

    # 使用asyncio运行事件循环
    plt.show()
    try:
        print("Running event loop")
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

if __name__ == '__main__':
    main()
