/* -*- c++ -*- */

#define EC_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "ec_swig_doc.i"


%{
#include "ec_ax25_decoder_b.h"
#include "ec_descrambler_bb.h"
#include "ec_invert_bit_values_bb.h"
%}


GR_SWIG_BLOCK_MAGIC(ec,ax25_decoder_b);
%include "ec_ax25_decoder_b.h"

GR_SWIG_BLOCK_MAGIC(ec,descrambler_bb);
%include "ec_descrambler_bb.h"
GR_SWIG_BLOCK_MAGIC(ec,invert_bit_values_bb);
%include "ec_invert_bit_values_bb.h"
