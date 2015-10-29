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

import json
import logging
import random
import sys

from numpy import matrix
from logging import config

from pylocating.engines import ParticleEngine
from pylocating.environment import Environment
from pylocating.particles import PSOParticle, FollowBestParticle
from pylocating.information import Information
from pylocating.strategies.init.position import on_beacon_sphere_surface


if len(sys.argv) <= 1:
    sys.stderr.write(
        ("Usage: {} num-particles-env-1\n").format(sys.argv[0]))
    sys.exit(1)


class Random3D(object):

    """Randomizer."""

    def random(self):
        """Return random [0,1) matrix 3x1."""
        return matrix([random.random(), random.random(), random.random()])


# Load logging configuration
log_config = "examples/start_from_sphere_surface.json"
with open(log_config) as data_file:
    data = json.load(data_file)
logging.config.dictConfig(data)

# random generator
random_generator = Random3D()

# environment configuration
env_config = {
    'inertial_weight': 2,
    'cognition': 2,
    'social': 1,
    'random': random_generator,
}
base = matrix([
    [0, 0, 0],      # beacon 1
    [60, -40, 0],   # beacon 2
    [50, 50, 0],    # beacon 3
    [25, 0, 25]     # beacon 4
])
radius = matrix([
    20,    # beacon 1
    60,    # beacon 2
    60,    # beacon 3
    30,    # beacon 4
])

# create environment
env = Environment(config=env_config, base=base, radius=radius)

# how many particles for each beacon
total = int(sys.argv[1])

# initial point generator (on sphere surface)
position_generator_1 = on_beacon_sphere_surface(environment=env,
                                                beacon_index=0,
                                                num_of_points=total)

position_generator_2 = on_beacon_sphere_surface(environment=env,
                                                beacon_index=1,
                                                num_of_points=total)

position_generator_3 = on_beacon_sphere_surface(environment=env,
                                                beacon_index=2,
                                                num_of_points=total)

position_generator_4 = on_beacon_sphere_surface(environment=env,
                                                beacon_index=3,
                                                num_of_points=total)

for i in range(total):
    # start around beacon 1
    PSOParticle(
        environment=env,
        id="P{}env1".format(i),
        current=Information(position=next(position_generator_1)),
        velocity=random_generator.random(),
        vmax=1
    )
    # start around beacon 2
    PSOParticle(
        environment=env,
        id="P{}env1".format(i + total),
        current=Information(position=next(position_generator_2)),
        velocity=random_generator.random(),
        vmax=1
    )
    # start around beacon 3
    PSOParticle(
        environment=env,
        id="P{}env1".format(i + total * 2),
        current=Information(position=next(position_generator_3)),
        velocity=random_generator.random(),
        vmax=1
    )
    # start around beacon 4
    FollowBestParticle(
        environment=env,
        id="P{}env1".format(i + total * 3),
        current=Information(position=next(position_generator_4)),
        velocity=random_generator.random(),
        vmax=1
    )

# start engine
engine = ParticleEngine(
    config={
        'max_iterations': 70
    },
    environment=env
)
engine.start()
engine.join()

bestParticle = env.best
print("Object located: ", bestParticle.best.position)
