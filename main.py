#!/usr/bin/python

from atlas.AtlasScientific import AtlasScientific


def main():
    reader = AtlasScientific()
    # writer = AwsIotCore()
    reading = reader.read_all()
    print(reading)
    # writer.write(reading)


if __name__ == '__main__':
    main()
