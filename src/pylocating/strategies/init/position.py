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

"""Init Strategy: position."""

from __future__ import absolute_import, unicode_literals

from ...utils import generate_points_in_surface_sphere


def around_beacons(environment):
    """Generate position around a beacon.

    The beacon selected is rotated every time.

    :param environment: environment of the particles
    :return: point as matrix
    """
    i = 0
    while True:
        random = environment.config['random']
        base = environment.config['base']
        (row, column) = base.shape
        yield base[i] + random.random()
        i = (i + 1) % row


def on_beacon_sphere_surface(environment, beacon_index, num_of_points):
    """Generate position around a beacon.

    The beacon selected is rotated every time.

    :param environment: environment of the particles
    :param beacon_index: index of the beacon
    :param num_of_points: how many points are generated in the surface
    :return: point as matrix
    """
    base = environment.config['base']
    radius = environment.config['radius']
    bi = beacon_index
    generator = generate_points_in_surface_sphere(base[bi],
                                                  radius.A[0][bi],
                                                  num_of_points)
    while True:
        yield next(generator)
