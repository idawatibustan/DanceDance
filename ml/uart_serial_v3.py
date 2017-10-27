import serial
import time
import pandas as pd
import predict_knn
import io
import threading

class Uart_Serial():
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyAMA0', 57600)
        self.handshake_flag = 1
        self.read_sensor_flag = 0
        self.prediction_flag = False
        self.prediction = 12
        self.header = "ax0,ay0,az0,gx0,gy0,gz0,ax1,ay1,az1,gx1,gy1,gz1\n"
        self._collect_thread = threading.Thread(target=self.start_reading, args=())
        if not self._collect_thread.isAlive():
            self._collect_thread = threading.Thread(target=self.start_reading, args=())
            self._collect_thread.start()

    def get_prediction(self):
        if self.self.prediction_flag == True:
            self.self.prediction_flag = False
            return self.prediction
        return 12

    def start_reading(self)
        print("Initialising handshake sequence")
        while self.handshake_flag:
            self.ser.write("1".encode(encoding='utf_8'))
            response = self.ser.readline() # this is blocking
            if response.rstrip() == "2":
                print("Received ACK2, sending confirmation ACK3")
                self.ser.write("3".encode(encoding='utf_8'))
                self.handshake_flag = 0
                self.read_sensor_flag = 1

        # use sys clock to get time frame
        timestr = time.strftime("%Y%m%d%H%M%S")
        filename = "datarec_" + timestr + ".csv"
        self.data_file = open(filename, "a")
        self.data_file.write(self.header)
        while self.read_sensor_flag:
            df = pd.DataFrame()
            count = 0
            while(count<145):
                received_string = self.ser.readline()
                if (len(received_string)>10):
                    self.data_file.write(received_string)
                    print(received_string)
                    row = pd.read_csv(io.BytesIO(self.header+received_string.rsplit(',', 1)[0]), sep=',' )
                    print self.header+received_string.rsplit(',', 1)[0]
                    df = df.append(row, ignore_index = True)
                    count = count + 1
            print df
            self.prediction = predict_knn.predict(df)
            print "Prediction!!!!!!!!!", self.prediction
            if self.prediction < 11:
                self.prediction_flag = True

    def shutdown(self):
        print("\nClosing port /dev/ttyAMA0")
        self.ser.write("4".encode(encoding='utf_8'))
        time.sleep(2)
        self.data_file.close()
        self.ser.close()

if __name__=="__main__":
    try:
        print("Initialising handshake sequence")
        while self.handshake_flag:
            self.ser.write("1".encode(encoding='utf_8'))
            response = self.ser.readline() # this is blocking
            if response.rstrip() == "2":
                print("Received ACK2, sending confirmation ACK3")
                self.ser.write("3".encode(encoding='utf_8'))
                self.handshake_flag = 0
                self.read_sensor_flag = 1

        # use sys clock to get time frame
        timestr = time.strftime("%Y%m%d%H%M%S")
        filename = "datarec_" + timestr + ".csv"
        self.data_file = open(filename, "a")
        header = "ax0,ay0,az0,gx0,gy0,gz0,ax1,ay1,az1,gx1,gy1,gz1\n"
        self.data_file.write(header)
        while self.read_sensor_flag:
            df = pd.DataFrame()
            count = 0
            while(count<145):
                received_string = self.ser.readline()
                if (len(received_string)>10):
                    self.data_file.write(received_string)
                    print(received_string)
                    row = pd.read_csv(io.BytesIO(header+received_string.rsplit(',', 1)[0]), sep=',' )
                    print header+received_string.rsplit(',', 1)[0]
                    df = df.append(row, ignore_index = True)
                    count = count + 1
            print df
            prediction = predict_knn.predict(df)
            print "Prediction!!!!!!!!!", prediction
            if prediction < 11:
                self.prediction_flag = True


    except KeyboardInterrupt:
        print("\nClosing port /dev/ttyAMA0")
        self.ser.write("4".encode(encoding='utf_8'))
        time.sleep(2)
        self.data_file.close()
        self.ser.close()
