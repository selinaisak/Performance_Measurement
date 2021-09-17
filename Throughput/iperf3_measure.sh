#!/bin/bash
if [ $# -lt 3 ]
then
    echo "Invalid number of arguments!"
    echo "Usage: $0 <Server-IP> <iterations> <connections>"
    exit
fi
SERVER_IP=$1
ITERATIONS=$2
CONNECTIONS=$3

for ((i = 1; i <= $ITERATIONS; i++))
do
    echo "------------------ ITERATION: $i -------------------"
    echo "------------------ DEFAULT MODE --------------------"
    iperf3 -c $SERVER_IP -P $CONNECTIONS
done

for ((i = 1; i <= $ITERATIONS; i++))
do
    echo "------------------ ITERATION: $i -------------------"
    echo "------------------ REVERSE MODE --------------------"
    iperf3 -c $SERVER_IP -P $CONNECTIONS -R
done
exit