from dothat import backlight
import dothat.lcd as lcd
import time
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 5

backlight.rgb(200,200,200)

def displayCurrentValues():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
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
