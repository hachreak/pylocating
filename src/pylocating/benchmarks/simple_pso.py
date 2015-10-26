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

"""Environment systematic builder."""

from __future__ import absolute_import, unicode_literals

from numpy import matrix
from pylocating.environment import Environment
from pylocating.utils import distance
from pylocating.benchmarks.utils import apply_noise_linear
from pylocating.particles import PSOParticle
from pylocating.information import Information
from pylocating.engines import ParticleEngine

from .matrix_generator import parameters_matrix


def builder(base, point, params, random_generator, position_initializator):
    """Sistematically generate environments from parameters combination."""
    index = 1
    for param in parameters_matrix(params):
        # read parameters from the matrix
        error = param[0]
        inertial_weight = param[1]
        cognition = param[2]
        social = param[3]
        num_particles = param[4]
        velocity_max = param[5]
        iterations_per_particle = param[6]
        # point disturbed by a gaussian noise
        disturbed_point = next(apply_noise_linear(point=point, error=error))
        # compute radius
        radius = matrix([distance(b, disturbed_point) for b in base])
        # build environment configuration
        env_config = {
            'inertial_weight': inertial_weight,
            'cognition': cognition,
            'social': social,
            'random': random_generator,
            'base': base,
            'radius': radius
        }
        env = Environment(config=env_config)
        # particle position generator
        position_generator = position_initializator(env)
        # particles inside env
        for i in range(num_particles):
            # particles
            PSOParticle(
                environment=env,
                id="P{}env{}".format(i, index),
                current=Information(position=next(position_generator)),
                velocity=velocity_max * random_generator.random(),
                vmax=velocity_max
            )

        # engine for env
        yield (param, ParticleEngine(
            config={
                'max_iterations': iterations_per_particle
            },
            environment=env
        ))

        # update environment index
