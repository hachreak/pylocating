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

"""Test Python Localization Information."""

from __future__ import absolute_import, unicode_literals

from numpy import matrix
from pylocating.information import Information


class TestInformation(object):

    """Test information."""

    def test_internal(self):
        """Test data inside information object."""
        position = matrix([4, 5, 6])
        fitness = 4
        velocity = matrix([7, 8, 9])
        info = Information(position=position, fitness=fitness,
                           velocity=velocity)

        assert (position == info.position).all()
        assert fitness == info.fitness
        assert (velocity == info.velocity).all()

    def test_equal(self):
        """Test information equal operator."""
        position1 = matrix([4, 5, 6])
        position2 = matrix([4, 5, 6])
        fitness1 = 4
        fitness2 = 4
        velocity1 = matrix([7, 8, 9])
        velocity2 = matrix([7, 8, 9])
        info1 = Information(position=position1, fitness=fitness1,
                            velocity=velocity1)
        info2 = Information(position=position2, fitness=fitness2,
                            velocity=velocity2)

        assert info1 == info2
