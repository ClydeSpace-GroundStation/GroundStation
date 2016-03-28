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
	_interleave = interleave;
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

		// read in data to internal array
		_data[_data_index] = in[i];

		// increment the data index
		_data_index++;

		// count number of samples received
		nconsumed++;

        	// we have enough samples, can now encode block
		if(_data_index >= interleave*(NN - NROOTS)) {

			// perfrom encoding of each block and copy to output
			for(int n=0; n < (_interleave+1); n++) {
				encode_rs_ccsds(&_data[n*NN], &_data[n*NN+(NN-NROOTS)], 0);
				//memcpy(&out[n*NN],&_data[n][0],NN);
			}

			// interleaving variables
			int x = 0;
			int y = 0;
			int n = 0;

			//perform the interleaving of the output
			while(int n=0; n >= NN; n++) {
				out[x*NN + y] = _data[n];
				n++;
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

