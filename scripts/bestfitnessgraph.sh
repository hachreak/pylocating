#!/bin/bash

# Note:
#  to works, the example shoud configure:
#   - the example script shoud be inside `examples/` directory
#   - particle name (e.g. P{particle_number}env{environment_number}
#   - the environment number start from 1 and particle number start from 0
#   - the name of log file generated for the particle engine should be:
#      `logs/{project_name}-particle-engine.json`
#   - The column where is contained the best fitness value is the 6th
#     e.g.
#        [time]   [particle] [property] [value]    [propery] [value]
#                 [  name  ]
#     1445342135768 [P38env1] fitness: 5116.7295565 best: 5116.729006365
#   - the script shoud be executed from the *project root*
#     e.g.  /pylocating> scripts/

USAGE="Usage: $0 project-name num-particles-env-1 num-particles-env-2 ..."

# example name
PROJECT=$1
[ -z "$PROJECT" ] && echo "[Error] example to execute is not defined\n\n$USAGE" && exit 1
# number of environments
ENUM=`expr $# - 1`
# number of particles for each environment (e.g. "10 20 15" it means that
# the 1th environment have 10 particles, the 2th environment have 20 particles
# and the 3th environment have 15 particles)
shift
PNUMS=${@}
[ -z "$PNUMS" ] && echo "[Error] number of particles per environment is not defined\n\n$USAGE" && exit 1


# extract first 10 best fitness
best_fitness(){
  cat logs/${PROJECT}-particle-engine.log | grep best | awk '{print $6}' | sort -nu | head
}

# analize log and filter information of time, fitness and best fitness
extract_particle_best(){
  FILE=$1
  ENVID=$2
  PID=$3
  cat $FILE | grep P${PID}env${ENVID} | awk '{print $1", "$6", "$4 }'
}

# put all fitness information in a separate file for every particle
separate_particle_best(){
  # read input
  TEMP_DIR=$1
  FILE=$2
  shift
  shift
  PNUMS=${@}
  ENVID=1
  # clean workspace
  rm $TEMP_DIR/* 2> /dev/null
  # start the information split
  for i in $PNUMS; do
    PNUM=`expr ${i} - 1`
    for j in `seq 0 $PNUM`; do
      extract_particle_best $FILE $ENVID $j > $TEMP_DIR/data-${ENVID}-${j}.log
    done
    ENVID=`expr $ENVID + 1`
  done
}

generate_graph(){
  # read input
  TEMP_DIR=$1
  shift
  PNUMS=${@}
  ENVID=1
  # for every environment, generate a separate graph
  for i in $PNUMS; do
    echo $ENVID, $i
    # create graph for env $ENVID
    scripts/bestfitnessgraph.m $TEMP_DIR $ENVID $i
    # next env
    ENVID=`expr $ENVID + 1`
  done
  ENVID=1
  echo "Images:"
  for i in $PNUMS; do
    echo "/tmp/image${ENVID}.jpg"
    ENVID=`expr $ENVID + 1`
  done
}

# clean logs
echo "clean logs.."
rm logs/${PROJECT}-* 2> /dev/null
# create temporary directory
TEMP_DIR=`mktemp -d`
# execute example
echo "execute script.."
RESULT=`python examples/${PROJECT}.py $PNUMS`
echo $RESULT
# split data
echo "analize logs.."
separate_particle_best $TEMP_DIR logs/${PROJECT}-particle-engine.log $PNUMS
# execute octave and generate the graph /tmp/image.jpg
generate_graph $TEMP_DIR $PNUMS
# clean temporary files
rm $TEMP_DIR -Rf
echo "script results.."
echo $RESULT
echo "best fitness.."
best_fitness
