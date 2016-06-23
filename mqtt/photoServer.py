from gpiozero import MotionSensor
from datetime import datetime
from signal import pause
import picamera
import paho.mqtt.client as mqtt
import os
from subprocess import check_output

topic = "/pi/camera"
server = "10.0.1.3"

camera = picamera.PiCamera()

output = check_output(['hostname', '-I'])
ipaddr = output.decode("utf-8").rstrip()

client = mqtt.Client()
client.loop_start()


def take_photo():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = 'pic_' + timestamp + '.jpg'
    camera.capture(filename)
    fqp = os.getcwd() + '/' + filename
    scp = 'pi@' + ipaddr + ':' + fqp
    client.publish(topic, "photo taken: " + scp)

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)

def on_message(client, userdata, msg):
    command = msg.payload.decode("utf-8")
    if command == "take photo":
        take_photo()

pir = MotionSensor(4)
pir.when_motion = take_photo

client.on_connect = on_connect
client.on_message = on_message
client.connect(server, 1883, 60)

pause()
client.loop_stop()
