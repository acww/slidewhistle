from time import sleep
import board
import pwmio
from adafruit_motor import servo
import usb_cdc

serial = usb_cdc.data

run = True

# create a PWMOut object on the control pin.
pwm = pwmio.PWMOut(board.GP2, duty_cycle=0, frequency=50)

servo1 = servo.Servo(pwm, min_pulse=400, max_pulse=2400)

pwm2 = pwmio.PWMOut(board.GP4, duty_cycle=0, frequency=30)

servo2 = servo.Servo(pwm2, min_pulse=400, max_pulse=2400)

back = 50
front = 150

pos = 130

lungs = 180
rate = 2

# midi note with approximate servo angle for the note and the rate at which the bellows decrease
m70 = [146, 1.75] # midi note 70
m71 = [139, 2]
m72 = [135, 2.25]
m73 = [130, 2.5]
m74 = [126, 3]
m75 = [122, 3]
m76 = [116, 3]
m77 = [114, 3]
m78 = [110, 4]
m79 = [105, 4]
m80 = [102, 4]
m81 = [98, 4]
m82 = [95, 4]
m83 = [91, 5]
m84 = [87, 5]
m85 = [84, 5]
m86 = [81, 5]

notes = [m70, m71, m72, m73, m74, m75, m76, m77, m78, m79, m80, m81, m82, m83, m84, m85, m86]

prev_note = 0
new_note = False

while run:
    wait = True
    while wait:
        if serial.in_waiting > 0:
            byte = serial.read()
            value = ord(byte)
            x = [int(a) for a in str(value)]
            if len(x) == 2:
                note = x[0]
            elif len(x) == 3:
                note = x[0]*10 + x[1]
            else:
                note = prev_note
            movement = x[-1]
            wait = False
        sleep(0.01)
    if note != prev_note:
        rate = notes[note-1][1]
        if new_note:
            rate += 15
            new_note = False
    lungs -= rate
    if lungs < 0 or value == 0:
        #print('this triggered')
        lungs = 180
        new_note = True
    servo2.angle = lungs
    if note != 0:
        pos = notes[note-1][0]
        if movement == 1:
            if lungs < 120 and lungs > 60:
                notes[note-1][0] += 1
                print('Moving up a lot. Current lungs position is: ', lungs, '  Servo position should now equal: ', notes[note-1][0])
        elif movement == 2:
            notes[note-1][0] += 0.1
            print('Moving up a bit. Servo position should now equal: ', notes[note-1][0])
        elif movement == 4:
            notes[note-1][0] -= 0.1
            print('Moving down a bit. Servo position should now equal: ', notes[note-1][0])
        elif movement == 5:
            if lungs < 120 and lungs > 60:
                notes[note-1][0] -= 1
                print('Moving down a lot. Current lungs position is: ', lungs, '  Servo position should now equal: ', notes[note-1][0])
        elif movement == 3:
            print('success at: ', servo1.angle)
    if pos > front:
        pos = front
    elif pos < back:
        pos = back
    servo1.angle = pos
    serial.reset_input_buffer()
    sleep(0.01)
