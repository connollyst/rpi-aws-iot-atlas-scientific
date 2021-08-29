#!/usr/bin/python

import time

from atlas.AtlasScientificI2C import AtlasScientificI2C
from atlas.AtlasScientificSensor import AtlasScientificSensor
from atlas.AtlasScientificSensorReading import AtlasScientificSensorReading


class AtlasScientific:
    READ_DELAY_SECS = 1
    DEFAULT_I2C_ADDRESS = 98

    READ_COMMAND = 'R'

    # TODO dependency injection
    def __init__(self, i2c: AtlasScientificI2C = None):
        # TODO create I2C if None
        self._i2c = i2c
        print('Starting Atlas Scientific with I2C:')
        print(i2c)
        self._current_address = self.DEFAULT_I2C_ADDRESS

    def list(self):
        sensors = []
        for sensor in self._i2c.list():
            sensors.append(AtlasScientificSensor(sensor))
        return sensors

    def read(self):
        try:
            sensors = self.list()
            for sensor in sensors:
                sensor.write(self.READ_COMMAND)
            time.sleep(self.READ_DELAY_SECS)
            readings = []
            for sensor in sensors:
                readings.append(AtlasScientificSensorReading(sensor.read()))
            return readings
        except IndexError as e:
            # TODO track down to the specific line
            print('Error:')
            print(e)
            print('Retrying..')
            self.read()
