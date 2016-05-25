"""
    Create a GNURadio readable text file of the first transmitted BAL frame
"""
import array
import scipy
import numpy
import matplotlib.pyplot as plt


# frame as a long hex string stream
frame_string = '1acffc1d'
frame_data = frame_string.decode("hex")

# create byte array
array.array('B', frame_data)
map(ord, frame_data)


print str(range(8))

# frame_data + range(256)
# frame_data.append(range(256))
# frame_data.append(range(256))
# frame_data.append(range(256))
# frame_data.append(range(256))

# plt.plot(frame_data)
# plt.show()

# create output file
file = open("ramp.bit","w")
file.write(frame_data)
