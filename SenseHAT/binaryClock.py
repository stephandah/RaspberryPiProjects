from sense_hat import SenseHat
from datetime import datetime
from time import sleep

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

sense = SenseHat()
sense.flip_v()

def convert2binary(number, digits):
    s = str(bin(number))[2:]
    if len(s) < digits:
        s = s.rjust(digits, '0')
    return s

def display(number, start, rows, color):
    binary = convert2binary(number, 8)
    for row in range(start, start+rows):
        for col, digit in enumerate(binary):
            if digit == '1':
                c = color
            else:
                c = black
            sense.set_pixel(row, 7-col, c)

try:
    while True:
        now = datetime.time(datetime.now())
        display(now.hour, 0, 2, green)
        display(now.minute, 3, 2, blue)
        display(now.second, 6, 2, red)
        sleep(1)
finally:
    sense.clear()

