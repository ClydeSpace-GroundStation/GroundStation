"""
    Read the input to the RS encoder, encoded stream and decoded stream.
    Compare to validate the performance of the RS encoder/decoder.
"""

import scipy
import binascii
import array
import numpy as np
import matplotlib.pyplot as plt

# print output as hex
np.set_printoptions(formatter={'int':hex})

# read in the data streams
input = np.array(scipy.fromfile(open("/home/thomasp/Groundstation/CCSDS/Reed Solomon Tests/RS Test 1/input.bin"), dtype=scipy.uint8))
encoded = np.array(scipy.fromfile(open("/home/thomasp/Groundstation/CCSDS/Reed Solomon Tests/RS Test 1/encoded.bin"), dtype=scipy.uint8))
output = np.array(scipy.fromfile(open("/home/thomasp/Groundstation/CCSDS/Reed Solomon Tests/RS Test 1/output.bin"), dtype=scipy.uint8))

input = input[:-1]

print "Length input: ", len(input)

print "Input: ", input[:32]
print "Encoded: ", encoded[:32]
print "Output: ", output[:32]

print "Output equals the input: ", input == output


plt.plot(input)
#plt.plot(encoded)
plt.plot(output)
plt.show()
