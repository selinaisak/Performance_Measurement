#!/bin/bash
if [ $# -lt 2 ]
then
    echo "Invalid number of arguments!"
    echo "Usage: $0 <Server-IP> <iterations>"
    exit
fi
SERVER_IP=$1
ITERATIONS=$2

for ((i = 1; i <= $ITERATIONS; i++))
do
    echo "------------------ ITERATION: $i -------------------"
    echo "------------------ DEFAULT MODE --------------------"
    iperf3 -c $SERVER_IP -P 10
done

for ((i = 1; i <= $ITERATIONS; i++))
do
    echo "------------------ ITERATION: $i -------------------"
    echo "------------------ REVERSE MODE --------------------"
    iperf3 -c $SERVER_IP -P 10 -R
done
exit