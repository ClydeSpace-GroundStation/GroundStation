#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/lib
export PATH=/home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/lib:$PATH
export LD_LIBRARY_PATH=/home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$PYTHONPATH
test-channelcoding 
