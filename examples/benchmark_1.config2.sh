#!/bin/sh

CONFIGFILE="examples/benchmark_1.config2.json"
LOGFILE="logs/benchmark_1.log"
IMAGE="/tmp/benchmark_1.config2.jpg"
# how many simulations is started
MATRIX=20
SIMULATIONS=${1:-10}
# extract this column from log to plot (X,Y)
X_COLUMN=6
Y_COLUMN=10

scripts/run_benchmark.sh $CONFIGFILE $LOGFILE $IMAGE $MATRIX $SIMULATIONS $X_COLUMN $Y_COLUMN
