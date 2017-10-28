import serial
import time
import pandas as pd
import predict_knn
import io
import threading

dance_moves = ['idle', 'wavehands', 'busdriver', 'frontback', 'jumping', 'jumpingjack', 'turnclap', 'squartturnclap', 'window', 'window360', 'prediction error', 'no detection']
sensor_0    = 1
sensor_1    = 1

class Uart_Serial():
    def __init__(self, print_sensor=True):
        self.ser = serial.Serial('/dev/ttyAMA0', 57600)
        self.handshake_flag = 1
        self.read_sensor_flag = 0
        self.prediction_flag = False
        self.print_flag = print_sensor
        self.prediction = 12
        self.header = "ax0,ay0,az0,gx0,gy0,gz0,ax1,ay1,az1,gx1,gy1,gz1\n"
        self._collect_thread = threading.Thread(target=self.start_reading, args=())
        if not self._collect_thread.isAlive():
            self._collect_thread = threading.Thread(target=self.start_reading, args=())
            self._collect_thread.start()

    def get_prediction(self):
        if self.prediction_flag == True:
            self.prediction_flag = False
            return self.prediction
        return 12

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
                    if self.print_flag:
                        print(received_string)
                    row = pd.read_csv(io.BytesIO(self.header+received_string.rsplit(',', 1)[0]), sep=',' )
                    if(row.ax0 == -1 and row.ay0 == -1 and row.az0 == -1 and row.gx0 == -1 and row.gy0 == -1 and row.gz0 == -1 ):
                        print "Sensor 0 down, I repeat sensor 0 is down"
                        sensor_0 = 0
                    if(row.ax1 == -1 and row.ay1 == -1 and row.az1 == -1 and row.gx1 == -1 and row.gy1 == -1 and row.gz1 == -1 ):
                        print "Sensor 1 down, I repeat sensor 1 is down"
                    sensor_0 = 1
                    sensor_1 = 1
                    df = df.append(row, ignore_index = True)
                    count = count + 1
            # only predict is both sensors are up
            start_time = time.time()
            if(sensor_0 == 1 and sensor_1 == 1 ):
                self.prediction = dance_moves[predict_knn.predict(df)]
                if self.print_flag:
                    print "> > > > > > Prediction", self.prediction
                if self.prediction < 11:
                    self.prediction_flag = True
            print "My program took", time.time() - start_time, "to predict"

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
                    # print header+received_string.rsplit(',', 1)[0]
                    if(row.ax0 == -1 and row.ay0 == -1 and row.az0 == -1 and row.gx0 == -1 and row.gy0 == -1 and row.gz0 == -1 ):
                        print "Sensor 0 down, I repeat sensor 0 is down"
                        sensor_0 = 0
                    if(row.ax1 == -1 and row.ay1 == -1 and row.az1 == -1 and row.gx1 == -1 and row.gy1 == -1 and row.gz1 == -1 ):
                        print "Sensor 1 down, I repeat sensor 1 is down"
                        sensor_1 = 0
                    # reset sensors
                    sensor_0 = 1
                    sensor_1 = 1
                    df = df.append(row, ignore_index = True)
                    count = count + 1

            # only predict is both sensors are up
            start_time = time.time()
            if(sensor_0 == 1 and sensor_1 == 1 ):
                print df
                prediction = dance_moves[predict_knn.predict(df)]
                print "Prediction!!!!!!!!!", prediction
                if prediction < 11:
                    self.prediction_flag = True
            print "My program took", time.time() - start_time, "to predict"



    except KeyboardInterrupt:
        print("\nClosing port /dev/ttyAMA0")
        self.ser.write("4".encode(encoding='utf_8'))
        time.sleep(2)
        self.data_file.close()
        self.ser.close()
