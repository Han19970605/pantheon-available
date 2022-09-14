#!/bin/bash
# shell脚本

SCHEMES=("xntp" "bbr" "cubic" "pcc" "vivace" "fillp" "ledbat")
DELAYS=(30 141)
# LOSSES=(0.0 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 0.11 0.12 0.13 0.14 0.15 0.16 0.17 0.18 0.19 0.2)
TRACES=("100mbps.trace")
FLOW_NUMS=(3 4 5 6 7 8 9 10)
#  mm-loss $loss
for trace in ${TRACES[@]}
do
    for delay in ${DELAYS[@]}
    do
        for num in ${FLOW_NUMS[@]}
        do
            for scheme in ${SCHEMES[@]}
            do 
                python test.py local --schemes=$scheme -f $num --prepend-mm-cmds "mm-delay $delay" --uplink-trace $trace --downlink-trace $trace --extra-mm-link-args "--uplink-queue droptail --uplink-queue-args bytes=5000000" --runtime 60
                echo "-----------------------------------running $delay $loss $scheme-----------------------------------"
                cd /opt/pantheon/src/analysis
                python analyze.py --schemes=$scheme
                cd /opt/pantheon/src/experiments/data
                mv pantheon_report.pdf $scheme-flow-$num-pantheon-report.pdf
                cd /opt/pantheon/src/experiments
            done
            cd /opt/pantheon/src/experiments/data
            mkdir rawdata-flow-$num-delay-$delay-loss-$loss
            mv *.npy ./rawdata-flow-$num-delay-$delay-loss-$loss
            mv *.pdf ./rawdata-flow-$num-delay-$delay-loss-$loss
            mv *.png ./rawdata-flow-$num-delay-$delay-loss-$loss
            echo "-------------------------------------  move finished ------------------------------------"
            cd /opt/pantheon/src/experiments
        done
    done
    cd /opt/pantheon/src/experiments/data
    mkdir $trace
    mv rawdata* $trace
    echo "-------------------------------------  move finished ------------------------------------"
    cd /opt/pantheon
    rm -rf ./tmp
    cd /opt/pantheon/src/experiments
done
