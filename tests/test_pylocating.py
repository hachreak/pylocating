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

import numpy

from pylocating import Particle, Information, Environment, move


class TestParticle(object):

    """Test particle."""

    def test_id(self):
        """Test if of a particle."""
        position = [1, 2, 3]
        fitness = 5
        myid = "myid"
        particle = Particle(
            environment=Environment(), id=myid,
            info=Information(position=position, fitness=fitness))

        assert myid == particle.id

        particle = Particle(
            environment=Environment(),
            info=Information(position=position, fitness=fitness))

        assert str(particle) == particle.id

    def test_particle_register_environment(self):
        """Test if particle update environment when set new best value."""
        position = numpy.matrix([1, 2, 3])
        fitness = 5
        myinfo = Information(position=position, fitness=fitness)

        class Environment(object):
            def updateParticleBest(self, info):
                assert info == myinfo

            def register(self, particle):
                assert self == particle.environment

        Particle(environment=Environment(), info=myinfo)

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

        position = numpy.matrix([1, 2, 3])
        fitness = 5
        info = Information(position=position, fitness=fitness)
        env.setInfo(Information(position=position, fitness=fitness))
        particle = Particle(environment=env, info=info)

        position = numpy.matrix([4, 5, 6])
        fitness = 4
        info = Information(position=position, fitness=fitness)
        env.setInfo(info)
        particle.bestResult = info


class TestEnvironment(object):

    """Test environment."""

    def test_env_best_result(self):
        """Test the computation of global best result."""
        env = Environment()
        position = numpy.matrix([0, 0, 0])

        particles = {}
        particles[1] = Particle(
            environment=env,
            info=Information(position=position, fitness=3))
        particles[2] = Particle(
            environment=env,
            info=Information(position=position, fitness=10))
        particles[3] = Particle(
            environment=env,
            info=Information(position=position, fitness=40))
        particles[4] = Particle(
            environment=env,
            info=Information(position=position, fitness=25))
        particles[5] = Particle(
            environment=env,
            info=Information(position=position, fitness=7))
        particles[6] = Particle(
            environment=env,
            info=Information(position=position, fitness=37))

        best = env.best
        assert particles[3] == best
        assert (particles[3].bestResult == best.bestResult).all()


class TestInformation(object):

    """Test information."""

    def test_internal(self):
        """Test data inside information object."""
        position = numpy.matrix([4, 5, 6])
        fitness = 4
        velocity = numpy.matrix([7, 8, 9])
        info = Information(position=position, fitness=fitness,
                           velocity=velocity)

        assert (position == info.position).all()
        assert fitness == info.fitness
        assert (velocity == info.velocity).all()

    def test_equal(self):
        """Test information equal operator."""
        position1 = numpy.matrix([4, 5, 6])
        position2 = numpy.matrix([4, 5, 6])
        fitness1 = 4
        fitness2 = 4
        velocity1 = numpy.matrix([7, 8, 9])
        velocity2 = numpy.matrix([7, 8, 9])
        info1 = Information(position=position1, fitness=fitness1,
                            velocity=velocity1)
        info2 = Information(position=position2, fitness=fitness2,
                            velocity=velocity2)

        assert info1 == info2


class TestMove(object):

    """Test default function to compute new position and velocity."""

    def test_move_one_values(self):
        """Test move."""
        class Random(object):
            def next(self):
                return 1

        info = Information(position=numpy.matrix([1, 1, 1]),
                           velocity=numpy.matrix([1, 1, 1]), fitness=5)
        binfo = Information(position=numpy.matrix([1, 1, 1]),
                           velocity=numpy.matrix([1, 1, 1]), fitness=5)
        w = 1
        c1 = 1
        c2 = 1
        new_info = move(info=info, binfo=binfo, w=w, c1=c1, c2=c2,
                            random=Random())
        assert (new_info.velocity == numpy.matrix([1, 1, 1])).all()
        assert (new_info.position == numpy.matrix([2, 2, 2])).all()
