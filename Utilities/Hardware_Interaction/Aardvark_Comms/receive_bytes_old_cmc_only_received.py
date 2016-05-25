"""
    Script to send a stream of bytes as which increment in a counter over
    I2C
"""

# import neccesary pieces
import sys
from aardvark_py import *
import time

# aardvark settings
BUFFER_SIZE =   2048
I2C_BITRATE =   100
BUS_TIMEOUT =   150  # ms

# device parameters
port = 0
addr = 0x25

# data settings
number_bytes = 64

# find all the attached devices
print "Detecting Aardvark adapters..."
(num, ports, unique_ids) = aa_find_devices_ext(16, 16)
print num,  ports,  unique_ids

# connect to the aardvark
handle = aa_open(ports[0])
if (handle <= 0):
    print "Unable to open Aardvark device on port %d" % port
    print "Error code = %d" % handle
    sys.exit()

# ensure that the I2C subsystem is enabled
aa_configure(handle, AA_CONFIG_SPI_I2C)

# enable the I2C bus pullup resistors
aa_i2c_pullup(handle, AA_I2C_PULLUP_BOTH)

# set the bitrate
bitrate = aa_i2c_bitrate(handle, I2C_BITRATE)

# Set the bus lock timeout
bus_timeout = aa_i2c_bus_timeout(handle, BUS_TIMEOUT)

# set the radio GMSK 9k6 up and down (mode 3)
aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, array('B', [0x00 & 0xff, 0x03]))
aa_sleep_ms(10)


# read back the config
aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x00 & 0xff]))
(count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, 1)
print "Config mode: ", data_in[0]

# set the radio rx frequency offset to 0d400 => 145MHz
aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, array('B', [0x07 & 0xff, 0x01, 0x90]))
# aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, array('B', [0x07 & 0xff, 0x00, 0x00]))
aa_sleep_ms(10)


# read back the freq
aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x07 & 0xff]))
(count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, 2)
print "Rx freq: ", 12.5*(256*data_in[0] + data_in[1])/1000 + 140 ,"MHz"

# set the radio tx frequency offset to 0d40 => 401MHz
aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, array('B', [0x09 & 0xff, 0x00, 0x28]))
aa_sleep_ms(10)

# enable debug leds
aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, array('B', [0x0D & 0xff, 0x07]))

# set mode - AX.25 mode, SCRAMRX on, SCRAMTX on, transparent off
aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, array('B', [0x10 & 0xff, 0x06]))



while(1):


    # read the ready signals
    aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x1A & 0xff]))
    (count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, 1)
    if (data_in[0] == 0):
        RR = 0
    elif (data_in[0] == 1):
        RR = 0
    elif (data_in[0] == 2):
        RR = 1
    elif (data_in[0] == 3):
        RR = 1


    # there is some data to read
    if(RR == 1):

        # read how many bytes are available
        aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x1B & 0xff]))
        (count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, 2)
        numb_bytes = 256*data_in[0] + data_in[1]
        print "Number of bytes available: ", numb_bytes

        print "Data received:"
        aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x1D & 0xff]))
        (count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, numb_bytes)
        # print format(data_in, '02x')
        print ' '.join('{:02x}'.format(x) for x in data_in)

    time.sleep(2)


# close the device
aa_close(handle)
