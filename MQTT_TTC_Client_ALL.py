import paho.mqtt.client as mqtt #import mqtt client
import time
import random
import json
import loraMessageDBHandler
from multiprocessing import Process
import logging
import UWAFarmConfiguration as UWAFarm

class thingsConnection:

    broker_address = UWAFarm.TTN_MQTT_BROKER
    client_user = UWAFarm.TTN_MQTT_USER_NAME_GPS
    client_password = UWAFarm.TTN_MQTT_PASSWORD_GPS
    broker_topic = UWAFarm.TTN_MQTT_TOPIC_GPS
    mqtt_ttn_tls_port = UWAFarm.TTN_MQTT_TSL_PORT
    mqtt_ttn_cert_auth = UWAFarm.TTN_MQTT_CERT_AUTH

    def __init__(self):
        logging.basicConfig()

    def on_message(self, client, userdata, message):
        decoded_message = str(message.payload.decode("utf-8"))
        parsed_json = json.loads(decoded_message)
        print(json.dumps(parsed_json, sort_keys=False, indent=4))

        lLoraMessage = loraMessageDBHandler.loraMessage()
        lLoraMessage.saveAll(parsed_json)


    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.client_user + self.broker_topic)  

    def run_mqtt(self):
        client = mqtt.Client()
        client.on_message=self.on_message
        client.on_connect=self.on_connect
        client.username_pw_set(self.client_user, self.client_password)
        client.tls_set(ca_certs=self.mqtt_ttn_cert_auth)
        client.connect(host=self.broker_address, port=self.mqtt_ttn_tls_port, keepalive=90)
        client.loop_forever()


lGPSThingsConnection = thingsConnection()
lGPSThingsConnection.broker_address = UWAFarm.TTN_MQTT_BROKER
lGPSThingsConnection.client_user = UWAFarm.TTN_MQTT_USER_NAME_GPS
lGPSThingsConnection.client_password = UWAFarm.TTN_MQTT_PASSWORD_GPS
lGPSThingsConnection.broker_topic = UWAFarm.TTN_MQTT_TOPIC_GPS

if __name__ == '__main__':
    p = Process(target=lGPSThingsConnection.run_mqtt)
    p.start()

lTempMoistureThingsConnection = thingsConnection()
lTempMoistureThingsConnection.broker_address = UWAFarm.TTN_MQTT_BROKER
lTempMoistureThingsConnection.client_user = UWAFarm.TTN_MQTT_USER_NAME_TM
lTempMoistureThingsConnection.client_password = UWAFarm.TTN_MQTT_PASSWORD_TM
lTempMoistureThingsConnection.broker_topic = UWAFarm.TTN_MQTT_TOPIC_TM

if __name__ == '__main__':
    q = Process(target=lTempMoistureThingsConnection.run_mqtt)
    q.start()


