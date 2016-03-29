#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import ccsds_swig as ccsds

class qa_rs_decode (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):

	interleave = 1

	# generate the transmitted data
	#orig_data = []
	#for i in range(0,223):
	#	orig_data.append(int(i));
	#	orig_data.append(int(i));
		#orig_data.append(int(i+2));
		#orig_data.append(int(i+3));

	orig_bit = open('rs_orig_data.txt','r')
    	orig_data = map(int,orig_bit.read().splitlines())

	print "Original Data: " , orig_data


	# read in received data from file
	bit = open('rs_encode_out.txt','r')
    	src_data = map(int,bit.read().splitlines())

	print "length: " , len(src_data)

	for i in range(0, 2):
		src_data[i] = 255

	#print "Received Data: " , src_data

	# set up 
	src = blocks.vector_source_b(src_data)
	rs_de = ccsds.rs_decode(interleave)
	dst = blocks.vector_sink_b()
	self.tb.connect(src, rs_de, dst)

        # run the test
        self.tb.run ()

        # check results
        result_data = dst.data()

	# change results to int
	result_data_int = []
	for n in result_data:
    		result_data_int.append(int(n))

	#print len(result_data_int)

	# print results
	print "Result Data: " , result_data_int
	
	# test errors have been corrected
	self.assertEquals(orig_data, result_data_int)


if __name__ == '__main__':
    gr_unittest.run(qa_rs_decode, "qa_rs_decode.xml")
