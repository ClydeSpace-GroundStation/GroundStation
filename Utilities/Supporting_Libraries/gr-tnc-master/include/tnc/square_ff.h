/* -*- c++ -*- */
/* 
 * Copyright 2014 <+YOU OR YOUR COMPANY+>.
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


#ifndef INCLUDED_TNC_SQUARE_FF_H
#define INCLUDED_TNC_SQUARE_FF_H

#include <tnc/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace tnc {

    /*!
     * \brief <+description of block+>
     * \ingroup tnc
     *
     */
    class TNC_API square_ff : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<square_ff> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of tnc::square_ff.
       *
       * To avoid accidental use of raw pointers, tnc::square_ff's
       * constructor is in a private implementation
       * class. tnc::square_ff::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace tnc
} // namespace gr

#endif /* INCLUDED_TNC_SQUARE_FF_H */

