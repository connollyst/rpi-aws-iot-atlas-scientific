#!/usr/bin/python

import io
import sys
import fcntl
import time
import copy
import string
from AtlasI2C import (
	 AtlasI2C
)

read_delay = 1

def print_devices(device_list):
    for i in device_list:
        print(" - " + i.get_device_info())


def get_devices():
    device = AtlasI2C()
    device_list = []
    for i in device.list_i2c_devices():
        print('Device #{}: {}'.format(i, device))
        device.set_i2c_address(i)
        response = device.query("I")
        moduletype = response.split(",")[1] 
        response = device.query("name,?").split(",")[1]
        device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))
    return device_list 
       
       
def main():
    try:
        device_list = get_devices()
        print_devices(device_list)
        for dev in device_list:
            dev.write("R")
        time.sleep(read_delay)
        for dev in device_list:
            print(dev.read())
            # TODO write to AWS
    except IndexError as e:
        print('Error: ' + e)
        print('Retrying..')
        main()
        
                    
if __name__ == '__main__':
    main()