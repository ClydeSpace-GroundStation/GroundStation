/* -*- c++ -*- */
/*
 * Copyright 2016 <+YOU OR YOUR COMPANY+>.
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

#include <gnuradio/io_signature.h>
#include "pdu_prepend_append_impl.h"

namespace gr {
  namespace ax25 {

    pdu_prepend_append::sptr
    pdu_prepend_append::make(int prepend_length, int append_length, uint8_t fill_byte)
    {
      return gnuradio::get_initial_sptr
        (new pdu_prepend_append_impl(prepend_length, append_length, fill_byte));
    }

    /*
     * The private constructor
     */
    pdu_prepend_append_impl::pdu_prepend_append_impl(int prepend_length, int append_length, uint8_t fill_byte)
      : gr::block("pdu_prepend_append",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(0, 0, 0))
    {

      // save the block inputs to the class
      _prepend_length = prepend_length;
      _append_length = append_length;
      _fill_byte = fill_byte;

      // create a PDU output port
      message_port_register_out(pmt::mp("pdu_out"));

      // create a PDU input port and bind the to message handler function
      message_port_register_in(pmt::mp("pdu_in"));
      set_msg_handler(pmt::mp("pdu_in"), boost::bind(&pdu_prepend_append_impl::output_frame, this, _1));

    }

    /*
     * Our virtual destructor.
     */
    pdu_prepend_append_impl::~pdu_prepend_append_impl()
    {
    }



    /*
    *   Receiced PDU handler.  Once called this function rearranges the data
    *   into the correct RS codeblocks, performs decoding and transmits a PDU
    *   of the original space frame packet
    */
    void pdu_prepend_append_impl::output_frame(pmt::pmt_t input_pdu)
    {

      // deconstruct the input PDU
      pmt::pmt_t meta = pmt::car(input_pdu);
      pmt::pmt_t vector = pmt::cdr(input_pdu);

      // retrieve the data
      size_t offset(0);
      const uint8_t* input_data = (const uint8_t*) pmt::uniform_vector_elements(vector, offset);
      int input_data_length = pmt::blob_length(vector);


      // create a PDU array that is long enough to store the prepended/appended array
      uint8_t frame[input_data_length + _prepend_length + _append_length];

      // deal with the prepending
      // are we adding or removing data?
      if(_prepend_length < 0) {

        // fill the data
        memcpy(frame, &input_data[-_prepend_length], input_data_length - _prepend_length - floor(-_append_length));

      } else {
        // fill the prepend
        memset(frame, _fill_byte, _prepend_length);

        // fill the data
        memcpy(&frame[_prepend_length], input_data, input_data_length);
      }

      // deal with the appending
      if(_append_length > 0) {

        // fill the append
        memset(&frame[_prepend_length + input_data_length], _fill_byte, _append_length);

      }

      // send the vector as a PDU
      pmt::pmt_t vecpmt(pmt::make_blob(frame, _prepend_length + input_data_length + _append_length));
      pmt::pmt_t output_pdu(pmt::cons(pmt::PMT_NIL, vecpmt));
      message_port_pub(pmt::mp("pdu_out"), output_pdu);

    }




  } /* namespace ax25 */
} /* namespace gr */
