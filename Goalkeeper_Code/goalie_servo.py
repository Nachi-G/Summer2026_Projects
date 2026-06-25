import time
import board
import pwmio
import usb_cdc

servo = pwmio.PWMOut(board.GP15, frequency=50, duty_cycle=0)

LEFT = 2000
CENTER = 5000
RIGHT = 8100

servo.duty_cycle = CENTER

while True:
    if usb_cdc.data.in_waiting > 0:
        command = usb_cdc.data.readline().decode().strip()

        if command == "0":
            servo.duty_cycle = RIGHT
            print("Right")

        elif command == "1":
            servo.duty_cycle = LEFT
            print("Left")

        time.sleep(0.3)
        servo.duty_cycle = CENTER