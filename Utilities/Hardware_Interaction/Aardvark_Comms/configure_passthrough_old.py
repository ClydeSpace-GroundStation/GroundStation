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
# addr = 0x28
addr = 0x25

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

# set the MODEM to GMSK down, AFSK up
data_out = array('B',[0x00, 0x02])
send_bytes(handle, addr, data_out)

# set the power to 27dBm
data_out = array('B',[0x06, 0x00])
send_bytes(handle, addr, data_out)

# set the mode to transparent with no coding (use 0x0D for coding)
data_out = array('B',[0x10, 0x05])
send_bytes(handle, addr, data_out)

# # set the Tx freqeuncy to 401MHz
# data_out = array('B',[0x0A, 0x28])

# set the Tx freqeuncy to 436MHz
data_out = array('B',[0x0A, 0xF0])
send_bytes(handle, addr, data_out)

# point to the Tx data register
data_out = array('B',[0x03])
send_bytes(handle, addr, data_out)

# alert user to succesful configuration
print "Configuration complete"

# read the rx frequency lock
aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x28 & 0xff]))
(count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, 1)
if (data_in[0] == 0):
    print "Rx not locked, Tx not locked"
elif (data_in[0] == 1):
    print "Rx locked, Tx not locked"
elif (data_in[0] == 2):
    print "Rx not locked, Tx locked"
elif (data_in[0] == 3):
    print "Rx locked, Tx locked"
else:
    print "Error: ", data_in[0]

# close the device
aa_close(handle)
