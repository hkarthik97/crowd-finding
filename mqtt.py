import json
import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
from pytz import timezone
import requests
import random
from json.decoder import JSONDecodeError
from _thread import start_new_thread
from pymongo import MongoClient


myclient = MongoClient("mongodb+srv://karthik:karthik@cluster0.dva2k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
mydb = myclient["myFirstDatabase"]
mycol = mydb["People"]
threadId = 1 # thread counter
waiting = 2 # 2 sec. waiting time

MQTT_SERVER = "broker.hivemq.com"
MQTT_PATH1 = "Sniffer"

# format = "%Y-%m-%dT%H:%M"
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Us/Eastern'))
print(now_asia)
dateString = str(now_asia)
ada = dateString[:10]+"T"+dateString[11:]
datee = ada[:19]
print (datee)
# format = "%Y-%m-%dT%H:%M"
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Us/Eastern'))
print(now_asia)
dateString = str(now_asia)
ada = dateString[:10]+"T"+dateString[11:]
datee = ada[:19]
print (datee)

conn = sqlite3.connect('data.db')


def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH1)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    now_utc = datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Us/Eastern'))
    print(now_asia)
    dateString = str(now_asia)
    ada = dateString[:10]+"T"+dateString[11:]
    datee = ada[:19]


    #print(msg.topic+" "+str(msg.payload))

    print("success")
    topic = msg.topic
    print(type(topic))

    if (topic==MQTT_PATH1):
        print(msg.payload)
        y = json.loads(msg.payload)
        print(y["MAC"])
        no_of_devices= len(y["MAC"])
        mydict = { "Devices": no_of_devices }
        x = mycol.insert_one(mydict)

        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()
