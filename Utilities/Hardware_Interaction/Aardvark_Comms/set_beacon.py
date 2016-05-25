"""
    Script to send a stream of bytes as which increment in a counter over
    I2C
"""

# import neccesary pieces
import sys
from aardvark_py import *

# aardvark settings
BUFFER_SIZE = 2048
I2C_BITRATE =  100

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


# point to tx data register
count = aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, array('B',[0x0B, 0x01]))

# point to tx data register
count = aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, array('B',[0x0C, 0x01]))

# point to tx data register
count = aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, array('B',[0x04, 0x01]))



# close the device
aa_close(handle)
