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

# clean logs
echo clear log ${LOGFILE}..
rm $LOGFILE 2> /dev/null
# execute simulations
echo -n "execute simulations.. "
for i in `seq $SIMULATIONS`; do
  echo -n "$i "
  python examples/benchmark_2.py $CONFIGFILE
done
echo ""
# extract avg values
echo "extract avg values.."
DATALOG=`mktemp`
scripts/extract_avg_values.sh $LOGFILE $MATRIX $X_COLUMN $Y_COLUMN $DATALOG
# generate graph
echo "generate graph.. $IMAGE"
./scripts/print_2d_graph.m $DATALOG $IMAGE
