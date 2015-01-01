#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from gi.repository import Gtk


class DotGraph():

    def __init__(self, context, data={}, colors={}, width=500, height=500):
        # context:
        #   Un cairo context sobre el cual dibujar.
        #
        # data:
        #   Los nombres de los datos a graficar como keys,
        #   y una lista de esas como los valores a graficar.
        #
        # colors:
        #   Las mimsas keys utilizadas en data, con una tupla
        #   con 3 flotantes(del 0 al 1) para indicar el color del elemento key.
        #
        # width:
        #   El ancho de la gráfica
        #
        # height:
        #   El Alto de la gráfica

        self.context = context
        self.data = data
        self.colors = colors
        self.width = width
        self.height = height
        self.background = (1, 1, 1)
        self.border = 10
        self.draw_frame = True
        self.frame_width = 2
        self.frame_color = (0.5, 0.5, 0.5)
        self.draw_axis = True
        self.draw_rows = True
        self.draw_marks = True
        self.draw_marks_labels = True
        self.axis_marks = 6
        self.axis_width = 4
        self.axis_color = (0, 0, 0)
        self.axis_labels_sizes = 15
        self.dots_radius = 5
        self.graph_line_width = 2

    def render(self):
        if self.data:
            self.calculate_things()
            self.render_background()
            if self.draw_frame:
                self.render_frame()
            if self.draw_axis:
                self.render_axis()
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

                if '.' in self.widest_v_label and len(self.widest_v_label.split('.')[1]) > 2:
                    self.widest_v_label = self.widest_v_label.split('.')[0] + '.' + self.widest_v_label.split('.')[1][:2]

                if self.max_v_label_size < self.context.text_extents(self.widest_v_label)[2]:
                    self.max_v_label_size = self.context.text_extents(self.widest_v_label)[2]

        self.space_for_references += 50 if self.space_for_references else 0 # The color box
        self.start_x += self.border# if self.draw_frame else 0
        self.start_x += self.axis_width if self.draw_axis else 0
        self.start_x += self.marks_sizes if self.draw_marks_labels else 0
        self.start_x += len(self.widest_v_label) * self.axis_labels_sizes if self.draw_marks_labels else 0
        self.start_y -= self.border
        self.start_y -= self.axis_width if self.draw_axis else 0
        self.start_y -= self.marks_sizes if self.draw_marks else 0
        self.start_y -= (self.axis_labels_sizes + 10) if self.draw_marks_labels else 0

        if self.start_x == self.border + self.axis_width:
            self.start_x += self.border + self.axis_width

        if self.start_y == self.height - self.border - self.axis_width:
            self.start_y -= self.axis_width + self.axis_width

        self.h_start = self.start_x - self.axis_width / 2
        self.h_end = self.width - self.start_x
        self.v_start = self.start_y - self.axis_width / 2
        self.v_end = self.height - self.start_y  # top
        self.h_distance = (self.h_end - self.h_start) / float(self.axis_marks)
        self.v_distance = (self.v_start - self.v_end) / float(self.axis_marks)
        self.h_step = (self.h_end - self.h_start) / float(self.max_h_label - 1)
        self.v_step = (self.v_start - self.v_end) / float(self.max_v_label)

    def render_background(self):
        cr = self.context

        cr.set_source_rgb(*self.background)
        cr.rectangle(0, 0, self.width, self.height)
        cr.fill()

    def render_frame(self):
        cr = self.context
        cr.set_line_width(self.frame_width)
        cr.set_source_rgb(*self.frame_color)

        cr.move_to(self.border, self.border)
        cr.line_to(self.width - self.border, self.border)
        cr.line_to(self.width - self.border, self.height - self.border)
        cr.line_to(self.border, self.height - self.border)
        cr.line_to(self.border, self.border - self.frame_width / 2)
        cr.stroke()

    def render_axis(self):
        cr = self.context
        cr.set_line_width(self.axis_width)
        cr.set_source_rgb(*self.axis_color)
        cr.set_font_size(self.axis_labels_sizes)

        cr.move_to(self.h_start, self.v_start)
        cr.line_to(self.h_end, self.v_start)
        cr.move_to(self.h_start, self.v_start)
        cr.line_to(self.h_start, self.v_end)
        cr.stroke()

        if self.draw_rows:
            # Horizontal row
            diference = self.axis_width / 4.0
            cr.move_to(self.h_end, self.start_y - diference)
            cr.line_to(self.h_end - 20, self.start_y - diference * 2 - 12)
            cr.move_to(self.h_end, self.start_y - diference * 3)
            cr.line_to(self.h_end - 20, self.start_y - diference * 2 + 12)

            # Vertical row
            cr.move_to(self.h_start + diference, self.height - self.v_start)
            cr.line_to(self.h_start + 12, self.height - self.v_start + 20)
            cr.move_to(self.h_start - diference, self.height - self.v_start)
            cr.line_to(self.h_start - 12, self.height - self.v_start + 20)

            cr.stroke()

        if self.draw_marks and self.data:
            for x in range(1, self.axis_marks + 1):
                hx = self.h_distance * x + self.h_start
                vx = self.start_x + 5 - self.axis_width / 2
                hy = self.height - self.v_end - 5 - self.axis_width / 2
                vy = self.v_start - self.v_distance * x

                if x != self.axis_marks or not self.draw_rows:
                    cr.move_to(hx, hy)
                    cr.line_to(hx, hy + 10)
                    cr.move_to(vx - 10, vy)
                    cr.line_to(vx, vy)

        if self.draw_marks_labels:
            for x in range(1, self.axis_marks + 1):
                hx = self.h_distance * x + self.h_start
                vx = self.start_x + 5 - self.axis_width / 2
                hy = self.height - self.v_end - 5 - self.axis_width / 2
                vy = self.v_start - self.v_distance * x

                h_value = (self.max_h_label / float(self.axis_marks)) * x
                v_value = (self.max_v_label / float(self.axis_marks)) * (self.axis_marks - x + 1)
                h_label = str(h_value)
                v_label = str(v_value)

                if '.' in h_label and len(h_label.split('.')[1]) > 2:
                    h_label = h_label.split('.')[0] + '.' + h_label.split('.')[1][:2]

                if '.' in v_label and len(v_label.split('.')[1]) > 2:
                    v_label = v_label.split('.')[0] + '.' + v_label.split('.')[1][:2]

                v_size = self.context.text_extents(v_label)[4]
                h_size = self.axis_labels_sizes + 10

                cr.move_to(
                    hx - h_size / 2.0,
                    hy + self.axis_width / 2 + h_size)
                cr.show_text(h_label)

                cr.move_to(
                    vx - len(v_label) * self.axis_labels_sizes, 
                    self.v_start - self.v_distance * (self.axis_marks - x + 1) + self.axis_labels_sizes / 2)
                cr.show_text(v_label)

            cr.stroke()

    def render_graph(self):
        for name, values in self.data.items():
            last_x, last_y = 0, 0
            draw_lines = False

            for index in range(0, len(values)):
                x = self.start_x + self.h_step * index - self.dots_radius / 2.0
                y = self.start_y - self.v_step * values[index] - self.dots_radius / 2.0

                if name in self.colors:
                    self.context.set_source_rgb(*self.colors[name])

                else:
                    self.context.set_source_rgb(0, 0, 0)

                if draw_lines:
                    self.context.set_line_width(self.graph_line_width)
                    self.context.move_to(last_x, last_y)
                    self.context.line_to(x, y)
                    self.context.stroke()
                else:
                    draw_lines = True

                self.context.arc(x, y, self.dots_radius, 0, 2 * math.pi)
                self.context.fill()
                last_x, last_y = x, y

"""
class Window(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)

        self._context = None
        self.area = Gtk.DrawingArea()

        self.area.connect('draw', self.__drag_cb)
        self.connect('destroy', Gtk.main_quit)

        self.add(self.area)
        self.show_all()

    def __drag_cb(self, widget, context):
        allocation = self.get_allocation()
        width = allocation.width
        height = allocation.height

        self._context = context
        data = {
            'Juan':  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'Jorge': [1, 5, 2, 6, 7, 3, 6, 4, 3 ,6],
            'Pepe':  [5, 0, 2, 5, 7, 9, 4, 5, 5, 3]}
        colors = {
            'Juan': (0.23, 0.53, 0.24),
            'Jorge': (0.5, 0.5, 0.0),
            'Pepe': (0.1, 0.4, 0.7)}
        graph = DotGraph(self._context, data=data, colors=colors, width=width, height=height)
        graph.render()


Window()
Gtk.main()
"""