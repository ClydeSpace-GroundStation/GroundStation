import scipy
import binascii
import array
import numpy as np
import matplotlib.pyplot as plt


## Format the reference data
# frame as a long hex string stream
ref_string = '67c6697351ff4aec29cdbaabf2fbe3467cc254f81be8e78d765a2e63339fc99a66320db73158a35a255d051758e95ed4abb2cdc69bb454110e827441213ddc8770e93ea141e1fc673e017e97eadc6b968f385c2aecb03bfb32af3c54ec18db5c021afe43fbfaaa3afb29d1e6053c7c9475d8be6189f95cbba8990f95b1ebf1b305eff700e9a13ae5ca0bcbd0484764bd1f231ea81c7b64c514735ac55e4b79633b706424119e09dcaad4acf21b10af3b33cde3504847155cbb6f2219ba9b7df50be11a1c7f23f829f8a41b13b5ca4ee8983238e0794d3d34bc5f4e77facb6c05ac86212baa1a55a2be70b5733b045cd33694b3afe2f0e49e4f321549fd824ea90870d4b28a2954489a0abcd50e18a844ac5bf38e4cd72d9b0942e506c433afcda3847f2dadd47647de321cec4ac430f62023856cfbb20704f4ec0bb920ba86c33e05f1ecd96733b79950a3e314d3d934f75ea0f210a8f6059401beb4bc4478fa4969e623d01ada696a7e4c7e5125b34884533a94fb319990325744ee9bbce9e525cf08f5e9e25e5360aad2b2d085fa54d835e8d466826498d9a8877565705a8a3f62802944de7ca5894e5759d351adac869580ec17e485f18c0c66f17cc07cbb22fce466da610b63af62bc83b4692f3affaf271693ac071fb86d11342d8def4f89d4b66335c1c7e4248367d8ed9612ec453902d8e50af89d7709d1a596c1f41f95aa82ca6c49ae90cd1668baac7aa6f2b4a8ca99b2c2372acb08cf61c9c3805e6e0328da4cd76a19edd2d3994c798b0022569ad418d1fee4d9cd45a391c601ffc92ad91501432fee150287617c13629e69fc7281cd7165a63eab49cf714bce3a75a74f76ea7e64ff81eb61fdfec39b67bf0de98c7e4e32bdf97c8c6ac75ba43c02f4b2ed7216ecf3014df000108b67cf99505b179f8ed4980a6103d1bca70dbe9bbfab0ed59801d6e5f2d6f67d3ec5168e212e2daf02c6b963c98a1f7097de0c56891a2b211b01070dd8fd8b16c2a1a4e3cfd292d2984b3561d555d16c33ddc2bcf7edde13efe520c7e2abdda44d81881c531aeeeb66244c3b791ea8acfb6a68f3584606472b260e0dd2ebb21f6c3a3bc0542aabba4ef8f6c7169e731108db0460220aa74d31b55b03a00d220d475dcd9b877856d5704c9c86ea0f98f2eb9c530da7fa5ad8b0b5db50c2fd5d095a2aa5e2a3fbb71347549a316332234ece765b7571b64d216b28712e25cf3780f9dc629cd719b01e6d4a4fd17c731f'
ref_data = ref_string.decode("hex")
array.array('B', ref_data)
map(ord, ref_data)


## Read in the GNURadio output
output = np.array(scipy.fromfile(open("/home/gs-laptop1/GroundStation/GroundStation/GNURadio/Test_Files/BAL_FEC_Test/frame_out.bit"), dtype=scipy.uint8))

print "Length of reference: ", len(ref_data), "\t Length of output: ", len(output)

plt.plot(output)
plt.plot(ref_data)
plt.show()

# np.set_printoptions(formatter={'int':hex})

# print ref_data[0:7]
# print output[0:7]


#
