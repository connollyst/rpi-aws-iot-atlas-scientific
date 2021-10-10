import time
from collections import deque

from .AtlasScientificSensorReading import AtlasScientificSensorReading
from ..comms.IO import IO


class AtlasScientificSensor:
    # Timeout needed to query readings and calibrations
    LONG_TIMEOUT = 1.5
    # Timeout for regular commands
    SHORT_TIMEOUT = .3

    NAME_COMMAND = 'name,?'
    INFO_COMMAND = 'I'
    READ_COMMAND = 'R'

    SAMPLE_COUNT = 10

    def __init__(self, address, io: IO, host=None, logger=None):
        if not host:
            raise RuntimeError("host required")
        self._host = host
        if not logger:
            raise RuntimeError("logger required")
        self._logger = logger
        self._address = address
        self._io = io
        name = self._io.send_and_receive(address, self.NAME_COMMAND, self.SHORT_TIMEOUT)
        info = self._io.send_and_receive(address, self.INFO_COMMAND, self.SHORT_TIMEOUT)
        logger.debug('> {}: {}'.format(self.NAME_COMMAND, name))
        logger.debug('> {}     : {}'.format(self.INFO_COMMAND, info))
        self._name = name.split(",")[1]
        self._module = info.split(",")[1]
        self._version = info.split(",")[2]
        self._reading = None
        self._readings = deque()
        self._variance = {}
        self._last_write = 0

    @property
    def address(self):
        return self._address

    @property
    def name(self):
        return self._name

    @property
    def module(self):
        return self._module

    @property
    def version(self):
        return self._version

    def read(self) -> AtlasScientificSensorReading:
        self._reading = AtlasScientificSensorReading(
            self._io.send_and_receive(self.address, self.READ_COMMAND, self.LONG_TIMEOUT))
        self._logger.debug("Atlas Scientific Device #{}: {}".format(self._address, self._reading))
        self._readings.append(self._reading)
        if len(self._readings) > self.SAMPLE_COUNT:
            self._readings.popleft()
        return self._reading

    def variance(self):
        self._logger.info('TODO calculating reading variance..')
        # TODO these aren't numeric, huh?
        return 0

    def secs_since_last_write(self):
        return time.time() - self._last_write

    def to_json(self):
        if not self._reading:
            raise RuntimeError("no reading taken")
        self._last_write = time.time()
        return {
            'name': self.name,
            'module': self.module,
            'version': self.version,
            'address': self.address,
            "host": self._host.identifier,
            'addressType': 'I2C',
            'reading': {
                'value': self._reading.value,
                'timestamp': self._reading.timestamp
            }
        }

    def __str__(self) -> str:
        if self._name == '':
            return self._module + ' ' + str(self.address)
        else:
            return self._module + ' ' + str(self.address) + ' ' + self._name
