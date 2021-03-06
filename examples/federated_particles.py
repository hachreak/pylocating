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


if len(sys.argv) <= 2:
    sys.stderr.write(
        ("Usage: {} num-particles-env-1 num-particles-env-2\n").format(
            sys.argv[0]))
    sys.exit(1)


class Random(object):

    """Randomizer."""

    def random(self):
        """Return random [0,1) matrix 3x1."""
        val = random.random()
        return matrix([val, val, val])


random_generator = Random()

env_config = {
    'inertial_weight': 2,
    'cognition': 2,
    'social': 1,
    'random': random_generator,
    'base': matrix([
        [0, 0, 0],      # beacon 1
        [60, -40, 0],   # beacon 2
        [50, 50, 0],    # beacon 3
        [25, 0, 25]     # beacon 4
    ]),
    'radius': matrix([
        20,    # beacon 1
        60,    # beacon 2
        60,    # beacon 3
        30,    # beacon 4
    ])
}
env1 = Environment(config=env_config)
env2 = Environment(config=env_config)
# connect environments
env1.registerNeighbor(env2)

position_generator = around_beacons(env1)

# particles inside env 1
for i in range(int(sys.argv[1])):
    PSOParticle(
        environment=env1,
        id="P{}env1".format(i),
        current=Information(position=next(position_generator)),
        velocity=random_generator.random(),
        vmax=5
    )

# particles inside env 2
for i in range(int(sys.argv[2])):
    PSOParticle(
        environment=env2,
        id="P{}env2".format(i),
        current=Information(position=next(position_generator)),
        velocity=random_generator.random(),
        vmax=5
    )

# Load logging configuration
log_config = "examples/federated_particles.json"
with open(log_config) as data_file:
    data = json.load(data_file)
logging.config.dictConfig(data)

# engine1 for env1
engine1 = ParticleEngine(
    config={
        'max_iterations': 40
    },
    environment=env1
)
engine1.start()
# engine2 for env2
engine2 = ParticleEngine(
    config={
        'max_iterations': 40
    },
    environment=env2
)
engine2.start()

# wait engines
engine1.join()
engine2.join()

bestParticle = env1.neighborBest
print("Object located: ", bestParticle.best.position)
