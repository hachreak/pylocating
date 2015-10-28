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

"""Example tracking a point."""

from __future__ import absolute_import, unicode_literals

import sys
import logging
import json

from logging import config
from numpy import matrix, random
from pylocating.environment import Environment
from pylocating.benchmarks.matrix_generator import \
    generate_matrix_of_points_in_cube
from pylocating.benchmarks.utils import apply_noise_linear
from pylocating.utils import distance, generate_sequential_points
from pylocating.strategies.init.position import around_beacons
from pylocating.particles import PSOParticle
from pylocating.information import Information
from pylocating.engines import ParticleEngine
from pylocating.benchmarks.moving_point import LoggingMovingPointEngine, \
    EnvironmentListener

# Load logging configuration
log_config = "examples/tracking_1.json"
with open(log_config) as data_file:
    data = json.load(data_file)
logging.config.dictConfig(data)


center = [1000, 1000, 1000]
side_length = 100

base_generator = generate_matrix_of_points_in_cube(
    center=center, side_length=side_length, num_of_points=4)
point_generator = generate_matrix_of_points_in_cube(
    center=center, side_length=side_length, num_of_points=1)

base = next(base_generator)
seq_point_gen = generate_sequential_points(
    start_point=next(point_generator), vmax=20, random=random)
point = next(seq_point_gen)
error = 10
disturbed_point_gen = apply_noise_linear(point=point, error=error)
radius = matrix([distance(b, next(disturbed_point_gen)) for b in base])

velocity_max = 5
num_particles = sys.argv[1] if 1 in sys.argv else 70
iterations_per_particle = sys.argv[2] if 2 in sys.argv else 100
# sleep_time = 0.1

# build environment configuration
env_config = {
    'inertial_weight': 1,
    'cognition': 2,
    'social': 1,
    'random': random,
    'base': base,
    'radius': radius
}
env = Environment(config=env_config)
# particle position generator
particle_position_generator = around_beacons(env)
# particles inside env
for i in range(num_particles):
    # particles
    PSOParticle(
        environment=env,
        id="P{}env{}".format(i, 1),
        current=Information(position=next(particle_position_generator)),
        velocity=velocity_max * random.random(3),
        vmax=velocity_max
    )

# engine for env
engine = ParticleEngine(
    config={},
    environment=env,
    stop_condition=(lambda engine: False)
)
mpe = LoggingMovingPointEngine(
    config={
        'sleep': 0.5
    },
    listener=EnvironmentListener(environment=env, error=10),
    start_point=point,
    positions=seq_point_gen,
    stop_condition=lambda mpe: mpe.iterations > 100000
)
mpe.start()
engine.start()
mpe.join()
# engine.join()
