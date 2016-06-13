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

#ifndef INCLUDED_CCSDS_ASM_DEFRAMER_PDU_IMPL_H
#define INCLUDED_CCSDS_ASM_DEFRAMER_PDU_IMPL_H

#include <vector>
#include <ccsds/asm_deframer_pdu.h>

namespace gr {
  namespace ccsds {

    class asm_deframer_pdu_impl : public asm_deframer_pdu
    {
     private:
      // pdu::vector_type     d_type;
      std::vector<unsigned char> _output_vector;
      // _output_vector.reserve(6*255);

      pmt::pmt_t           d_pdu_meta;
      pmt::pmt_t           d_pdu_vector;

      static const unsigned int _asm_preamble = 0x1ACFFC1D;  //0xB83FF358;
      unsigned char _random_array[255*6];
      unsigned char _output_array[255*6];
      unsigned int _data_shift_reg;
      unsigned int _nshift;
      unsigned char _frame;
      unsigned char _byte_out;
      unsigned long _count_samples;
      unsigned int _out_i;
      int _randomise;
      int _distance;			// the hanmming distance to mark finding preamble
      int _interleave;
      int _block_size;

      // pmt::pmt_t d_key, d_me; //d_key is the tag name, d_me is the block name + unique ID

      // FILE *f;


      enum {
        ACCESS_CODE=0,
        DATA=1
      } _state;

     public:
      asm_deframer_pdu_impl(int distance, int interleave, int randomise, int block_size);
      ~asm_deframer_pdu_impl();

      void set_distance(int distance) { _distance = distance; };
      int distance() const { return _distance; };

      void set_interleave(int interleave) { _interleave = interleave; };
      int interleave() const { return _interleave; };

      void set_randomise(int randomise) { _randomise = randomise; };
      int randomise() const { return _randomise; };

      void set_block_size(int block_size) { _block_size = block_size; };
      int block_size() const { return _block_size; };


      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
      // int work(int noutput_items,
		       gr_vector_int &ninput_items,
		       gr_vector_const_void_star &input_items,
		       gr_vector_void_star &output_items);
    };

  } // namespace ccsds
} // namespace gr

#endif /* INCLUDED_CCSDS_ASM_DEFRAMER_PDU_IMPL_H */
