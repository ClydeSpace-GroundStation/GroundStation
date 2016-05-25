#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Outernet Flatsat Flowgraph
# Author: Thomas Parry
# Description: Allows communication between the satellite and TMTC for use in a flatsat environement.
# Generated: Thu May 19 15:57:58 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt4 import Qt
from ax25_encode_heir import ax25_encode_heir  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fec
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import ais
import ax25
import ccsds
import pyqt
import time


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self, puncpat='11'):
        gr.top_block.__init__(self, "Outernet Flatsat Flowgraph")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Outernet Flatsat Flowgraph")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.puncpat = puncpat

        ##################################################
        # Variables
        ##################################################
        self.rate = rate = 2
        self.polys = polys = [79, 109]
        self.k = k = 7
        self.frame_size = frame_size = 32
        self.uhd_samp_rate = uhd_samp_rate = 614400
        self.tx_gain = tx_gain = 0
        self.samples_per_symbol = samples_per_symbol = 64
        self.rx_gain = rx_gain = 0
        self.rf_tx_freq = rf_tx_freq = 145e6
        self.rf_rx_freq = rf_rx_freq = 401e6
        self.rf_offset_freq = rf_offset_freq = 80e3
        self.rf_bw = rf_bw = 100e3
        self.interleave = interleave = 4
        
        
        self.dec_cc = dec_cc = fec.cc_decoder.make(frame_size, k, rate, (polys), 0, -1, fec.CC_STREAMING, False)
            

        ##################################################
        # Blocks
        ##################################################
        self._tx_gain_range = Range(0, 90, 1, 0, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, "TX Gain", "counter_slider", float)
        self.top_layout.addWidget(self._tx_gain_win)
        self._rx_gain_range = Range(0, 90, 1, 0, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, "RX Gain", "counter_slider", float)
        self.top_layout.addWidget(self._rx_gain_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_clock_rate(30.72e6, uhd.ALL_MBOARDS)
        self.uhd_usrp_source_0.set_samp_rate(uhd_samp_rate)
        self.uhd_usrp_source_0.set_center_freq(rf_rx_freq, 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_bandwidth(rf_bw, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        	"packet_len",
        )
        self.uhd_usrp_sink_0.set_clock_rate(30.72e6, uhd.ALL_MBOARDS)
        self.uhd_usrp_sink_0.set_samp_rate(uhd_samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(rf_tx_freq, 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_bandwidth(rf_bw, 0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=8,
                decimation=1,
                taps=None,
                fractional_bw=0.125,
        )
        self.pyqt_text_input_0 = pyqt.text_input()
        self._pyqt_text_input_0_win = self.pyqt_text_input_0;
        self.top_layout.addWidget(self._pyqt_text_input_0_win)
        self.fec_extended_decoder_0 = fec.extended_decoder(decoder_obj_list=dec_cc, threading= None, ann=None, puncpat=puncpat, integration_period=10000)
        self.digital_scrambler_bb_0 = digital.scrambler_bb(0x21, 0x00, 16)
        self.digital_map_bb_0 = digital.map_bb(([-1, 1]))
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
        	samples_per_symbol=8,
        	bt=0.5,
        	verbose=False,
        	log=False,
        )
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
        	samples_per_symbol=samples_per_symbol,
        	gain_mu=0.175,
        	mu=0.5,
        	omega_relative_limit=0.005,
        	freq_error=0.0,
        	verbose=False,
        	log=False,
        )
        self.ccsds_rs_decode_pdu_0 = ccsds.rs_decode_pdu(interleave)
        self.ccsds_asm_deframer_pdu_0 = ccsds.asm_deframer_pdu(0, interleave, 1, 255)
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, "packet_len", 64*8)
        self.blocks_socket_pdu_1_0 = blocks.socket_pdu("TCP_CLIENT", "127.0.0.1", "51423", 892, False)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.blocks_message_debug_0_1 = blocks.message_debug()
        self.blocks_char_to_float_0_0 = blocks.char_to_float(1, 1)
        self.ax25_nrzi_encoder_0 = ax25.nrzi_encoder(0)
        self.ax25_encode_heir_0_0 = ax25_encode_heir(
            destination_callsign="PICASS",
            destination_ssid=0,
            post_flag_quantity=16,
            post_sync_quantity=16,
            pre_flag_quantity=16,
            pre_sync_quantity=128,
            source_callsign="BISAGS ",
            source_ssid=14,
            sync_value=85,
        )
        self.ais_invert_0 = ais.invert()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_1_0, 'pdus'), (self.ax25_encode_heir_0_0, 'pdus in'))    
        self.msg_connect((self.blocks_socket_pdu_1_0, 'pdus'), (self.blocks_message_debug_0_1, 'print_pdu'))    
        self.msg_connect((self.ccsds_asm_deframer_pdu_0, 'pdus'), (self.ccsds_rs_decode_pdu_0, 'pdu_in'))    
        self.msg_connect((self.ccsds_rs_decode_pdu_0, 'pdu_out'), (self.blocks_socket_pdu_1_0, 'pdus'))    
        self.msg_connect((self.pyqt_text_input_0, 'pdus'), (self.ax25_encode_heir_0_0, 'pdus in'))    
        self.msg_connect((self.pyqt_text_input_0, 'pdus'), (self.blocks_message_debug_0_1, 'print_pdu'))    
        self.connect((self.ais_invert_0, 0), (self.digital_map_bb_0, 0))    
        self.connect((self.ax25_encode_heir_0_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))    
        self.connect((self.ax25_nrzi_encoder_0, 0), (self.digital_scrambler_bb_0, 0))    
        self.connect((self.blocks_char_to_float_0_0, 0), (self.fec_extended_decoder_0, 0))    
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.ax25_nrzi_encoder_0, 0))    
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.digital_gmsk_mod_0, 0))    
        self.connect((self.digital_gmsk_demod_0, 0), (self.ais_invert_0, 0))    
        self.connect((self.digital_gmsk_mod_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.digital_map_bb_0, 0), (self.blocks_char_to_float_0_0, 0))    
        self.connect((self.digital_scrambler_bb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))    
        self.connect((self.fec_extended_decoder_0, 0), (self.ccsds_asm_deframer_pdu_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.digital_gmsk_demod_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_puncpat(self):
        return self.puncpat

    def set_puncpat(self, puncpat):
        self.puncpat = puncpat

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

    def get_uhd_samp_rate(self):
        return self.uhd_samp_rate

    def set_uhd_samp_rate(self, uhd_samp_rate):
        self.uhd_samp_rate = uhd_samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.uhd_samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.uhd_samp_rate)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)
        	

    def get_samples_per_symbol(self):
        return self.samples_per_symbol

    def set_samples_per_symbol(self, samples_per_symbol):
        self.samples_per_symbol = samples_per_symbol

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)
        	

    def get_rf_tx_freq(self):
        return self.rf_tx_freq

    def set_rf_tx_freq(self, rf_tx_freq):
        self.rf_tx_freq = rf_tx_freq
        self.uhd_usrp_sink_0.set_center_freq(self.rf_tx_freq, 0)

    def get_rf_rx_freq(self):
        return self.rf_rx_freq

    def set_rf_rx_freq(self, rf_rx_freq):
        self.rf_rx_freq = rf_rx_freq
        self.uhd_usrp_source_0.set_center_freq(self.rf_rx_freq, 0)

    def get_rf_offset_freq(self):
        return self.rf_offset_freq

    def set_rf_offset_freq(self, rf_offset_freq):
        self.rf_offset_freq = rf_offset_freq

    def get_rf_bw(self):
        return self.rf_bw

    def set_rf_bw(self, rf_bw):
        self.rf_bw = rf_bw
        self.uhd_usrp_source_0.set_bandwidth(self.rf_bw, 0)
        self.uhd_usrp_sink_0.set_bandwidth(self.rf_bw, 0)

    def get_interleave(self):
        return self.interleave

    def set_interleave(self, interleave):
        self.interleave = interleave
        self.ccsds_asm_deframer_pdu_0.set_interleave(self.interleave,self.interleave)
        self.ccsds_rs_decode_pdu_0.set_interleave(self.interleave)

    def get_dec_cc(self):
        return self.dec_cc

    def set_dec_cc(self, dec_cc):
        self.dec_cc = dec_cc


def argument_parser():
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option(
        "", "--puncpat", dest="puncpat", type="string", default='11',
        help="Set puncpat [default=%default]")
    return parser


def main(top_block_cls=top_block, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(puncpat=options.puncpat)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
