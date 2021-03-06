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
from pylocating.particles import Particle


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

        # test set id == 0
        env = Environment(config={})
        p = Particle(environment=env, id=0)

        assert p.id == 0
        assert env.particles[0] == p

    def test_particle_register_environment(self):
        """Test if particle update environment when set new best value."""
        env = Environment(config={})
        position = matrix([1, 2, 3])
        fitness = 5
        myinfo = Information(position=position, fitness=fitness)

        p1 = Particle(
            environment=env, best=myinfo)
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
        particle = Particle(
            environment=env, best=info)

        position = matrix([4, 5, 6])
        fitness = 4
        info = Information(position=position, fitness=fitness)
        env.setInfo(info)
        particle.current = info

    def test_update_best(self):
        """Test update best result."""
        env = Environment(config={})

        old_best = Information(position=None, fitness=5)
        better_best = Information(position=None, fitness=3)
        worse_best = Information(position=None, fitness=7)
        particle = Particle(
            environment=env, current=old_best)

        assert particle.best == old_best

        particle.current = better_best
        assert particle.best == better_best

        particle.current = worse_best
        assert particle.best == better_best

    def test_set_high_velocity(self):
        """Test set high velocity."""
        env = Environment(config={})

        position = matrix([1, 2, 3])
        fitness = 5
        velocity = matrix([3, 100, 10])
        info = Information(position=position, fitness=fitness)

        particle = Particle(
            current=info,
            environment=env, vmax=1000,
            velocity=velocity
        )

        assert (particle.velocity == matrix([3, 100, 10])).all()

        particle = Particle(
            current=info,
            environment=env, vmax=20,
            velocity=velocity
        )

        assert (particle.velocity == matrix([3, 20, 10])).all()

        particle = Particle(
            current=info,
            environment=env, vmax=4,
            velocity=velocity
        )

        assert (particle.velocity == matrix([3, 4, 4])).all()

        particle = Particle(
            current=info,
            environment=env, vmax=1,
            velocity=velocity
        )

        assert (particle.velocity == matrix([1, 1, 1])).all()

    def test_index(self):
        """Test particle index."""
        env = Environment(config={})
        particles = []

        for i in range(10):
            particles.append(Particle(environment=env, id=i))

        for i in range(len(particles)):
            p = env.particles[i]
            assert p.index == i
