/* -*- c++ -*- */
/* 
 * Copyright 2012 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING. If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_EC_DESCRAMBLER_BB_H
#define INCLUDED_EC_DESCRAMBLER_BB_H

#include <ec_api.h>
#include <gnuradio/sync_block.h>

class ec_descrambler_bb;
typedef boost::shared_ptr<ec_descrambler_bb> ec_descrambler_bb_sptr;

EC_API ec_descrambler_bb_sptr ec_make_descrambler_bb (unsigned int tap_mask, unsigned int preload);

/*!
* \brief <+description+>
*
*/
class EC_API ec_descrambler_bb : public gr::sync_block
{
friend EC_API ec_descrambler_bb_sptr ec_make_descrambler_bb (unsigned int tap_mask, unsigned int preload);

ec_descrambler_bb (unsigned int tap_mask, unsigned int preload);

  unsigned int d_shift_register;
  int          d_taps[32];
  int          d_tap_count;

public:
~ec_descrambler_bb ();


int work (int noutput_items,
gr_vector_const_void_star &input_items,
gr_vector_void_star &output_items);
};

#endif /* INCLUDED_EC_DESCRAMBLER_BB_H */

