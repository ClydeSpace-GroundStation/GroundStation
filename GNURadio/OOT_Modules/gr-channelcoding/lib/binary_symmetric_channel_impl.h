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

#ifndef INCLUDED_CHANNELCODING_BINARY_SYMMETRIC_CHANNEL_IMPL_H
#define INCLUDED_CHANNELCODING_BINARY_SYMMETRIC_CHANNEL_IMPL_H

#include <channelcoding/binary_symmetric_channel.h>
#include <gnuradio/random.h>
// #include <gnuradio/thread.h>

namespace gr {
  namespace channelcoding {

    class binary_symmetric_channel_impl : public binary_symmetric_channel
    {
     private:
      //  friend chancoding_bsc_bb_sptr chancoding_make_bsc_bb (float ber, unsigned bits_per_byte, long seed);

 

 	     float d_ber;
 	     int d_bits_per_byte;
 	     gr::random d_random;
 	     gr::thread::mutex d_mutex;

     public:
      binary_symmetric_channel_impl(float ber, unsigned bits_per_byte, long seed);
      ~binary_symmetric_channel_impl();

      float ber() { return d_ber; };
	    void set_ber(float ber);

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace channelcoding
} // namespace gr

#endif /* INCLUDED_CHANNELCODING_BINARY_SYMMETRIC_CHANNEL_IMPL_H */
