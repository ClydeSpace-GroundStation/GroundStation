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
import time

class qa_asm_deframer (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
	
	# read in source data from file
	#bit = open('/home/tom/software/gnuradio-build/gnuradio/gr-ccsds/python/bit_in.txt','r')
    	#src_data = map(int,bit.read().splitlines())
	#print src_data
	
	src_data = []
	for n in range(0,255*8+32):
		src_data.append(0)

	print src_data

	# read in expected output from file
	byte = open('/home/tom/software/gnuradio-build/gnuradio/gr-ccsds/python/byte_out.txt')
    	expected_result = map(int,byte.read().splitlines())
	#print expected_result
        
	# map input and output streams
	src = blocks.vector_source_b(src_data)
        sqr = ccsds.asm_deframer(32,1)
	dst = blocks.vector_sink_b()
	self.tb.connect(src, sqr, dst)

	# run test
	self.tb.run()

	# check results
        result_data = dst.data()

	# change results to int
	result_data_int = []
	for n in result_data:
    		result_data_int.append(int(n))

	print "output: " , result_data_int

	self.assertEquals(expected_result, result_data_int)


if __name__ == '__main__':
    gr_unittest.run(qa_asm_deframer, "qa_asm_deframer.xml")
