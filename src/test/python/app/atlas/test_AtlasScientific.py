import unittest
from unittest.mock import MagicMock

from src.main.python.app.Logger import get_logger
from src.main.python.app.atlas.AtlasScientific import AtlasScientific


class test_AtlasScientific(unittest.TestCase):

    def test_should_initialize_I2C(self):
        # Given
        logger = get_logger(__name__)
        print(logger)
        hub = AtlasScientific(host=MagicMock(), logger=logger)

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
