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

"""Test Python Object Localization."""

from __future__ import absolute_import, unicode_literals

from numpy import matrix
from pylocating.information import Information
from pylocating.environment import Environment
from pylocating.particles import PSOParticle


class TestPSOParticle(object):

    """Test PSO Particle."""

    def test_move_one_values(self):
        """Test move."""
        class Random(object):
            def random(self):
                return 1

        info = Information(position=matrix([1, 1, 1]), fitness=5)
        binfo = Information(position=matrix([1, 1, 1]), fitness=5)
        velocity = matrix([1, 1, 1])

        config = {}
        config['inertial_weight'] = 1
        config['cognition'] = 1
        config['social'] = 1
        config['random'] = Random()
        env = Environment(config)

        particle = PSOParticle(environment=env,
                               current=info, best=binfo, velocity=velocity)
        new_info = particle.move()
        assert (particle.velocity == matrix([1, 1, 1])).all()
        assert (new_info.position == matrix([2, 2, 2])).all()

    def test_move_defined_values(self):
        """Test move."""
        class Random(object):
            def random(self):
                return 1

        config = {
            'inertial_weight': 1,
            'cognition': 1,
            'social': 1,
            'random': Random(),
            'base': matrix([
                [0, 0, 0],   # beacon 1
                [7, 5, 0],   # beacon 2
                [5, -4, 0],  # beacon 3
            ]),
            'radius': matrix([
                3.024,   # beacon 1
                6.4,     # beacon 2
                6.63,  # beacon 3
            ])
        }
        env = Environment(config)

        particle = PSOParticle(environment=env,
                               current=Information(position=matrix([1, 1, 1])))
        particle.fitness()
        assert 20.14 < particle.best.fitness < 20.15

        particle.move()
        assert (particle.current.position == matrix([2, 2, 2])).all()

        particle.fitness()
        assert 10.85 < particle.best.fitness < 10.86

        particle.move()
        assert (particle.current.position == matrix([3, 3, 3])).all()

        particle.fitness()
        assert 47.85 < particle.current.fitness < 47.86
        assert 10.85 < particle.best.fitness < 10.86

        particle.move()
        assert (particle.current.position == matrix([2, 2, 2])).all()
