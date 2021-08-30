#!/usr/bin/python

from atlas.AtlasScientific import AtlasScientific
from aws.AwsIotCore import AwsIotCore

AWS_ENDPOINT = 'a12dev37b8fhwi-ats.iot.us-west-2.amazonaws.com'


def main():
    sensors = AtlasScientific().get_all_sensors()
    writer = AwsIotCore(AWS_ENDPOINT)
    for sensor in sensors:
        reading = sensor.take_reading()
        print(reading)
        # writer.write(reading)


if __name__ == '__main__':
    main()
