#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2013 <+YOU OR YOUR COMPANY+>.
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

import numpy
from gnuradio import gr,blocks
from satisfi import ax25
from math import pi
import pmt
from gnuradio import digital
import sys
import time
import tnc
import array



class hdlc_framer(gr.sync_block):
    """
    docstring for block hdlc_framer
    """
    def __init__(self, preamble_length,postamble_length,verbose,use_scrambler):
        gr.sync_block.__init__(self,
            name="hdlc_framer",
            in_sig=None,
            out_sig=None)

        self.use_scrambler = use_scrambler
        self.preamble_length = preamble_length
        self.postamble_length = postamble_length

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'),self.handle_msg)

        self.message_port_register_out(pmt.intern('out'))
        
    def hex_string(self,inp):
        hex_str = '['
        for i in range(len(inp)):
            hex_str = hex_str + ", %x" % inp[i]
        hex_str = hex_str + "]"
        return hex_str

    def handle_msg(self, msg):

        #if message run hdlc encoder
        meta = pmt.car(msg)
        data =  pmt.cdr(msg)
        if not pmt.is_u8vector(data):
            raise NameError("Data is no u8 vector")
        
        payload = pmt.u8vector_elements(data)
        
        payload = array.array('B',payload)
        
        outstream=ax25.sendpacket(payload,self.preamble_length,self.postamble_length)
        if(self.use_scrambler):
            outstream=ax25.scrambler(outstream)
        outstream=ax25.nrziencode(outstream)
        outstream=array.array('B',outstream)
        
        #print outstream
        self.message_port_pub(pmt.intern('out'),pmt.cons(pmt.PMT_NIL,pmt.init_u8vector(len(outstream),outstream)))

        return 0

