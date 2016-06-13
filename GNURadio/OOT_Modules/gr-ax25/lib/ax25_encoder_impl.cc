/* -*- c++ -*- */
/*
 * Copyright 2016 Clyde Space.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <iostream>
#include <cstring>
#include <gnuradio/io_signature.h>
#include <boost/crc.hpp>
#include <boost/integer.hpp>
#include <cassert>
#include <algorithm>  // for std::for_each
#include "ax25_encoder_impl.h"


/* Number of 1's which need a 0 appended */
#define BIT_STUFF_ONES 5

namespace gr {
  namespace ax25 {

    ax25_encoder::sptr
    ax25_encoder::make(const std::string &dest_addr, const std::string &src_addr, int dest_ssid, int src_ssid)
    {
      return gnuradio::get_initial_sptr
        (new ax25_encoder_impl(dest_addr, src_addr, dest_ssid, src_ssid));
    }

    /*
     * The private constructor
     */
    ax25_encoder_impl::ax25_encoder_impl(const std::string &dest_addr, const std::string &src_addr, int dest_ssid, int src_ssid)
      : gr::block("ax25_encoder",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(0, 0, 0))
    {

      // convert the destination address to uint8_t
      char * cstr = new char [7];
      strncpy(cstr,dest_addr.c_str(),6);
      memcpy(_dest_addr, cstr, 6);

      // shift the ASCII code up one bit
      for(int i = 0; i < 6; i++) {
        _dest_addr[i] = _dest_addr[i] << 1;
      }

      // convert the source address to uint8_t
      strncpy(cstr,src_addr.c_str(),6);
      memcpy(_src_addr, cstr, 6);

      // shift the ASCII code up one bit
      for(int i = 0; i < 6; i++) {
        _src_addr[i] = _src_addr[i] << 1;
      }

      // copy the SSID inputs
      _dest_ssid = dest_ssid;
      _src_ssid = src_ssid;

      // create a PDU output port
      message_port_register_out(pmt::mp("pdu_out"));

      // create a PDU input port and bind the to message handler function
      message_port_register_in(pmt::mp("pdu_in"));
      set_msg_handler(pmt::mp("pdu_in"), boost::bind(&ax25_encoder_impl::output_frame, this, _1));

    }

    /*
     * Our virtual destructor.
     */
    ax25_encoder_impl::~ax25_encoder_impl()
    {
    }


    /*
     * Function to reverse order of the bits in a byte (ie. MSB to LSB)
     */
    uint8_t ax25_encoder_impl::bit_reverse(uint8_t data) {
      return ((data * 0x80200802ULL) & 0x0884422110ULL) * 0x0101010101ULL >> 32;
    }

    /*
     * Function to reverse order of the bits in a byte array (ie. MSB to LSB)
     */
    void ax25_encoder_impl::bit_reverse_arr(uint8_t *data, uint32_t length) {

      for(int i=0; i < length; i++) {
        data[i] = ((data[i] * 0x80200802ULL) & 0x0884422110ULL) * 0x0101010101ULL >> 32;
      }
    }



    /*  Add the first 128 bit (16 byte) frame header to the frame
     *  using the source and destination details passed to it
     */
    void ax25_encoder_impl::add_header() {

      // TODO add error handling here

      // enter the destination call sign and SSID
      memcpy(&_frame[0],&_dest_addr[0],6);
      _frame[6] = 0x60 | (_dest_ssid << 1);

      // enter the source call sign and SSID
      memcpy(&_frame[7],&_src_addr[0],6);
      _frame[13] = 0x61 | (_src_ssid << 1);

      // enter the control byte
      _frame[14] = 0x03;

      // enter the protocol identifier
      _frame[15] = 0xF0;

    }




    /*  Calculate and append the CRC to the end of the frame
     */
    void ax25_encoder_impl::add_CRC( uint32_t input_data_length ) {

      // calculate the frame length
      int frame_length = input_data_length + 16;

      // create the CRC
      boost::crc_optimal<16, 0x1021, 0xFFFF, 0xFFFF, false, false>  crc_ccitt;
      crc_ccitt = std::for_each(_frame, _frame + frame_length, crc_ccitt );

      // insert the CRC into the frame
      _frame[frame_length] = (crc_ccitt() & 0xFF00) >> 8;
      _frame[frame_length+1] = (crc_ccitt() & 0x00FF);

    }


