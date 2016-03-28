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
import random

class qa_rs_encode (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):

	interleave = 1

        # set up source data
	src_data = []

	for i in range(0,223*interleave):
		src_data.append(random.randint(0,223))

	#for i in range(0,223):
		#src_data.append(i);
		#src_data.append(i);
		#src_data.append(i+2);
		#src_data.append(i+3);


	#print "Src data: " , src_data


	f = open('rs_orig_data.txt','w')
	for item in src_data:
  		f.write("%u\n" % item)
	f.close()


	src = blocks.vector_source_b(src_data)

	# set up 
	rs_en = ccsds.rs_encode(interleave)
	dst = blocks.vector_sink_b()
	self.tb.connect(src, rs_en, dst)

	# run the test
        self.tb.run ()

        # check results
        result_data = dst.data()

	# change results to int
	result_data_int = []
	for n in result_data:
    		result_data_int.append(int(n))

	# print results
	#print "Result Data: " , result_data_int

	# write the data to file to be used with the decode QA script
	f = open('rs_encode_out.txt','w')
	for item in result_data_int:
  		f.write("%u\n" % item)
	f.close()


if __name__ == '__main__':
    gr_unittest.run(qa_rs_encode, "qa_rs_encode.xml")
