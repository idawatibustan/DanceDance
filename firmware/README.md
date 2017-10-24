# Firmware

RPi commands:
- view connected device
```dmesg | grep tty```

RPi config history
(25-Sept)
ref: <a>https://raspberrypi.stackexchange.com/questions/45570/how-do-i-make-serial-work-on-the-raspberry-pi3</a>
- Added `dtoverlay=pi3-disable-bt` on `/boot/config.txt`

ref: <a>https://raspberrypi.stackexchange.com/questions/45570/how-do-i-make-serial-work-on-the-raspberry-pi3</a>
- on `raspi-config`, select `Interfacing Options / Serial` then disable Serial console (no) and the Serial Port hardware enabled (yes)
- Added `console=serial0(or ttyAMA0),115200` on `/boot/cmdline.txt`

ref: <a>https://www.raspberrypi.org/forums/viewtopic.php?t=123081</a>
- sudo systemctl stop serial-getty@ttyAMA0.service
- sudo systemctl disable serial-getty@ttyAMA0.service

ref:
<a>https://stackoverflow.com/questions/27858041/oserror-errno-13-permission-denied-dev-ttyacm0-using-pyserial-from-pyth</a>
- enabled permissions for /dev/ttyAMA0
- `sudo chmod 666 /dev/ttyACM0`

ref:
<a>https://raspberrypi.stackexchange.com/questions/55366/serial-communication-between-raspi-and-arduino-mega</a>

ref:
<a>http://wiringpi.com/download-and-install/</a>
- Installed wiringpi to control GPIO pins on the raspberry pi

ref:
<a>http://robotics.hobbizine.com/raspiduino.html</a>
- Coding guide for setting up SPI on RPi

28/9/17 - Abandoned SPI for UART communications between Arduino and RPi

IMPORTANT FILES/FOLDERS
- dummy_server/uart_serial.py
    - Handshaking with Arduino Mega, receives and write to .txt file (prints to console too)
- just_sending/just_sending.ino
    - Receives sensor data and sends them to the RPi
    - No circular buffer, includes handshaking
- firmware.ino
    - Similar to just_sending.ino but with FreeRTOS implementation
-rpi_socket.py
     - Communicates with the evaluation server

THINGS TO DO:
1. Confirm rpi_socket.py works with a sample_auth_server.py being executed on a MAC
2. Combine rpi_socket.py with uart_serial.py
3. Python scripts should execute on power on

RPi:
1. Perform handshaking with Mega
    a. Mega will perform hardware calibration
    b. Handshake sequence completes when calibration is complete -> ACK is then sent to RPi to begin receiving
2. Create socket and connect to the evaluation server
    a. Action will be shown by the server
    b. Perform action, receive data from Mega
    c. Send data to ML script, identify the action and all relevant data
    d. Package data and send to evaluation server

Mega:
1. 

### CONNECTING RPI TO YOUR NETWORK OF CHOICE

###### Note: The RPi is unable to connect directly to the school's network due to how it was configured. A workaround for this is using your Laptop as a hotspot for the RPi to connect indirectly

##### You'll require a monitor and input devices (keyboard & mouse)
1. Setup your hotspot SSID and password if you haven't already
2. `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`
3. Scroll to the end of the file and add the following lines
    - network={
        ssid="Test Wifi Network"
        psk="SecretPassWord"
        }
    - Or follow the format already present in the file
4. `sudo reboot` - to reboot the device for the changes to take effect at the next boot up
5. `ifconfig wlan0` - look out for inet addr:<IP ADDRESS> to confirm that you're connected to your network of choice

### COLLECTING DATA

1. Make sure the RPi is connected to your device's hotspot
2. SSH into RPi
    - `ssh pi@<IP ADDRESS>`
    - password: dance12
3. `cd Documents/pi_socket/` 
4. `python rpi_socket.py`
    - The RPi will start receiving data from the Mega
    - Outputs to a file plus prints to console for debugging purposes

###### If nothing is being printed out (your output file will probably be empty as well)
1. Check that the correct .ino file is uploaded to the Mega (The one that sends data through the Serial1 port)
2. Reset the Mega if it's confirmed the correct .ino file (The handshaking sequence might have been interrupted)
    - Make sure to also reset the python script