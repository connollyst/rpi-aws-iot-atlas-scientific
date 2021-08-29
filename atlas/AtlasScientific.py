#!/usr/bin/python

from atlas.AtlasScientificI2C import AtlasScientificI2C
import time
import copy

from i2c.I2C import I2C


class AtlasScientific:

    READ_DELAY_SECS = 1
    DEFAULT_I2C_ADDRESS = 98

    # TODO dependency injection
    def __init__(self, i2c: AtlasScientificI2C = AtlasScientificI2C):
        self._i2c = i2c
        self._current_address = self.DEFAULT_I2C_ADDRESS

    def list(self):
        self._i2c.list()

    def read(self):
        try:
            device_list = self.list()
            for device in device_list:
                device.write("R")
            time.sleep(self.READ_DELAY_SECS)
            for device in device_list:
                message = device.read()
                print(message)
                return ...
        except IndexError as e:
            print('Error:')
            print(e)
            print('Retrying..')
            self.read()
