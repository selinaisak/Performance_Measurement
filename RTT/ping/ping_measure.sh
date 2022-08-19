#!/bin/bash
if [ $# -lt 2 ]
then
    echo "Invalid number of arguments!"
    echo "Usage: $0 <Server-IP> <iterations>"
    exit
fi
SERVER_IP=$1
ITERATIONS=$2
TIMESTAMP=`date +%Y-%m-%d_%H-%M-%S`
FILENAME="ping_${TIMESTAMP}.txt"
FILE=~/storage/shared/pinglogs/${FILENAME}
touch $FILE

for ((i = 1; i <= $ITERATIONS; i++))
do
    echo "------------------ ITERATION: $i -------------------" | tee -a $FILE
    ping -i 0.2 -c 10 $SERVER_IP | tee -a $FILE
done

exit