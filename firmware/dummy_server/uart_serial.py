import serial
import time

# opening port ttyAMA0 at baudrate 115200
ser = serial.Serial('/dev/ttyAMA0', 115200)

handshake_flag = 1
read_sensor_flag = 0

try:
    print("Initialising handshake sequence")
    while handshake_flag:
        ser.write("1".encode(encoding='utf_8'))
        response = ser.readline() # this is blocking
        if response.rstrip() == "2":
            print("Received ACK2, sending confirmation")
            ser.write("3".encode(encoding='utf_8'))
            handshake_flag = 0
            read_sensor_flag = 1

    # use sys clock to get time frame
    while read_sensor_flag:
        received_string = ser.readline()
        data_list = received_string.rstrip().split(" ")

        print(data_list)
        print(received_string)
except KeyboardInterrupt:
    print("\nClosing port /dev/ttyAMA0")
    ser.write("4".encode(encoding='utf_8'))
    time.sleep(2)
    ser.close()
