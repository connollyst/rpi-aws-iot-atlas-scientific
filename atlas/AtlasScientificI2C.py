#!/usr/bin/python

from atlas.AtlasScientificSensor import AtlasScientificSensor
from atlas.AtlasScientificSensorReading import AtlasScientificSensorReading
from i2c.I2C import I2C


class AtlasScientificI2C:
    # the default bus for I2C on the newer Raspberry Pis,
    # certain older boards use bus 0
    DEFAULT_BUS = 1
    # the default address for the sensor
    DEFAULT_ADDRESS = 98

    # the timeout needed to query readings and calibrations
    LONG_TIMEOUT = 1.5
    # timeout for regular commands
    SHORT_TIMEOUT = .3
    LONG_TIMEOUT_COMMANDS = ("R", "CAL")
    SLEEP_COMMAND = "SLEEP"
    READ_DELAY_SECS = 1

    def __init__(self, i2c: I2C = None, address=None, bus=None):
        """
        open two file streams, one for reading and one for writing
        the specific I2C channel is selected with bus
        it is usually 1, except for older revisions where its 0
        wb and rb indicate binary read and write
        """
        self._i2c = i2c or I2C()
        self._address = address or self.DEFAULT_ADDRESS
        self.bus = bus or self.DEFAULT_BUS

    def list_sensors(self):
        sensors = []
        for i2c_address in self._i2c.find_all_i2c_devices():
            print('Found sensor @ address {}'.format(i2c_address))
            name = self.__query_i2c(i2c_address, "name,?")
            print('> name,?: {}'.format(name))
            info = self.__query_i2c(i2c_address, "I")
            print('> I     : {}'.format(info))
            sensors.append(AtlasScientificSensor(name, info, i2c_address))
        return sensors

    def read_sensors(self):
        readings = []
        for sensor in self.list_sensors():
            print('Taking reading!')
            readings.append(AtlasScientificSensorReading(self.__query_i2c(sensor.address, 'R')))
        return readings

    def __query_i2c(self, address, command):
        return self._i2c.query(address, command, self.__get_command_timeout(command))

    def __get_command_timeout(self, command):
        timeout = None
        if command.upper().startswith(self.LONG_TIMEOUT_COMMANDS):
            timeout = self.LONG_TIMEOUT
        elif not command.upper().startswith(self.SLEEP_COMMAND):
            timeout = self.SHORT_TIMEOUT
        return timeout
