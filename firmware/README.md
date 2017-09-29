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
- MPU6050_duo_short_temp/
- dummy_server/uart_serial.py
- uart_interface/