    /* Takes input array 'in' of bit length 'N'
     * & outputs a bit stuffed version in 'out'.
     * Total number of bytes written during
     * stuffing returned by function.
     * Please ensure 'out' is long enough to
     * support the operation.
     *
     * A quick back of the envelope shows that
     * worst case senario for bit-stuff is all
     * 1's in in the input array. This would
     * place a 0 every 'BIT_STUFF_ONES' bit's
     * along. So we can see the output length
     * in bytes will always be at most:
     *
     *  out_length
     *    = in_length_bytes
     *    + in_length_bytes/BIT_STUFF_ONES
     *    + 1
     *
     * The +1 is for good luck.
     */
     uint32_t ax25_encoder_impl::bit_stuff( uint8_t *in,
                                            uint8_t *out,
                                            uint32_t N)
    {
      uint16_t i      = 0;        // input byte counter
      uint16_t o      = 0xFFFF;   // output byte counter
      int8_t   b      = 7;        // input bit counter
      uint16_t out_b  = 7;        // bit position of output
      uint8_t  one_n  = 0;        // number of consequtive ones
      uint8_t  bit    = 0;        // current bit
      uint32_t out_N  = 0;

      // ensure the out array is filled with zeros
      memset(out, 0, 274);

      /* o is initialised with 0xFFFF to force
       * it to equal 0 on the first loop. This
       * ensures the correct number of bytes
       * are reported back.
       */

       /* Always clear the next output byte
        * so you don't have to 'write' zeros
        */
      out[0] = 0;

      int stuff_count = 0;

      // input byte loop
      while(N--){

        out_N++;

        if(out_b == 7){
          o = (o + 1) & 0xFFFF;
          out[o] = 0;
        }

        // anything > 0 is a bit
        bit = in[i] & (1 << b);

        if (bit){
          // bit is a 1
          out[o] |= (1 << out_b);
          one_n++;

          if(one_n == BIT_STUFF_ONES){

            stuff_count += 1;

            // update output counters to bit-stuff
            out_N++;
            out_b = (out_b - 1) & 0x07;

            if(out_b == 7){
              o = (o + 1) & 0xFFFF;
              out[o] = 0;
            }
            // reset counter
            one_n = 0;
          }
        } else {
          // bit is a 0
          // reset counter
          one_n = 0;
        }

        // update output counters
        out_b = (out_b - 1) & 0x07;
        b = (b - 1) & 0x07;

        if(b == 7){
          // move to the next input input array element
          i++;
        }
      }

      return out_N;
    }



    /*
    *   Receiced PDU handler.  Once called this function rearranges the data
    *   into the correct RS codeblocks, performs decoding and transmits a PDU
    *   of the original space frame packet
    */
    void ax25_encoder_impl::output_frame(pmt::pmt_t input_pdu)
    {

      // deconstruct the input PDU
      pmt::pmt_t meta = pmt::car(input_pdu);
      pmt::pmt_t vector = pmt::cdr(input_pdu);

      // retrieve the data
      size_t offset(0);
      const uint8_t* input_data = (const uint8_t*) pmt::uniform_vector_elements(vector, offset);
      uint32_t input_data_length = pmt::blob_length(vector);

      // add the header to the frame
      ax25_encoder_impl::add_header();

      // insert the information into the frame
      memcpy(&_frame[16], &input_data[0], input_data_length);

      // reverse the bit order, change from MSB to LSB
      ax25_encoder_impl::bit_reverse_arr(_frame, input_data_length + 16);

      // append the CRC
      ax25_encoder_impl::add_CRC(input_data_length);

      // bit stuff to avoid 0b01111110 in frame
      uint32_t frame_length_bits = ax25_encoder_impl::bit_stuff(_frame, &_bitstuffed_frame[1], 8*(input_data_length+18));

      // figure to append the CRC in a bit order (may not be on byte boundary)
      uint8_t extra_byte = 1;

      if((frame_length_bits % 8) > 0){
        extra_byte = 1;
      }

      uint32_t frame_length = (frame_length_bits / 8) + extra_byte + 1;
      _bitstuffed_frame[0] = 0x7E;

      _bitstuffed_frame[frame_length - 1] = _bitstuffed_frame[frame_length-1] | (0xFF & (0x7E >> frame_length_bits%8));
      _bitstuffed_frame[frame_length] = 0xFF & (0x7E00 >> frame_length_bits%8);

      // send the vector as a PDU
      pmt::pmt_t vecpmt(pmt::make_blob(_bitstuffed_frame, frame_length + 1));
      pmt::pmt_t output_pdu(pmt::cons(pmt::PMT_NIL, vecpmt));
      message_port_pub(pmt::mp("pdu_out"), output_pdu);

    }

  } /* namespace ax25 */
} /* namespace gr */
