import time
import serial

pico = serial.Serial("COM9", 115200, timeout=1)
time.sleep(2)

pico.write(b"0\n")
pico.flush()
time.sleep(1)

pico.write(b"1\n")
pico.flush()