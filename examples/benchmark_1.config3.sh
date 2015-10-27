#!/bin/sh

CONFIGFILE="examples/benchmark_1.config3.json"
LOGFILE="logs/benchmark_1.log"
IMAGE="/tmp/benchmark_1.config3.jpg"
# how many simulations is started
MATRIX=60
SIMULATIONS=${1:-10}
# extract this column from log to plot (X,Y)
X_COLUMN=9
Y_COLUMN=10
# script to execute
SCRIPT=examples/benchmark_1.py

scripts/run_benchmark.sh $CONFIGFILE $LOGFILE $IMAGE $MATRIX $SIMULATIONS $X_COLUMN $Y_COLUMN $SCRIPT
