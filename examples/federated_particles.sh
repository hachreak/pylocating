#!/bin/sh

# clean logs
echo "clean logs.."
rm logs/federated_particles-*
# execute example
echo "execute script.."
python examples/federated_particles.py
# split data
echo "analize logs.."
scripts/bestfitnessgraph.sh logs/federated_particles-particle-engine.log 2 20
# execute octave and generate the graph /tmp/image.jpg
echo "to generate image /tmp/image.jpg"
scripts/bestfitnessgraph.m
