import sys
import time
from aardvark_py import *

def send_bytes(handle, addr, bytes):

    time_delay = 0.01 # seconds

    count = aa_i2c_write(handle, addr, AA_I2C_NO_FLAGS, bytes)
    time.sleep(time_delay)

    # check how succesful the operation was
    if (count < 0):
        print "error: %s" % aa_status_string(count)
    elif (count == 0):
        print "error: no bytes written"
        print "  are you sure you have the right slave address?"
    elif (count != len(bytes)):
        print "error: only a partial number of bytes written"
        print "  (%d) instead of full (%d)" % (count, num_write)
