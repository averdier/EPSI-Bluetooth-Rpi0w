# -*- coding: utf-8 -*-


class Config:
    """
    Base configuration
    """
    DEVICE_ID = 'sensor_1'
    KEY = 'xWocdVJp1FL9GfNC'
    SERVER = 'http://vps475171.ovh.net/public/iot/api'
    BLUETOOTH_DEVICE_ID = 0


class DevelopmentConfig(Config):
    """
    Development configuration
    """


class ProductionConfig(Config):
    """
    Development configuration
    """


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}