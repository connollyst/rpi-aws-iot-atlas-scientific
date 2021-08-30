import json
import unittest
from unittest.mock import ANY
from unittest.mock import MagicMock, Mock

from atlas.AtlasScientificSensor import AtlasScientificSensor


class TestAtlasScientificSensor(unittest.TestCase):
    SENSOR_ADDRESS = 'testSensorAddress'

    def test_sensor_address(self):
        # Given
        sensor = AtlasScientificSensor(self.SENSOR_ADDRESS, MagicMock())
        # Then
        self.assertEqual(self.SENSOR_ADDRESS, sensor.address)

    def test_sensor_name(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock(return_value='?NAME,myAtlasScientificSensor')
        sensor = AtlasScientificSensor(self.SENSOR_ADDRESS, mock_io)
        # Then
        self.assertEqual('myAtlasScientificSensor', sensor.name)

    def test_sensor_name_undefined(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock(return_value='?NAME,')
        sensor = AtlasScientificSensor(self.SENSOR_ADDRESS, mock_io)
        # Then
        self.assertEqual('', sensor.name)

    def test_sensor_name_error(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock(return_value='Err')
        sensor = AtlasScientificSensor(self.SENSOR_ADDRESS, mock_io)
        # Then
        self.assertEqual('Err', sensor.name)

    def test_sensor_module(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock(return_value='?I,RTD,2.11')
        sensor = AtlasScientificSensor(self.SENSOR_ADDRESS, mock_io)
        # Then
        self.assertEqual('RTD', sensor.module)

    def test_sensor_module_error(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock(return_value='Err')
        sensor = AtlasScientificSensor(self.SENSOR_ADDRESS, mock_io)
        # Then
        self.assertEqual('Err', sensor.module)

    def test_sensor_version(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock(return_value='?I,RTD,2.11')
        sensor = AtlasScientificSensor(self.SENSOR_ADDRESS, mock_io)
        # Then
        self.assertEqual('2.11', sensor.version)

    def test_sensor_version_error(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock(return_value='Err')
        sensor = AtlasScientificSensor(self.SENSOR_ADDRESS, mock_io)
        # Then
        self.assertEqual('Err', sensor.version)

    def test_sensor_read_queries_io(self):
        # Given
        mock_io = MagicMock()
        sensor = AtlasScientificSensor(self.SENSOR_ADDRESS, mock_io)
        # When
        sensor.take_reading()
        # Then
        mock_io.send_and_receive.assert_called_with(self.SENSOR_ADDRESS, 'R', ANY)

    def test_sensor_read_value(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock(return_value='28.306')
        sensor = AtlasScientificSensor(self.SENSOR_ADDRESS, mock_io)
        # When
        reading = sensor.take_reading()
        # Then
        self.assertEqual('28.306', reading.value)

    def test_sensor_read_value_humidity(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock(return_value='97.36,31.60,Dew,31.13')
        sensor = AtlasScientificSensor(self.SENSOR_ADDRESS, mock_io)
        # When
        reading = sensor.take_reading()
        # Then
        self.assertEqual('97.36,31.60,Dew,31.13', reading.value)

    def test_sensor_read_value_error(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock(return_value='Err')
        sensor = AtlasScientificSensor(self.SENSOR_ADDRESS, mock_io)
        # When
        reading = sensor.take_reading()
        # Then
        self.assertEqual('Err', reading.value)

    def test_sensor_json(self):
        # Given
        mock_io = MagicMock()
        mock_io.send_and_receive = Mock()
        mock_io.send_and_receive.side_effect = ['?NAME,myAtlasScientificSensor', '?I,HUM,1.0', '97.36,31.60,Dew,31.13']
        sensor = AtlasScientificSensor(self.SENSOR_ADDRESS, mock_io)
        # When
        output = sensor.to_json()
        print(output)
        # Then
        data = json.loads(output)
        self.assertEqual(self.SENSOR_ADDRESS, data['address'])
        self.assertEqual('myAtlasScientificSensor', data['name'])
        self.assertEqual('HUM', data['module'])
        self.assertEqual('1.0', data['version'])
        self.assertEqual('97.36,31.60,Dew,31.13', data['reading']['value'])


if __name__ == '__main__':
    unittest.main()
