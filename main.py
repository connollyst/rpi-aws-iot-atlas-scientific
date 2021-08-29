#!/usr/bin/python

from atlas.AtlasScientific import AtlasScientific
from aws.AwsIotCore import AwsIotCore


def main():
    reader = AtlasScientific()
    writer = AwsIotCore()
    reading = reader.read()
    writer.write(reading)


if __name__ == '__main__':
    main()
