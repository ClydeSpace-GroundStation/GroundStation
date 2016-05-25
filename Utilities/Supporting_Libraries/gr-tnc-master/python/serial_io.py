#!/usr/bin/env python
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
from gnuradio import gr
try: import pmt
except: from gruel import pmt
from math import pi
import serial
import thread
import satisfi

NONE = 0
EVEN = 1 
ODD = 2

STOPBITS_ONE = 0
STOPBITS_TWO = 1

WORD_SIZE_7 = 0 
WORD_SIZE_8 = 1

class serial_io(gr.sync_block):
    """
    docstring for block serial_io
    """
    def __init__(self,device,parity,baudrate,stopbits,bytesize,wait_for_newline):
        gr.sync_block.__init__(self,
            name="serial_io",
            in_sig=None,
            out_sig=None
        )
        
        self.device = device
        self.parity = parity
        self.baudrate = baudrate 
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.wait_for_newline = wait_for_newline
        
        
        #set parity
        if self.parity == NONE:
            self.parity = serial.PARITY_NONE
        elif self.parity == EVEN:
            self.parity = serial.PARITY_EVEN
        else:
            self.parity = serial.PARITY_ODD
        
        #set stopbits
        if self.stopbits == STOPBITS_ONE:
            self.stopbits = serial.STOPBITS_ONE
        elif self.stopbits == STOPBITS_TWO:
            self.stopbits = serial.STOPBITS_TWO
        
        #set bytes size
        if self.bytesize == WORD_SIZE_7:
            self.bytesize = serial.SEVENBITS
        else:
            self.bytesize = serial.EIGHTBITS
        
        # configure the serial connections (the parameters differs on the device you are connecting to)
        
        self.ser = serial.Serial(
            port=self.device,
            baudrate=self.baudrate,
            parity=self.parity,
            stopbits=self.stopbits,
            bytesize=self.bytesize
        )

        '''
        self.ser = serial.Serial(
            port=self.device,
            baudrate=self.baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        '''
        print "Opened: ",self.ser.portstr       # check which port was really used
        #self.ser.write("hel;lkfsdsa;lkfjdsaflo\n\r")      # write a string
        #ser.close()             # close port

        self.message_port_register_out(pmt.intern('out'))
        
        self.msg_list = []
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'),
                             self.handle_msg)
                             
        self.message_port_register_in(pmt.intern('ctrl'))
        self.set_msg_handler(pmt.intern('ctrl'),
                             self.handle_ctrl)
        
        thread.start_new_thread( self.tx_work, (self.ser , ))

    def handle_msg(self, msg):
        # Create a new PMT from long value and put in list
        tx_string = pmt.symbol_to_string(msg)
        self.ser.write(tx_string)
        
    def handle_ctrl(self, msg):
        ctrl_string = pmt.symbol_to_string(msg)
        
        if ctrl_string == "PTT":
            self.ser.setRTS(True)
            print "PTT RTS ON"
        elif ctrl_string == "!PTT":
            self.ser.setRTS(False)
            print "PTT RTS OFF"
        else:
            print "Invalid ctrl command"

    def tx_work(self,ser):
        while(1):
            if(self.wait_for_newline):
                rx_buf = ser.readline()
            else:
                rx_buf = ser.read()
            #write string rx_buf to pmt
            msg = pmt.string_to_symbol(rx_buf)
            self.message_port_pub(pmt.intern('out'),
                                  msg)
            
    

