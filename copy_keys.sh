#!/bin/bash
if [ ! -f "$HOME/.ssh/id_rsa.pub" ]; then
    ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
fi

device=$(cat /proc/net/dev | grep enp0 | awk '{print $1}' | sed -e "s/://g")
sudo ifconfig $device 10.42.0.1 up

ssh-copy-id robot@10.42.0.3
