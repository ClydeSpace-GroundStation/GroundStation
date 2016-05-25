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
#include "asm_deframer_impl.h"
#include <cstdio>

namespace gr {
  namespace ccsds {

    asm_deframer::sptr
    asm_deframer::make(int distance, int interleave, int randomise, int block_size)
    {
      return gnuradio::get_initial_sptr
        (new asm_deframer_impl(distance, interleave, randomise, block_size));
    }

    /*
     * The private constructor
     */
    asm_deframer_impl::asm_deframer_impl(int distance, int interleave, int randomise, int block_size)
      : gr::block("asm_deframer",
              gr::io_signature::make(1, 1, sizeof(unsigned char)),
              gr::io_signature::make(1, 1, sizeof(unsigned char)))
    {
      _distance = distance;
      _interleave = interleave;
      _randomise = randomise;
      _block_size = block_size;

      _data_shift_reg = 0;
      _state = ACCESS_CODE;
      _byte_out = 0;
      _count_samples = 0;
      _out_i = 0;

      // set up the tagged output
      std::stringstream str;
      str << name() << unique_id();
      d_me = pmt::string_to_symbol(str.str());
      d_key = pmt::string_to_symbol("packet_length");


      unsigned char temp_array[255] = {255, 72, 14, 192, 154, 13, 112, 188, 142, 44, 147, 173, 167, 183, 70, 206, 90, 151, 125, 204, 50, 162, 191, 62, 10, 16, 241, 136, 148, 205,
					234, 177, 254, 144, 29, 129, 52, 26, 225, 121, 28, 89, 39, 91, 79, 110, 141, 156, 181, 46, 251, 152, 101, 69, 126, 124, 20, 33, 227, 17, 41,
					155, 213, 99, 253, 32, 59, 2, 104, 53, 194, 242, 56, 178, 78, 182, 158, 221, 27, 57, 106, 93, 247, 48, 202, 138, 252, 248, 40, 67, 198, 34,
					83, 55, 170, 199, 250, 64, 118, 4, 208, 107, 133, 228, 113, 100, 157, 109, 61, 186, 54, 114, 212, 187, 238, 97, 149, 21, 249, 240, 80, 135,
					140, 68, 166, 111, 85, 143, 244, 128, 236, 9, 160, 215, 11, 200, 226, 201, 58, 218, 123, 116, 108, 229, 169, 119, 220, 195, 42, 43, 243, 224,
					161, 15, 24, 137, 76, 222, 171, 31, 233, 1, 216, 19, 65, 174, 23, 145, 197, 146, 117, 180, 246, 232, 217, 203, 82, 239, 185, 134, 84, 87, 231,
					193, 66, 30, 49, 18, 153, 189, 86, 63, 210, 3, 176, 38, 131, 92, 47, 35, 139, 36, 235, 105, 237, 209, 179, 150, 165, 223, 115, 12, 168, 175,
					207, 130, 132, 60, 98, 37, 51, 122, 172, 127, 164, 7, 96, 77, 6, 184, 94, 71, 22, 73, 214, 211, 219, 163, 103, 45, 75, 190, 230, 25, 81, 95,
					159, 5, 8, 120, 196, 74, 102, 245, 88};

      memcpy(_random_array,temp_array,255*sizeof(unsigned char));

    }

    /*
     * Our virtual destructor.
     */
    asm_deframer_impl::~asm_deframer_impl()
    {
    }

    void
    asm_deframer_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = 8*noutput_items;
    }

    int
    asm_deframer_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out = (unsigned char *) output_items[0];
      unsigned int hamming_distance = 0;
      unsigned int n_produced = 0;

      uint64_t abs_out_sample_cnt = nitems_written(0);

      // Do <+signal processing+>
      for (int i = 0; i < noutput_items; i++) {

	       // shift in data to shift register
         _data_shift_reg = (_data_shift_reg << 1) | (in[i] & 1);
         _count_samples++;

         // state machine
         switch(_state) {

           case ACCESS_CODE:

           // compute the hamming hamming_distance between shift register and preamble
           hamming_distance = (_data_shift_reg & 0xFFFFFFFF) ^ _asm_preamble;
           hamming_distance = ((hamming_distance & 0xAAAAAAAA) >> 1) + (hamming_distance & 0x55555555);
           hamming_distance = ((hamming_distance & 0xCCCCCCCC) >> 2) + (hamming_distance & 0x33333333);
           hamming_distance = ((hamming_distance & 0xF0F0F0F0) >> 4) + (hamming_distance & 0x0F0F0F0F);
           hamming_distance = (hamming_distance >> 24) + ((hamming_distance >> 16) & 0x0F) + ((hamming_distance >> 8) & 0x0F) + (hamming_distance & 0x0F);

           // does the hamming_distance meet the requirements for preamble match
           if (hamming_distance <= _distance) {

             std::cout << "found" << std::endl;
             _state = DATA;
             _nshift = 0;
             _data_shift_reg = 0;
             add_item_tag( 0,                                           // stream id
                          abs_out_sample_cnt,                           // sample
                          d_key,                                        // frame info
                          pmt::from_long((_interleave+1)*_block_size),  // data size of frame
		                      d_me                                          // block src id
		                      );
           }
           break;

           case DATA:

           // if a byte has been received, save it
           //if (((++_nshift) % 8) == 0) {
           if (++_nshift >= 8) {

             // derandomise the data?
             if(_randomise == 1) {
               out[n_produced] = (_data_shift_reg & 0xFF) ^ _random_array[_out_i%_block_size];
             } else {
               out[n_produced] = _data_shift_reg & 0xFF;
             }

             // increment the sample index
             _out_i++;
             n_produced++;

             _data_shift_reg = 0;
             _nshift = 0;

             // full frame has been found, switch to access code state
             if (_out_i == _block_size*_interleave) {
               _state = ACCESS_CODE;
               _data_shift_reg = 0;
               _nshift = 0;
               _out_i = 0;
             }
           }
           break;
         }
       }

       // Tell runtime system how many input items we consumed on
       // each input stream.
       consume_each(noutput_items);

        // Tell runtime system how many output items we produced.
        return n_produced;
    }

  } /* namespace ccsds */
} /* namespace gr */
