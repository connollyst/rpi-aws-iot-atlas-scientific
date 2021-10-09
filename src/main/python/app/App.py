import json
import time
from uuid import uuid4

from .atlas.AtlasScientific import AtlasScientific
from .aws.AwsIotCore import AwsIotCore


class App:
    AWS_ENDPOINT = 'a12dev37b8fhwi-ats.iot.us-west-2.amazonaws.com'
    AWS_IOT_MQTT_TOPIC = 'iot/devices/readings'
    AWS_CLIENT_ID = "iot-atlas-" + str(uuid4())

    MIN_DELAY = 0.5
    MAX_DELAY = 30
    MAX_VARIANCE = 0.1

    def __init__(self, logger, sensor=None, aws=None):
        self._logger = logger
        # self._sensor = sensor or eTapeReader(host=Host(), logger=self._logger)
        self._sensors = AtlasScientific().get_all_sensors()
        self._writer = aws or AwsIotCore(endpoint=self.AWS_ENDPOINT, logger=self._logger)
        self._running = False
        self._last_publication = 0

    def start(self):
        self._running = True
        # self._sensor.start()
        while self._running:
            try:
                for sensor in self._sensors:
                    # TODO relies on take_reading side effect
                    self._publish(sensor)
                time.sleep(self.MIN_DELAY)
            except KeyboardInterrupt:
                self._logger.info("Stopping..")
                self._running = False
                # self._sensor.stop()

    def _publish(self, sensor):
        self._writer.connect(self.AWS_CLIENT_ID)
        self._writer.write(self.AWS_IOT_MQTT_TOPIC,
                           json.dumps(sensor.to_json().replace(r'\u0000', ''), indent=4, default=str))
        self._writer.disconnect()
        self._last_publication = time.time()

    def _secs_since_last_publication(self):
        return time.time() - self._last_publication
