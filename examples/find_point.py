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

    """Random generator."""

    def random(self):
        """Get random matrix 3x1 with values [0,1)."""
        return matrix([random.random(),
                       random.random(),
                       random.random()])
config = {
    'inertial_weight': 1,
    'cognition': 2,
    'social': 1.8,
    'random': Random(),
    'base': matrix([
        [0, 0, 0],   # beacon 1
        [7, 5, 0],   # beacon 2
        [5, -4, 0],  # beacon 3
    ]),
    'radius': matrix([
        3.024,   # beacon 1
        6.4,     # beacon 2
        6.63,    # beacon 3
    ])
}
env = Environment(config=config)

PSOParticle(
    environment=env,
    id="P1",
    current=Information(
        position=config['base'][0]
    ),
    velocity=matrix([0.1, 0.1, 0.1]),
    vmax=3
)
PSOParticle(
    environment=env,
    id="P2",
    current=Information(position=config['base'][1]),
    vmax=10
)
PSOParticle(
    environment=env,
    id="P3",
    current=Information(position=config['base'][2]),
    vmax=10
)

logging.basicConfig(filename='logs/find_point.log',
                    level=logging.DEBUG)

engine = ParticleEngine(
    config={
        'max_iterations': 100
    },
    environment=env
)
engine.start()
engine.join()

bestParticle = env.best
print("Object located: ", bestParticle.best.position)
