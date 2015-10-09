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

"""Python Localization Information Unit."""

from __future__ import absolute_import, unicode_literals

from numpy import matrix


class Information(object):

    """Single unit of Information shareb by the particles."""

    def __init__(self, position=None, fitness=None, velocity=None):
        """Init information."""
        self.position = position if position is not None else \
            matrix([0, 0, 0])
        self.fitness = fitness or 0
        self.velocity = velocity if velocity is not None else \
            matrix([0, 0, 0])

    def isBetterThan(self, info):
        """Check if this is better that the other iformation."""
        return self.fitness >= info.fitness

    def __eq__(self, other):
        """Test if `self` is equal to `other`."""
        return (self.position == other.position).all() and \
            self.fitness == other.fitness and \
            (self.velocity == other.velocity).all()
