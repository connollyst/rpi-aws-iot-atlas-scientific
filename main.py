#!/usr/bin/python

from uuid import uuid4

from atlas.AtlasScientific import AtlasScientific
from aws.AwsIotCore import AwsIotCore

AWS_ENDPOINT = 'a12dev37b8fhwi-ats.iot.us-west-2.amazonaws.com'


def main():
    atlas = AtlasScientific()
    sensors = atlas.get_all_sensors()
    writer = AwsIotCore(AWS_ENDPOINT)
    writer.connect("test-" + str(uuid4()))
    for sensor in sensors:
        reading = sensor.take_reading()
        print(reading)
        # TODO serialize sensor & reading
        writer.write(reading.value)
    writer.disconnect()
    atlas.close()


if __name__ == '__main__':
    main()
