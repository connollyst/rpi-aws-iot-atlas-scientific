import time
from threading import Thread

from .comms.AtlasScientificI2C import AtlasScientificI2C
from .comms.AtlasScientificIO import AtlasScientificIO
from ..rpi.Host import Host


class AtlasScientific:
    SAMPLE_COUNT = 10
    SAMPLE_FREQUENCY = 0.5

    def __init__(self, io: AtlasScientificIO = None, host: Host = None, logger=None):
        self._logger = logger
        # TODO always default to I2C?
        self._io = io or AtlasScientificI2C(host, logger)
        self._running = False
        self._thread = None
        self._devices = self._io.find_devices()

    @property
    def devices(self):
        return self._devices

    def start(self):
        self._logger.debug("Starting Atlas Scientific Tentacle Shield reader..")
        self._running = True
        self._thread = Thread(target=self._sample_devices)
        self._thread.start()

    def _sample_devices(self):
        while self._running:
            [device.read() for device in self._devices]
            time.sleep(self.SAMPLE_FREQUENCY)

    def stop(self):
        self._logger.info('Stopping Atlas Scientific Tentacle Shield reader..')
        self._running = False
        self._thread.join()
        # TODO correct order here?
        self._io.close()
