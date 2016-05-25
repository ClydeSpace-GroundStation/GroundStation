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

    print "-------------------------------------------------------------------------------"

    # read the rx signal strength
    aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x2A & 0xff]))
    (count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, 2)
    print "Received signal strength: ", (256*data_in[0] + data_in[1])*(3.0/4096.0), "V"

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

    # read how many packets ave been received
    aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x23 & 0xff]))
    (count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, 2)
    print "Number of received packets: ", 256*data_in[0] + data_in[1]

    # read how many packets failed CRC
    aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x21 & 0xff]))
    (count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, 2)
    print "Number of CRC fails: ", 256*data_in[0] + data_in[1]

    # read the ready signals
    aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x1A & 0xff]))
    (count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, 1)
    if (data_in[0] == 0):
        print "Rx not ready, Tx not ready"
        RR = 0
    elif (data_in[0] == 1):
        print "Rx not ready, Tx ready"
        RR = 0
    elif (data_in[0] == 2):
        print "Rx ready, Tx not ready"
        RR = 1
    elif (data_in[0] == 3):
        print "Rx ready, Tx ready"
        RR = 1
    else:
        print "Error: ", data_in[0]

    # read how many bytes are available
    aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x1B & 0xff]))
    (count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, 2)
    numb_bytes = 256*data_in[0] + data_in[1]
    print "Number of bytes available: ", numb_bytes


    # there is some data to read
    if(RR == 1):

        print "Data received:"
        aa_i2c_write(handle, addr, AA_I2C_NO_STOP, array('B', [0x1D & 0xff]))
        (count, data_in) = aa_i2c_read(handle, addr, AA_I2C_NO_FLAGS, numb_bytes)
        print data_in

    time.sleep(2)


# close the device
aa_close(handle)
