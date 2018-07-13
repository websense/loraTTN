import paho.mqtt.client as mqtt #import mqtt client
import time
import random
import json

broker_address = "eu.thethings.network"
client_user = "hd_ttn_gps"
#Password Removed
client_password = ""
broker_topic = "/devices/gps_tracker_1/up"


def on_message(client, userdata, message):
    decoded_message = str(message.payload.decode("utf-8"))
    #print("message received " , decoded_message)
    parsed_json = json.loads(decoded_message)
    print(json.dumps(parsed_json, sort_keys=False, indent=4))
    #print(parsed_json['payload_fields']['temperature'])
    for gateway_record in parsed_json['metadata']['gateways']:
        print(gateway_record['gtw_id'])
        print(gateway_record['rssi'])
        print(gateway_record['snr'])

    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

def on_connect(client, userdata, flags, rc):
    client.subscribe(client_user + broker_topic)  

client = mqtt.Client()
client.on_message=on_message
client.on_connect=on_connect
client.username_pw_set(client_user, client_password)
client.connect(host=broker_address, keepalive=90)
client.loop_forever()



