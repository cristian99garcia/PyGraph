#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


def html_to_cairo(color):
    # Convertir un html color(hexadecimal) a un cairo color. 
    if color.startswith('#'): 
        color = color[1:] 

    (r, g, b) = (int(color[:2], 16),
                 int(color[2:4], 16),
                 int(color[4:], 16))

    return rgb_to_cairo((r, g, b)) 


def rgb_to_cairo(color): 
    # Convertir un color RGB a un cairo color
    return (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)


def get_cairo_color(color):
    # Convertir un html color o un rgb color a un cairo color
    if type(color) == str:
        # color HTML
        return html_to_cairo(color)

    elif type(color) in [list, tuple]:
        if max(color) >= 1.0:
            return rgb_to_cairo(color)

        else:
            return color

    else:
        raise TypeError('"color" must be a list, a tuple, or a string, not a %s' % (str(type(color))).split(' ')[1][:-1])


def get_random_color():
    return (random.randint(1, 100) / 100.0, random.randint(1, 100) / 100.0, random.randint(1, 100) / 100.0)


def get_opposite_color(color):
    color = get_cairo_color(color)
    if color != (0.5, 0.5, 0.5):
        return (1.0 - color[0], 1.0 - color[1], 1.0 - color[2])
    else:
        return (1.0, 1.0, 1.0)