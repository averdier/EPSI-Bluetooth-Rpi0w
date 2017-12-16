# -*- coding: utf-8 -*-

import json
import time
import paho.mqtt.client as mqtt
from .Bluetooth import BluetoothScanner
from iot.rest import IOTApi
from config import config


class App:
    def __init__(self, config_name='default'):
        self._config = config[config_name]
        self._api = IOTApi(self._config.DEVICE_ID, self._config.KEY, self._config.SERVER)
        self._mqtt = mqtt.Client()
        self._scanner = BluetoothScanner(self._config.BLUETOOTH_DEVICE_ID)
        self._device_config = None
        self._scanner_started = False

    def on_connect(self, userdata, flags, rc):
        if rc == 4:
            raise Exception('Invalid username or password')

        if rc != 0:
            raise Exception('Unable to connect to mqtt service')

        print('MQTT connected')
        self._scanner.init_bluetooth()
        if self._scanner.get_inquiry_mode() != 1:
            self._scanner.set_inquiry_mode(1)
        self._scanner_started = True
        print('Bluetooth scanner started')

    def on_message(self, userdata, msg):
        pass

    def start(self):
        self._device_config = self._api.get_configuration()
        self._mqtt.username_pw_set(
            self._device_config['mqtt_account']['username'],
            self._device_config['mqtt_account']['password']
        )

        def on_mqtt_message(client, userdata, msg):
            nonlocal self
            self.on_message(userdata, msg)

        def on_mqtt_connect(client, userdata, flags, rc):
            nonlocal self
            self.on_connect(userdata, flags, rc)

        self._mqtt.on_connect = on_mqtt_connect
        self._mqtt.on_message = on_mqtt_message

        self._mqtt.connect(
            self._device_config['mqtt_account']['server'],
            self._device_config['mqtt_account']['port'],
            self._device_config['mqtt_account']['keep_alive']
        )

    def stop(self):
        self._mqtt.disconnect()

    def loop(self):
        self._mqtt.loop()

        if self._scanner_started:
            t0 = time.time()
            devices = self._scanner.get_devices_from_inquiry_with_rssi()
            t1 = time.time()

            if len(devices) > 0:
                payload = {
                    'start_timestamp': t0,
                    'end_timestamp': t1,
                    'devices': [{'mac': d[0], 'rssi': d[1]} for d in devices]
                }

                self._mqtt.publish(self._device_config['mqtt_account']['device_topic'], json.dumps(payload))
                print('datas sent')

