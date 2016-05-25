#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
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

import numpy as np
from gnuradio import gr
import pmt
import struct


class encode(gr.basic_block):
    """
    docstring for block encode
    """
    def __init__(self, dest_callsign, dest_ssid, source_callsign, source_ssid):
        gr.basic_block.__init__(self,
            name="encode",
            in_sig=[],       # should be PDU based input
            out_sig=[])      # should be PDU based output

        # create the input message port
        self.message_port_register_in(pmt.intern("pdu_in"))
        self.message_port_register_out(pmt.intern("pdu_out"))

        # assign the message handler
        self.set_msg_handler(pmt.intern("pdu_in"), self.pdu_handler)


    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        output_items[0][:] = input_items[0]
        consume(0, len(input_items[0]))
        #self.consume_each(len(input_items[0]))
        return len(output_items[0])

    """
        function to retrieve the PDU message and form the
    """
    def pdu_handler(self, msg_pmt):

        # Collect metadata, convert to Python format:
        meta = pmt.to_python(pmt.car(msg_pmt))

        # Collect message, convert to Python format:
        msg = pmt.cdr(msg_pmt)

        # Make sure it's a u8vector
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type.\n"
            return

        # create the AX.25 packet
        packeddata = DynamicPack(msg)
        frame = AX25_Frame(packeddata.packed)
        CRC = CheckCRC(frame.Frame)
        Stuffeddata = BitStuffer(CRC.appendmodulus)
        fullframe = HDLCFramer(Stuffeddata.Stuffed)


        # send the message on
        self.message_port_pub(pmt.intern('pdu_out'),msg_pmt)




    ########################################################################################################################
    # Check endianess of packed data (remember it is unpacked as well)
    # Confirm CRC
    # Do I want to pass this one byte at a time?? GR_EC does this
    # How do I pull in sample rate from a variable?
    ########################################################################################################################
    #Probably should form a seperate module as lower OSI level(HDLC Handling)
    def BitStuffer(CRC):

        #Takes an empty string and fills it with unpacked data
        bitstreamin=''
        bitstreamout=''
        for i in range(0,len(CRC)):
            byteat=np.array(struct.unpack('B',CRC[i]))
            byteat=format(int(byteat),'008b')
            bitstreamin+=byteat

        #Fill a buffer with 5 string elements for analysis
        for i in range(0,len(bitstreamin)):
            buf=bitstreamin[i:(i+5)]

            #fills a buffer with input values. Reads buffer for on or zero
            if buf[0]=='0':
                bitstreamout+=str(buf[0])#bitstreamout.append(str(buf[0]))

            elif buf[0]=='1':
                 #Appends buffer value to bitstring but if last 5 bitstring values are ones then stuffs.
                bitstreamout+=str(buf[0])
                if bitstreamout[(len(bitstreamout)-5):]=='11111':
                     bitstreamout+=str('0')
            else:
                   print "Buffer length error while bit stuffing"

        #Repacks the data into packed bytes
        appendbyte=''
        for i in range (0,len(bitstreamout),8):
            byteout=int(bitstreamout[i:i+8],2)
            byteoutpack=struct.pack('!B',byteout)
            appendbyte+=byteoutpack

        self.Stuffed=appendbyte


    def HDLCFramer():
        #Sets the structure of the HDLC frame - Sync bytes used as per CMC ICD
        self.flag=struct.pack('!B',0x7E)
        self.sync=struct.pack('!B',0xCC)
        self.HDLCFrame=self.sync+self.sync+self.sync+self.flag+Stuffeddata.Stuffed+self.flag

    ########################################################################################################################
    #Framing etc.
    def AX25_Frame():

        #Sets the structure of AX.25 frame (excluding CMC) in line with AX25 and CMC ICD
        address = struct.pack('14B',0xa6,0xa0,0x82,0x86,0x8a,0x40,0x61,0x86,0x82,0xa4,0xa8,0x90,0x40,0xe0)
        control = struct.pack('B',0x03)
        pid = struct.pack('B',0xf0)
        Frame = address + control + pid + packed


    def DynamicPack(inputarray):

        #Python Struct.pack does not allow packing of variable length data structures - this does this manually
        packedbytes = bytes(inputarray)
        appenddata = ''
        for i in range(0,len(data),8):
            byteout = struct.pack('B',int(packedbytes[i:i+8],2))
            appenddata += byteout
        # self.packed = appenddata
        return appenddata

    def CheckCRC():

        #http://stackoverflow.com/questions/25239423/crc-ccitt-16-bit-python-manual-calculation
        #Kermet CRC extracted from the above. Need to confirm this is the correct CRC
        self.data=struct.pack('2B',0,0)

        poly = 0x1021
        reg = 0xFFFF

        for byte in data:
            mask = 0x80
            while mask > 0:
                #left shift by one
                reg <<= 1
                if ord(byte) & mask:
                    reg += 1
                mask >>= 1
                #if a one popped out left of reg then XOR w/poly
                if reg > 0xFFFF:
                    #destroy the one
                    reg &= 0xFFFF
                    #XOR with poly
                    reg^=poly
        self.modulus=reg

        #Careful in here, using different encoding for byte
        self.appendmodulus=frame.Frame+struct.pack('!I',self.modulus)
