#!/usr/bin/python

from io.CommsProtocol import CommsProtocol

from atlas.AtlasScientificSensorReading import AtlasScientificSensorReading


class AtlasScientificSensor:
    # the timeout needed to query readings and calibrations
    LONG_TIMEOUT = 1.5
    # timeout for regular commands
    SHORT_TIMEOUT = .3

    def __init__(self, address, io: CommsProtocol):
        self._address = address
        self._io = io
        name = self._io.send_and_receive(address, "name,?", self.SHORT_TIMEOUT)
        print('> name,?: {}'.format(name))
        info = self._io.send_and_receive(address, "I", self.SHORT_TIMEOUT)
        print('> I     : {}'.format(info))
        try:
            self._name = name.split(",")[1]
        except IndexError:
            # TODO do better than this!
            self._name = name
        try:
            self._module = info.split(",")[1]
        except IndexError:
            # TODO do better than this!
            self._module = info

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def module(self):
        return self._module

    def take_reading(self) -> AtlasScientificSensorReading:
        # TODO store reading
        # TODO support multiple readings
        return AtlasScientificSensorReading(self._io.send_and_receive(self.address, 'R', self.LONG_TIMEOUT))

    def __str__(self):
        if self._name == "":
            return self._module + " " + str(self.address)
        else:
            return self._module + " " + str(self.address) + " " + self._name
