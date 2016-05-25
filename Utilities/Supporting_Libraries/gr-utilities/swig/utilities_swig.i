/* -*- c++ -*- */

#define UTILITIES_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "utilities_swig_doc.i"

%{
#include "utilities/insert_pdu_into_stream.h"
%}


%include "utilities/insert_pdu_into_stream.h"
GR_SWIG_BLOCK_MAGIC2(utilities, insert_pdu_into_stream);
