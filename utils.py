# -*- coding: utf-8 -*-
"""Utilities.

Cells coordinates are represented in tuple (x, y).
"""
import re
import textwrap
import math
import itertools


def wrap_tagged(text, width, **kwargs):
    """Wrap text which contains BearLibTerminal tags like '[color=red]something[/color]'.

    Can pass kwargs to textwrap.wrap().
    drop_whitespace=False by default."""
    lines = text.splitlines()
    wrapped_lines = []

    # handling bearlibterminal's tag with textwrap, it was hard for me!
    # 1. find and extract tag and its positions
    # 2. textwrap (w/o tag strings)
    # 3. insert extracted tags at original position
    pattern = r'\[.*?\]'  # tag syntax
    for line_ in lines:
        iterator = re.finditer(pattern, line_)
        tags = []

        for match in iterator:
            tags.append((match.start(), match.group()))

        line_ = re.sub(pattern, '', line_)

        wrapped_line = textwrap.wrap(line_, width, drop_whitespace=False, **kwargs)

        compensation = 0  # we need this because textwrap does not count tag strings
        for start, group in tags:
            # cur = start + compensation
            cur = start
            num = cur // (width + compensation)

            # insert
            wrapped_line[num] = group.join([wrapped_line[num][:cur], wrapped_line[num][cur:]])

            compensation += len(group)

        wrapped_lines.extend(wrapped_line)

    return wrapped_lines


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
        raise ValueError('Function degree_between() receives two identical points.')

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

    if degree_difference(direction, degree_between(src_x, src_y, dst_x, dst_y)) < angle_range / 2:
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
    for cur_x, cur_y in itertools.product(range(left, right), range(bottom, top)):
        if (distance(src_x, src_y, cur_x, cur_y) <= radius
                and in_angle(src_x, src_y, cur_x, cur_y, direction, angle)):
            cells.append((cur_x, cur_y))

    return cells


def disk(center_x, center_y, radius, bnd_x=1000, bnd_y=1000):
    """Return a list of cells which shapes a disk."""
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
        cells.extend([(right, y) for y in range(top, bottom) if 0 <= y < bnd_y])
    if 0 <= bottom < bnd_y:  # bottomright to bottomleft
        cells.extend([(x, bottom) for x in range(right, left, -1) if 0 <= x < bnd_x])
    if 0 <= left < bnd_x:  # bottomleft to topleft
        cells.extend([(left, y) for y in range(bottom, top, -1) if 0 <= y < bnd_y])

    # print(frame)

    return cells


def line(x1, y1, x2, y2):
    """Return a list of cells generated by Bresenham's line algorithm."""

    # when slope is 1
    if x1 == x2:
        # take care when y2 < y1
        step = sign(y2 - y1)
        return [(x1, y) for y in range(y1, y2 + step, step)]

    # when slope is 0
    if y1 == y2:
        step = sign(x2 - x1)
        return [(x, y1) for x in range(x1, x2 + step, step)]

    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    cells = []
    for x in range(x1, x2 + 1):
        cell = (y, x) if is_steep else (x, y)
        cells.append(cell)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        cells.reverse()
    return cells


def distance(src_x, src_y, dst_x, dst_y):
    """Return a distance of two points."""
    return math.sqrt((dst_x - src_x) ** 2 + (dst_y - src_y) ** 2)


def sign(num):
    """Python has no sign."""
    return int(math.copysign(1, num))
