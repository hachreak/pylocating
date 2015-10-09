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

"""Python Localization Particle."""

from __future__ import absolute_import, unicode_literals

from .information import Information


class Particle(object):

    """Particle representation."""

    def __init__(self, environment, id=None, current=None, best=None):
        """Init particle."""
        self._id = id
        self.environment = environment
        self.environment.register(self)
        self.current = current or Information()
        self.best = best or Information()

    @property
    def id(self):
        """Get id."""
        return self._id if self._id else str(self)

    @id.setter
    def id(self, value):
        """Set id."""
        self._id = value
