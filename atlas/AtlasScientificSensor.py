#!/usr/bin/python

from i2c.I2C import I2C

class AtlasScientificSensor:

    def __init__(self, name, type, address, i2c: I2C):
        self._name = name
        self._type = type
        self._address = address
        self._i2c = i2c
       
    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def type(self):
        return self._type

    def info(self):
        if(self._name == ""):
            return self._type + " " + str(self.address)
        else:
            return self._type + " " + str(self.address) + " " + self._name

    def read(self):
        return self._i2c.query('R')
