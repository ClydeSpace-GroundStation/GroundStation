#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Outernet Flatsat Flowgraph
# Author: Thomas Parry
# Description: Allows communication between the satellite and TMTC for use in a flatsat environement.
# Generated: Tue May 31 15:22:46 2016
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
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import ax25
import bruninga
import ec
import sip
import time


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
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
        # Variables
        ##################################################
        self.afsk_space = afsk_space = 2200
        self.afsk_mark = afsk_mark = 1200
        self.bitrate = bitrate = 1200
        self.afsk_deviation = afsk_deviation = (afsk_space - afsk_mark)/2
        self.uhd_samp_rate = uhd_samp_rate = 614400
        self.tx_gain = tx_gain = 0
        self.rx_gain = rx_gain = 0
        self.rf_tx_freq = rf_tx_freq = 145e6
        self.rf_rx_freq = rf_rx_freq = 401e6
        self.rf_offset_freq = rf_offset_freq = 80e3
        self.rf_bw = rf_bw = 100e3
        self.interpolation = interpolation = 16
        self.afsk_sensitivity = afsk_sensitivity = 2.0*afsk_deviation/bitrate
        self.afsk_centre_freq = afsk_centre_freq = afsk_mark + afsk_deviation

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
        )
        self.uhd_usrp_sink_0.set_clock_rate(30.72e6, uhd.ALL_MBOARDS)
        self.uhd_usrp_sink_0.set_samp_rate(uhd_samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(rf_tx_freq, 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_bandwidth(rf_bw, 0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=4,
                decimation=1,
                taps=None,
                fractional_bw=0.25,
        )
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	uhd_samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_0_win)
        
        self.qtgui_sink_x_0_0.enable_rf_freq(False)
        
        
          
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, bitrate*interpolation, 1.2*afsk_deviation, 50, firdes.WIN_HAMMING, 6.76))
        self.ec_ax25_decoder_b_0 = ec.ax25_decoder_b(True, 0, "")
        self.bruninga_fsk_demod_0 = bruninga.fsk_demod(19200)
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, "packet_len", 4096)
        self.blocks_socket_pdu_1_0 = blocks.socket_pdu("TCP_CLIENT", "127.0.0.1", "51423", 10000, False)
        self.blocks_socket_pdu_1 = blocks.socket_pdu("TCP_CLIENT", "127.0.0.1", "51423", 10000, False)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.ax25_nrzi_encoder_0 = ax25.nrzi_encoder(0)
        self.ax25_encode_heir_0 = ax25_encode_heir(
            destination_callsign="SPACE",
            destination_ssid=0,
            post_flag_quantity=16,
            post_sync_quantity=16,
            pre_flag_quantity=16,
            pre_sync_quantity=128,
            source_callsign="EARTH",
            source_ssid=0,
            sync_value=85,
        )
        self.analog_sig_source_x_0 = analog.sig_source_c(bitrate*interpolation, analog.GR_COS_WAVE, afsk_centre_freq, 1, 0)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=bitrate*interpolation,
        	quad_rate=uhd_samp_rate/4,
        	tau=75e-6*0,
        	max_dev=2.5e3,
        	fh=-1.0,
                )
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=19200,
        	quad_rate=4*153600,
        	tau=0.01,
        	max_dev=2.5e3,
          )
        self.analog_cpfsk_bc_0 = analog.cpfsk_bc(afsk_sensitivity, 1, interpolation)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_1_0, 'pdus'), (self.ax25_encode_heir_0, 'pdus in'))    
        self.msg_connect((self.ec_ax25_decoder_b_0, 'pdus'), (self.blocks_socket_pdu_1, 'pdus'))    
        self.connect((self.analog_cpfsk_bc_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.analog_nbfm_rx_0, 0), (self.bruninga_fsk_demod_0, 0))    
        self.connect((self.analog_nbfm_tx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.ax25_encode_heir_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))    
        self.connect((self.ax25_nrzi_encoder_0, 0), (self.analog_cpfsk_bc_0, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.analog_nbfm_tx_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.ax25_nrzi_encoder_0, 0))    
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.qtgui_sink_x_0_0, 0))    
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.bruninga_fsk_demod_0, 0), (self.ec_ax25_decoder_b_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.analog_nbfm_rx_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_afsk_space(self):
        return self.afsk_space

    def set_afsk_space(self, afsk_space):
        self.afsk_space = afsk_space
        self.set_afsk_deviation((self.afsk_space - self.afsk_mark)/2)

    def get_afsk_mark(self):
        return self.afsk_mark

    def set_afsk_mark(self, afsk_mark):
        self.afsk_mark = afsk_mark
        self.set_afsk_deviation((self.afsk_space - self.afsk_mark)/2)
        self.set_afsk_centre_freq(self.afsk_mark + self.afsk_deviation)

    def get_bitrate(self):
        return self.bitrate

    def set_bitrate(self, bitrate):
        self.bitrate = bitrate
        self.set_afsk_sensitivity(2.0*self.afsk_deviation/self.bitrate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.bitrate*self.interpolation, 1.2*self.afsk_deviation, 50, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0.set_sampling_freq(self.bitrate*self.interpolation)

    def get_afsk_deviation(self):
        return self.afsk_deviation

    def set_afsk_deviation(self, afsk_deviation):
        self.afsk_deviation = afsk_deviation
        self.set_afsk_sensitivity(2.0*self.afsk_deviation/self.bitrate)
        self.set_afsk_centre_freq(self.afsk_mark + self.afsk_deviation)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.bitrate*self.interpolation, 1.2*self.afsk_deviation, 50, firdes.WIN_HAMMING, 6.76))

    def get_uhd_samp_rate(self):
        return self.uhd_samp_rate

    def set_uhd_samp_rate(self, uhd_samp_rate):
        self.uhd_samp_rate = uhd_samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.uhd_samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.uhd_samp_rate)
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.uhd_samp_rate)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)
        	

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

    def get_interpolation(self):
        return self.interpolation

    def set_interpolation(self, interpolation):
        self.interpolation = interpolation
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.bitrate*self.interpolation, 1.2*self.afsk_deviation, 50, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0.set_sampling_freq(self.bitrate*self.interpolation)

    def get_afsk_sensitivity(self):
        return self.afsk_sensitivity

    def set_afsk_sensitivity(self, afsk_sensitivity):
        self.afsk_sensitivity = afsk_sensitivity

    def get_afsk_centre_freq(self):
        return self.afsk_centre_freq

    def set_afsk_centre_freq(self, afsk_centre_freq):
        self.afsk_centre_freq = afsk_centre_freq
        self.analog_sig_source_x_0.set_frequency(self.afsk_centre_freq)


def main(top_block_cls=top_block, options=None):

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
