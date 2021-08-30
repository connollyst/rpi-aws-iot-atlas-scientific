#!/usr/bin/python

class AtlasScientificSensorReading:

    def __init__(self, value: str):
        print('Creating new sensor reading!')
        self._value = value

    @property
    def value(self):
        return self._value

    def __str__(self):
        return self.value
