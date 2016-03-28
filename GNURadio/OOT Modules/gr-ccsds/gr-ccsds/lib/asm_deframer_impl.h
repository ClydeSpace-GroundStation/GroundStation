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

#ifndef INCLUDED_CCSDS_ASM_DEFRAMER_IMPL_H
#define INCLUDED_CCSDS_ASM_DEFRAMER_IMPL_H

#include <ccsds/asm_deframer.h>


namespace gr {
  namespace ccsds {

    class asm_deframer_impl : public asm_deframer
    {
     private:
      	static const unsigned int _asm_preamble = 0x1ACFFC1D;  //0xB83FF358;
        unsigned char _random_array[255*6];
        unsigned int _data_shift_reg;
        unsigned int _nshift;
        unsigned char _frame;
        unsigned char _byte_out;
        unsigned long _count_samples;
        unsigned int _out_i;
        int _randomise;
        int _distance;			// the hanmming distance to mark finding preamble
        int _interleave;

        enum {
          ACCESS_CODE=0,
          DATA=1
        } _state;

      public:
        asm_deframer_impl(int distance, int interleave, int randomise);
        ~asm_deframer_impl();

      void set_distance(int distance) { _distance = distance; };
      int distance() const { return _distance; };

      void set_interleave(int interleave) { _interleave = interleave; };
      int interleave() const { return _interleave; };

      void set_randomise(int randomise) { _randomise = randomise; };
      int randomise() const { return _randomise; };



      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
		       gr_vector_int &ninput_items,
		       gr_vector_const_void_star &input_items,
		       gr_vector_void_star &output_items);
    };

  } // namespace ccsds
} // namespace gr

#endif /* INCLUDED_CCSDS_ASM_DEFRAMER_IMPL_H */
