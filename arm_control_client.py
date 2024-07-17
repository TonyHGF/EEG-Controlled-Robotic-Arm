# arm_control_server.py
import asyncio
import websockets
import json
import serial

ser = serial.Serial(
    port='COM5',  # 根据实际情况修改端口号
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


global steer0
global steer1
global steer2
global steer3
global steer4
global hand


def move_left(steer0):
    if steer0 == 500:
        return "#000P500T1500!\n"
    else:
        steer0 -= 100
        return f"#000P{steer0}T1500!\n"
    
def move_right(steer0):
    if steer0 == 2000:
        return "#000P2000T1500!\n"
    else:
        steer0 += 100
        return f"#000P{steer0}T1500!\n"
    
def move_down(steer1):
    if steer1 == 1300:
        return "#001P1300T1500!\n"
    else:
        steer1 -= 100
        return f"#001P{steer1}T1500!\n"
    
def move_up(steer1):
    if steer1 == 1700:
        return "#001P1700T1500!\n"
    else:
        steer1 += 100
        return f"#001P{steer1}T1500!\n"
    
def move_forward(steer2):
    if steer2 == 1300:
        return "#002P1300T1500!\n"
    else:
        steer2 -= 100
        return f"#002P{steer2}T1500!\n"
    
def move_backward(steer2):
    if steer2 == 1700:
        return "#002P1700T1500!\n"
    else:
        steer2 += 100
        return f"#002P{steer2}T1500!\n"

def move_forward3(steer3):
    if steer3 == 2000:
        return "#003P1000T1500!\n"
    else:
        steer3 += 100
        return f"#003P{steer3}T1500!\n"  
    
def move_backward3(steer3):
    if steer3 == 1000:
        return "#003P2000T1500!\n"
    else:
        steer3 -= 100
        return f"#003P{steer3}T1500!\n"  
    
def move_left4(steer4):
    if steer4 == 1000:
        return "#004P1000T1500!\n"
    else:
        steer4 -= 100
        return f"#004P{steer4}T1500!\n"
    
def move_right4(steer4):
    if steer4 == 2000:
        return "#004P2000T1500!\n"
    else:
        steer4 += 100
        return f"#004P{steer4}T1500!\n"
    
def move_open(hand):
    if hand  == 1000:
        return "#005P1000T1500!\n"
    else:
        hand -= 100
        return f"#005P{hand}T1500!\n"
    
def move_close(hand):
    if hand  == 2000:
        return "#005P2000T1500!\n"
    else:
        hand += 100
        return f"#005P{hand}T1500!\n"
    


    


def convert_to_arm_command(classification_data):
    # 示例转换函数，需根据具体需求实现
    # if classification_data["classification"] == "move_up":
    #     return move_left(steer0)
    # elif classification_data["classification"] == "move_down":
    #     return "#001P1000T1500!\n"
    # elif classification_data["classification"] == "move_left":
    #     return "#002P1000T1500!\n"

    if classification_data == 0:
        return move_left(steer0)
    elif classification_data == 1:
        return move_right(steer0)
    elif classification_data == 2:
        return move_down(steer1)
    elif classification_data == 3:
        return move_up(steer1)
    elif classification_data == 4:
        return move_forward(steer2)
    elif classification_data == 5:
        return move_backward(steer2)
    elif classification_data == 6:
        return move_forward3(steer3)
    elif classification_data == 7:
        return move_backward3(steer3)
    elif classification_data == 8:
        return move_left4(steer4)
    elif classification_data == 9:
        return move_right4(steer4)   
    return "$DST!"

if __name__ == '__main__':
    steer0 = 1500
    steer1 = 1500
    steer2 = 1500
    steer3 = 1500
    steer4 = 1500
    hand = 1500
    asyncio.get_event_loop().run_until_complete(receive_classification())
    asyncio.get_event_loop().run_forever()
