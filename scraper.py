#!/usr/bin/python3

import requests
import re
from bs4 import BeautifulSoup
import paho.mqtt.client as mqtt
import time

mqtt_topic = "/solis"
mqtt_addr = "***REMOVED***"
mqtt_port = 1883
addr = "***REMOVED***"
user = "admin"
passwd = "admin"
url = "http://%s/status.html" % addr

def scrape():
    try:
        page = requests.get(url, auth=(user, passwd))
    except requests.exceptions.ConnectionError:
        return 0
    try:
        soup = BeautifulSoup(page.content, 'html.parser')
        data = soup.find_all('script')[1]
        obj = re.search(r"""var webdata_now_p = "(\d*)";""", data.get_text())
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



