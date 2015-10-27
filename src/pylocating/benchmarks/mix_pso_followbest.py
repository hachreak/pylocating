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
from pylocating.particles import PSOParticle, FollowBestParticle
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
        num_psoparticles = param[4]
        num_fbparticles = param[5]
        velocity_max = param[6]
        iterations_per_particle = param[7]
        # point disturbed by a gaussian noise
        disturbed_point_gen = apply_noise_linear(point=point, error=error)
        # compute radius
        radius = matrix([distance(b, next(disturbed_point_gen)) for b in base])

        # build environments configuration
        env_config = {
            'inertial_weight': inertial_weight,
            'cognition': cognition,
            'social': social,
            'random': random_generator,
            'base': base,
            'radius': radius
        }

        # [ENV1 - PSOParticles]
        env1 = Environment(config=env_config)
        # particle position generator
        position_generator = position_initializator(env1)
        # particles inside env1
        for i in range(num_psoparticles):
            # particles
            PSOParticle(
                environment=env1,
                id="P{}env1-{}".format(i, index),
                current=Information(position=next(position_generator)),
                velocity=random_generator.random(),
                vmax=velocity_max
            )

        # [ENV2 - FollowBestParticles]
        env2 = Environment(config=env_config)
        # particle position generator
        position_generator = position_initializator(env2)
        # particles inside env2
        for i in range(num_fbparticles):
            # particles
            FollowBestParticle(
                environment=env2,
                id="P{}env2-{}".format(i, index),
                current=Information(position=next(position_generator)),
                velocity=random_generator.random(),
                vmax=velocity_max
            )

        # connect environments
        env1.registerNeighbor(env2)

        # engines for env1 and env2
        yield (param,
               ParticleEngine(
                   config={
                       'max_iterations': iterations_per_particle
                   },
                   environment=env1
               ),
               ParticleEngine(
                   config={
                       'max_iterations': iterations_per_particle
                   },
                   environment=env2
               ))
