#!/usr/bin/python

import time
import json
import copy

# TODO move to another class
from awscrt import mqtt


class AtlasScientificHub:

    READ_DELAY_SECS = 1

    def list_i2c_devices(self):
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

    def read_sensors(self, mqtt_connection):
        try:
            device_list = self.get_sensors()
            self.print_sensors(device_list)
            for dev in device_list:
                dev.write("R")
            time.sleep(self.READ_DELAY_SECS)
            for dev in device_list:
                message = dev.read()
                print(message)
                message = {
                    'message': message
                }
                message_json = json.dumps(message).replace(r'\u0000', '')
                mqtt_connection.publish(
                    topic='atlas',
                    payload=message_json,
                    qos=mqtt.QoS.AT_LEAST_ONCE)
                time.sleep(1)
        except IndexError as e:
            print('Error:')
            print(e)
            print('Retrying..')
            self.read_sensors(mqtt_connection)
