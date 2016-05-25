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

#ifndef INCLUDED_AX25_NRZI_ENCODER_IMPL_H
#define INCLUDED_AX25_NRZI_ENCODER_IMPL_H

#include <ax25/nrzi_encoder.h>

namespace gr {
  namespace ax25 {

    class nrzi_encoder_impl : public nrzi_encoder
    {
     private:
      unsigned char _last_bit;
      int _polarity;

     public:
      nrzi_encoder_impl(int polarity);
      ~nrzi_encoder_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace ax25
} // namespace gr

#endif /* INCLUDED_AX25_NRZI_ENCODER_IMPL_H */
