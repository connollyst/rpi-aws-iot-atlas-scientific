#!/usr/bin/python

from i2c.I2C import I2C


class AtlasScientificI2C:
    # the timeout needed to query readings and calibrations
    LONG_TIMEOUT = 1.5
    # timeout for regular commands
    SHORT_TIMEOUT = .3
    # the default bus for I2C on the newer Raspberry Pis,
    # certain older boards use bus 0
    DEFAULT_BUS = 1

    LONG_TIMEOUT_COMMANDS = ("R", "CAL")
    SLEEP_COMMANDS = ("SLEEP",)

    def __init__(self, i2c: I2C = None, address=None, bus=None):
        '''
        open two file streams, one for reading and one for writing
        the specific I2C channel is selected with bus
        it is usually 1, except for older revisions where its 0
        wb and rb indicate binary read and write
        '''
        # TODO set I2C
        self._address = address or self.DEFAULT_ADDRESS
        self.bus = bus or self.DEFAULT_BUS
        self._long_timeout = self.LONG_TIMEOUT
        self._short_timeout = self.SHORT_TIMEOUT

    @property
    def long_timeout(self):
        return self._long_timeout

    @property
    def short_timeout(self):
        return self._short_timeout

    def list(self):
        i2c_devices = []
        for i2c_address in range(0, 128):
            try:
                self.i2c.ping(i2c_address)
                i2c_devices.append(i2c_address)
            except IOError:
                pass
        return i2c_devices

    def ping(self, i2c_address):
        self._i2c.ping(i2c_address)
        # TODO try/catch with boolean response
