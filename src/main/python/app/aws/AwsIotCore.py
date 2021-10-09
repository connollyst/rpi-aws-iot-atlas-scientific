import time

from awscrt import io, mqtt
from awsiot import mqtt_connection_builder


class AwsIotCore:

    def __init__(self,
                 endpoint,
                 cert_filepath='certs/device.pem.crt',
                 ca_filepath='certs/Amazon-root-CA-1.pem',
                 private_key_filepath='certs/private.pem.key',
                 logger=None):
        self._logger = logger
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
            clean_session=True,
            keep_alive_secs=30,
        )
        self._logger.info("Connecting to {} with client ID '{}'...".format(self.endpoint, client_id))
        connect_future = mqtt_connection.connect()
        connect_future.result()
        self._connection = mqtt_connection
        self._logger.debug("Connected to AWS.")

    def write(self, topic, json):
        self._logger.info("Sending to '{}': {}".format(topic, json))
        self._connection.publish(topic=topic, payload=json, qos=mqtt.QoS.AT_LEAST_ONCE)
        time.sleep(1)

    def disconnect(self):
        self._logger.debug("Disconnecting from AWS...")
        disconnect_future = self._connection.disconnect()
        disconnect_future.result()
        self._logger.debug("Disconnected from AWS.")
