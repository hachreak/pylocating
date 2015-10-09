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

"""Python Object Localization."""

from __future__ import absolute_import, unicode_literals

from .information import Information

__version__ = "0.1.0"


def move(info, binfo, w, c1, c2, random):
    """Compute next position and velocity of the particle.

    :param info: information about current particle
    :param binfo: information about the particle with best fitness
    :param w: inertial weight
    :param c1: cognition parameter
    :param c2: social parameter
    :param random: randomizer object that return random diagonal matrix with
        values uniformed distributed in the interval [0,1)
    :return: new information of the particle
    """
    next_velocity = w * info.velocity + \
        c1 * random.next() * (binfo.velocity - info.velocity) + \
        c2 * random.next() * (binfo.position - info.position)
    next_position = info.position + next_velocity
    return Information(position=next_position, velocity=next_velocity,
                       fitness=info.fitness)
