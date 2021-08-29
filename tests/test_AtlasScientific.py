import unittest

from unittest.mock import MagicMock
from atlas.AtlasScientific import AtlasScientific

class test_main(unittest.TestCase):

    def test_list(self):
        # Given
        hub = AtlasScientific(i2c = MagicMock())
        # When
        hub.list()
        # Then
        hub._i2c.list.assert_called()

    def test_read_calls_list(self):
        # Given
        hub = AtlasScientific(i2c = MagicMock())
        # When
        hub.read()
        # Then
        hub._i2c.list.assert_called()

if __name__ == '__main__':
    unittest.main()
