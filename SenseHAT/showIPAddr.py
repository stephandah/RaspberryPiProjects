from time import sleep
from subprocess import check_output
from sense_hat import SenseHat

blue = [0,0,255]
green = [0, 255, 0]
red = [255,0,0]

color = green

sense = SenseHat()
output = check_output(['hostname', '-I'])
ipaddr = output.decode("utf-8").rstrip()

try:
    for i in range(10):
        sense.show_message(ipaddr, scroll_speed=0.03, text_colour=color)
        sense.show_letter(ipaddr[-1], text_colour=color)
        sleep(1)
finally:
    sense.clear()
