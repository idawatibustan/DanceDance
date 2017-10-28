import uart_serial_v3_checksum as uart
import time
import threading

dance_moves = ['idle', 'wavehands', 'busdriver', 'frontback', 'sidestep', 'jumping', 'jumpingjack', 'turnclap', 'squartturnclap', 'window', 'window360', 'prediction error', 'not ready yet']

if __name__=="__main__":
    us = uart.Uart_Serial(print_sensor=False)
    try:
        while True:
            res = us.get_prediction()
            # if not res == 11:
            print dance_moves[res]
            time.sleep(1)
            if not us._collect_thread.isAlive():
                us._collect_thread = threading.Thread(
                    target=us.start_reading,
                    args=()
                    )
                us._collect_thread.start()
    except KeyboardInterrupt:
        us.shutdown()
        exit()
    except Exception as e:
        print "Exception caught:", str(e)
        us.shutdown()
        exit()
