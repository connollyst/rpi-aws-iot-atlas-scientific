#!/usr/bin/python

import json
import time
from uuid import uuid4

from awscrt import mqtt
from awsiot import mqtt_connection_builder

import comms
from atlas.__OfficialReference import AtlasI2C

read_delay = 1


def print_sensors(device_list):
    for dev in device_list:
        print(" - " + dev.get_device_info())


def get_sensors():
    device = AtlasI2C()
    device_list = []
    for i in device.list_i2c_devices():
        print('Device #{}: {}'.format(i, device))
        device.set_i2c_address(i)
        response = device.query("I")
        moduletype = response.split(",")[1]
        response = device.query("name,?").split(",")[1]
        device_list.append(
            AtlasI2C(address=i, moduletype=moduletype, name=response))
    return device_list


def connect_to_mqtt():
    event_loop_group = comms.EventLoopGroup(1)
    host_resolver = comms.DefaultHostResolver(event_loop_group)
    client_bootstrap = comms.ClientBootstrap(event_loop_group, host_resolver)
    endpoint = 'a12dev37b8fhwi-ats.iot.us-west-2.amazonaws.com'
    client_id = "test-" + str(uuid4())
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        client_bootstrap=client_bootstrap,
        cert_filepath='/home/pi/aws/certs/device.pem.crt',
        pri_key_filepath='/home/pi/aws/certs/private.pem.key',
        ca_filepath='/home/pi/aws/certs/Amazon-root-CA-1.pem',
        client_id=client_id,
        clean_session=False,
        keep_alive_secs=30,
    )
    print("Connecting to {} with client ID '{}'...".format(
        endpoint, client_id))
    connect_future = mqtt_connection.connect()
    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")
    return mqtt_connection


def disconnect_from_mqtt(mqtt_connection):
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")


def read_sensors(mqtt_connection):
    try:
        device_list = get_sensors()
        print_sensors(device_list)
        for dev in device_list:
            dev.write("R")
        time.sleep(read_delay)
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
        read_sensors(mqtt_connection)


def main():
    mqtt_connection = connect_to_mqtt()
    read_sensors(mqtt_connection)
    disconnect_from_mqtt(mqtt_connection)


if __name__ == '__main__':
    main()
