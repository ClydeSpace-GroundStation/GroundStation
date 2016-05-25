/* -*- c++ -*- */

#define CCSDS_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "ccsds_swig_doc.i"

%{
#include "ccsds/asm_deframer.h"
#include "ccsds/rs_encode.h"
#include "ccsds/rs_decode.h"
#include "ccsds/asm_deframer_pdu.h"
#include "ccsds/rs_decode_pdu.h"
%}


%include "ccsds/asm_deframer.h"
GR_SWIG_BLOCK_MAGIC2(ccsds, asm_deframer);
%include "ccsds/rs_encode.h"
GR_SWIG_BLOCK_MAGIC2(ccsds, rs_encode);
%include "ccsds/rs_decode.h"
GR_SWIG_BLOCK_MAGIC2(ccsds, rs_decode);
%include "ccsds/asm_deframer_pdu.h"
GR_SWIG_BLOCK_MAGIC2(ccsds, asm_deframer_pdu);
%include "ccsds/rs_decode_pdu.h"
GR_SWIG_BLOCK_MAGIC2(ccsds, rs_decode_pdu);
