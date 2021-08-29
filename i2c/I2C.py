#!/usr/bin/python

import fcntl
import io
import sys
import time


class I2C:
    DEFAULT_ADDRESS = 98
    # the default bus for I2C on the newer Raspberry Pis, 
    # certain older boards use bus 0
    DEFAULT_BUS = 1

    def __init__(self, bus=None):
        '''
        '''
        self.bus = bus or self.DEFAULT_BUS
        print('Initializing I2C interface.')
        self.file_read = io.open(file="/dev/i2c-{}".format(self.bus),
                                 mode="rb",
                                 buffering=0)
        self.file_write = io.open(file="/dev/i2c-{}".format(self.bus),
                                  mode="wb",
                                  buffering=0)
        self.set_i2c_address(self.DEFAULT_ADDRESS)

    def ping(self, address):
        self.set_i2c_address(address)
        self.read(1)

    def set_i2c_address(self, address):
        '''
        set the I2C communications to the slave specified by the address
        the commands for I2C dev using the ioctl functions are specified in
        the i2c-dev.h file from i2c-tools
        '''
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.file_read, I2C_SLAVE, address)
        fcntl.ioctl(self.file_write, I2C_SLAVE, address)
        self._address = address

    def query(self, command) -> str:
        '''
        Write a command, wait the appropriate timeout, & read the response.
        '''
        self.__write(command)
        time.sleep(self.__get_command_timeout(command))
        return self.__read()

    def __write(self, command):
        '''
        Appends the null character and sends the string over I2C
        '''
        command += "\00"
        self.file_write.write(command.encode('latin-1'))

    def __get_command_timeout(command):
        return 1  # TODO replace

    def __read(self, bytes=31):
        '''
        Reads a specified number of bytes from I2C, then parses and displays the result
        '''
        raw_data = self.file_read.read(bytes)
        response = self.__get_response(raw_data=raw_data)
        print(response)
        is_valid, error_code = self.__is_response_valid(response=response)
        if is_valid:
            char_list = self.handle_raspi_glitch(response[1:])
            result = "Success " + self.info() + ": " + str(''.join(char_list))
        else:
            result = "Error " + self.info() + ": " + error_code
        return result

    def __handle_raspi_glitch(self, response):
        '''
        Change MSB to 0 for all received characters except the first 
        and get a list of characters
        NOTE: having to change the MSB to 0 is a glitch in the raspberry pi, 
        and you shouldn't have to do this!
        '''
        if self.app_using_python_two():
            return list(map(lambda x: chr(ord(x) & ~0x80), list(response)))
        else:
            return list(map(lambda x: chr(x & ~0x80), list(response)))

    def __get_command_timeout(self, command):
        timeout = None
        if command.upper().startswith(self.LONG_TIMEOUT_COMMANDS):
            timeout = self._long_timeout
        elif not command.upper().startswith(self.SLEEP_COMMANDS):
            timeout = self.short_timeout
        return timeout

    def __is_response_valid(self, response):
        valid = True
        error_code = None
        if (len(response) > 0):
            if self.__app_using_python_two():
                error_code = str(ord(response[0]))
            else:
                error_code = str(response[0])
            if error_code != '1':
                valid = False
        return valid, error_code

    def __app_using_python_two(self):
        return sys.version_info[0] < 3

    def close(self):
        self.file_read.close()
        self.file_write.close()
