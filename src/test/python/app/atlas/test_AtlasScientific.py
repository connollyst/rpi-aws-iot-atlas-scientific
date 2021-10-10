import unittest
from unittest.mock import MagicMock

from src.main.python.app.Logger import get_logger
from src.main.python.app.atlas.AtlasScientific import AtlasScientific

logger = get_logger('unittest')


class test_AtlasScientific(unittest.TestCase):

    def test_should_find_devices_on_init(self):
        # Given
        io = MagicMock()
        # When
        AtlasScientific(io=io, host=MagicMock(), logger=logger)
        # Then
        io.find_devices.assert_called()

    def test_close_devices_on_stop(self):
        # Given
        io = MagicMock()
        tentacle = AtlasScientific(io=io, host=MagicMock(), logger=logger)
        # When
        tentacle.stop()
        # Then
        io.close.assert_called()


if __name__ == '__main__':
    unittest.main()
