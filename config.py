# -*- coding: utf-8 -*-


class Config:
    """
    Base configuration
    """
    DEVICE_ID = ''
    KEY = ''
    SERVER = ''
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