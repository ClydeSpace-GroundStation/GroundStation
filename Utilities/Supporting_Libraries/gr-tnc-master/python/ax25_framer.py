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

AX25_MAX_PAYLOAD = 255

class ax25_framer(gr.sync_block):
    """
    docstring for block ax25_framer
    """
    def __init__(self,mycall,destcall,verbose):
        gr.sync_block.__init__(self,
            name="ax25_framer",
            in_sig=None,
            out_sig=None)

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'),self.handle_msg)

        self.message_port_register_out(pmt.intern('out'))
        
        self.mycall = mycall
        self.destcall = destcall
        self.verbose = verbose
        
    
    def set_destcall(self,destcall):
        self.destcall = destcall
    
    def set_mycall(self,mycall):
        self.mycall = mycall
        
    def hex_string(self,inp):
        hex_str = '['
        for i in range(len(inp)):
            hex_str = hex_str + ", %x" % inp[i]
        hex_str = hex_str + "]"
        return hex_str

    def handle_msg(self, msg):

        

        meta = pmt.car(msg)
        data =  pmt.cdr(msg)
        if not pmt.is_u8vector(data):
            raise NameError("Data is no u8 vector")
        
        
        
        payload = pmt.u8vector_elements(data)
        
        payload = array.array('B',payload)
            
        if len(payload) > AX25_MAX_PAYLOAD:
            print 'Payload too large for an HDLC(AX25) frame'
            return 0
                    
        #TODO - add paramters for each in this functions
        packet=ax25.buildpacket(self.mycall,1,self.destcall,0,"0",0,0x03,0xf0,payload.tostring())
        
        
        
        if self.verbose:
            print "Payload: ",payload.tostring()
            print "Packet: ",packet        
            print "********Framer:",time.time()
            print self.hex_string(packet)
            
        packet = array.array('B',packet)
        
        #print outstream
        self.message_port_pub(pmt.intern('out'),pmt.cons(pmt.PMT_NIL,pmt.init_u8vector(len(packet),packet)))

        return 0
