# -*- coding: utf-8 -*-

import json
import requests
from requests.auth import HTTPBasicAuth
BASE_URL = 'http://93.118.34.190/public/iot/api'


class IOTResourcesAPI:
    """
    IOT Resources API
    """

    def __init__(self, uuid, key):
        """
        Constructor

        :param uuid: Device uuid
        :param key: Device key
        """
        self._uuid = uuid
        self._key = key
        self._token = None

    def _renew_token(self):
        """
        Renew auth token
        """

        response = requests.get(BASE_URL + '/token/',
                                headers={
                                    'content-type': "application/json"
                                },
                                auth=HTTPBasicAuth(self._uuid, self._key))

        # TODO handle errors
        token = json.loads(response.text)['token']
        print('token: {0}'.format(token))
        self._token = token

    def _get_auth_headers(self):
        """
        Return headers with authorization

        :return: Headers with authorization
        :rtype: dict
        """
        if self._token is not None:
            headers = {
                'Authorization': 'Token {}'.format(self._token),
                'content-type': "application/json"
            }

            return headers

        else:
            raise Exception('No token found')

    def _get_with_auth_context(self, url_suffix):
        """
        Get from api with auth context

        :param url_suffix: Base url suffix
        :return: Requests response
        """

        if self._token is None:
            self._renew_token()

        headers = self._get_auth_headers()

        return requests.get(BASE_URL + url_suffix, headers=headers)

    def get_config(self):
        """
        Return device configuration from API

        :return: Configuration
        :rtype: dict
        """

        return json.loads(self._get_with_auth_context('/config').text)

