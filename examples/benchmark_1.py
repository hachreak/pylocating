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

"""Benchmark."""

from __future__ import absolute_import, unicode_literals

import logging
import json

from logging import config
from numpy import random, matrix
from pylocating.utils import distance
from pylocating.benchmarks.env_builder import builder
from pylocating.strategies.init.position import around_beacons
from pylocating.benchmarks.matrix_generator import \
    generate_matrix_of_points_in_cube


class Random(object):

    """Randomizer."""

    def random(self):
        """Return random [0,1) matrix 3x1."""
        return random.random(3)


center = matrix([1000, 1000, 1000])
side_length = 100

base_generator = generate_matrix_of_points_in_cube(
    center=center, side_length=side_length, num_of_points=3)
point_generator = generate_matrix_of_points_in_cube(
    center=center, side_length=side_length, num_of_points=1)

base = next(base_generator)
point = next(point_generator)

random_generator = Random()

params = [
    {"start": 0, "step": 1, "end": 3},  # standard deviation
    {"start": 1, "step": 1, "end": 3},  # inertial weight
    {"start": 1, "step": 1, "end": 3},  # cognition
    {"start": 1, "step": 1, "end": 3},  # social
    {"start": 50, "step": 10, "end": 60},  # number of particles
    {"start": 1, "step": 1, "end": 5},  # max particle velocity
    {"start": 60, "step": 10, "end": 100},  # iterations per particle
]

# Load logging configuration
log_config = "examples/benchmark_1.json"
with open(log_config) as data_file:
    data = json.load(data_file)
logging.config.dictConfig(data)

logger = logging.getLogger("benchmark")

for param, engine in builder(base, point, params, random_generator,
                             around_beacons):
    engine.start()
    engine.join()

    bestParticle = engine.environment.neighborBest
    best_position = bestParticle.best.position
    error = distance(point, best_position)

    logger.debug("{} {} {} {} {} {} {} {}".format(
        param[0], param[1], param[2], param[3], param[4], param[5],
        param[6], error))
