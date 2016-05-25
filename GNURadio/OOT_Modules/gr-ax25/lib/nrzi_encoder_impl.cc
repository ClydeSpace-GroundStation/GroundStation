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
#include "nrzi_encoder_impl.h"

namespace gr {
  namespace ax25 {

    nrzi_encoder::sptr
    nrzi_encoder::make(int polarity)
    {
      return gnuradio::get_initial_sptr
        (new nrzi_encoder_impl(polarity));
    }

    /*
     * The private constructor
     */
    nrzi_encoder_impl::nrzi_encoder_impl(int polarity)
      : gr::sync_block("nrzi_encoder",
              gr::io_signature::make(1, 1, sizeof(unsigned char)),
              gr::io_signature::make(1, 1, sizeof(unsigned char)))
    {
        _polarity = polarity;
        _last_bit = 0;
    }

    /*
     * Our virtual destructor.
     */
    nrzi_encoder_impl::~nrzi_encoder_impl()
    {
    }

    int
    nrzi_encoder_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out = (unsigned char *) output_items[0];

      for(int i = 0; i < noutput_items; i++) {
        if(in[i] == _polarity) {
          if(_last_bit) {
            out[i] = 0;
            _last_bit = 0;
          } else {
            out[i] = 1;
            _last_bit = 1;
          }
        } else {
          out[i] = _last_bit;
        }
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace ax25 */
} /* namespace gr */
