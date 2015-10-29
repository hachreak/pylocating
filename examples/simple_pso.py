# -*- coding: utf-8 -*-
#
# This file is part of pysenslog.
# Copyright 2015 Leonardo Rossi <leonardo.rossi@studenti.unipr.it>.
#
# pysenslog is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# pysenslog is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pysenslog.  If not, see <http://www.gnu.org/licenses/>.

"""Test Python Locating."""

from __future__ import absolute_import, unicode_literals

import random
import json
import logging
import sys

from numpy import matrix
from logging import config

from pylocating.engines import ParticleEngine
from pylocating.environment import Environment
from pylocating.particles import PSOParticle
from pylocating.information import Information
from pylocating.strategies.init.position import around_beacons
from pylocating.benchmarks.utils import apply_noise_linear
from pylocating.utils import generate_matrix_of_points_in_cube, distance


if len(sys.argv) <= 1:
    sys.stderr.write(
        ("Usage: {} num-particles-env-1\n").format(
            sys.argv[0]))
    sys.exit(1)


class Random(object):

    """Randomizer."""

    def random(self):
        """Return random [0,1) matrix 3x1."""
        val = random.random()
        return matrix([val, val, val])


random_generator = Random()

center = [1000, 1000, 1000]
side_length = 100

base_generator = generate_matrix_of_points_in_cube(
    center=center, side_length=side_length, num_of_points=4)
point_generator = generate_matrix_of_points_in_cube(
    center=center, side_length=side_length, num_of_points=1)

base = next(base_generator)
point = next(point_generator)
error = 10
disturbed_point_gen = apply_noise_linear(point=point, error=error)
radius = matrix([distance(b, next(disturbed_point_gen)) for b in base])

env_config = {
    'inertial_weight': 2,
    'cognition': 2,
    'social': 1,
    'random': random_generator,
}
env1 = Environment(config=env_config, base=base, radius=radius)

position_generator = around_beacons(env1)

vmax = 5

# particles inside env 1
for i in range(int(sys.argv[1])):
    PSOParticle(
        environment=env1,
        id="P{}env1".format(i),
        current=Information(position=next(position_generator)),
        velocity=vmax * random_generator.random() - matrix([
            vmax / 2, vmax / 2, vmax / 2]),
        vmax=vmax
    )

# Load logging configuration
log_config = "examples/simple_pso.json"
with open(log_config) as data_file:
    data = json.load(data_file)
logging.config.dictConfig(data)

# engine1 for env1
engine1 = ParticleEngine(
    config={
        'max_iterations': 100
    },
    environment=env1
)
engine1.start()

# wait engines
engine1.join()

bestParticle = env1.neighborBest
print("Object located: ", bestParticle.best.position, "\n")
print("error: ", point - bestParticle.best.position, "\n")
print("distance: ", distance(point, bestParticle.best.position), "\n")
