#!/bin/bash

if [[ $EUID -eq 0 ]]; then
	echo "Root permission required - please run script again prefixed with 'sudo '"
  	exit 1
fi

cp 50-aardvark.rules /lib/udev/rules.d/
cp 50-usrp.rules /lib/udev/rules.d/

