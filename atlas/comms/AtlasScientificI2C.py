#!/usr/bin/python

from atlas.AtlasScientificSensor import AtlasScientificSensor
from atlas.comms.AtlasScientificIO import AtlasScientificIO
from comms.I2C import I2C


class AtlasScientificI2C(AtlasScientificIO):

    def __init__(self, i2c: I2C = None):
        self._i2c = i2c or I2C()

    def list_sensors(self):
        sensors = []
        for i2c_address in self._i2c.find_all_i2c_devices():
            print('Found I2C sensor @ address {}'.format(i2c_address))
            sensors.append(AtlasScientificSensor(i2c_address, self._i2c))
        return sensors

    def close(self):
        self._i2c.close()
