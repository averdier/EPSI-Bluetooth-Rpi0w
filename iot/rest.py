# -*- coding: utf-8 -*-

import json
import requests
from requests.auth import HTTPBasicAuth


class IOTApi:
    def __init__(self, device_id, key, base_url):
        self._device_id = device_id
        self._key = key
        self._base_url = base_url

    def _get_with_authorization_context(self, url_suffix):
        response = requests.get(self._base_url + url_suffix, headers={
            'content-type': 'application/json'
        }, auth=HTTPBasicAuth(self._device_id, self._key))

        return response

    def get_configuration(self):
        response = self._get_with_authorization_context('/config')

        if response.status_code != 200:
            raise Exception(response.text)

        else:
            return json.loads(response.text)
