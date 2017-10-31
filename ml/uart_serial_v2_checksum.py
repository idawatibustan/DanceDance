import serial
import time
import pandas as pd
import predict_knn
import io

ser = serial.Serial('/dev/ttyAMA0', 57600)

handshake_flag = 1
read_sensor_flag = 0
prediction_flag = False
prediction = 12

def get_prediction():
    if prediction_flag == True:
        prediction_flag = False
        return prediction
    return 12

def verify_checksum(received_string):
    result_list = received_string.split(",")
    checksum_value = float(result_list[-1].strip())
    total = 0.0
    return_string = ""
    for values in result_list[0:len(result_list)-1]:
        try:
            total = total + float(values)
        except ValueError as e:
            pass
        return_string = return_string + values + ","
    return_string = return_string[0:len(return_string)-1] + "\n"
    return total == checksum_value, return_string

# def verify_checksum(received_string):
#     result_list = received_string.split(",")
#     checksum_value = float(result_list[-1])
#     total = 0.0
#     return_string = ""
#     for values in result_list[0:len(result_list)-1]:
#         total = total + float(values)
#         return_string = return_string + values + ","
#     return_string = return_string[0:len(return_string)-1] + "\n"
#     return total == checksum_value, return_string


if __name__=="__main__":
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
        # filename = "datarec_" + timestr + ".csv"
        # data_file = open(filename, "a")
        header = "ax0,ay0,az0,gx0,gy0,gz0,ax1,ay1,az1,gx1,gy1,gz1\n"
        # data_file.write(header)
        while read_sensor_flag:
            df = pd.DataFrame()
            print "Empty", df
            ser.flushInput()
            count = 0
            while(count < 145):
                received_string = ser.readline()
                if (len(received_string)>10):
                    ser.write("A".encode(encoding="utf_8"))

                    # row = pd.read_csv(io.BytesIO(header+received_string), sep=',' )
                    cv, rs = verify_checksum(received_string)
                    if cv == True:
                        row = pd.read_csv(io.BytesIO(header+rs), sep=',' )
                        # if row.isnull().values.any() == False:
                        df = df.append(row, ignore_index = True)
                        count = count + 1
                        # cv, rs = verify_checksum(received_string)
                        # if cv:
                        # row = pd.read_csv(io.BytesIO(header+rs), sep=',' )

            print "Appended", df
            prediction = predict_knn.predict(df)
            print "Prediction!!!!!!!!!", prediction
            if prediction < 11:
                prediction_flag = True


    except KeyboardInterrupt:
        print("\nClosing port /dev/ttyAMA0")
        ser.write("4".encode(encoding='utf_8'))
        time.sleep(2)
        # data_file.close()
        ser.close()

    except Exception as e:
        print "we know why", str(e)
        print("\nClosing port /dev/ttyAMA0")
        ser.write("4".encode(encoding='utf_8'))
        time.sleep(2)
        # data_file.close()
        ser.close()
