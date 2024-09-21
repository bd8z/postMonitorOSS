#!/usr/bin/python3

import base64
import datetime
import json
import time

import gpiozero
import requests
from libcamera import controls
from picamera2 import Picamera2

pin_shutdwn = gpiozero.DigitalOutputDevice(pin=17)
pin_daynight = gpiozero.DigitalOutputDevice(pin=27)
pin_camled = gpiozero.DigitalOutputDevice(pin=19)
pin_shutdwn.off()
pin_daynight.off()
pin_camled.off()

##camera
pin_camled.on()
picam2 = Picamera2()
sizeH = int(2304)
sizeW = int(1296)
imagePath = "/home/***/PostMonitor/out.jpg"


preview_config = picam2.create_preview_configuration(main={"size": (sizeH, sizeW)})
picam2.configure(preview_config)
picam2.start()

picam2.set_controls({"AfMode":controls.AfModeEnum.Continuous})
time.sleep(2)
picam2.capture_file(imagePath)
picam2.close()
print("[log]shot success!")
pin_camled.off()

##Nwcheck
print("[log]shot.py start!")
while (True):
    statusCode = 400
    try:
        res = requests.get("https://google.com",timeout=(5,10))
        statusCode = res.status_code
    except:
        pass

    if (statusCode == 200):
        print("[log]network check end!")
        break
    else:
        time.sleep(0.1)

##send
data = open(imagePath, 'rb').read()
encoded_data = base64.b64encode(data).decode('utf-8')
wbData = base64.b64decode(encoded_data)
url = 'https://***.execute-api.ap-northeast-1.amazonaws.com/prod/ImageUpload'
payload = {'file': encoded_data, 'extension': 'jpg'}
statusCode = 400
for i in range(3):
    try:
        response = requests.post(url, data=json.dumps(payload),timeout=(5,10))
        statusCode = response.status_code
        if (statusCode == 200):
            print("[log]upload success!")
            break
    except:
        pass

dt_now = datetime.datetime.now()
if ((dt_now.hour>20) or (dt_now.hour<9)):
    pin_daynight.on()
    print("[log]night! hour:",dt_now.hour)
else:
    print("[log]daytime!")
    pin_daynight.off()
pin_shutdwn.on()
while(True):
    time.sleep(5)