# arm_control_server.py
import asyncio
import websockets
import json
import serial

ser = serial.Serial(
    port='COM7',  # 根据实际情况修改端口号
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

async def receive_classification():
    async with websockets.connect("ws://localhost:5000") as websocket:
        while True:
            classification_data = await websocket.recv()
            classification_data = json.loads(classification_data)
            arm_command = convert_to_arm_command(classification_data)
            ser.write(arm_command.encode())
            print(f"Sent command: {arm_command}")

global bottom
global middle
global top

def move_left(bottom):
    if bottom == 0:
        return "#000P0000T1500!\n"
    else:
        bottom -= 100
        return f"#000P{bottom}T1500!\n"
    
def move_right(bottom):
    if bottom == 2500:
        return "#000P2500T1500!\n"
    else:
        bottom += 100
        return f"#000P{bottom}T1500!\n"
    
def move_up(middle):
    if middle == 0:
        return "#001P0000T1500!\n"
    else:
        middle -= 100
        return f"#001P{middle}T1500!\n"
    
def move_down(middle):
    if middle == 2500:
        return "#001P2500T1500!\n"
    else:
        middle += 100
        return f"#001P{middle}T1500!\n"
    
def move_forward(top):
    if top == 0:
        return "#002P0000T1500!\n"
    else:
        top -= 100
        return f"#002P{top}T1500!\n"
    
def move_backward(top):
    if top == 2500:
        return "#002P2500T1500!\n"
    else:
        top += 100
        return f"#002P{top}T1500!\n"
    


def convert_to_arm_command(classification_data):
    # 示例转换函数，需根据具体需求实现
    # if classification_data["classification"] == "move_up":
    #     return move_left(bottom)
    # elif classification_data["classification"] == "move_down":
    #     return "#001P1000T1500!\n"
    # elif classification_data["classification"] == "move_left":
    #     return "#002P1000T1500!\n"

    if classification_data == 1:
        return move_left(bottom)
    elif classification_data == 2:
        return move_right(bottom)
    elif classification_data == 3:
        return move_up(middle)
    elif classification_data == 4:
        return move_down(middle)
    return "$DST!"

if __name__ == '__main__':
    bottom = 1500
    middle = 1500
    top = 1500
    asyncio.get_event_loop().run_until_complete(receive_classification())
    asyncio.get_event_loop().run_forever()
