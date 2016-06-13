#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/python
export PATH=/home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/python:$PATH
export LD_LIBRARY_PATH=/home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/build/swig:$PYTHONPATH
/usr/bin/python2 /home/thomasp/GroundStation/GNURadio/OOT_Modules/gr-channelcoding/python/qa_binary_symmetric_channel.py 
