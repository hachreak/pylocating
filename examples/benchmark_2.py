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

"""Benchmark mixed PSO and FollowBest Particles."""

from __future__ import absolute_import, unicode_literals

import logging
import json
import sys

from logging import config
from numpy import matrix
from pylocating.utils import distance, Random
from pylocating.benchmarks.mix_pso_followbest import builder
from pylocating.strategies.init.position import around_beacons
from pylocating.utils import generate_matrix_of_points_in_cube


# load log configuration
log_config = sys.argv[1]
with open(log_config) as data_file:
    data = json.load(data_file)

# Load parameters configuration
#   error introduced
#   inertial weight
#   cognition
#   social
#   number of PSOParticles
#   number of FollowBestParticles
#   max particle velocity
#   interations per particle
params = data['parameters']
# Load space where happen the simulation
center = matrix(data['space']['center'])
side_length = data['space']['side_length']

base_generator = generate_matrix_of_points_in_cube(
    center=center, side_length=side_length, num_of_points=4)
point_generator = generate_matrix_of_points_in_cube(
    center=center, side_length=side_length, num_of_points=1)

base = next(base_generator)
point = next(point_generator)

random_generator = Random()

# Load logging configuration
log_config = "examples/benchmark_2.log.json"
with open(log_config) as data_file:
    data = json.load(data_file)
logging.config.dictConfig(data)

logger = logging.getLogger("benchmark")

for index, (param, engine1, engine2) in enumerate(builder(base, point, params,
                                                          random_generator,
                                                          around_beacons)):
    engine1.start()
    engine2.start()
    engine1.join()
    engine2.join()

    bestParticle = engine1.environment.neighborBest
    best_position = bestParticle.best.position
    error = distance(point, best_position)
    fitness = bestParticle.best.fitness

    logger.debug(
        "{} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f}".
        format(
            index, param[0], param[1], param[2], param[3], param[4], param[5],
            param[6], param[7], error))
