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

import logging
import random

from numpy import matrix

from pylocating.engines import ParticleEngine
from pylocating.environment import Environment
from pylocating.information import Information
from pylocating.particles import PSOParticle


class Random(object):

    """Randomizer."""

    def random(self):
        """Return random [0,1) matrix 3x1."""
        val = random.random()
        return matrix([val, val, val])


random_generator = Random()

config = {
    'inertial_weight': 2,
    'cognition': 2,
    'social': 1,
    'random': random_generator,
    'base': matrix([
        [0, 0, 0],   # beacon 1
        [60, -40, 0],   # beacon 2
        [50, 50, 0],  # beacon 3
    ]),
    'radius': matrix([
        20,   # beacon 1
        60,     # beacon 2
        60,    # beacon 3
    ])
}
env = Environment(config=config)

for i in range(20):
    PSOParticle(
        environment=env,
        id="P{}".format(i),
        current=Information(
            position=config['base'][i % 3][0] + random_generator.random(),
        ),
        velocity=random_generator.random(),
        vmax=5
    )

logging.basicConfig(filename='find_point_2.log',
                    level=logging.DEBUG)

engine = ParticleEngine(
    config={
        'logger': logging,
        'max_iterations': 100
    },
    environment=env
)
engine.start()
engine.join()

bestParticle = env.best
print("Object located: ", bestParticle.best.position)
