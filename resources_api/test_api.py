from resources_api.iotresources import IOTResourcesAPI


uuid = 'rpi0w_01'
key = 'xWocdVJp1FL9GfNC'


if __name__ == '__main__':
    api = IOTResourcesAPI(uuid, key)
    config = api.get_config()

    print('{0}'.format(config))