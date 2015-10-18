#!/bin/sh

# log file
FILE=$1
# number of environment
ENUM=$2
# number of particles
PNUM=`expr ${3} - 1)`

extract_particle_best(){
  FILE=$1
  ENVID=$2
  PID=$3
  cat $FILE | grep P${PID}env${ENVID} | awk '{print $1", "$6", "$4 }'
}

mkdir -p /tmp/data
for i in `seq $ENUM`; do
  for j in `seq 0 $PNUM`; do
    extract_particle_best $FILE $i $j > /tmp/data/data-${i}-${j}.log
  done
done
