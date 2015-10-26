#!/bin/sh

CONFIGFILE="examples/benchmark_2.config1.json"
LOGFILE="logs/benchmark_2.log"
IMAGE="/tmp/benchmark_2.config1.jpg"
# how many simulations is started
MATRIX=30
SIMULATIONS=${1:-10}
# extract this column from log to plot (X,Y)
X_COLUMN=8
Y_COLUMN=11

scripts/run_benchmark.sh $CONFIGFILE $LOGFILE $IMAGE $MATRIX $SIMULATIONS $X_COLUMN $Y_COLUMN
