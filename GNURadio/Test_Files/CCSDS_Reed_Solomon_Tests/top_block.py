#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Mon Mar 21 15:45:41 2016
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
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import ccsds
import sys

from distutils.version import StrictVersion
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
        self.samp_rate = samp_rate = 32000
        self.interleave = interleave = 4

        ##################################################
        # Blocks
        ##################################################
        self.ccsds_rs_encode_0 = ccsds.rs_encode(interleave)
        self.ccsds_rs_decode_0_0 = ccsds.rs_decode(interleave)
        self.blocks_vector_source_x_0 = blocks.vector_source_b(range(223)+range(223)+range(223)+range(223)+[0], False, 1, [])
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_char*1, "/home/thomasp/Groundstation/CCSDS/Reed Solomon Tests/RS Test 1/output.bin", False)
        self.blocks_file_sink_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, "/home/thomasp/Groundstation/CCSDS/Reed Solomon Tests/RS Test 1/encoded.bin", False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, "/home/thomasp/Groundstation/CCSDS/Reed Solomon Tests/RS Test 1/input.bin", False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.blocks_vector_source_x_0, 0), (self.ccsds_rs_encode_0, 0))    
        self.connect((self.ccsds_rs_decode_0_0, 0), (self.blocks_file_sink_0_0_0, 0))    
        self.connect((self.ccsds_rs_encode_0, 0), (self.blocks_file_sink_0_0, 0))    
        self.connect((self.ccsds_rs_encode_0, 0), (self.ccsds_rs_decode_0_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_interleave(self):
        return self.interleave

    def set_interleave(self, interleave):
        self.interleave = interleave
        self.ccsds_rs_decode_0_0.set_interleave(self.interleave)
        self.ccsds_rs_encode_0.set_interleave(self.interleave)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = top_block()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
