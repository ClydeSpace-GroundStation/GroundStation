# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: AX.25 Line Coding Heir Block
# Author: Thomas Parry
# Description: Performs the line coding neccesary for AX.25.  Set "scrambler" to 0 to disable scrambling, set to 1 to enable.
# Generated: Tue May 31 14:14:10 2016
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
import ax25


class ax25_line_coding_heir(gr.hier_block2):

    def __init__(self, scrambler=0):
        gr.hier_block2.__init__(
            self, "AX.25 Line Coding Heir Block",
            gr.io_signature(1, 1, gr.sizeof_char*1),
            gr.io_signature(1, 1, gr.sizeof_char*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.scrambler = scrambler

        ##################################################
        # Blocks
        ##################################################
        self.digital_scrambler_bb_0 = digital.scrambler_bb(0x21, 0x00, 16)
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_char*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=scrambler,
        	output_index=0,
        )
        self.ax25_nrzi_encoder_0 = ax25.nrzi_encoder(0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.ax25_nrzi_encoder_0, 0), (self.blks2_selector_0, 0))    
        self.connect((self.ax25_nrzi_encoder_0, 0), (self.digital_scrambler_bb_0, 0))    
        self.connect((self.blks2_selector_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))    
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.ax25_nrzi_encoder_0, 0))    
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self, 0))    
        self.connect((self.digital_scrambler_bb_0, 0), (self.blks2_selector_0, 1))    
        self.connect((self, 0), (self.blocks_packed_to_unpacked_xx_0, 0))    

    def get_scrambler(self):
        return self.scrambler

    def set_scrambler(self, scrambler):
        self.scrambler = scrambler
        self.blks2_selector_0.set_input_index(int(self.scrambler))
