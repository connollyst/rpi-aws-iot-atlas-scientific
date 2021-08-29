#!/usr/bin/python

class AtlasScientificSensorReading:

    def __init__(self, value:str):
        print('Creating new sensor reading!')
        self._value = value

    @property
    def value(self:str):
        return self._value
