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


#ifndef INCLUDED_CHANNELCODING_BINARY_SYMMETRIC_CHANNEL_H
#define INCLUDED_CHANNELCODING_BINARY_SYMMETRIC_CHANNEL_H

#include <channelcoding/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace channelcoding {

    /*!
     * \brief <+description of block+>
     * \ingroup channelcoding
     *
     */
    class CHANNELCODING_API binary_symmetric_channel : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<binary_symmetric_channel> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of channelcoding::binary_symmetric_channel.
       *
       * To avoid accidental use of raw pointers, channelcoding::binary_symmetric_channel's
       * constructor is in a private implementation
       * class. channelcoding::binary_symmetric_channel::make is the public interface for
       * creating new instances.
       */
      static sptr make(float ber, unsigned bits_per_byte, long seed);
    };

  } // namespace channelcoding
} // namespace gr

#endif /* INCLUDED_CHANNELCODING_BINARY_SYMMETRIC_CHANNEL_H */

