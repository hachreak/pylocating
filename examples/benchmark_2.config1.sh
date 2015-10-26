#!/bin/sh

CONFIGFILE="examples/benchmark_2.config1.json"
LOGFILE="logs/benchmark_2.log"
# how many simulations is started
MATRIX=30
SIMULATIONS=${1:-10}

# compute avg value
avg(){
  LOGFILE=$1
  INDEX=$2
  cat $LOGFILE | awk '{print $2" "$8" "$11}' | grep ^"${INDEX} " | awk '{ sum+=$3; n++; x=$2 } END{ if (n > 0) print x" "(sum / n); }'
}

# extract all avg values
extract_avg_values(){
  LOGFILE=$1
  MATRIX=$2
  TOT=`expr $MATRIX - 1`
  for i in `seq 0 $TOT`; do
    echo `avg $LOGFILE $i`
  done
}

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
extract_avg_values $LOGFILE $MATRIX > $DATALOG
# generate graph
echo "generate graph.."
./examples/benchmark_1.m $DATALOG
