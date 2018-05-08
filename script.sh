#!/bin/bash
#snap interface to the lego mindstorms robot installation

#Runs python script to append the required files to the pythonpath
python pathappend.py

ifconfig
sudo ifconfig enp0s26u1u4 10.42.0.1 up
ifconfig

#Runs the program
python snap-ev3.py
