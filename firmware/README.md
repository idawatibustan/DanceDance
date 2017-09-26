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
- sudo chmod 666 /dev/ttyACM0
