# -*- coding: utf-8 -*-

import paramiko
from paramiko import SSHClient
from scp import SCPClient
import paho.mqtt.client as mqtt
import os
from PIL import Image

topic = "/pi/camera"
server = "10.0.1.3"

ssh = SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_system_host_keys()

def substring_between(string, start, end):
    rest = string.partition(start)[2]
    return rest.partition(end)[0]
    
def substring_after_last(string, delim):
    return string.rpartition(delim)[2]

def download_photo(host, user, photo):
    ssh.connect(host, username=user)
    with SCPClient(ssh.get_transport()) as scp:
        scp.get(photo)
        
def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)

def parse_photo_taken(line):
    user = substring_between(line, ": ", "@")
    host = substring_between(line, "@", ":")
    path = substring_after_last(line, ":")
    return (user, host, path)
    
def on_message(client, userdata, msg):
    command = msg.payload.decode("utf-8")
    if command.startswith("photo taken: "):
        user, host, path = parse_photo_taken(command)
        download_photo(host, user, path)
        filename = os.path.basename(path)
        image = Image.open(filename)
        image.show()
        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(server, 1883, 60)
client.loop_forever()

