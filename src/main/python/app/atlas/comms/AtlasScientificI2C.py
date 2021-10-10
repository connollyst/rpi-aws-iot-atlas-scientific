from .AtlasScientificIO import AtlasScientificIO
from ..AtlasScientificSensor import AtlasScientificSensor
from ...comms.I2C import I2C
from ...rpi.Host import Host


class AtlasScientificI2C(AtlasScientificIO):

    def __init__(self, i2c: I2C = None, host: Host = None, logger=None):
        self._i2c = i2c or I2C()
        self._host = host
        self._logger = logger

    def find_devices(self):
        self._logger.info('Finding all connected I2C devices..')
        # TODO replace with list comprehension
        devices = []
        for i2c_address in self._i2c.find_all_i2c_devices():
            self._logger.info('Found I2C device @ address {}'.format(i2c_address))
            devices.append(AtlasScientificSensor(i2c_address, self._i2c, self._host, self._logger))
        return devices

    def close(self):
        self._i2c.close()
