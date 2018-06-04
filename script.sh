#!/bin/bash
#snap interface to the lego mindstorms robot installation

device=$(cat /proc/net/dev | grep enp0 | awk '{print $1}' | sed -e "s/://g")
sudo ifconfig $device 10.42.0.1 up
python snap-ev3.py
