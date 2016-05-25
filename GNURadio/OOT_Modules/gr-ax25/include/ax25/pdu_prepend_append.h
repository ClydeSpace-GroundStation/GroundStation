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


#ifndef INCLUDED_AX25_PDU_PREPEND_APPEND_H
#define INCLUDED_AX25_PDU_PREPEND_APPEND_H

#include <ax25/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace ax25 {

    /*!
     * \brief <+description of block+>
     * \ingroup ax25
     *
     */
    class AX25_API pdu_prepend_append : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<pdu_prepend_append> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of ax25::pdu_prepend_append.
       *
       * To avoid accidental use of raw pointers, ax25::pdu_prepend_append's
       * constructor is in a private implementation
       * class. ax25::pdu_prepend_append::make is the public interface for
       * creating new instances.
       */
      static sptr make(int prepend_length, int append_length, uint8_t fill_byte);
    };

  } // namespace ax25
} // namespace gr

#endif /* INCLUDED_AX25_PDU_PREPEND_APPEND_H */
