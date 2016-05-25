#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu May 19 15:41:52 2016
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

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import ax25
import pmt
import pyqt
import sys
import time


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 614.4e3
        self.rf_freq = rf_freq = 145e6
        self.rf_bw = rf_bw = 100e3
        self.gain = gain = 0

        ##################################################
        # Blocks
        ##################################################
        self._gain_range = Range(0, 90, 1, 0, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "gain", "counter_slider", float)
        self.top_layout.addWidget(self._gain_win)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		otw_format="sc12",
        		channels=range(1),
        	),
        	"packet_len",
        )
        self.uhd_usrp_sink_0.set_clock_rate(30.72e6, uhd.ALL_MBOARDS)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(rf_freq, 0)
        self.uhd_usrp_sink_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0.set_bandwidth(rf_bw, 0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=8,
                decimation=1,
                taps=None,
                fractional_bw=0.125,
        )
        self.pyqt_text_output_0 = pyqt.text_output()
        self._pyqt_text_output_0_win = self.pyqt_text_output_0;
        self.top_layout.addWidget(self._pyqt_text_output_0_win)
        self.digital_scrambler_bb_0 = digital.scrambler_bb(0x21, 0x00, 16)
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
        	samples_per_symbol=8,
        	bt=0.5,
        	verbose=False,
        	log=False,
        )
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, "packet_len", 64*8)
        self.blocks_random_pdu_0 = blocks.random_pdu(32, 256, chr(0xFF), 1)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "packet_len")
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("TEST"), 100)
        self.ax25_pdu_prepend_append_0_0 = ax25.pdu_prepend_append(40, 2, 0x7e)
        self.ax25_pdu_prepend_append_0 = ax25.pdu_prepend_append(512, 256, 0xFF)
        self.ax25_nrzi_encoder_0 = ax25.nrzi_encoder(0)
        self.ax25_ax25_encoder_0 = ax25.ax25_encoder("PICASS", "BISAGS ", 0, 14)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ax25_ax25_encoder_0, 'pdu_out'), (self.ax25_pdu_prepend_append_0_0, 'pdu_in'))    
        self.msg_connect((self.ax25_pdu_prepend_append_0, 'pdu_out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.msg_connect((self.ax25_pdu_prepend_append_0_0, 'pdu_out'), (self.ax25_pdu_prepend_append_0, 'pdu_in'))    
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.blocks_random_pdu_0, 'generate'))    
        self.msg_connect((self.blocks_random_pdu_0, 'pdus'), (self.ax25_ax25_encoder_0, 'pdu_in'))    
        self.connect((self.ax25_nrzi_encoder_0, 0), (self.digital_scrambler_bb_0, 0))    
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.ax25_nrzi_encoder_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))    
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.digital_gmsk_mod_0, 0))    
        self.connect((self.digital_gmsk_mod_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.digital_scrambler_bb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_rf_freq(self):
        return self.rf_freq

    def set_rf_freq(self, rf_freq):
        self.rf_freq = rf_freq
        self.uhd_usrp_sink_0.set_center_freq(self.rf_freq, 0)

    def get_rf_bw(self):
        return self.rf_bw

    def set_rf_bw(self, rf_bw):
        self.rf_bw = rf_bw
        self.uhd_usrp_sink_0.set_bandwidth(self.rf_bw, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink_0.set_gain(self.gain, 0)
        	


def main(top_block_cls=top_block, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
