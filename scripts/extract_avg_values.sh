#!/bin/bash

LOGFILE=$1
MATRIX=${2:-20}
X=${3:-8}
Y=${4:-11}
DATALOG=$5

# compute avg value
avg(){
  LOGFILE=$1
  INDEX=$2
  X=$3
  Y=$4
  cat $LOGFILE | awk -v X=$X -v Y=$Y '{print $2" "$X" "$Y}' | grep ^"${INDEX} " | awk '{ sum+=$3; n++; x=$2 } END{ if (n > 0) print x" "(sum / n); }'
}

# extract all avg values
extract_avg_values(){
  LOGFILE=$1
  MATRIX=$2
  X=$3
  Y=$4
  TOT=`expr $MATRIX - 1`
  for i in `seq 0 $TOT`; do
    avg $LOGFILE $i $X $Y
  done
}

# check input
[ -z "$LOGFILE" ] && echo "Usage: $0 [logfile] [matrix-count] [x] [y]" && exit 1
! [ -f "$LOGFILE" ] && echo "Error: $LOGFILE doesn't exist!" && exit 2
! [ -f "$DATALOG" ] && DATALOG=`mktemp`
# extract avg values
echo "extract avg values and save them in $DATALOG .."
extract_avg_values $LOGFILE $MATRIX $X $Y > $DATALOG
