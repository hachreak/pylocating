#!/bin/sh

# clean logs
echo "clean logs.."
rm logs/followbest_particles-*
# execute example
echo "execute script.."
RESULT=`python examples/followbest_particles.py`
echo $RESULT
# split data
echo "analize logs.."
scripts/bestfitnessgraph.sh logs/followbest_particles-particle-engine.log 2 20
# execute octave and generate the graph /tmp/image.jpg
echo "[ENV 1] to generate image /tmp/image1.jpg"
scripts/bestfitnessgraph.m 1 20
echo "[ENV 2] to generate image /tmp/image2.jpg"
scripts/bestfitnessgraph.m 2 20
echo "script results.."
echo $RESULT
