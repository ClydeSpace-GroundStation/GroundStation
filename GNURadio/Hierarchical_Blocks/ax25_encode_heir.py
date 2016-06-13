# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: AX.25 Encoding Heir Block
# Author: Thomas Parry
# Description: Receive PDUs and output tagged streams ready for line coding
# Generated: Thu May 26 21:13:31 2016
##################################################

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import ax25


class ax25_encode_heir(gr.hier_block2):

    def __init__(self, destination_callsign="SPACE", destination_ssid=0, post_flag_quantity=16, post_sync_quantity=16, pre_flag_quantity=16, pre_sync_quantity=128, source_callsign="EARTH", source_ssid=0, sync_value=85):
        gr.hier_block2.__init__(
            self, "AX.25 Encoding Heir Block",
            gr.io_signature(0, 0, 0),
            gr.io_signature(1, 1, gr.sizeof_char*1),
        )
        self.message_port_register_hier_in("pdus in")

        ##################################################
        # Parameters
        ##################################################
        self.destination_callsign = destination_callsign
        self.destination_ssid = destination_ssid
        self.post_flag_quantity = post_flag_quantity
        self.post_sync_quantity = post_sync_quantity
        self.pre_flag_quantity = pre_flag_quantity
        self.pre_sync_quantity = pre_sync_quantity
        self.source_callsign = source_callsign
        self.source_ssid = source_ssid
        self.sync_value = sync_value

        ##################################################
        # Blocks
        ##################################################
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "packet_len")
        self.ax25_pdu_prepend_append_0_0 = ax25.pdu_prepend_append(pre_flag_quantity, post_flag_quantity, 0x7e)
        self.ax25_pdu_prepend_append_0 = ax25.pdu_prepend_append(pre_sync_quantity, post_sync_quantity, sync_value)
        self.ax25_ax25_encoder_0 = ax25.ax25_encoder(destination_callsign, source_callsign, destination_ssid, source_ssid)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ax25_ax25_encoder_0, 'pdu_out'), (self.ax25_pdu_prepend_append_0_0, 'pdu_in'))    
        self.msg_connect((self.ax25_pdu_prepend_append_0, 'pdu_out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.msg_connect((self.ax25_pdu_prepend_append_0_0, 'pdu_out'), (self.ax25_pdu_prepend_append_0, 'pdu_in'))    
        self.msg_connect((self, 'pdus in'), (self.ax25_ax25_encoder_0, 'pdu_in'))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self, 0))    

    def get_destination_callsign(self):
        return self.destination_callsign

    def set_destination_callsign(self, destination_callsign):
        self.destination_callsign = destination_callsign

    def get_destination_ssid(self):
        return self.destination_ssid

    def set_destination_ssid(self, destination_ssid):
        self.destination_ssid = destination_ssid

    def get_post_flag_quantity(self):
        return self.post_flag_quantity

    def set_post_flag_quantity(self, post_flag_quantity):
        self.post_flag_quantity = post_flag_quantity

    def get_post_sync_quantity(self):
        return self.post_sync_quantity

    def set_post_sync_quantity(self, post_sync_quantity):
        self.post_sync_quantity = post_sync_quantity

    def get_pre_flag_quantity(self):
        return self.pre_flag_quantity

    def set_pre_flag_quantity(self, pre_flag_quantity):
        self.pre_flag_quantity = pre_flag_quantity

    def get_pre_sync_quantity(self):
        return self.pre_sync_quantity

    def set_pre_sync_quantity(self, pre_sync_quantity):
        self.pre_sync_quantity = pre_sync_quantity

    def get_source_callsign(self):
        return self.source_callsign

    def set_source_callsign(self, source_callsign):
        self.source_callsign = source_callsign

    def get_source_ssid(self):
        return self.source_ssid

    def set_source_ssid(self, source_ssid):
        self.source_ssid = source_ssid

    def get_sync_value(self):
        return self.sync_value

    def set_sync_value(self, sync_value):
        self.sync_value = sync_value
