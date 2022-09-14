#!/bin/bash

rm ../../tmp/*   
rm ./data/xntp*
rm ./XNTP*
python test.py local --schemes="xntp" --append-mm-cmds "mm-delay 30" \
--uplink-trace 100mbps.trace \
--extra-mm-link-args="--uplink-queue=droptail \
--uplink-queue-args bytes=1500000" -f 3 -t 60 --interval 5 
python ../analysis/analyze.py --schemes="xntp"
   

