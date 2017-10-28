import uart_serial_v3 as uart
import time

if __name__=="__main__":
    us = uart.Uart_Serial(print_sensor=False)
    try:
        while True:
            res = us.get_prediction()
            if not res == 11:
                print res
            time.sleep(1)
            if not us._collect_thread.isAlive():
                us._collect_thread = threading.Thread(
                    target=self.start_reading,
                    args=()
                    )
                us._collect_thread.start()
    except KeyboardInterrupt:
        us.shutdown()
    except Exception as e:
        print "Exception caught:", str(e)
        us.shutdown()