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
addr = 0x28

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

# create the data to send
data_out = array('B',[0x1A, 0xCF, 0x02, 0x01, 0x02, 0x03])

# point to ready signals register
count = aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, array('B',[0x1A, 0x1A]))

# point to tx data register
count = aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, array('B',[0x03, 0x03]))

# write the data to the bus
count = aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, data_out)

# check how succesful the operation was
if (count < 0):
    print "error: %s" % aa_status_string(count)
elif (count == 0):
    print "error: no bytes written"
    print "  are you sure you have the right slave address?"
elif (count != len(data_out)):
    print "error: only a partial number of bytes written"
    print "  (%d) instead of full (%d)" % (count, len(data_out))

# close the device
aa_close(handle)
