#!/bin/bash

DELAYS=(20 40 60 80 100)
SCHEMES=(cubic bbr pcc vivace xntp fillp ledbat)

for delay in ${DELAYS[@]}
do
    cd ./data
    mkdir ${delay}_ms
    for scheme in ${SCHEMES[@]}
    do
        python test.py local --append-mm-cmds "mm-delay ${delay}" -c ../config/${scheme}.yml
        cd ../analysis/
        python analyze.py --schemes=${scheme}
        cd ../experiments/data
        mv pantheon_report.pdf ${scheme}.pdf
        mv ${scheme}.pdf ./${delay}_ms/
        cd ..
    done
done

