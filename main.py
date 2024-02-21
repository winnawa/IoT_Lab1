import random
import sys
from Adafruit_IO import MQTTClient
import time
from ai_recognition import predictWearingMask

AIO_FEED_IDs = ["nutnhan1","nutnhan2"]
AIO_USERNAME = "namkhoapham"
AIO_KEY = "aio_OoOw32ZFLJ20ZsxAcgUYAFFubbwC"

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_IDs: 
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

counter = 10
counter_ai = 5
while True:
    counter = counter -1
    if counter <= 0:
        counter = 10
        print("Data is publishing")
        temp = random.randint(10,20)
        client.publish("cambien1", temp)
        humi = random.randint(50,70)
        client.publish("cambien2", humi)
        light = random.randint(100,500)
        client.publish("cambien3", light)

    counter_ai = counter_ai -1
    imageStatus = ""
    imagePreviousStatus = ""
    if counter_ai <= 0:
        counter_ai = 5
        ai_result = predictWearingMask()
        print("ai detect: ", ai_result)
        imagePreviousStatus = imageStatus
        imageStatus = ai_result
        if imageStatus != imagePreviousStatus:
            client.publish("ai", imageStatus)
    time.sleep(1)