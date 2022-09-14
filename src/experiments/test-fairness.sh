#!/bin/bash

# SCHEMES=("xntp" "bbr" "cubic" "pcc" "vivace" "fillp" "ledbat")
# DELAYS=(30 141)
# TRACES=("100mbps.trace")
FLOW_NUMS=(1 2 3 4 5 6 7 8 9 10)

for num in ${FLOW_NUMS[@]}
do
    python test.py local --schemes="xntp" -f $num --append-mm-cmds "mm-delay 30" --uplink-trace 192mbps.trace --extra-mm-link-args "--uplink-queue droptail --uplink-queue-args bytes=5000000" --runtime 60
    python Extract.py
    rm ../../third_party/xntp/sender/*
    rm ../../tmp/*
done
