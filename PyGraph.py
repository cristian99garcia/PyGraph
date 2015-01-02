#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PyGraph.py
#
# Copyright (c) 2015 Cristian García
#
# Author: Cristian García <cristian99garcia@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import math
import utils


class DotGraph():

    def __init__(self, context=None, data={},
                 colors={}, width=500, height=500):

        """
        context:
            Un cairo context sobre el cual dibujar.

        data:
            Un diccionario, con los nombres de los datos a graficar
            como keys, y una lista de esas como los valores a graficar.

        colors:
            Un diccionario, con las mimsas keys utilizadas en data, con una
            tupla con 3 decimales(del 0 al 1) para indicar el color del
            elemento key.

        width:
            Un entero o un decimal, el ancho total de la gráfica.
            Para usar el ancho total de un GtkDrawingArea:

            allocation = area.get_allocation()
            width = allocation.width

        height:
            Un entero o un decimal, el alto total de la gráfica.
            Para usar el alto total de un GtkDrawingArea:

            allocation = area.get_allocation()
            height = allocation.height
        """

        self.context = context
        self.set_data(data)
        self.set_colors(colors)
        self.set_width(width)
        self.set_height(height)
        self.background = (1, 1, 1)
        self.border = 10
        self.draw_frame = True
        self.frame_width = 2
        self.frame_color = (0.5, 0.5, 0.5)
        self.draw_axes = True
        self.draw_rows = True
        self.draw_marks = True
        self.draw_marks_labels = True
        self.axes_marks = 6
        self.axes_width = 4
        self.axes_color = (0, 0, 0)
        self.axes_labels_sizes = 15
        self.dots_radius = 5
        self.graph_line_width = 2

    def set_context(self, context):
        """
        context:
            Un cairo context sobre el cual dibujar
        """

        self.context = context

    def get_context(self):
        return self.context

    def set_data(self, data):
        """
        data:
            Un diccionario, con los nombres de los datos a graficar
            como keys, y una lista con los valores a graficar.
        """

        if type(data) == dict:
            self.data = data
        else:
            return TypeError('"data" must be a dict')

    def get_data(self):
        return self.data

    def set_colors(self, colors):
        """
        colors:
            Un diccionario, con las mimsas keys utilizadas en self.data, con
            una tupla con 3 decimales(del 0 al 1) para indicar el color del
            elemento key.
            También puede ser un color de HTML(hexadecimal) o un color
            RGB(una tupla o lista con valores del 0 al 255)
        """

        if type(colors) == dict:
            for name in colors:
                colors[name] = utils.get_cairo_color(colors[name])

            self.colors = colors
        else:
            return TypeError('"colors" must be a dict')

    def set_width(self, width):
        """
        width:
            Un entero o un decimal, el ancho total de la gráfica.
            Para usar el ancho total de un GtkDrawingArea:

            allocation = area.get_allocation()
            width = allocation.width
        """

        if type(width) in [float, int]:
            self.width = width
        else:
            raise TypeError('"width" must be a int or float')

    def get_width(self):
        return self.width

    def set_height(self, height):
        """
        height:
            Un entero o un decimal, el alto total de la gráfica
            Para usar el alto total de un GtkDrawingArea:

            allocation = area.get_allocation()
            height = allocation.height
        """

        if type(height) in [float, int]:
            self.height = height
        else:
            raise TypeError('"height" must be a int or float')

    def set_background(self, background):
        """
        background:
            Una lista o una tupla con tres valores,
            del 0.0 al 1.0 o del 0 al 255, ejemplos:
            [0.4, 0.3, 0.6]    (0.2, 0.6, 1.0)    [35, 200, 110]

            También puede ser una cadena de texto, en formato hexadecimal
            Por ejemplo:
                "#32FF32"
        """

        if type(background) in [list, tuple, str]:
            self.background = utils.get_cairo_color(background)
        else:
            raise TypeError(
                '"background" must be a list, a tuple, or a string')

    def get_background(self):
        return self.background

    def set_border(self, border):
        """
        border:
            Un entero o un decimal
        """

        if type(border) in [int, float]:
            self.border = border
        else:
            raise TypeError('"border" must be a int or float')

    def get_border(self):
        return self.border

    def set_draw_frame(self, draw_frame):
        """
        draw_frame:
            Un booleano
        """

        if type(draw_frame) == bool:
            self.draw_frame = draw_frame
        else:
            raise TypeError('"draw_frame" must be a bool')

    def get_draw_frame(self):
        return self.draw_frame

    def set_frame_width(self, frame_width):
        """
        frame_width:
            Un entero o un decimal
        """

        if type(frame_width) in [int, float]:
            self.frame_width = frame_width
        else:
            raise TypeError('"frame_width" must be a int or float')

    def get_frame_width(self):
        return self.frame_width

    def set_frame_color(self, frame_color):
        """
        frame_color:
            Un color(ya sea hexadecimal, rgb, o cairo color) para pintar
            el fondo de la gráfica
        """

        if type(frame_color) in [list, tuple, str]:
            self.frame_color = utils.get_cairo_color(frame_color)
        else:
            raise TypeError(
                '"background" must be a list, a tuple, or a string')

    def get_frame_color(self):
        return self.frame_color

    def set_draw_axes(self, draw_axes):
        """
        draw_axes:
            Un booleano, indica si se dibujan los ejes
        """

        if type(draw_axes) == bool:
            self.draw_axes = draw_axes
        else:
            raise TypeError('"draw_axes" must be a bool')

    def get_draw_axes(self):
        return self.draw_axes

    def set_draw_rows(self, draw_rows):
        """
        draw_rows:
            Un booleano, indica si se dibujan las flechas de los ejes
        """

        if type(draw_rows) == bool:
            self.draw_rows = draw_rows
        else:
            raise TypeError('"draw_rows" must be a bool')

    def get_draw_rows(self):
        return self.draw_rows

    def set_draw_marks(self, draw_marks):
        """
        draw_marks:
            Un booleano, indica si se dibujan las marcas en los ejes
        """

        if type(draw_marks) == bool:
            self.draw_marks = draw_marks
        else:
            raise TypeError('"draw_marks" must be a bool')

    def get_draw_marks(self):
        return self.draw_marks

    def set_draw_marks_labels(self, draw_marks_labels):
        """
        draw_marks_labels:
            Un booleano, indica si se dibujan las etiquetas que indican los
            valores de las marcas en los ejes
        """

        if type(draw_marks_labels) == bool:
            self.draw_marks_labels = draw_marks_labels
        else:
            raise TypeError('"draw_marks_labels" must be a bool')

    def get_draw_marks_labels(self):
        return self.draw_marks_labels

    def set_number_of_axes_marks(self, axis_marks):
        """
        axis_marks:
            Un entero, la cantidad de marcas en los ejes
        """

        if type(axis_marks) == int:
            self.axis_marks = axis_marks
        else:
            raise TypeError('"axis_marks" must be a int')

    def get_number_of_axes_marks(self):
        return self.axis_marks

    def set_axes_width(self, axes_width):
        """
        axes_width:
            Un entero o decimal, el ancho de los ejes
        """

        if type(axes_width) in [int, float]:
            self.axes_width = axes_width
        else:
            raise TypeError('"axes_width" must be a number')

    def get_axes_width(self):
        return self.axes_width

    def set_axes_color(self, axes_color):
        """
        axes_color:
            El color para dibujar los ejes
        """

        if type(axes_color) in [list, tuple, str]:
            self.axes_color = utils.get_cairo_color(axes_color)
        else:
            raise TypeError('"axes_color" must be a list, a tuple or a str')

    def get_axes_color(self):
        return self.axes_color

    def set_axes_labels_sizes(self, axes_labels_sizes):
        """
        axes_labels_sizes:
            Un entero, el tamaño de la fuente de las etiquetas de las marcas
            de los ejes
        """

        if type(axes_labels_sizes) == int:
            self.axes_color = utils.get_cairo_color(axes_labels_sizes)
        else:
            raise TypeError('"axes_labels_sizes" must be a int')

    def set_dots_radius(self, dots_radius):
        """
        dots_radius:
            Un entero, el tamaño del radio de los puntos en la gráfica
        """

        if type(dots_radius) in [int, float]:
            self.dots_radius = dots_radius
        else:
            raise TypeError('"dots_radius" must be a number')

    def get_dots_radius(self):
        return self.dots_radius

    def set_graph_line_width(self, graph_line_width):
        """
        graph_line_width:
            Un entero o decimal, el ancho de las líneas que unen
            los puntos en la gráfica
        """

        if type(graph_line_width) in [int, float]:
            self.graph_line_width = graph_line_width
        else:
            raise TypeError('"graph_line_width" must be a number')

    def get_graph_line_width(self):
        return self.graph_line_width

    def render(self):
        if self.data and self.context:
            self.calculate_things()
            self.render_background()
            if self.draw_frame:
                self.render_frame()
            if self.draw_axes:
                self.render_axes()
            self.render_graph()

    def calculate_things(self):
        self.space_for_references = 0
        self.max_h_label = 0
        self.max_v_label = 0
        self.widest_v_label = ''
        self.start_x = 0
        self.start_y = self.height
        self.marks_sizes = 10
        self.max_v_label_size = 0

        for name, values in self.data.items():
            if self.max_h_label < len(values):
                self.max_h_label = len(values)

            if self.max_v_label < max(values):
                self.max_v_label = max(values)

            if self.space_for_references < self.context.text_extents(name)[2]:
                self.space_for_references = self.context.text_extents(name)[2]

        for x in range(1, 7):
            if len(str(self.max_v_label * 1.0 / x)) < self.widest_v_label:
                self.widest_v_label = str(self.max_v_label * 1.0 / x)

                if '.' in self.widest_v_label and \
                        len(self.widest_v_label.split('.')[1]) > 2:

                    self.widest_v_label = self.widest_v_label.split('.')[0] + \
                        '.' + self.widest_v_label.split('.')[1][:2]

                if self.max_v_label_size < self.context.text_extents(
                        self.widest_v_label)[2]:

                    self.max_v_label_size = self.context.text_extents(
                        self.widest_v_label)[2]

        self.space_for_references += 50 if \
            self.space_for_references else 0  # The color box
        self.start_x += self.border
        self.start_x += self.axes_width if self.draw_axes else 0
        self.start_x += self.marks_sizes if self.draw_marks_labels else 0
        self.start_x += len(self.widest_v_label) * self.axes_labels_sizes \
            if self.draw_marks_labels else 0
        self.start_y -= self.border
        self.start_y -= self.axes_width if self.draw_axes else 0
        self.start_y -= self.marks_sizes if self.draw_marks else 0
        self.start_y -= (self.axes_labels_sizes + 10) \
            if self.draw_marks_labels else 0

        if self.start_x == self.border + self.axes_width:
            self.start_x += self.border + self.axes_width

        if self.start_y == self.height - self.border - self.axes_width:
            self.start_y -= self.axes_width + self.axes_width

        self.h_start = self.start_x - self.axes_width / 2
        self.h_end = self.width - self.start_x
        self.v_start = self.start_y - self.axes_width / 2
        self.v_end = self.height - self.start_y  # top
        self.h_distance = (self.h_end - self.h_start) / float(self.axes_marks)
        self.v_distance = (self.v_start - self.v_end) / float(self.axes_marks)
        self.h_step = (self.h_end - self.h_start) / float(self.max_h_label - 1)
        self.v_step = (self.v_start - self.v_end) / float(self.max_v_label)

        for name in self.data.keys():
            if name not in self.colors.keys():
                self.colors[name] = utils.get_random_color()

    def render_background(self):
        self.context.set_source_rgb(*self.background)
        self.context.rectangle(0, 0, self.width, self.height)
        self.context.fill()

    def render_frame(self):
        self.context.set_line_width(self.frame_width)
        self.context.set_source_rgb(*self.frame_color)

        self.context.move_to(self.border, self.border)
        self.context.line_to(self.width - self.border, self.border)
        self.context.line_to(
            self.width - self.border, self.height - self.border)
        self.context.line_to(self.border, self.height - self.border)
        self.context.line_to(self.border, self.border - self.frame_width / 2)
        self.context.stroke()

    def render_axes(self):
        self.context.set_line_width(self.axes_width)
        self.context.set_source_rgb(*self.axes_color)
        self.context.set_font_size(self.axes_labels_sizes)

        self.context.move_to(self.h_start, self.v_start)
        self.context.line_to(self.h_end, self.v_start)
        self.context.move_to(self.h_start, self.v_start)
        self.context.line_to(self.h_start, self.v_end)
        self.context.stroke()

        if self.draw_rows:
            # Horizontal row
            diference = self.axes_width / 4.0
            self.context.move_to(self.h_end, self.start_y - diference)
            self.context.line_to(
                self.h_end - 20, self.start_y - diference * 2 - 12)
            self.context.move_to(self.h_end, self.start_y - diference * 3)
            self.context.line_to(
                self.h_end - 20, self.start_y - diference * 2 + 12)

            # Vertical row
            self.context.move_to(
                self.h_start + diference, self.height - self.v_start)
            self.context.line_to(
                self.h_start + 12, self.height - self.v_start + 20)
            self.context.move_to(
                self.h_start - diference, self.height - self.v_start)
            self.context.line_to(
                self.h_start - 12, self.height - self.v_start + 20)

            self.context.stroke()

        if self.draw_marks and self.data:
            for x in range(1, self.axes_marks + 1):
                hx = self.h_distance * x + self.h_start
                vx = self.start_x + 5 - self.axes_width / 2
                hy = self.height - self.v_end - 5 - self.axes_width / 2
                vy = self.v_start - self.v_distance * x

                if x != self.axes_marks or not self.draw_rows:
                    self.context.move_to(hx, hy)
                    self.context.line_to(hx, hy + 10)
                    self.context.move_to(vx - 10, vy)
                    self.context.line_to(vx, vy)

        if self.draw_marks_labels:
            for x in range(1, self.axes_marks + 1):
                hx = self.h_distance * x + self.h_start
                vx = self.start_x + 5 - self.axes_width / 2
                hy = self.height - self.v_end - 5 - self.axes_width / 2
                vy = self.v_start - self.v_distance * x

                h_value = (self.max_h_label / float(self.axes_marks)) * x
                v_value = (self.max_v_label / float(
                    self.axes_marks)) * (self.axes_marks - x + 1)
                h_label = str(h_value)
                v_label = str(v_value)

                if '.' in h_label and len(h_label.split('.')[1]) > 2:
                    h_label = h_label.split('.')[0] + '.' + \
                        h_label.split('.')[1][:2]

                if '.' in v_label and len(v_label.split('.')[1]) > 2:
                    v_label = v_label.split('.')[0] + '.' + \
                        v_label.split('.')[1][:2]

                self.context.move_to(
                    hx - (self.axes_labels_sizes + 10) / 2.0,
                    hy + self.axes_width / 2 + (self.axes_labels_sizes + 10))
                self.context.show_text(h_label)

                self.context.move_to(
                    vx - len(v_label) * self.axes_labels_sizes,
                    self.v_start - self.v_distance * (
                        self.axes_marks - x + 1) + self.axes_labels_sizes / 2)
                self.context.show_text(v_label)

            self.context.stroke()

    def render_graph(self):
        for name, values in self.data.items():
            x0, y0 = 0, 0
            draw_lines = False

            for index in range(0, len(values)):
                x = self.start_x + self.h_step * index - \
                    self.dots_radius / 2.0
                y = self.start_y - self.v_step * values[index] - \
                    self.dots_radius / 2.0

                self.context.set_source_rgb(*self.colors[name])

                if draw_lines:
                    self.context.set_line_width(self.graph_line_width)
                    self.context.move_to(x0, y0)
                    self.context.line_to(x, y)
                    self.context.stroke()
                else:
                    draw_lines = True

                self.context.arc(x, y, self.dots_radius, 0, 2 * math.pi)
                self.context.fill()
                x0, y0 = x, y


