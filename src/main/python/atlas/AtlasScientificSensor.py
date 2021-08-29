#!/usr/bin/python

import sys
import time

class AtlasScientificSensor:

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def moduletype(self):
        return self._module

    def get_device_info(self):
        if(self._name == ""):
            return self._module + " " + str(self.address)
        else:
            return self._module + " " + str(self.address) + " " + self._name

    def query(self, command):
        '''
        write a command to the board, wait the correct timeout, 
        and read the response
        '''
        self.write(command)
        current_timeout = self.get_command_timeout(command=command)
        if not current_timeout:
            return "sleep mode"
        else:
            time.sleep(current_timeout)
            return self.read()

    def write(self, cmd):
        '''
        appends the null character and sends the string over I2C
        '''
        cmd += "\00"
        self.file_write.write(cmd.encode('latin-1'))

    def read(self, num_of_bytes=31):
        '''
        reads a specified number of bytes from I2C, then parses and displays the result
        '''
        raw_data = self.file_read.read(num_of_bytes)
        response = self.get_response(raw_data=raw_data)
        # print(response)
        is_valid, error_code = self.response_valid(response=response)

        if is_valid:
            char_list = self.handle_raspi_glitch(response[1:])
            result = "Success " + self.get_device_info() + ": " + str(''.join(char_list))
            #result = "Success: " +  str(''.join(char_list))
        else:
            result = "Error " + self.get_device_info() + ": " + error_code
        return result

    def get_response(self, raw_data):
        if self.app_using_python_two():
            response = [i for i in raw_data if i != '\x00']
        else:
            response = raw_data
        return response

    def response_valid(self, response):
        valid = True
        error_code = None
        if(len(response) > 0):
            if self.app_using_python_two():
                error_code = str(ord(response[0]))
            else:
                error_code = str(response[0])
            if error_code != '1':  # 1:
                valid = False
        return valid, error_code

    def app_using_python_two(self):
        return sys.version_info[0] < 3

    def close(self):
        self.file_read.close()
        self.file_write.close()
