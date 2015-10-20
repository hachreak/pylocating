#!/bin/sh

PROJECT="start_from_sphere_surface"

best_fitness(){
  cat logs/${PROJECT}-particle-engine.log | grep best | awk '{print $6}' | sort -nu | head
}

# clean logs
echo "clean logs.."
rm logs/${PROJECT}-*
# execute example
echo "execute script.."
RESULT=`python examples/${PROJECT}.py`
echo $RESULT
# split data
echo "analize logs.."
scripts/bestfitnessgraph.sh logs/${PROJECT}-particle-engine.log 1 16
# execute octave and generate the graph /tmp/image.jpg
echo "[ENV 1] to generate image /tmp/image1.jpg"
scripts/bestfitnessgraph.m 1 16
echo "script results.."
echo $RESULT
echo "best fitness.."
best_fitness
