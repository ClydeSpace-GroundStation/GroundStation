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


#ifndef INCLUDED_CCSDS_ASM_DEFRAMER_PDU_H
#define INCLUDED_CCSDS_ASM_DEFRAMER_PDU_H

#include <ccsds/api.h>
#include <gnuradio/block.h>
#include <gnuradio/blocks/pdu.h>

namespace gr {
  namespace ccsds {

    /*!
     * \brief <+description of block+>
     * \ingroup ccsds
     *
     */
    class CCSDS_API asm_deframer_pdu : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<asm_deframer_pdu> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of ccsds::asm_deframer_pdu.
       *
       * To avoid accidental use of raw pointers, ccsds::asm_deframer_pdu's
       * constructor is in a private implementation
       * class. ccsds::asm_deframer_pdu::make is the public interface for
       * creating new instances.
       */
      static sptr make(int distance, int interleave, int randomise, int block_size);
    };

  } // namespace ccsds
} // namespace gr

#endif /* INCLUDED_CCSDS_ASM_DEFRAMER_PDU_H */
