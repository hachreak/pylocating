__version__ = "0.1.0"

# Base matrix
#
# [x0] [y0] [z0] - position of beacon 0
# [x1] [y1] [z1] - position of beacon 1
# [x2] [y2] [z2] - position of beacon 2
#  ..   ..   ..
# [xM] [yM] [zM] - position of beacon M
#
# Radius (distance of the object from the beacon
# [r0] - from beacon 0
# [r1] - from beacon 1
# [r2] - from beacon 2
#  ..
# [rM] - from beacon M
#
# Point (selected by the Bee)
# [px] [py] [px]
#

import numpy

def fitness(base, point, radius):
    """Fitness function."""
    mpoint = numpy.matrix([point, point, point])
    mbase = numpy.matrix(base)
    mradius = numpy.matrix(radius)
    difference = mbase - mpoint
    square_difference = numpy.multiply(difference, difference)
    sum_square_diff = square_difference.sum(axis=1)
    result = sum_square_diff - mradius.transpose()
    return result.sum()
