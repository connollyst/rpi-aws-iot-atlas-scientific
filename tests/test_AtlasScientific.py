import unittest
from unittest.mock import MagicMock, Mock

from atlas.AtlasScientific import AtlasScientific


class test_main(unittest.TestCase):

    def test_list(self):
        # Given
        hub = AtlasScientific(i2c=MagicMock())
        # When
        hub.list()
        # Then
        hub._i2c.list.assert_called()

    def test_read_calls_list(self):
        # Given
        hub = AtlasScientific(i2c=MagicMock())
        # When
        hub.read()
        # Then
        hub._i2c.list.assert_called()

    def test_read_calls_list2(self):
        # Given
        mock_i2c = MagicMock()
        mock_i2c.list = Mock(return_value=[42, 137])
        hub = AtlasScientific(i2c=mock_i2c)

        # When
        hub.list()
        # Then
        hub._i2c.list.assert_called()


if __name__ == '__main__':
    unittest.main()
