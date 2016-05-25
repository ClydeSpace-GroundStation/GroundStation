#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Tue Mar 29 15:54:19 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import ccsds

class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 0.01

        ##################################################
        # Blocks
        ##################################################
        self.ccsds_asm_deframer_pdu_0 = ccsds.asm_deframer_pdu(0, 1, False, 255)
        self.blocks_vector_source_x_0_0 = blocks.vector_source_b(range(255)+range(255), False, 1, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_b((0x1A, 0xCF, 0xFC, 0x1D), False, 1, [])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_char*1, (4, 510))
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.blocks_message_debug_0 = blocks.message_debug()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ccsds_asm_deframer_pdu_0, 'pdus'), (self.blocks_message_debug_0, 'print_pdu'))    
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.ccsds_asm_deframer_pdu_0, 0))    
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))    
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_stream_mux_0, 0))    
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_stream_mux_0, 1))    


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()
