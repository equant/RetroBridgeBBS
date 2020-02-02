#!/bin/sh
PROTOCOL=$1
DEV=$2
BAUD=$3
FILE=$4
stty -F $DEV $BAUD
#rb -$PROTOCOL $FILE > $DEV < $DEV
rb -$PROTOCOL > $DEV < $DEV
