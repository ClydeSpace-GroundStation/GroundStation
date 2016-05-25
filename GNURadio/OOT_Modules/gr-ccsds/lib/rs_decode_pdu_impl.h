/* -*- c++ -*- */
/*
 * Copyright 2016 -  Thomas Parry - Clyde Space.
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

#ifndef INCLUDED_CCSDS_RS_DECODE_PDU_IMPL_H
#define INCLUDED_CCSDS_RS_DECODE_PDU_IMPL_H

// define the reed solomon code parameters
#define NN 255
#define NROOTS 32

#include <ccsds/rs_decode_pdu.h>

namespace gr {
  namespace ccsds {

    class rs_decode_pdu_impl : public rs_decode_pdu
    {
      private:
        int _interleave;
        unsigned char _data[6][NN];
        int _error_positions[6][NROOTS];
        int _number_of_errors[6];
        int _failure;

      public:
        rs_decode_pdu_impl(int interleave);
        ~rs_decode_pdu_impl();

        // getter and setters
        void set_interleave(int interleave) {
          if(interleave < 1) {
            _interleave = 1;
          } else if(interleave > 6) {
            _interleave = 5;
          } else {
            _interleave = interleave;
          }
        };

        int interleave() const { return _interleave; };

        void output_frame(pmt::pmt_t input_pdu);

    };

  } // namespace ccsds
} // namespace gr

#endif /* INCLUDED_CCSDS_RS_DECODE_PDU_IMPL_H */
