import unittest
from unittest.mock import MagicMock, Mock

from atlas.AtlasScientificSensor import AtlasScientificSensor


class TestAtlasScientificSensor(unittest.TestCase):
    def test_sensor_name(self):
        # Given
        sensor = AtlasScientificSensor('testName', 'testType', 'testAddress', MagicMock())
        # Then
        self.assertEqual(sensor.name, 'testName')

    def test_sensor_type(self):
        # Given
        sensor = AtlasScientificSensor('testName', 'testType', 'testAddress', MagicMock())
        # Then
        self.assertEqual(sensor.type, 'testType')

    def test_sensor_address(self):
        # Given
        sensor = AtlasScientificSensor('testName', 'testType', 'testAddress', MagicMock())
        # Then
        self.assertEqual(sensor.address, 'testAddress')

    def test_sensor_info(self):
        # Given
        sensor = AtlasScientificSensor('testName', 'testType', 'testAddress', MagicMock())
        # Then
        self.assertEqual(sensor.info(), 'testType testAddress testName')

    def test_sensor_read_queries_i2c(self):
        # Given
        sensor = AtlasScientificSensor('testName', 'testType', 'testAddress', MagicMock())
        # When
        sensor.read()
        # Then
        sensor._i2c.query.assert_called_with('R')

    def test_sensor_read_value(self):
        # Given
        mockI2C = MagicMock()
        mockI2C.query = Mock(return_value='Hello World!')
        sensor = AtlasScientificSensor('testName', 'testType', 'testAddress', mockI2C)
        # When
        reading = sensor.read()
        # Then
        self.assertEqual(reading.value, 'Hello World!')


if __name__ == '__main__':
    unittest.main()
