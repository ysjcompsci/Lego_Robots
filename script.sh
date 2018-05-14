#!/bin/bash
#snap interface to the lego mindstorms robot installation

sudo ifconfig enp0s26u1u4 10.42.0.1 up
python snap-ev3.py
