# -*- coding: utf-8 -*-
"""
Utility functions, such as calculating differently shaped areas
on the map grid.

Cell coordinates are represented as a tuple with x and y coordinates
in the map grid (x, y).
"""
from typing import List, Tuple
import re
import textwrap
import math
import itertools


def circle(center_x, center_y, size, radius):
    """
    Return a list of cells that form a circle.
    """
    cells = []
    for x in range(-size, size + 1):
        for y in range(-size, size + 1):
            if x * x + y * y < radius * radius:
                cells.append((center_x + x, center_y + y))
    return cells


def degree_between(src_x, src_y, dst_x, dst_y):
    """
    Return the degree between two coordinates.

    Return value: [0, 360)

    Examples:
    - (1, 0), (0, 1) -> 90
    - (1, 0), (0, -1) -> 270
    """
    dist = distance(src_x, src_y, dst_x, dst_y)

    if dist == 0:
        raise ValueError(
            'Cannot calculate degree if source and destination coordinates are the same.'
        )

    degree = math.degrees(math.asin((dst_y - src_y) / dist))

    if dst_x - src_x < 0:
        degree = 180 - degree
    elif degree < 0:
        degree += 360

    return degree


def degree_difference(deg1, deg2):
    """Return a difference between deg1 and deg2.

    deg1: (-inf, inf)
    deg2: (-inf, inf)
    return value: [0, 180)
    """

    if deg1 - deg2 > 0:
        dif = math.fmod(deg1 - deg2, 360)
    else:
        dif = math.fmod(deg2 - deg1, 360)
    return 360 - dif if dif >= 180 else dif


def in_angle(src_x, src_y, dst_x, dst_y, direction, angle_range):
    """Return True if the destination point is in given angle.

    direction: [0, 360) (like where you look at)
    angle_range: [0, 360) (like how wide your vision is)

    If destination is identical to source, return False.
    """

    if src_x == dst_x and src_y == dst_y:
        return False

    if degree_difference(direction, degree_between(src_x, src_y, dst_x,
                                                   dst_y)) < angle_range / 2:
        return True

    return False


def sector(src_x, src_y, dst_x, dst_y, angle, radius, bnd_x=1000, bnd_y=1000):
    """Return a list of cells which shapes sector.

    direction: float in [0, 360)
    angle: float in [0, 360)
    radius: float in [0, inf)
    """
    left = max(src_x - radius, 0)
    right = min(src_x + radius + 1, bnd_x)
    bottom = max(src_y - radius, 0)
    top = min(src_y + radius + 1, bnd_y)

    if src_x == dst_x and src_y == dst_y:
        return []

    direction = degree_between(src_x, src_y, dst_x, dst_y)

    cells = []

    for cur_x, cur_y in itertools.product(range(left, right),
                                          range(bottom, top)):
        if (distance(src_x, src_y, cur_x, cur_y) <= radius
                and in_angle(src_x, src_y, cur_x, cur_y, direction, angle)):
            cells.append((cur_x, cur_y))

    return cells


def disk(center_x, center_y, radius, bnd_x=1000, bnd_y=1000):
    """
    Return a list of cells that shapes a disk (a diamond shape).
    """
    left = max(center_x - radius, 0)
    right = min(center_x + radius + 1, bnd_x)
    bottom = max(center_y - radius, 0)
    top = min(center_y + radius + 1, bnd_y)

    cells = []

    # Limit the search area within square
    for cur_y in range(bottom, top):
        for cur_x in range(left, right):
            if distance(center_x, center_y, cur_x, cur_y) <= radius:
                cells.append((cur_x, cur_y))

    return cells


def frame(center_x, center_y, radius, bnd_x=1000, bnd_y=1000):
    """
    Return a list of cells that shape a frame.
    """
    left = center_x - radius
    right = center_x + radius
    bottom = center_y + radius
    top = center_y - radius

    cells = []

    #→ ↓
    #↑ ←
    if 0 <= top < bnd_y:  # topleft to topright
        cells.extend([(x, top) for x in range(left, right) if 0 <= x < bnd_x])
    if 0 <= right < bnd_x:  # topright to bottomright
        cells.extend([(right, y) for y in range(top, bottom)
                      if 0 <= y < bnd_y])
    if 0 <= bottom < bnd_y:  # bottomright to bottomleft
        cells.extend([(x, bottom) for x in range(right, left, -1)
                      if 0 <= x < bnd_x])
    if 0 <= left < bnd_x:  # bottomleft to topleft
        cells.extend([(left, y) for y in range(bottom, top, -1)
                      if 0 <= y < bnd_y])

    return cells


def distance(src_x, src_y, dst_x, dst_y):
    # Return distance between two points.
    return math.sqrt((dst_x - src_x)**2 + (dst_y - src_y)**2)
