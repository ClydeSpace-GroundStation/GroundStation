"""
    Script to configure the CMC for pass through transmission
"""

# import neccesary pieces
import sys
import time
from send_bytes import *
from aardvark_py import *

# aardvark settings
BUFFER_SIZE = 2048
I2C_BITRATE =  100

# device parameters
port = 0
addr = 0x28

# find all the attached devices
print "Detecting Aardvark adapters..."
(num, ports, unique_ids) = aa_find_devices_ext(16, 16)
#print num,  ports,  unique_ids

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

# set the MODEM to GMSK up and down
data_out = array('B',[0x00, 0x03])
send_bytes(handle, addr, data_out)

# set the power to 27dBm
data_out = array('B',[0x06, 0x00])
send_bytes(handle, addr, data_out)

# set the mode to transparent with no coding (use 0x0D for coding)
data_out = array('B',[0x10, 0x05])
send_bytes(handle, addr, data_out)

# set the Tx freqeuncy to 401MHz
data_out = array('B',[0x0A, 0x28])
send_bytes(handle, addr, data_out)

# point to the Tx data register
data_out = array('B',[0x03])
send_bytes(handle, addr, data_out)

# alert user to succesful configuration
print "Configuration complete"

# close the device
aa_close(handle)
