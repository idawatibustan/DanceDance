import serial
import time

def main():
    ser = serial.Serial('/dev/ttyAMA0', 57600)
    handshake_flag = 1
    read_sensor_flag = 0

    try:
        print("Initialising handshake sequence")
        while handshake_flag:
            ser.write("1".encode(encoding='utf_8'))
            response = ser.readline() # this is blocking
            if response.rstrip() == "2":
                print("Received ACK2, sending confirmation ACK3")
                ser.write("3".encode(encoding='utf_8'))
                handshake_flag = 0
                read_sensor_flag = 1

        # use sys clock to get time frame
        timestr = time.strftime("%Y%m%d%H%M%S")
        filename = "datarec_" + timestr + ".csv"
        data_file = open(filename, "a")
        data_file.write("ax0,ay0,az0,gx0,gy0,gz0,ax1,ay1,az1,gx1,gy1,gz1\n")
        while read_sensor_flag:
            received_string = ser.readline()
            if (len(received_string)>10):
                data_file.write(received_string)
                print(received_string)
                ser.write("A".encode(encoding='utf_8')) # to acknowledge that the RPi is still receiving

    except KeyboardInterrupt:
        print("\nClosing port /dev/ttyAMA0")
        ser.write("4".encode(encoding='utf_8'))
        time.sleep(2)
        data_file.close()
        ser.close()

main()