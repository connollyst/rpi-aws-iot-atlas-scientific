import json
import time
from uuid import uuid4

from awscrt.exceptions import AwsCrtError

from .atlas.AtlasScientific import AtlasScientific
from .aws.AwsIotCore import AwsIotCore
from .rpi.Host import Host


class App:
    AWS_ENDPOINT = 'a12dev37b8fhwi-ats.iot.us-west-2.amazonaws.com'
    AWS_IOT_MQTT_TOPIC = 'iot/devices/readings'
    AWS_CLIENT_ID = "iot-atlas-" + str(uuid4())

    MIN_DELAY = 5  # 0.5
    MAX_DELAY = 30
    MAX_VARIANCE = 0.1

    def __init__(self, logger, tentacle=None, aws=None):
        if not logger:
            raise RuntimeError('logger required')
        self._logger = logger
        self._tentacle = tentacle or AtlasScientific(host=Host(), logger=self._logger)
        self._writer = aws or AwsIotCore(endpoint=self.AWS_ENDPOINT, logger=self._logger)
        self._running = False

    def start(self):
        self._running = True
        self._tentacle.start()
        while self._running:
            try:
                for device in self._tentacle.devices:
                    if device.variance() >= self.MAX_VARIANCE:
                        self._logger.info(
                            "Publishing device {} due to high variance: {}".format(
                                device.address, device.variance()
                            )
                        )
                        self._publish(device)
                    elif device.secs_since_last_write() >= self.MAX_DELAY:
                        self._logger.info(
                            "Publishing device {} due to delay: {}s".format(
                                device.address, device.secs_since_last_write()
                            )
                        )
                        self._publish(device)
                time.sleep(self.MIN_DELAY)
            except KeyboardInterrupt:
                self._logger.info("Stopping app..")
                self._running = False
                self._tentacle.stop()

    def _publish(self, device):
        try:
            self._writer.connect(self.AWS_CLIENT_ID)
            self._writer.write(self.AWS_IOT_MQTT_TOPIC,
                               json.dumps(device.to_json(), indent=4, default=str).replace(r'\u0000', ''))
            self._writer.disconnect()
        except AwsCrtError as e:
            self._logger.error("Failed to publish to AWS: {}".format(e.message))
