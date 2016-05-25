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

#ifndef INCLUDED_EC_INVERT_BIT_VALUES_BB_H
#define INCLUDED_EC_INVERT_BIT_VALUES_BB_H

#include <ec_api.h>
#include <gnuradio/sync_block.h>

class ec_invert_bit_values_bb;
typedef boost::shared_ptr<ec_invert_bit_values_bb> ec_invert_bit_values_bb_sptr;

EC_API ec_invert_bit_values_bb_sptr ec_make_invert_bit_values_bb ();

/*!
* \brief <+description+>
*
*/
class EC_API ec_invert_bit_values_bb : public gr::sync_block
{
friend EC_API ec_invert_bit_values_bb_sptr ec_make_invert_bit_values_bb ();

ec_invert_bit_values_bb ();

public:
~ec_invert_bit_values_bb ();


int work (int noutput_items,
gr_vector_const_void_star &input_items,
gr_vector_void_star &output_items);
};

#endif /* INCLUDED_EC_INVERT_BIT_VALUES_BB_H */

