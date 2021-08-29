import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from atlas.AtlasScientificSensor import AtlasScientificSensor
from i2c.I2C import I2C

def add(x,y):
    return x + y

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(add(3,4), 7)


class Test2(unittest.TestCase):
    def test_sensor_name(self):
        sensor = AtlasScientificSensor('testName', 'testType', 'testAddress', MagicMock())
        self.assertEqual(sensor.name, 'testName')
    
    def test_sensor_type(self):
        sensor = AtlasScientificSensor('testName', 'testType', 'testAddress', MagicMock())
        self.assertEqual(sensor.type, 'testType')
    
    def test_sensor_address(self):
        sensor = AtlasScientificSensor('testName', 'testType', 'testAddress', MagicMock())
        self.assertEqual(sensor.address, 'testAddress')
    
    def test_sensor_info(self):
        sensor = AtlasScientificSensor('testName', 'testType', 'testAddress', MagicMock())
        self.assertEqual(sensor.info(), 'testType testAddress testName')
    
    def test_sensor_read_queries_i2c(self):
        sensor = AtlasScientificSensor('testName', 'testType', 'testAddress', MagicMock())
        sensor.read()
        sensor._i2c.query.assert_called_with('R')


if __name__ == '__main__':
    unittest.main()
