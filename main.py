#!/usr/bin/python

from main.python.atlas.AtlasI2C import AtlasI2C
from main.python.aws.AwsIotCore import AwsIotCore
from main.python.i2c.I2C import I2C


def main():
    reader = AtlasI2C()
    writer = AwsIotCore()
    reading = reader.read()
    writer.write(reading)
        
                    
if __name__ == '__main__':
    main()
