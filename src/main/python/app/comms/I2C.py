import fcntl
import io
import sys
import time

from .IO import IO


class I2C(IO):
    I2C_SLAVE = 0x703
    DEFAULT_ADDRESS = 98
    # the default bus for I2C on the newer Raspberry Pis, 
    # certain older boards use bus 0
    DEFAULT_BUS = 1

    def __init__(self, bus=None):
        self.bus = bus or self.DEFAULT_BUS
        print('Initializing I2C interface.')
        self.file_read = io.open(file="/dev/i2c-{}".format(self.bus),
                                 mode="rb",
                                 buffering=0)
        self.file_write = io.open(file="/dev/i2c-{}".format(self.bus),
                                  mode="wb",
                                  buffering=0)
        self.__set_i2c_address(self.DEFAULT_ADDRESS)

    def close(self):
        self.file_read.close()
        self.file_write.close()

    def send_and_receive(self, address, message, wait=0):
        """
        Write a command, wait the appropriate timeout, & read the response.
        """
        self.__set_i2c_address(address)
        self.__write(message)
        time.sleep(wait)
        response, success = self.__read()
        if not success:
            print('Retrying..')
            # TODO smarter retries please
            time.sleep(wait)
            response, success = self.__read()
            if not success:
                response = 'Err'
                # raise IOError('Failed to receive I2C response at address {} with command {}!'.format(address, message))
        return response

    def send(self, address, message):
        """
        Write a command and return immediately.
        """
        self.__set_i2c_address(address)
        self.__write(message)

    def receive(self, address) -> str:
        self.__set_i2c_address(address)
        response, success = self.__read()
        # TODO if unsuccessful, retry
        return response

    def find_all_i2c_devices(self):
        i2c_devices = []
        for i2c_address in range(0, 128):
            try:
                self.__ping(i2c_address)
                i2c_devices.append(i2c_address)
            except IOError:
                pass
        return i2c_devices

    def __ping(self, address):
        self.__set_i2c_address(address)
        self.__read(1)

    def __set_i2c_address(self, address):
        """
        set the I2C communications to the slave specified by the address
        the commands for I2C dev using the ioctl functions are specified in
        the i2c-dev.h file from i2c-tools
        """
        fcntl.ioctl(self.file_read, self.I2C_SLAVE, address)
        fcntl.ioctl(self.file_write, self.I2C_SLAVE, address)

    def __write(self, command):
        """
        Appends the null character and sends the string over I2C
        """
        command += "\00"
        self.file_write.write(command.encode('latin-1'))

    def __read(self, bytes=31):
        """
        Reads a specified number of bytes from I2C, then parses and displays the result
        """
        raw_data = self.file_read.read(bytes)
        response = self.__get_response(raw_data)
        is_valid, error_code = self.__is_response_valid(response)
        if is_valid:
            char_list = self.__handle_raspi_glitch(response[1:])
            return str(''.join(char_list)), is_valid
        else:
            return error_code, is_valid

    def __get_response(self, raw_data):
        if self.__app_using_python_two():
            response = [i for i in raw_data if i != '\x00']
        else:
            response = raw_data
        return response

    def __is_response_valid(self, response):
        valid = True
        error_code = None
        if len(response) > 0:
            if self.__app_using_python_two():
                error_code = str(ord(response[0]))
            else:
                error_code = str(response[0])
            if error_code != '1':
                valid = False
        return valid, error_code

    def __handle_raspi_glitch(self, response):
        """
        Change MSB to 0 for all received characters except the first
        and get a list of characters
        NOTE: having to change the MSB to 0 is a glitch in the raspberry pi,
        and you shouldn't have to do this!
        """
        if self.__app_using_python_two():
            return list(map(lambda x: chr(ord(x) & ~0x80), list(response)))
        else:
            return list(map(lambda x: chr(x & ~0x80), list(response)))

    def __app_using_python_two(self):
        return sys.version_info[0] < 3
