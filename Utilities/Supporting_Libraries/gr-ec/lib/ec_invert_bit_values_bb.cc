/* -*- c++ -*- */
/* 
 * Copyright 2012 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING. If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <ec_invert_bit_values_bb.h>


ec_invert_bit_values_bb_sptr
ec_make_invert_bit_values_bb ()
{
return ec_invert_bit_values_bb_sptr (new ec_invert_bit_values_bb ());
}


ec_invert_bit_values_bb::ec_invert_bit_values_bb ()
     : gr::sync_block ("invert_bit_values_bb",
		       gr::io_signature::make (1, 1, sizeof (unsigned char)),
		       gr::io_signature::make (1, 1, sizeof (unsigned char)))
{
}


ec_invert_bit_values_bb::~ec_invert_bit_values_bb ()
{
}


int
ec_invert_bit_values_bb::work (int noutput_items,
			       gr_vector_const_void_star &input_items,
			       gr_vector_void_star &output_items)
{
const unsigned char *in = (const unsigned char *) input_items[0];
unsigned char *out = (unsigned char *) output_items[0];
  unsigned char        bit_in;
  unsigned char        bit_out;
  for (int i = 0; i < noutput_items; i++)
    {   if(in[i] == 0)
          {
            out[i] = 1;
          }
        else
          {
            out[i] = 0;
          }
        //out[i] = bit_out;

    }
// Do <+signal processing+>

// Tell runtime system how many output items we produced.
return noutput_items;
}

