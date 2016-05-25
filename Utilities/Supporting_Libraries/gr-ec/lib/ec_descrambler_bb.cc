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
#include <ec_descrambler_bb.h>
#include <stdexcept>


ec_descrambler_bb_sptr
ec_make_descrambler_bb (unsigned int tap_mask, unsigned int preload)
{
return ec_descrambler_bb_sptr (new ec_descrambler_bb (tap_mask, preload));
}


ec_descrambler_bb::ec_descrambler_bb (unsigned int tap_mask, unsigned int preload)
     : gr::sync_block ("descrambler_bb",
		       gr::io_signature::make (1, 1, sizeof (unsigned char)),
		       gr::io_signature::make (1, 1, sizeof (unsigned char))),
           d_shift_register(preload)
{
    // EXCEPTION TEST FOR tap_mask containing bit 0
    if((tap_mask&0x01) == 1)
      {
        /*fprintf(stderr, "derandomize_b: tap_mask cannot contain bit 0).\n");
        throw std::invalid_argument ("derandomize_b: tap_mask cannot contain bit 0).");*/
      }

    // Record which bits are set in the tap_mask
    d_tap_count = 0;
    for(int i=0; i<32; i++)
      {
        if(tap_mask&0x01 == 1)
          {
            d_taps[d_tap_count] = i;
            d_tap_count++;
          }
        tap_mask = tap_mask >> 1;
      }
}

ec_descrambler_bb::~ec_descrambler_bb ()
{
}



int
ec_descrambler_bb::work (int                       noutput_items,
			             gr_vector_const_void_star &input_items,
			             gr_vector_void_star       &output_items)
{
  const unsigned char* in  = (const unsigned char *) input_items[0];
  unsigned char*       out = (unsigned char *) output_items[0];
  unsigned char        unscrambled_bit;
  unsigned char        scrambled_bit;
  int                  tap_bit;

  for (int i = 0; i < noutput_items; i++)
    {
        // Get next bit
        scrambled_bit = in[i] & 0x01;

        // Shift the shift_register left by one bit
        d_shift_register <<= 1;

        // Compute the XOR of the scrambled bit and the selected tap bits.
        unscrambled_bit = scrambled_bit;
        for(int t=0; t<d_tap_count; t++)
          {
            tap_bit = (d_shift_register >> d_taps[t]) & 0x01;
            unscrambled_bit = unscrambled_bit ^ tap_bit;
          }

        // Feed scrambled bit into shift register
        d_shift_register |= scrambled_bit;

        // Output the unscrambled bit
        out[i] = unscrambled_bit;
    }
  return noutput_items;
}
