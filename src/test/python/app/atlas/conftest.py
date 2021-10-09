import sys

import fake_rpi


def pytest_configure(config):
    _stub_i2c_interface()


def _stub_i2c_interface():
    sys.modules['smbus'] = fake_rpi.smbus
