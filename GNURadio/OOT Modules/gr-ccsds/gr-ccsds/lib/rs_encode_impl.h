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

#ifndef INCLUDED_CCSDS_RS_ENCODE_IMPL_H
#define INCLUDED_CCSDS_RS_ENCODE_IMPL_H

#include <ccsds/rs_encode.h>

#define NN 255
#define NROOTS 32

namespace gr {
  namespace ccsds {

    class rs_encode_impl : public rs_encode
    {
     private:

      // data arrays used for interleaving blocks
      unsigned char _data[6*NN];
      int _data_index;
      int _data_array_index;
      int _interleave;


     public:
      rs_encode_impl(int interleave);
      ~rs_encode_impl();

      // getter and setters
      void set_interleave(int interleave) { 
	if(interleave < 1) {
		_interleave = 1;
	} else if(interleave > 6) {
		_interleave = 5;
	} else {		
		_interleave = interleave - 1;
	}
      };


      int interleave() const { return _interleave; };

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
		       gr_vector_int &ninput_items,
		       gr_vector_const_void_star &input_items,
		       gr_vector_void_star &output_items);
    };

  } // namespace ccsds
} // namespace gr

#endif /* INCLUDED_CCSDS_RS_ENCODE_IMPL_H */

