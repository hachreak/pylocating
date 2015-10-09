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
from pylocating import move
from pylocating.information import Information


class TestMove(object):

    """Test default function to compute new position and velocity."""

    def test_move_one_values(self):
        """Test move."""
        class Random(object):
            def next(self):
                return 1

        info = Information(position=matrix([1, 1, 1]),
                           velocity=matrix([1, 1, 1]), fitness=5)
        binfo = Information(position=matrix([1, 1, 1]),
                            velocity=matrix([1, 1, 1]), fitness=5)
        w = 1
        c1 = 1
        c2 = 1
        new_info = move(info=info, binfo=binfo, w=w, c1=c1, c2=c2,
                        random=Random())
        assert (new_info.velocity == matrix([1, 1, 1])).all()
        assert (new_info.position == matrix([2, 2, 2])).all()