class PieGraph():

    width = 0
    height = 0
    line_width = 0

    def __init__(self, context=None, data={},
                 colors={}, width=500, height=500, radius=-100):

        self.context = context
        self.set_data(data)
        self.set_colors(colors)
        self.set_width(width)
        self.set_height(height)
        self.set_radius(radius if radius != 0 else min([width, height]) / 2.0)
        self.start_angle = 0
        self.inner_radius = 0
        self.line_color = (0.0, 0.0, 0.0)
        self.line_width = 2
        self.font_size = 15

    def set_context(self, context):
        """
        context:
            Un cairo context sobre el cual dibujar.
        """

        self.context = context

    def get_context(self):
        return self.context

    def set_data(self, data):
        """
        data:
            Un diccionario, con los nombres de los datos a graficar
            como keys, y el valor correspondiente de cada dato como value.
        """

        if type(data) == dict:
            self.data = data
        else:
            return TypeError('"data" must be a dict')

    def get_data(self):
        return self.data

    def set_colors(self, colors):
        """
        colors:
            Un diccionario, con las mimsas keys utilizadas en self.data, con
            una tupla con 3 decimales(del 0 al 1) para indicar el color del
            elemento key.
            También puede ser un color de HTML(hexadecimal) o un color
            RGB(una tupla o lista con valores del 0 al 255)
        """

        if type(colors) == dict:
            for name in colors:
                colors[name] = utils.get_cairo_color(colors[name])

            self.colors = colors
        else:
            return TypeError('"colors" must be a dict')

    def set_width(self, width):
        """
        width:
            Un entero o un decimal, el ancho total de la gráfica.
            Para usar el ancho total de un GtkDrawingArea:

            allocation = area.get_allocation()
            width = allocation.width
        """

        if type(width) in [float, int]:
            self.width = width - self.line_width
            self.radius = min([self.width, self.height]) / 2.0
        else:
            raise TypeError('"width" must be a int or float')

    def get_width(self):
        return self.width

    def set_height(self, height):
        """
        height:
            Un entero o un decimal, el alto total de la gráfica
            Para usar el alto total de un GtkDrawingArea:

            allocation = area.get_allocation()
            height = allocation.height
        """

        if type(height) in [float, int]:
            self.height = height - self.line_width
            self.radius = min([self.width, self.height]) / 2.0
        else:
            raise TypeError('"height" must be a int or float')

    def set_background(self, background):
        """
        background:
            Una lista o una tupla con tres valores,
            del 0.0 al 1.0 o del 0 al 255, ejemplos:
            [0.4, 0.3, 0.6]    (0.2, 0.6, 1.0)    [35, 200, 110]

            También puede ser una cadena de texto, en formato hexadecimal
            Por ejemplo:
                "#32FF32"
        """

        if type(background) in [list, tuple, str]:
            self.background = utils.get_cairo_color(background)
        else:
            raise TypeError(
                '"background" must be a list, a tuple, or a string')

    def get_background(self):
        return self.background

    def set_radius(self, radius):
        """
        radius:
            El radio del círculo de la gráfica.
        """

        if type(radius) in [int, float]:
            self.radius = radius
        else:
            raise TypeError('"radius" must be a int or float')

    def render(self):
        self.render_background()
        if self.data and self.context:
            self.calculate_things()
            self.render_graph()
            self.render_labels()

    def render_background(self):
        self.context.set_source_rgb(*self.background)
        self.context.rectangle(0, 0, self.width, self.height)
        self.context.fill()

    def calculate_things(self):
        self.center_x = self.width / 2.0 + self.line_width / 2.0
        self.center_y = self.height / 2.0 + self.line_width / 2.0
        self.total = sum([value for name, value in self.data.items()])

        for name in self.data.keys():
            if name not in self.colors.keys():
                self.colors[name] = utils.get_random_color()

    def render_graph(self):
        start = self.start_angle
        end = 0

        for name, value in self.data.items():
            end = start + 2.0 * math.pi * value / self.total

            self.context.set_source_rgba(*self.colors[name])
            self.draw_piece(start, end)
            self.context.fill()

            self.context.set_source_rgba(*self.line_color)
            self.draw_piece(start, end)
            self.context.stroke()

            start = end

    def draw_piece(self, start, end):
        cx, cy = self.center_x, self.center_y
        self.context.set_line_width(self.line_width)
        self.context.move_to(cx + self.inner_radius * math.cos(start),
                             cy + self.inner_radius * math.sin(start))
        self.context.line_to(cx + self.radius * math.cos(start),
                             cy + self.radius * math.sin(start))
        self.context.arc(cx, cy, self.radius, start, end)
        self.context.line_to(cx + self.inner_radius * math.cos(end),
                             cy + self.inner_radius * math.sin(end))
        self.context.arc_negative(cx, cy, self.inner_radius, end, start)
        self.context.close_path()

    def render_labels(self):
        start = self.start_angle
        end = 0
        x0, y0 = self.center_x, self.center_y
        self.context.set_font_size(self.font_size)

        for name, value in self.data.items():
            end = start + 2.0 * math.pi * value / self.total
            self.context.set_source_rgba(
                *utils.get_opposite_color(self.colors[name]))
            w = self.context.text_extents(name)[2]
            h = self.context.text_extents(name)[4]
            x = x0 + (self.radius - w) * math.cos(
                (start + end) / 2.0) - w + self.line_width * 2
            y = y0 + (self.radius - h) * math.sin(
                (start + end) / 2.0) - self.line_width

            self.context.move_to(x, y)
            self.context.show_text(name)
            start = end


