#!/bin/bash
if [ ! -f "$HOME/.ssh/id_rsa.pub" ]; then
    ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
fi
sudo ifconfig enp0s26u1u4 10.42.0.1 up
ssh-copy-id robot@10.42.0.3
