#!/usr/bin/python

import time
import json

# TODO move to another class
from awscrt import mqtt


class AtlasScientificHub:

    READ_DELAY_SECS = 1

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
