import time, board, pwmio

servo = pwmio.PWMOut(board.GP15, frequency=50, duty_cycle=0)

while True:
    #set_angle(0)
    servo.duty_cycle = 2000   #0 degrees (right)
    print("0")
    time.sleep(1)
    

    #set_angle(90)
    servo.duty_cycle = 5000   #90 degrees (vertical)
    print("90")
    time.sleep(1)

    #set_angle(180)
    servo.duty_cycle = 8100  #180 degrees (left)
    print("180")
    time.sleep(1)