/* -*- c++ -*- */
/*
 * Copyright 2016 Clyde Space.
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

#ifndef INCLUDED_AX25_AX25_ENCODER_IMPL_H
#define INCLUDED_AX25_AX25_ENCODER_IMPL_H

#include <ax25/ax25_encoder.h>

namespace gr {
  namespace ax25 {

    class ax25_encoder_impl : public ax25_encoder
    {
     private:
      uint8_t _dest_addr[6];
      uint8_t _src_addr[6];
      uint8_t _dest_ssid;
      uint8_t _src_ssid;

      // maximum number of bytes is 274
      // does not include bit stuffing or the flags at either end of the frame
      uint8_t _frame[274];

      // bit stuff the frame
      // maximum number of bytes is 331
      // 2192 bits / 5 + 2192 bits = 2631 bits = 329 bytes
      // add pre and post flag bytes, max frame length = 329 + 2 = 331 bytes
      uint8_t _bitstuffed_frame[331];

      uint8_t bit_reverse(uint8_t data);
      void bit_reverse_arr(uint8_t *data, uint32_t length);
      void add_header();
      void add_CRC( uint32_t input_data_length );
      uint32_t bit_stuff( uint8_t *in, uint8_t *out, uint32_t N);
      void output_frame(pmt::pmt_t input_pdu);

     public:
      ax25_encoder_impl(const std::string &dest_addr, const std::string &src_addr, int dest_ssid, int src_ssid);
      ~ax25_encoder_impl();

    };

  } // namespace ax25
} // namespace gr

#endif /* INCLUDED_AX25_AX25_ENCODER_IMPL_H */
