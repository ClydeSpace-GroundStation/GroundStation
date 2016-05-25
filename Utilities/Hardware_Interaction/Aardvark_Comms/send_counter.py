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

# create the data to send
# ramp = range(number_bytes)
# asm = [0x1A, 0xCF, 0xFC, 0x1D]
# message = (map(ord,"Testing the CMC radio. "))
# data = ramp + asm + message + asm + message + asm + message
# data_out = array('B',data)

data_out = array('B',[0x03, 0x1A, 0xCF, 0x02, 0x01, 0x02, 0x03, 0x06])

# read the ready signals
aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x1A & 0xff]))
(count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, 1)
if (data_in[0] == 0):
    print "Rx not ready, Tx not ready"
    TR = 0
elif (data_in[0] == 1):
    print "Rx not ready, Tx ready"
    TR = 1
elif (data_in[0] == 2):
    print "Rx ready, Tx not ready"
    TR = 0
elif (data_in[0] == 3):
    print "Rx ready, Tx ready"
    TR = 1
else:
    print "Error: ", data_in[0]


if (TR == 1):

    # point to tx data register
    # count = aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, array('B',[0x03, 0x03]))
    # count = aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, array('B',[0x03]))

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
    else:
        print count, " bytes written"


    # read the rx signal strength
    aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x36 & 0xff]))
    (count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, 2)
    x = (256*data_in[0] + data_in[1])*(3.0/4096.0)
    power = 32.5 - 68838*pow(x,6) + 228000*pow(x,5) - 218934*pow(x,3) - 85741*pow(x,2) + 17660*x - 1511.8
    print "Tx forward power: ", power, "dBm"

    # read the rx signal strength
    aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x38 & 0xff]))
    (count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, 2)
    x = (256*data_in[0] + data_in[1])*(3.0/4096.0)
    power = 32.5 - 68838*pow(x,6) + 228000*pow(x,5) - 218934*pow(x,3) - 85741*pow(x,2) + 17660*x - 1511.8
    print "Tx reverse power: ", power, "dBm"


    # close the device
    aa_close(handle)
