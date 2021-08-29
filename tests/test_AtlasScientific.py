import unittest

from atlas.AtlasScientific import AtlasScientific

class test_main(unittest.TestCase):

    def test_list(self):
        # Given
        hub = AtlasScientific()
        # TODO inject mock I2C
        # Then
        self.assertEqual(hub.list(), '???')

if __name__ == '__main__':
    unittest.main()
