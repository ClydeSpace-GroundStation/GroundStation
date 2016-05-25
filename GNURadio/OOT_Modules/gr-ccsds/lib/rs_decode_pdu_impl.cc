/* -*- c++ -*- */
/*
 * Copyright 2016 -  Thomas Parry - Clyde Space.
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

#include "rs_decode_pdu_impl.h"
#include "fec.h"
#include <iomanip>
#include <gnuradio/io_signature.h>


namespace gr {
  namespace ccsds {

    rs_decode_pdu::sptr
    rs_decode_pdu::make(int interleave)
    {
      return gnuradio::get_initial_sptr
        (new rs_decode_pdu_impl(interleave));
    }

    /*
     * The private constructor
     */
    rs_decode_pdu_impl::rs_decode_pdu_impl(int interleave)
      : gr::block("rs_decode_pdu",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(0, 0, 0))
    {
      _interleave = interleave;

      // create a PDU output port
      message_port_register_out(pmt::mp("pdu_out"));

      // create a PDU input port and bind the to message handler function
      message_port_register_in(pmt::mp("pdu_in"));
      set_msg_handler(pmt::mp("pdu_in"), boost::bind(&rs_decode_pdu_impl::output_frame, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    rs_decode_pdu_impl::~rs_decode_pdu_impl()
    {
    }

    /*
    *   Receiced PDU handler.  Once called this function rearranges the data
    *   into the correct RS codeblocks, performs decoding and transmits a PDU
    *   of the original space frame packet
    */
    void rs_decode_pdu_impl::output_frame(pmt::pmt_t input_pdu)
    {

      // deconstruct the input PDU
      pmt::pmt_t meta = pmt::car(input_pdu);
      pmt::pmt_t vector = pmt::cdr(input_pdu);

      // retrieve the data
      size_t offset(0);
      const uint8_t* input_data = (const uint8_t*) pmt::uniform_vector_elements(vector, offset);

      // sort the input data into the RS codeblocks
      for(int n=0; n < _interleave*NN; n++) {
        _data[n%_interleave][(int)n/_interleave] = input_data[n];
      }

      // reset the failure flag
      _failure = 0;

      // perfrom decoding of each block and copy to output
      for(int n=0; n < _interleave; n++) {

        // decode the RS codewords
        int result = decode_rs_ccsds(&_data[n][0], &_error_positions[n][0], 0, 0);

        // test for failure
        _failure += result;
      }

      // decide what to do with the failed codeblocks
      if(_failure) {

        // decoding has failed!
        // std::cout << "Reed Solomon decoding has failed!" << std::endl;

      } else {

        // decoding has worked
        // std::cout << "Reed Solomon decoding has succeeded!" << std::endl;

        // rearrange the codeblocks into the corrcect original message
        std::vector<unsigned char> output_vector((NN-NROOTS) * _interleave);

        for(int n=0; n < ((NN-NROOTS) * _interleave); n++) {
          output_vector[n] = _data[n%_interleave][n/_interleave];
        }

        // send the vector as a PDU
        pmt::pmt_t vecpmt(pmt::make_blob(&output_vector[0], (NN-NROOTS) * _interleave));
        pmt::pmt_t output_pdu(pmt::cons(pmt::PMT_NIL, vecpmt));
        message_port_pub(pmt::mp("pdu_out"), output_pdu);

      }
    }

  } /* namespace ccsds */
} /* namespace gr */
