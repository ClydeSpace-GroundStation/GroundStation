/* -*- c++ -*- */

#define CHANNELCODING_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "channelcoding_swig_doc.i"

%{
#include "channelcoding/binary_symmetric_channel.h"
%}


%include "channelcoding/binary_symmetric_channel.h"
GR_SWIG_BLOCK_MAGIC2(channelcoding, binary_symmetric_channel);
