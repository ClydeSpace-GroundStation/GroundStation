#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/gs-laptop1/Groundstation/GNURadio/OOT\ Modules/CCSDS/gr-ccsds/lib
export GR_CONF_CONTROLPORT_ON=False
export PATH=/home/gs-laptop1/Groundstation/GNURadio/OOT Modules/CCSDS/gr-ccsds/build/lib:$PATH
export LD_LIBRARY_PATH=/home/gs-laptop1/Groundstation/GNURadio/OOT\ Modules/CCSDS/gr-ccsds/build/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$PYTHONPATH
test-ccsds 
