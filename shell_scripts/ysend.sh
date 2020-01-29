#!/bin/sh
#DEV=/dev/ttyUSB0
DEV=$1
#BAUD=57600
BAUD=$2
FILE=$3
stty -F $DEV $BAUD
sb $FILE > $DEV < $DEV
