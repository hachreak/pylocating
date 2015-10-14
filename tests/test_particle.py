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

"""Test Python Localization Particle."""

from __future__ import absolute_import, unicode_literals

from numpy import matrix
from pylocating.environment import Environment
from pylocating.information import Information
from pylocating.particle import Particle


class TestParticle(object):

    """Test particle."""

    def test_id(self):
        """Test if of a particle."""
        position = [1, 2, 3]
        fitness = 5
        myid = "myid"
        particle = Particle(
            environment=Environment(config={}), id=myid,
            best=Information(position=position, fitness=fitness))

        assert myid == particle.id

        particle = Particle(
            environment=Environment(config={}),
            best=Information(position=position, fitness=fitness))

        assert str(particle) == particle.id

    def test_particle_register_environment(self):
        """Test if particle update environment when set new best value."""
        env = Environment(config={})
        position = matrix([1, 2, 3])
        fitness = 5
        myinfo = Information(position=position, fitness=fitness)

        p1 = Particle(environment=env, best=myinfo)
        assert env.best == p1

    def test_register_new_local_best_result(self):
        """Register new local best result."""
        class Environment(object):
            def setInfo(self, info):
                self.info = info

            def updateParticleBest(self, info):
                assert info == self.info

            def register(self, particle):
                assert self == particle.environment

        env = Environment()

        position = matrix([1, 2, 3])
        fitness = 5
        info = Information(position=position, fitness=fitness)
        env.setInfo(Information(position=position, fitness=fitness))
        particle = Particle(environment=env, best=info)

        position = matrix([4, 5, 6])
        fitness = 4
        info = Information(position=position, fitness=fitness)
        env.setInfo(info)
        particle.best = info
