import serial
import time
import pandas as pd
import predict_knn
import io
import threading

def verify_checksum(received_string):
    result_list = received_string.split(",")
    checksum_value = int(result_list[-1].strip())
    total = 0
    return_string = ""
    for values in result_list[0:len(result_list)-3]:
        try:
            total = total + int(values)
        except ValueError as e:
            pass
        return_string = return_string + values + ","
    for values in result_list[12:len(result_list)-1]:
        float_value = float(values.strip())
        try:
            total = total + int(float_value)
        except ValueError as e:
            pass
        return_string = return_string + values.strip() + ","
    return_string = return_string[0:len(return_string)-1] + "\n"
    return total == checksum_value, return_string

def extract(processed_string):
    processed_list = processed_string.split(",")
    voltage = float( processed_list[-2].strip() )
    current = float( processed_list[-1].strip() )
    power = voltage * current
    return voltage, current, power

class Uart_Serial():
    def __init__(self, print_sensor=True):
        self.ser = serial.Serial('/dev/ttyAMA0', 57600)
        self.handshake_flag = 1
        self.read_sensor_flag = 0
        self.prediction_flag = False
        self.print_flag = print_sensor
        self.prediction = 13
        self.header = "ax0,ay0,az0,gx0,gy0,gz0,ax1,ay1,az1,gx1,gy1,gz1\n"
        self._collect_thread = threading.Thread(target=self.start_reading, args=())
        self.voltage = 0
        self.current = 0
        self.power = 0
        self.cumpower= 0.0
        if not self._collect_thread.isAlive():
            print "Thread is not alive, re-initializing"
            self._collect_thread = threading.Thread(target=self.start_reading, args=())
            self._collect_thread.start()

    def get_prediction(self):
        if self.prediction_flag == True:
            self.prediction_flag = False
            return self.prediction
        return 13

    def get_info(self):
        v = "%.5f" % self.voltage
        c = "%.5f" % self.current
        p = "%.3f" % self.power
        cp = "%.3f" % self.cumpower
        return v, c, p, cp

    def start_reading(self):
        print("Initialising handshake sequence")
        while self.handshake_flag:
            self.ser.write("1".encode(encoding='utf_8'))
            response = self.ser.readline() # this is blocking
            if response.rstrip() == "2":
                print("Received ACK2, sending confirmation ACK3")
                self.ser.write("3".encode(encoding='utf_8'))
                self.handshake_flag = 0
                self.read_sensor_flag = 1

        count = 0
        df = pd.DataFrame()
        self.ser.flushInput()
        start_time_one = time.time()
        while self.read_sensor_flag:
            received_string = self.ser.readline()
            if (len(received_string)>10):
                # print(received_string)
                cv, rs = verify_checksum(received_string)
                # print "rs", rs
                # print "cv", cv
                if cv == True:
                    self.ser.write("A".encode(encoding="utf_8"))
                    row = pd.read_csv(io.BytesIO(self.header+rs.rsplit(',', 3)[0]), sep=',' )
                    df = df.append(row, ignore_index = True)
                    self.voltage, self.current, self.power = extract(rs)
                    self.cumpower = self.cumpower + self.power
                    count = count + 1
            if count == 100:
                print "My program took", time.time() - start_time_one, "to collect"
                start_time = time.time()
                self.prediction = predict_knn.predict(df)
                self.prediction_flag = True
                print "My program took", time.time() - start_time, "to predict"
                # print predict_knn.predict_prob(df)
                count = 0
                df = pd.DataFrame()
                self.ser.flushInput()
                start_time_one = time.time()


    def shutdown(self):
        print("\nClosing port /dev/ttyAMA0")
        self.ser.write("4".encode(encoding='utf_8'))
        if self._collect_thread.isAlive():
            self._collect_thread.join()
        time.sleep(2)
        self.ser.close()
