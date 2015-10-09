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

from pylocating import Particle, Information, Environment


class TestParticle(object):

    """Test particle."""

    def test_id(self):
        """Test if of a particle."""
        position = [1, 2, 3]
        fitness = 5
        myid = "myid"
        particle = Particle(environment=Environment(), id=myid,
                            position=position, bestResult=fitness)

        assert myid == particle.id

        particle = Particle(environment=Environment(),
                            position=position, bestResult=fitness)

        assert str(particle) == particle.id

    def test_particle_register_environment(self):
        """Test if particle update environment when set new best value."""
        position = [1, 2, 3]
        fitness = 5
        myinfo = Information(position, fitness)

        class Environment(object):
            def updateParticleBest(self, info):
                assert info == myinfo

            def register(self, particle):
                assert self == particle.environment

        Particle(environment=Environment(),
                 position=position, bestResult=fitness)

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

        position = [1, 2, 3]
        fitness = 5
        env.setInfo(Information(position, fitness))
        particle = Particle(environment=env,
                            position=position, bestResult=fitness)

        position = [4, 5, 6]
        fitness = 4
        env.setInfo(Information(position, fitness))
        particle.position = position
        particle.bestResult = fitness


class TestEnvironment(object):

    """Test environment."""

    def test_env_best_result(self):
        """Test the computation of global best result."""
        class Particle(object):
            def __init__(self, value):
                self.bestResult = value

        particles = {}
        particles[1] = Particle(3)
        particles[2] = Particle(10)
        particles[3] = Particle(40)
        particles[4] = Particle(25)
        particles[5] = Particle(7)
        particles[6] = Particle(37)

        env = Environment()
        env.particles = particles

        assert 40 == env.bestResult


class TestInformation(object):

    """Test information."""

    def test_internal(self):
        """Test data inside information object."""
        position = [4, 5, 6]
        fitness = 4
        info = Information(position=position, fitness=fitness)

        assert position == info.position
        assert fitness == info.fitness

    def test_equal(self):
        """Test information equal operator."""
        position1 = [4, 5, 6]
        position2 = [4, 5, 6]
        fitness1 = 4
        fitness2 = 4
        info1 = Information(position=position1, fitness=fitness1)
        info2 = Information(position=position2, fitness=fitness2)

        assert info1 == info2
