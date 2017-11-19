# -*- coding: utf-8 -*-

import json
import sys
from app.Bluetooth import BluetoothScanner


if __name__ == '__main__':

    scanner = BluetoothScanner(0)

    try:
        scanner.init_bluetooth()
        if scanner.get_inquiry_mode() != 1:
            scanner.set_inquiry_mode(1)

        while True:
            devices = scanner.get_devices_from_inquiry_with_rssi()
            print(json.dumps(devices, indent=4))


    except Exception as ex:
        print(ex)
        sys.exit(1)



