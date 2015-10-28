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

"""Test Benchmarks Moving Point Engine."""

from __future__ import absolute_import, unicode_literals

from numpy import matrix
from pylocating.benchmarks.moving_point import MovingPointEngine, \
    EnvironmentListener
from pylocating.utils import distance


class TestBenchmarksMatrixGenerator(object):

    """Test Benchmarks Matrix generator."""

    def test_generate_matrix_of_points_in_cube(self):
        """Test moving point engine."""
        config = {'sleep': 0.01}
        point = matrix([0, 0, 0])

        def generator():
            while True:
                yield point

        class Listener(object):
            def position(self, value):
                pass

        # test 1
        count = 5
        mp = MovingPointEngine(
            config=config, listener=Listener(),
            start_point=matrix([0, 0, 0]),
            positions=generator(),
            stop_condition=lambda mp: mp.iterations >= count)
        mp.start()
        mp.join()
        assert mp.iterations == count

        # test 2
        count = 43
        mp = MovingPointEngine(
            config=config, listener=Listener(),
            start_point=matrix([0, 0, 0]),
            positions=generator(),
            stop_condition=lambda mp: mp.iterations >= count)
        mp.start()
        mp.join()
        assert mp.iterations == count

        # test 3
        count = -1
        mp = MovingPointEngine(
            config=config, listener=Listener(),
            start_point=matrix([0, 0, 0]),
            positions=generator(),
            stop_condition=lambda mp: mp.iterations >= count)
        mp.start()
        mp.join()
        assert mp.iterations == 0

    def test_default_generator(self):
        """Test default generator."""
        config = {'sleep': 0.01}
        point = matrix([0, 0, 0])

        def generator():
            i = point
            while True:
                yield i
                i = i + 1

        class Listener(object):

            def __init__(self):
                self._point = point

            def position(self, value):
                assert (self._point == value).all()
                self._point = self._point + 1

        # test 1
        count = 12
        mp = MovingPointEngine(
            config=config, listener=Listener(),
            start_point=matrix([0, 0, 0]),
            positions=generator(),
            stop_condition=lambda mp: mp.iterations >= count)
        mp.start()
        mp.join()
        assert mp.iterations == count

    def test_stop_iteration(self):
        """Test when finish next positions."""
        config = {'sleep': 0.01}
        point = matrix([0, 0, 0])

        def generator():
            return iter([
                matrix([0, 0, 0]), matrix([1, 1, 1]), matrix([2, 2, 2]),
                matrix([3, 3, 3])
            ])

        class Listener(object):

            def __init__(self):
                self._point = point

            def position(self, value):
                assert (self._point == value).all()
                self._point = self._point + 1

        # test 1
        count = 12
        mp = MovingPointEngine(
            config=config, listener=Listener(),
            start_point=matrix([0, 0, 0]),
            positions=generator(),
            stop_condition=lambda mp: mp.iterations >= count)
        mp.start()
        mp.join()
        assert mp.iterations == 4

    def test_env_listener(self):
        """Test env listener."""
        class Environment(object):
            def __init__(self):
                self.config = {
                    'base': matrix([
                        [1, 2, 4],
                        [5, 6, 7],
                        [8, 9, 10]
                    ])
                }
        env = Environment()
        listener = EnvironmentListener(environment=env, error=1)
        point = matrix([6, 5, 4])
        listener.position(point)

        result = matrix([distance(env.config['base'].A[0], point),
                         distance(env.config['base'].A[1], point),
                         distance(env.config['base'].A[2], point)])
        assert (env.config['radius'] != result).all()
