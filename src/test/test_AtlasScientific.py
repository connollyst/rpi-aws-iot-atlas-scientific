import unittest
from unittest.mock import MagicMock

from src.main.atlas.AtlasScientific import AtlasScientific


class test_AtlasScientific(unittest.TestCase):

    def test_list(self):
        # Given
        hub = AtlasScientific(io=MagicMock())
        # When
        hub.get_all_sensors()
        # Then
        hub._io.list_sensors.assert_called()

    def test_close(self):
        # Given
        hub = AtlasScientific(io=MagicMock())
        # When
        hub.close()
        # Then
        hub._io.close.assert_called()


if __name__ == '__main__':
    unittest.main()
