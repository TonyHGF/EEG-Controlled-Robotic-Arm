import asyncio
import websockets
import json
import serial
import time

ser = serial.Serial(
    port='COM8',  # 根据实际情况修改端口号
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# global steer0, steer1, steer2, steer3, steer4, hand_open
steer_limit = {
    0: (500, 2000),
    1: (1300, 1700),
    2: (1300, 2200),
    3: (1000, 2000),
    4: (500, 2500),
    5: (500, 1500)
}

def move_steer2(steer_id, direction=0):
    global steers
    if direction == 0:
        pass

def move_steer(steer_id, direction=0):
    # 0: left, 1: right
    global steers
    if direction == 0:
        if steers[steer_id] == steer_limit[steer_id][0]:
            return f"#{steer_id:03}P{steer_limit[steer_id][0]}T1500!\n"
        else:
            steers[steer_id] -= 100
            return f"#{steer_id:03}P{steers[steer_id]}T1500!\n"
    else:
        if steers[steer_id] == steer_limit[steer_id][1]:
            return f"#{steer_id:03}P{steer_limit[steer_id][1]}T1500!\n"
        else:
            steers[steer_id] += 100
            return f"#{steer_id:03}P{steers[steer_id]}T1500!\n"



    # if direction == 0:
    #     if steer_id == 0:
    #         return "#000P500T1500!\n"
    #     elif steer_id == 1:
    #         return "#001P1300T1500!\n"
    #     elif steer_id == 2:
    #         return "#002P1300T1500!\n"
    #     elif steer_id == 3:
    #         return "#003P1000T1500!\n"
    # else:
    #     if steer_id == 0:
    #         return "#000P2000T1500!\n"
    #     elif steer_id == 1:
    #         return "#001P1700T1500!\n"
    #     elif steer_id == 2:
    #         return "#002P2000T1500!\n"
    #     elif steer_id == 3:
    #         return "#003P2000T1500!\n"



def convert_to_arm_command(classification_data):
    # if 0 <= classification_data < 8:
    # if classification_data.type == int:
    global hand_open
    if isinstance(classification_data, int):
        # if classification_data == 0:
        #     return move_steer(0, 0)
        # elif classification_data == 1:
        #     return move_steer(1, 0)
        # elif classification_data == 2:
        #     return move_steer(2, 0)
        # elif classification_data == 3:
        #     return 114514
        steer_id = classification_data // 2
        direction = classification_data % 2
        return move_steer(steer_id, direction)
        
    elif classification_data == "blink":
        if hand_open:
            hand_open = False
            return "#005P1500T1500!\n"
        else:
            hand_open = True
            return "#005P0500T1500!\n"
    return "$DST!"

async def process_signal(websocket, path):
    try:
        async for message in websocket:
            classification_data = json.loads(message)
            print(f"Received classification data: {classification_data}")
            arm_command = convert_to_arm_command(classification_data)
            print(f"Sending arm command: {arm_command}")
            if arm_command == 114514:
                move_back()
            else:
                ser.write(arm_command.encode())
            response = json.dumps({"status": "received", "command": arm_command})
            await websocket.send(response)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")

start_server = websockets.serve(process_signal, "localhost", 5000)

def move_back():
    for i in range(6):
        ser.write(f"#00{i}P1500T1500!\n".encode())
        time.sleep(1.5)

if __name__ == '__main__':
    global steers
    steers = [1500 for _ in range(6)]
    global hand_open
    hand_open = True

    ser.write("#005P0500T1500!\n".encode())
    time.sleep(10)
    # ser.write("#005P1500T1500!\n".encode())

    print("go\n")
    time.sleep(2)
    # move_back()
    # time.sleep(3)

    ser.write("#000P2000T1500!\n".encode())
    time.sleep(3)
    ser.write("#001P1200T1500!\n".encode())
    time.sleep(3)
    # ser.write("#001P1500T1500!\n".encode())
    # # ser.write()
    ser.write("#002P1800T1500!\n".encode())
    time.sleep(5)
    # ser.write("#002P1500T1500!\n".encode())
    # time.sleep(3)
    ser.write("#003P1000T1500!\n".encode())
    time.sleep(5)
    ser.write("#005P1500T1500!\n".encode())
    time.sleep(5)
    ser.write("#002P1500T1500!\n".encode())
    time.sleep(5)
    ser.write("#000P1500T1500!\n".encode())
    time.sleep(5)
    ser.write("#002P1800T1500!\n".encode())
    time.sleep(5)
    ser.write("#005P1500T1500!\n".encode())
    time.sleep(5)
    ser.write("#005P0500T1500!\n".encode())
    move_back()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()


