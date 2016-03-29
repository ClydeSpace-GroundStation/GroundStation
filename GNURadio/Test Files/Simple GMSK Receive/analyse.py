import scipy
import binascii
# import array
import sys
import numpy as np
from matplotlib.pyplot import *

# print output as hex
np.set_printoptions(formatter={'int':hex})

# read in the data streams
input = np.array(scipy.fromfile(open("/home/gs-laptop1/GroundStation/GroundStation/GNURadio/Test Files/Simple GMSK Receive/out.bin"), dtype=scipy.uint8))

plot(input)
show()

print input[840:870]


message = "Testing the CMC radio."
data = [0x1A, 0xCF, 0xFC, 0x1D] + (map(ord,message))

# plot(data)
# show()
