import time
import serial


def ardClient():
    ser = serial.Serial("COM5", 115200)

    time.sleep(2)

    ser.write(b'1')

    time.sleep(1)
    while ser.inWaiting() > 0:
        line = ser.readline()
        # if line:
        #    print(line.decode().strip())

    ser.close()
    return line.decode().strip()

    

