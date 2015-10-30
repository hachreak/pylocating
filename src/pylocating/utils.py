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

"""Utilities."""

from __future__ import absolute_import, unicode_literals

try:
    from functools import lru_cache
except ImportError:
    from functools32.functools32 import lru_cache

from copy import deepcopy
from numpy import matrix, linspace, meshgrid, sin, cos, pi, sqrt, multiply, \
    random as nprandom


class Random(object):

    """Randomizer."""

    def random(self):
        """Return random [0,1) matrix 3x1."""
        val = nprandom.random()
        return matrix([val, val, val])


class Random3D(object):

    """Randomizer."""

    def random(self):
        """Return random [0,1) matrix 3x1."""
        return matrix([nprandom.random(),
                       nprandom.random(),
                       nprandom.random()])


class RandomND(object):

    """Randomizer."""

    def __init__(self, dimensions=1):
        """Init."""
        self._dimensions = dimensions

    def random(self):
        """Return random [0,1) matrix 3x1."""
        return matrix([nprandom.random() for i in range(self._dimensions)])


class Randn(object):

    """Randomizer with a normal distribution."""

    def __init__(self, sigma=None, mu=None):
        """Init."""
        self._sigma = sigma or 1
        self._mu = mu or 0

    def _random_num(self, count=1):
        """Get new random num."""
        return self._sigma * nprandom.randn(count) + self._mu

    def random(self):
        """Return random [0,1) matrix 3x1."""
        return matrix(self._random_num(1))


class Randn3D(Randn):

    """Randomizer with a normal distribution."""

    def random(self):
        """Return random [0,1) matrix 3x1."""
        return matrix(self._random_num(3))


@lru_cache(maxsize=100)
def _points_in_surface_sphere(num_of_points):
    """Return a point in the surface of the sphere.

    :param num_of_points: how many point to describe the surface
    :return: points
    """
    row = int(sqrt(num_of_points))
    if num_of_points % (row**2) > 0:
        row = row + 1
    [phi, theta] = meshgrid(linspace(0, 2 * pi, row), linspace(0, pi, row))
    phi = matrix(phi)
    theta = matrix(theta)
    x = multiply(sin(theta), cos(phi))
    y = multiply(sin(theta), sin(phi))
    z = cos(theta)

    return list(map(lambda x, y, z: matrix([x, y, z]), x.A1, y.A1, z.A1))


def generate_points_in_surface_sphere(center, radius, num_of_points):
    """Generate a point on sphere surface defined by center and radius.

    :param center: sphere center
    :param radius: sphere radius
    :param num_of_points: how many points to describe the surface
    :return: point as matrix
    """
    points = iter(_points_in_surface_sphere(num_of_points))
    while True:
        yield radius * next(points) + center


def generate_points_random_in_surface_sphere(center, radius, random=None):
    """Generate random points on sphere surface defined by center and radius.

    e.g. generate randomly point around center [10, 10, 10] distant 4 from it.

    .. code-block:: python

        from numpy import matrix
        center = matrix([10, 10, 10])
        radius = 4
        generator = generate_points_random_in_surface_sphere(center, radius)
        point = next(generator)

    :param center: sphere center
    :param radius: shere radius
    :param random: random number generator
    :return: point as matrix
    """
    while True:
        random = random or nprandom
        phi = 2.0 * pi * random.random()
        theta = pi * random.random()
        x = radius * sin(theta) * cos(phi)
        y = radius * sin(theta) * sin(phi)
        z = radius * cos(theta)
        yield matrix([x, y, z]) + center


def generate_sequential_points(start_point, vmax=None, random=None):
    """Generate sequential points.

    :param start_point: point where to start
    :param random: random generator
    :return: next point
    """
    point = deepcopy(start_point)
    vmax = vmax or 1.0
    random = random or RandomND(dimensions=point.shape[1])
    while True:
        point = point + vmax * random.random() - \
            matrix([vmax/2, vmax/2, vmax/2])
        yield point


def generate_line_of_points(start_point, vmax=None):
    """Generate sequential points.

    :param start_point: point where to start
    :param random: random generator
    :return: next point
    """
    point = deepcopy(start_point)
    vmax = vmax or 1.0
    while True:
        point = point + vmax
        yield point


def generate_matrix_of_points_in_cube(center, side_length, num_of_points,
                                      random=None):
    """Generate a matrix of points inside a cube.

    e.g. Generate a matrix of 3 points inside a cube centered in
         (1000, 1000, 1000) with a side length of 40 (9980<x,y,z<1020)

    .. code-block:: python

        gen = generate_points_in_cube(matrix([1000,1000,1000]), 40, 3)

        mypoints = next(gen)

    :param center: sphere center
    :param num_of_points: number of row of the generated matrix
    :param side_length: cube side_length
    :return: matrix of point inside the cube.
    """
    random = random or nprandom
    new_center = center - matrix([side_length/2, side_length/2, side_length/2])
    while True:
        yield matrix(random.rand(num_of_points, 3)) * side_length + new_center


def distance(point_1, point_2):
    """Compute the euclidean distance from the two points."""
    return sqrt(sum((point_1-point_2).A[0]**2))
