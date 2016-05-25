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

#ifndef INCLUDED_AX25_PDU_PREPEND_APPEND_IMPL_H
#define INCLUDED_AX25_PDU_PREPEND_APPEND_IMPL_H

#include <ax25/pdu_prepend_append.h>

namespace gr {
  namespace ax25 {

    class pdu_prepend_append_impl : public pdu_prepend_append
    {
     private:
      int _prepend_length;
      int _append_length;
      uint8_t _fill_byte;

     public:
      pdu_prepend_append_impl(int prepend_length, int append_length, uint8_t fill_byte);
      ~pdu_prepend_append_impl();

      void output_frame(pmt::pmt_t input_pdu);

    };

  } // namespace ax25
} // namespace gr

#endif /* INCLUDED_AX25_PDU_PREPEND_APPEND_IMPL_H */