"""
import random
from gi.repository import Gtk


class Window(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)

        self.context = None
        self.area = Gtk.DrawingArea()
        self.colors = {'Juan': utils.get_random_color(),
                       'Jorge': utils.get_random_color(),
                       'Pepe': utils.get_random_color()}

        graph = 0

        if graph == 0:
            self.draw_dots_graph()
        elif graph == 1:
            self.draw_pie_graph()

        self.set_title('PyGraphExample')
        self.set_size_request(400, 400)

        self.area.connect('draw', self.__drag_cb)
        self.connect('destroy', Gtk.main_quit)

        self.add(self.area)
        self.show_all()

    def draw_dots_graph(self):
        data = {'Juan': random.sample(xrange(20), 10),
                'Jorge': random.sample(xrange(20), 10),
                'Pepe': random.sample(xrange(20), 10)}

        self.graph = DotGraph(data=data, colors=self.colors)

    def draw_pie_graph(self):
        data = {'Juan': random.randint(1, 100),
                'Jorge': random.randint(1, 100),
                'Pepe': random.randint(1, 100)}

        self.graph = PieGraph(data=data, colors=self.colors)

    def __drag_cb(self, widget, context):
        allocation = self.get_allocation()
        width = allocation.width
        height = allocation.height
        self.context = context

        self.graph.set_context(self.context)
        self.graph.set_width(width)
        self.graph.set_height(height)
        self.graph.render()


Window()
Gtk.main()
"""
