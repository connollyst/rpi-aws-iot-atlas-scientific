#!/usr/bin/python

from atlas.AtlasScientificHub import AtlasScientificHub
from aws.AwsIotCore import AwsIotCore


def main():
    reader = AtlasScientificHub()
    writer = AwsIotCore()
    reading = reader.read()
    writer.write(reading)
        
                    
if __name__ == '__main__':
    main()
