#!/usr/bin/python

from atlas.comms.AtlasScientificI2C import AtlasScientificI2C
from atlas.comms.AtlasScientificIO import AtlasScientificIO


class AtlasScientific:

    def __init__(self, io: AtlasScientificIO = None):
        # TODO inject dependencies rather than defaulting to I2C
        self._io = io or AtlasScientificI2C()

    def get_all_sensors(self):
        return self._io.list_sensors()

    def close(self):
        self._io.close()
