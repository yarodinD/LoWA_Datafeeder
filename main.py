
# Import modules

import json
import websocket
# https://github.com/websocket-client/websocket-client

from decoder import decode

# importing the requests library
import requests

# defining the api-endpoint
API_ENDPOINT = "http://46.101.243.178:8080/v1/lorawan"
headers = {'content-type': 'application/json'}

# Functions


def on_message(ws, msg):
    msg_dict = json.loads(msg)

    if msg_dict['EUI'] in ['70B3D57BA0000DE0', '70B3D57BA0000DE1', '70B3D57BA0000DE2', '0004A30B001F97AA', '0004A30B002426AF', '0004A30B00241452', '0004A30B00239E55', '70B3D57BA0001215']:

        data = bytes(str(msg_dict['data']), encoding='utf8')
        EUI = msg_dict['EUI']

        result = json.dumps(decode(data, EUI, hex=True))

        print(result)
        requests.post(url=API_ENDPOINT, data=result, headers=headers)

        with open('data.txt', 'a') as outfile:
            json.dump(result, outfile)

    elif msg_dict['EUI'] == 'DD4E545010000123':

        result = {
            "Device ID": 3553,
            "Protocol version": 2,
            "Battery voltage": {
                "value": 3.108,
                "unit": "V"
            },
            "Air temperature": {
                "value": 32.30296787975891,
                "unit": "\\u00b0C"
            },
            "Air humidity": {
                "value": 58.42832074464027,
                "unit": "%"
            },
            "Barometric pressure": {
                "value": 100682,
                "unit": "Pa"
            },
            "Ambient light (visible + infrared)": {
                "value": 18,
                "unit": 'null'
            },
            "Ambient light (infrared)": {
                "value": 3,
                "unit": 'null'
            },
            "Illuminance": {
                "value": 20.279232,
                "unit": "lx"
            },
            "CO2 concentration": {
                "value": 657,
                "unit": "ppm"
            },
            "CO2 sensor status": {
                "value": 0,
                "unit": 'null'
            },
            "Raw IR reading": {
                "value": 37049,
                "unit": 'null'
            },
            "Activity counter": {
                "value": 107,
                "unit": 'null'
            },
            "Wind speed": {
                "value": 8.25, 
                "unit": "m\u22c5s\u207b\u00b9"
            },
            "Precipitation": {
                "value": 20.0, 
                "unit": "mm"
            },
            "Total VOC": {"value": 344, 
            "unit": "ppb"
            }
        }

        print(result)
        requests.post(url=API_ENDPOINT, data=result, headers=headers)

    else:
        print(msg)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("### opened ###")

# Main Program


wsUri = "wss://mvv.loriot.io/app?token=vgEAKwAAAA1tdnYubG9yaW90LmlvkdUZ1OtxmDyLCjpH81dcPg=="

websocket.enableTrace(True)
ws = websocket.WebSocketApp(wsUri,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.on_open = on_open
ws.run_forever()
