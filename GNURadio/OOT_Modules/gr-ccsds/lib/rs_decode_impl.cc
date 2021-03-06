/* -*- c++ -*- */
/*
 * Copyright 2015 <+YOU OR YOUR COMPANY+>.
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
#include "rs_decode_impl.h"
#include <cstdio>
#include "rs_encode_impl.h"
#include "fec.h"

namespace gr {
  namespace ccsds {

    rs_decode::sptr
    rs_decode::make(int interleave)
    {
      return gnuradio::get_initial_sptr
        (new rs_decode_impl(interleave));
    }

    /*
     * The private constructor
     */
    rs_decode_impl::rs_decode_impl(int interleave)
      : gr::block("rs_decode",
              gr::io_signature::make(1, 1, sizeof(unsigned char)),
              gr::io_signature::make(1, 1, sizeof(unsigned char)))
    {
	     // initialise variables
       _data_index = 0;
       _data_array_index = 0;

       if(interleave < 1) {
         _interleave = 1;
       } else if(interleave > 6) {
         _interleave = 5;
       } else {
         _interleave = interleave - 1;
       }
       memset(_number_of_errors,0,6);
     }

    /*
     * Our virtual destructor.
     */
    rs_decode_impl::~rs_decode_impl()
    {
    }

    void
    rs_decode_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        ninput_items_required[0] = noutput_items;
    }

    int
    rs_decode_impl::general_work (int noutput_items,
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

	       // read in data to internal array
         _data[_data_array_index][_data_index] = in[i];

         // increment the data indexes
         if(_data_array_index < _interleave) {
           _data_array_index++;
         } else {
           _data_array_index = 0;
           _data_index++;
         }

         // count number of samples received
         nconsumed++;

         ///_error_positions[1][1] = 3;

         // we have enough samples, can now decode block(s)
         if(_data_index >= NN) {

           // perfrom decoding of each block and copy to output
           for(int n=0; n < (_interleave+1); n++) {
             int result = decode_rs_ccsds(&_data[n][0], &_error_positions[n][0], _number_of_errors[0], 0);
             std::cout << result << std::endl;

            //  // output the decoded data (old method)
            //  memcpy(&out[n*(NN-NROOTS)],&_data[n][0],NN-NROOTS);

             // output the decoded data (new method)
             for(int m=0; m < NN; m++) {
               out[m*(_interleave+1) + n] = _data[n][m];
              //  printf("Sample: %d",m);
              //  printf("\t%x",_data[n][m]);
              //  printf("\tout_index: %d\n",m*(_interleave+1) + n);
             }
           }



           // reset the data indices
           _data_index = 0;
           _data_array_index = 0;

           // tell the runtime how many samples have been received
           consume_each(nconsumed);

           // tell runtime system we've created a RS codeblock
           nproduced = (NN-NROOTS)*(_interleave+1);
           return nproduced;

         }
       }

       // tell the runtime how many samples have been received
       consume_each(nconsumed);

       // tell runtime system how many output items we produced (none).
       return nproduced;
    }

  } /* namespace ccsds */
} /* namespace gr */
