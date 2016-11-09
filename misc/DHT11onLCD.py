from dothat import backlight
import dothat.lcd as lcd
import time
import Adafruit_DHT
from colour import Color

def temp_color(temp):
    if temp < 5:
        return Color('white')
    if 5 <= temp <= 10:
        return list(Color('white').range_to(Color('blue'), 6))[temp-5]
    if 10 <= temp <= 18:
        return list(Color('blue').range_to(Color('yellow'), 9))[temp-10]
    if 18 <= temp <= 22:
        return list(Color('yellow').range_to(Color('orange'), 5))[temp - 18]
    if 22 <= temp <= 30:
        return list(Color('orange').range_to(Color('red'), 9))[temp - 22]
    return Color('red')

sensor = Adafruit_DHT.DHT11
pin = 5

backlight.rgb(200,200,200)

def displayCurrentValues():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    color = temp_color(int(temperature))
    backlight.rgb(int(color.red * 255), int(color.green * 255), int(color.blue * 255))
    lcd.set_cursor_position(0, 0)
    lcd.write("Temperatur: " + str(temperature))
    lcd.set_cursor_position(0,1)
    lcd.write("Humidity:   " + str(humidity))
    time.sleep(10.01)

try:
    while True:
        displayCurrentValues()
finally:
    lcd.clear()
    backlight.off()
