#!/usr/bin/python

from datetime import datetime


class AtlasScientificSensorReading:

    def __init__(self, value: str):
        self._value = value
        self._timestamp = datetime.now()

    @property
    def value(self):
        return self._value

    @property
    def timestamp(self):
        return self._timestamp

    def __str__(self):
        return self.value
