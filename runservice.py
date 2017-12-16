# -*- coding: utf-8 -*-

import json
import sys
import time
import paho.mqtt.client as ns_client
from app.Bluetooth import BluetoothScanner
from resources_api.iotresources import IOTResourcesAPI
from iot.rest import IOTApi


uuid = 'rpi0w_01'
key = 'xWocdVJp1FL9GfNC'
bluetooth_device_id = 0
mqtt_port = 1883
mqtt_keep_alive = 60

api = IOTResourcesAPI(uuid, key)
mqtt = ns_client.Client()
scanner = BluetoothScanner(bluetooth_device_id)


if __name__ == '__main__':
    try:
        configuration = api.get_config()
        if configuration is None:
            print('Unable to get configuration')
            sys.exit(1)

        if len(configuration['accounts']) == 0:
            print('No accounts found')
            sys.exit(1)

        mqtt_account = None
        for account in configuration['accounts']:
            if account['provider'] == 'mqtt':
                mqtt_account = account
                break

        if mqtt_account is None:
            print('No mqtt account found')
            sys.exit(1)

        mqtt.username_pw_set(
            mqtt_account['username'],
            mqtt_account['password']
        )

        mqtt.connect(
            mqtt_account['server_address'],
            mqtt_port,
            mqtt_keep_alive
        )

        scanner.init_bluetooth()
        if scanner.get_inquiry_mode() != 1:
            scanner.set_inquiry_mode(1)

        mqtt.publish('sensor/' + mqtt_account['username'] + '/from_device', 'started')
        last_publish = time.time()
        while True:
            t0 = time.time()
            devices = scanner.get_devices_from_inquiry_with_rssi()
            t1 = time.time()

            if len(devices) > 0:
                payload = {
                    'start_timestamp' : t0,
                    'end_timestamp': t1,
                    'devices': [{'mac': d[0], 'rssi': d[1]} for d in devices]
                }

                if time.time() - last_publish > mqtt_keep_alive -10:
                    mqtt.connect(
                        mqtt_account['server_address'],
                        mqtt_port,
                        mqtt_keep_alive
                    )

                mqtt.publish('sensor/' + mqtt_account['username'] + '/from_device', '{0}'.format(json.dumps(payload)))
                last_publish = time.time()
                print('datas sent')
            time.sleep(5)

    except Exception as ex:
        print(ex)
        sys.exit(1)

