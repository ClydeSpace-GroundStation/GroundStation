# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: CCSDS Channel Decoding
# Author: Thomas Parry
# Description: Block to perform the channel decoding as defined in the CCSDS channel coding standard
# Generated: Mon Jun  6 14:48:59 2016
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
from gnuradio.filter import firdes
import ais
import ccsds


class ccsds_decode(gr.hier_block2):

    def __init__(self, hamming_distance=4, interleave=4):
        gr.hier_block2.__init__(
            self, "CCSDS Channel Decoding",
            gr.io_signature(1, 1, gr.sizeof_char*1),
            gr.io_signature(0, 0, 0),
        )
        self.message_port_register_hier_out("out")

        ##################################################
        # Parameters
        ##################################################
        self.hamming_distance = hamming_distance
        self.interleave = interleave

        ##################################################
        # Variables
        ##################################################
        self.rate = rate = 2
        self.polys = polys = [79, 109]
        self.k = k = 7
        self.frame_size = frame_size = 32
        self.puncpat = puncpat = '11'
        
        
        self.dec_cc = dec_cc = fec.cc_decoder.make(frame_size, k, rate, (polys), 0, -1, fec.CC_STREAMING, False)
            

        ##################################################
        # Blocks
        ##################################################
        self.fec_extended_decoder_0 = fec.extended_decoder(decoder_obj_list=dec_cc, threading= None, ann=None, puncpat=puncpat, integration_period=10000)
        self.digital_map_bb_0 = digital.map_bb(([-1, 1]))
        self.ccsds_rs_decode_pdu_0 = ccsds.rs_decode_pdu(interleave)
        self.ccsds_asm_deframer_pdu_0 = ccsds.asm_deframer_pdu(hamming_distance, interleave, 1, 255)
        self.blocks_char_to_float_0_0 = blocks.char_to_float(1, 1)
        self.ais_invert_0 = ais.invert()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ccsds_asm_deframer_pdu_0, 'pdus'), (self.ccsds_rs_decode_pdu_0, 'pdu_in'))    
        self.msg_connect((self.ccsds_rs_decode_pdu_0, 'pdu_out'), (self, 'out'))    
        self.connect((self.ais_invert_0, 0), (self.digital_map_bb_0, 0))    
        self.connect((self.blocks_char_to_float_0_0, 0), (self.fec_extended_decoder_0, 0))    
        self.connect((self.digital_map_bb_0, 0), (self.blocks_char_to_float_0_0, 0))    
        self.connect((self.fec_extended_decoder_0, 0), (self.ccsds_asm_deframer_pdu_0, 0))    
        self.connect((self, 0), (self.ais_invert_0, 0))    

    def get_hamming_distance(self):
        return self.hamming_distance

    def set_hamming_distance(self, hamming_distance):
        self.hamming_distance = hamming_distance
        self.ccsds_asm_deframer_pdu_0.set_distance(self.hamming_distance,self.hamming_distance)

    def get_interleave(self):
        return self.interleave

    def set_interleave(self, interleave):
        self.interleave = interleave
        self.ccsds_rs_decode_pdu_0.set_interleave(self.interleave)
        self.ccsds_asm_deframer_pdu_0.set_interleave(self.interleave,self.interleave)

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate

    def get_polys(self):
        return self.polys

    def set_polys(self, polys):
        self.polys = polys

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_frame_size(self):
        return self.frame_size

    def set_frame_size(self, frame_size):
        self.frame_size = frame_size

    def get_puncpat(self):
        return self.puncpat

    def set_puncpat(self, puncpat):
        self.puncpat = puncpat

    def get_dec_cc(self):
        return self.dec_cc

    def set_dec_cc(self, dec_cc):
        self.dec_cc = dec_cc
