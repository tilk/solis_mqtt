#!/usr/bin/python3

import requests
import re
import paho.mqtt.client as mqtt
import time
from config import *

url = "http://%s/status.html" % addr

def scrape():
    try:
        page = requests.get(url, auth=(user, passwd))
    except requests.exceptions.ConnectionError:
        return 0
    try:
        data = page.text
        obj = re.search(r"""var webdata_now_p = "(\d*)";""", data)
        return int(obj.group(1))
    except:
        return -1

client = mqtt.Client()

client.connect(mqtt_addr, mqtt_port, 60)
client.loop_start()

while True:
    watts = scrape()
    client.publish(mqtt_topic, watts)
    time.sleep(300)



