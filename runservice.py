# -*- coding: utf-8 -*-

import json
import sys
from paho.mqtt.client as mqtt
from app.Bluetooth import BluetoothScanner


mqtt_server = ''
mqtt_port = 1883
mqtt_keep_alive = 60
mqtt_topic = ''
mqtt_username = ''
mqtt_password = ''
device_id = ''

def on_connect(client, userdata, flags, rc):
    """
    On mqtt connect

    :param client:
    :param userdata:
    :param flags:
    :param rc:
    :return:
    """
    print("Connected with result code " + str(rc))

    if rc == 4:
        print('Invalid credentials')
        sys.exit(1)

    client.publish(mqtt_topic, device_id + ":STARTED")


if __name__ == '__main__':

    scanner = BluetoothScanner(0)
    client = mqtt.Client()
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_connect = on_connect

    try:
        client.connect(mqtt_server, mqtt_port, mqtt_keep_alive)
        scanner.init_bluetooth()
        if scanner.get_inquiry_mode() != 1:
            scanner.set_inquiry_mode(1)

        while True:
            devices = scanner.get_devices_from_inquiry_with_rssi()
            print(json.dumps(devices, indent=4))


    except Exception as ex:
        print(ex)
        sys.exit(1)



