import logging
import sys
import unittest
from unittest.mock import ANY
from unittest.mock import MagicMock, Mock

from src.main.python.app.atlas.AtlasScientificSensor import AtlasScientificSensor

logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

SENSOR_ADDRESS = 'testSensorAddress'
SENSOR_NAME = '?NAME,myAtlasScientificSensor'
SENSOR_INFO = '?I,TEST,1.0'
SENSOR_READING = '1.37'


class TestAtlasScientificSensor(unittest.TestCase):

    def test_should_init_device_address(self):
        # Given
        sensor = AtlasScientificSensor(address=SENSOR_ADDRESS, io=MagicMock(), host=MagicMock(), logger=logger)
        # Then
        self.assertEqual(SENSOR_ADDRESS, sensor.address)

    def test_should_init_device_name(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock()
        mock_io.send_and_receive.side_effect = ['?NAME,myAtlasScientificSensor', SENSOR_INFO]
        sensor = AtlasScientificSensor(address=SENSOR_ADDRESS, io=mock_io, host=MagicMock(), logger=logger)
        # Then
        self.assertEqual('myAtlasScientificSensor', sensor.name)

    def test_should_init_device_name_undefined(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock()
        mock_io.send_and_receive.side_effect = ['?NAME,', SENSOR_INFO]
        sensor = AtlasScientificSensor(address=SENSOR_ADDRESS, io=mock_io, host=MagicMock(), logger=logger)
        # Then
        self.assertEqual('', sensor.name)

    def test_should_init_device_module(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock()
        mock_io.send_and_receive.side_effect = [SENSOR_NAME, '?I,TEST,1.0']
        sensor = AtlasScientificSensor(address=SENSOR_ADDRESS, io=mock_io, host=MagicMock(), logger=logger)
        # Then
        self.assertEqual('TEST', sensor.module)

    def test_should_init_device_version(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock()
        mock_io.send_and_receive.side_effect = [SENSOR_NAME, '?I,TEST,4.2']
        sensor = AtlasScientificSensor(address=SENSOR_ADDRESS, io=mock_io, host=MagicMock(), logger=logger)
        # Then
        self.assertEqual('4.2', sensor.version)

    def test_should_get_reading_from_io(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive.side_effect = [SENSOR_NAME, SENSOR_INFO, SENSOR_READING]
        sensor = AtlasScientificSensor(address=SENSOR_ADDRESS, io=mock_io, host=MagicMock(), logger=logger)
        # When
        sensor.read()
        # Then
        mock_io.send_and_receive.assert_called_with(SENSOR_ADDRESS, 'R', ANY)

    def test_should_get_reading_value(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive.side_effect = [SENSOR_NAME, SENSOR_INFO, '28.306']
        sensor = AtlasScientificSensor(address=SENSOR_ADDRESS, io=mock_io, host=MagicMock(), logger=logger)
        # When
        reading = sensor.read()
        # Then
        self.assertEqual('28.306', reading.value)

    def test_should_get_reading_value_for_humidity(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive.side_effect = [SENSOR_NAME, SENSOR_INFO, '97.36,31.60,Dew,31.13']
        sensor = AtlasScientificSensor(address=SENSOR_ADDRESS, io=mock_io, host=MagicMock(), logger=logger)
        # When
        reading = sensor.read()
        # Then
        self.assertEqual('97.36,31.60,Dew,31.13', reading.value)

    def test_should_return_json_for_humidity(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock()
        mock_io.send_and_receive.side_effect = ['?NAME,myAtlasScientificSensor', '?I,HUM,1.0', '97.36,31.60,Dew,31.13']
        sensor = AtlasScientificSensor(address=SENSOR_ADDRESS, io=mock_io, host=MagicMock(), logger=logger)
        sensor.read()
        # When
        json = sensor.to_json()
        print(json)
        # Then
        self.assertEqual(SENSOR_ADDRESS, json['address'])
        self.assertEqual('myAtlasScientificSensor', json['name'])
        self.assertEqual('HUM', json['module'])
        self.assertEqual('1.0', json['version'])
        self.assertEqual('97.36,31.60,Dew,31.13', json['reading']['value'])


if __name__ == '__main__':
    unittest.main()
