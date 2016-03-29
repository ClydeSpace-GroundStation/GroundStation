#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/gs-laptop1/GroundStation/GroundStation/GNURadio/OOT\ Modules/gr-ccsds/python
export GR_CONF_CONTROLPORT_ON=False
export PATH=/home/gs-laptop1/GroundStation/GroundStation/GNURadio/OOT Modules/gr-ccsds/build/python:$PATH
export LD_LIBRARY_PATH=/home/gs-laptop1/GroundStation/GroundStation/GNURadio/OOT\ Modules/gr-ccsds/build/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/home/gs-laptop1/GroundStation/GroundStation/GNURadio/OOT\ Modules/gr-ccsds/build/swig:$PYTHONPATH
/usr/bin/python2 /home/gs-laptop1/GroundStation/GroundStation/GNURadio/OOT Modules/gr-ccsds/python/qa_rs_decode.py 
