#!/usr/bin/python

import time
import copy

class AtlasScientific:

    READ_DELAY_SECS = 1

    def list(self):
        '''
        save the current address so we can restore it after
        '''
        prev_addr = copy.deepcopy(self._address)
        i2c_devices = []
        for i in range(0, 128):
            try:
                self.set_i2c_address(i)
                self.read(1)
                i2c_devices.append(i)
            except IOError:
                pass
        # restore the address we were using
        self.set_i2c_address(prev_addr)
        return i2c_devices

    def read(self):
        try:
            device_list = self.get_sensors()
            self.print_sensors(device_list)
            for dev in device_list:
                dev.write("R")
            time.sleep(self.READ_DELAY_SECS)
            for dev in device_list:
                message = dev.read()
                print(message)
                return ...
        except IndexError as e:
            print('Error:')
            print(e)
            print('Retrying..')
            self.read()
