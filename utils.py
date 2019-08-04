# -*- coding: utf-8 -*-
"""Utilities.

Cells coordinates are represented in tuple (x, y).
"""
import re
import textwrap
import math
import itertools


def degree_between(src_x, src_y, dst_x, dst_y):
    """Return degree between two coordinates.

    Return value: [0, 360)

    Examples:
    - (1, 0), (0, 1) -> 90
    - (1, 0), (0, -1) -> 270
    """
    dist = distance(src_x, src_y, dst_x, dst_y)

    # avoid zero dividing
    if dist == 0:
        raise ValueError(
            'Function degree_between() receives two identical points.')

    # degree in [-90, 90]
    degree = math.degrees(math.asin((dst_y - src_y) / dist))

    # imagine graph
    if dst_x - src_x < 0:
        degree = 180 - degree
    elif degree < 0:  # delta x > 0 and...
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
    """Return a list of cells which shapes sector (fan shaped figure).

    direction: float in [0, 360)
    angle: float in [0, 360)
    radius: float in [0, inf)
    """
    left = max(src_x - radius, 0)
    right = min(src_x + radius + 1, bnd_x)
    bottom = max(src_y - radius, 0)
    top = min(src_y + radius + 1, bnd_y)

    # return empty list if given two identical points
    # degree_between() raise an error if given those points
    if src_x == dst_x and src_y == dst_y:
        return []

    direction = degree_between(src_x, src_y, dst_x, dst_y)

    cells = []

    # limit search area within square
    for cur_x, cur_y in itertools.product(range(left, right),
                                          range(bottom, top)):
        if (distance(src_x, src_y, cur_x, cur_y) <= radius
                and in_angle(src_x, src_y, cur_x, cur_y, direction, angle)):
            cells.append((cur_x, cur_y))

    return cells


def disk(center_x, center_y, radius, bnd_x=1000, bnd_y=1000):
    # Return a list of cells which shapes a disk.
    left = max(center_x - radius, 0)
    right = min(center_x + radius + 1, bnd_x)
    bottom = max(center_y - radius, 0)
    top = min(center_y + radius + 1, bnd_y)

    cells = []

    # limit search area within square
    for cur_y in range(bottom, top):
        for cur_x in range(left, right):
            if distance(center_x, center_y, cur_x, cur_y) <= radius:
                cells.append((cur_x, cur_y))

    return cells


def frame(center_x, center_y, radius, bnd_x=1000, bnd_y=1000):
    """Return a list of cells which shapes a frame.

    You can specify boundary.
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
