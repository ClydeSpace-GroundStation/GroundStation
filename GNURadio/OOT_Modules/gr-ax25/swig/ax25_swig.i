/* -*- c++ -*- */

#define AX25_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "ax25_swig_doc.i"

%{
#include "ax25/ax25_encoder.h"
#include "ax25/pdu_prepend_append.h"
#include "ax25/nrzi_encoder.h"
%}


%include "ax25/ax25_encoder.h"
GR_SWIG_BLOCK_MAGIC2(ax25, ax25_encoder);
%include "ax25/pdu_prepend_append.h"
GR_SWIG_BLOCK_MAGIC2(ax25, pdu_prepend_append);
%include "ax25/nrzi_encoder.h"
GR_SWIG_BLOCK_MAGIC2(ax25, nrzi_encoder);
