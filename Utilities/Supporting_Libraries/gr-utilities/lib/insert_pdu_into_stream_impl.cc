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
#include "insert_pdu_into_stream_impl.h"

namespace gr {
  namespace utilities {

    insert_pdu_into_stream::sptr
    insert_pdu_into_stream::make(output_type)
    {
      return gnuradio::get_initial_sptr
        (new insert_pdu_into_stream_impl(output_type));
    }

    /*
     * The private constructor
     */
    insert_pdu_into_stream_impl::insert_pdu_into_stream_impl(output_type)
      : gr::block("insert_pdu_into_stream",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(1, 1, sizeof(unsigned char)))
    {
      // initialise the buffer counters
      buffer_position = 0;
      buffer_remaining = 0;

      // create a PDU output port
      message_port_register_out(pmt::mp("pdu_out"));

      // create a PDU input port and bind the to message handler function
      message_port_register_in(pmt::mp("pdu_in"));
      set_msg_handler(pmt::mp("pdu_in"), boost::bind(&ax25_encoder_impl::output_frame, this, _1));

    }

    /*
     * Our virtual destructor.
     */
    insert_pdu_into_stream_impl::~insert_pdu_into_stream_impl()
    {
    }

    void
    insert_pdu_into_stream_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
    }


    /*
    *   Receiced PDU handler, save to an internal array and add to output stream in general work
    */
    void ax25_encoder_impl::output_frame(pmt::pmt_t input_pdu)
    {

      // deconstruct the input PDU
      pmt::pmt_t meta = pmt::car(input_pdu);
      pmt::pmt_t vector = pmt::cdr(input_pdu);

      // retrieve the data
      size_t offset(0);
      const uint8_t* input_data = (const uint8_t*) pmt::uniform_vector_elements(vector, offset);
      int input_data_length = pmt::blob_length(vector);

      // add the
      buffer_remaining += input_data_length;

      // test if we have enough space for the new data
      if(buffer_remaining > BUFFER_SIZE) {
        std::cout << "Error! buffer is full" << std::endl;
      }

      // test if we have to wrap around the buffer
      if((buffer_position + input_data_length) > (BUFFER_SIZE - 1)) {

      }

      // insert the information into the frame
      memcpy(&_frame[16], &input_data[0], input_data_length);

    }


    int
    insert_pdu_into_stream_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out = (unsigned char *) output_items[0];

      // count how many samples come into and out of the module
      int nconsumed = 0;
      int nproduced = 0;

      // can we output new samples?
      for (int i = 0; i < noutput_items; i++) {


       }

       // tell the runtime how many samples have been received
       consume_each(nconsumed);

       // tell runtime system how many output items we produced (none).
       return nproduced;
    }

  } /* namespace utilities */
} /* namespace gr */
