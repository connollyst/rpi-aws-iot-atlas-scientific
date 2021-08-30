#!/usr/bin/python

import json
import time

from awscrt import io, mqtt
from awsiot import mqtt_connection_builder


class AwsIotCore:

    def __init__(self,
                 endpoint,
                 cert_filepath='/home/pi/aws/certs/device.pem.crt',
                 ca_filepath='/home/pi/aws/certs/Amazon-root-CA-1.pem',
                 private_key_filepath='/home/pi/aws/certs/private.pem.key'):
        self._endpoint = endpoint
        self._cert_filepath = cert_filepath
        self._ca_filepath = ca_filepath
        self._private_key_filepath = private_key_filepath
        self._connection = None

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def cert_filepath(self):
        return self._cert_filepath

    @property
    def ca_filepath(self):
        return self._ca_filepath

    @property
    def private_key_filepath(self):
        return self._private_key_filepath

    def connect(self, client_id):
        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
        mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=self.endpoint,
            client_bootstrap=client_bootstrap,
            cert_filepath=self.cert_filepath,
            pri_key_filepath=self.private_key_filepath,
            ca_filepath=self.ca_filepath,
            client_id=client_id,
            clean_session=False,
            keep_alive_secs=30,
        )
        print("Connecting to {} with client ID '{}'...".format(self.endpoint, client_id))
        connect_future = mqtt_connection.connect()
        connect_future.result()
        self._connection = mqtt_connection
        print("Connected!")

    def write(self, data):
        message = {
            'message': data
        }
        message_json = json.dumps(message).replace(r'\u0000', '')
        self._connection.publish(
            topic='atlas',
            payload=message_json,
            qos=mqtt.QoS.AT_LEAST_ONCE)
        time.sleep(1)

    def disconnect(self):
        print("Disconnecting from AWS...")
        disconnect_future = self._connection.disconnect()
        disconnect_future.result()
        print("Disconnected from AWS.")
