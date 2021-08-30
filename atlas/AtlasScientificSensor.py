#!/usr/bin/python


class AtlasScientificSensor:

    def __init__(self, name, info, address):
        try:
            self._name = name.split(",")[1]
        except IndexError:
            # TODO do better than this!
            self._name = name
        try:
            self._module = info.split(",")[1]
        except IndexError:
            # TODO do better than this!
            self._module = info
        self._address = address

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def module(self):
        return self._module

    def info(self) -> str:
        if self._name == "":
            return self._module + " " + str(self.address)
        else:
            return self._module + " " + str(self.address) + " " + self._name

    def __str__(self):
        return self.info()
