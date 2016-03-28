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
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.	If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <cstdio>
#include "rs_encode_impl.h"
#include "fec.h"

namespace gr {
  namespace ccsds {

		rs_encode::sptr
		rs_encode::make(int interleave)
		{
			return gnuradio::get_initial_sptr
				(new rs_encode_impl(interleave));
		}

		/*
		 * The private constructor
		 */
		rs_encode_impl::rs_encode_impl(int interleave)
			: gr::block("rs_encode",
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
		}

		/*
		 * Our virtual destructor.
		 */
		rs_encode_impl::~rs_encode_impl()
		{
		}

		void
		rs_encode_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
		{
	     ninput_items_required[0] = noutput_items;
		}

		int
		rs_encode_impl::general_work (int noutput_items,
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

          // printf("Data array index: %d",_data_array_index);
          // printf("\tData index: %d",_data_index);
          // printf("\t_data index: %d",NN*_data_array_index + _data_index);
          // printf("\t Data: %d\n",in[i]);

            // read in data to internal array
		        _data[NN*_data_array_index + _data_index] = in[i];

		        // // increment the data index
		        // if(_data_index < NN-NROOTS-1) {
			      //     _data_index++;
		        // } else {
			      //     _data_index = 0;
			      //     _data_array_index++;
		        // }

            // increment the data index
		        if(_data_array_index < _interleave) {
			          _data_array_index++;
		        } else {
			          _data_array_index = 0;
			          _data_index++;
		        }

		        // count number of samples received
		        nconsumed++;


            //
            // printf("\t term 1: %d, term 2: %d\n",(_data_index+1)*(_data_array_index+1),((_interleave*NN)+(NN-NROOTS-1)));

			      // we have enough samples, can now encode block(s)
            if((_data_index+1)*(_data_array_index+1) > ((_interleave+1)*(NN-NROOTS))) {

                // printf("here2");

                // perfrom encoding of each block and copy to output
                for(int n=0; n < (_interleave+1); n++) {
                    encode_rs_ccsds(&_data[n*NN], &_data[NN*(n+1)-NROOTS], 0);
                    // printf("here");
                }

			          // interleaving variables
			          int x = 0;
			          int y = 0;
			          int n = 0;

			          // //perform the interleaving of the output (old method)
			          // while(x < NN) {
                //
                //   out[n] = _data[y*NN + x];
				        //   n++;
                //
				        //   if(y >= _interleave) {
					      //       x++;
					      //       y=0;
				        //   } else {
					      //       y++;
				        //   }
			          // }

                //perform the interleaving of the output (new method)
			          while(x < NN*_interleave) {

                  //printf("n: %d\ty: %d\tx: %d\tNN: %d\tindex: %d\tdata: %d\n",n,y,x,NN,y*NN + x,_data[y*NN + x]);

                  out[n] = _data[y*NN + x];
				          n++;

                  if(y < (_interleave)) {
                    y++;
                  } else {
                    x++;
                    y=0;
                  }
			          }

			          // reset the data indices
			          _data_index = 0;
			          _data_array_index = 0;

			          // tell the runtime how many samples have been received
			          consume_each(nconsumed);

			          // tell runtime system we've created a RS codeblock
			          nproduced = NN*(_interleave+1);
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
