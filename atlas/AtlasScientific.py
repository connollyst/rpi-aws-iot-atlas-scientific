#!/usr/bin/python

from atlas.AtlasScientificI2C import AtlasScientificI2C


class AtlasScientific:

    def __init__(self, i2c: AtlasScientificI2C = None):
        self._i2c = i2c or AtlasScientificI2C()

    def list_all(self):
        return self._i2c.list_sensors()

    def read_all(self):
        return self._i2c.read_sensors()
