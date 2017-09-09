# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2017-09-09 10:09:40
# @Last Modified by:   lorenzo
# @Last Modified time: 2017-09-09 10:14:04


"""
.. module:: visualizer

**********
Visualizer
**********

Allow to easily visualize simulation output.

    """

import pygame
import numpy as np

class Point:
    """
===============
The Point class
===============

.. class:: Point(coords)

        Create a Point instance.

    """

    def __init__(self, coords):
        self.coords = coords

    def rotate(self, angle):
        """
.. method:: rotate(angle)

        Rotate vector from reference origin to point by :samp:`angle` angle.

        """
        new_x = np.cos(angle) * self.coords[0] - np.sin(angle) * self.coords[1]
        new_y = np.sin(angle) * self.coords[0] + np.cos(angle) * self.coords[1]
        return Point((new_x, new_y))

    def __add__(self, point):
        """
.. method:: add(point)

        Return the sum between self and :samp:`point` coordinates.

        """
        return Point(((self.coords[0] + point.coords[0]), (self.coords[1] + point.coords[1])))

    def int_coords(self):
        """
.. method:: int_coords()

        Return a tuple of integer self coordinates.

        """
        return (int(self.coords[0]), int(self.coords[1]))


class PlayerSurf:
    """
====================
The PlayerSurf class
====================

.. class:: PlayerSurf(dim, ori)

        Create a PlayerSurf instance with :samp:`dim` width-height dimensions and :samp:`ori`
        orientation.
        It allows to easily manage a rotating pygame surface.

    """
    def __init__(self, dim, ori):
        self.dim = dim
        self.ori = None
        self.update_ori(ori)

    def update_ori(self, nori):
        """
.. method:: update_ori(nori)

        Change surface orientation.

        """
        if nori != self.ori:
            nsurf = pygame.Surface(self.dim)
            nsurf.set_colorkey((255, 0, 0))
            self.surf = pygame.transform.rotate(nsurf, np.degrees(nori))
            self.ori = nori

    def cntr2tl(self, cntr_pos):
        """
.. method:: cntr2tl(cntr_pos)

        Return surface top left corner coordinates as a Point object given center position as a
        tuple.

        """
        return Point((cntr_pos[0] - self.dim[0]/2, cntr_pos[1] + self.dim[1]/2))


class SimScreen:
    """
===================
The SimScreen class
===================

.. class:: SimScreen(screen_size, font_size)

        Create a SimScreen instance with :samp:`screen_size` screen size and :samp:`font_size`
        font size.
        It allows to easily manage pygame screen, used as simulation animation output screen, 
        through custom helper methods.
        SimScreen coordinate frame origin is placed at bottom left corner.

    """
    def __init__(self, screen_size, font_size):
        pygame.init()

        pygame.font.init()
        self._font_size = font_size
        self._font = pygame.font.SysFont('opensans', font_size, bold=True)

        self._init_colors()

        self._screen_size = screen_size
        self._screen = pygame.display.set_mode(screen_size)
        self.clear()

    def _init_colors(self):
        self.colors = {
            'grey' : (  90, 90,  90),
            'black': (  0,   0,   0),
            'white': (255, 255, 255),
            'blue' : (  0,   0, 255),
            'green': (  0, 255,   0),
            'red'  : (255,   0,   0)
        }

    def clear(self):
        """
.. method:: clear()

        Clear simulation screen.

        """
        self._screen.fill(self.colors['white'])

    def update(self):
        """
.. method:: update()

        Update simulation screen: must be called to make screen changes effective.

        """
        pygame.display.flip()

    def _pgs2ss_coords(self, pos):
        """
.. method:: _pgs2ss_coords(pos)

        (_pygamescreen2simscreen_coords)

        Convert :samp:`pos` Point object coordinates from pygame screen frame (top-left origin) to
        SimScreen frame (bottom-left origin) returning a coordinates tuple.

        """
        return Point((pos.coords[0], self._screen_size[1] - pos.coords[1])).int_coords()

    def draw_line(self, color, point0, point1):
        """
.. method:: draw_line(color, point0, point1)

        Draw a colored line from :samp:`point0` to :samp:`point1`, where :samp:`color` is a string
        from the following list::

            ['grey', 'black', 'white', 'blue', 'green', 'red']

        """
        pygame.draw.line(self._screen, self.colors[color], 
                self._pgs2ss_coords(point0), self._pgs2ss_coords(point1))

    def display_text(self, text, level=0):
        """
.. method:: display_text(text, level=0)

        Display string :samp:`text` on SimScreen.
        :samp:`level` is an integer indicating where to display :samp:`text` vertically, starting 
        from the top.

        """
        textsurface = self._font.render(text, False, (0, 0, 0))
        self._screen.blit(textsurface, (20, int(self._font_size * 1.7) * (level + 1) ))

    def blit_center(self, psurf, cntr_pos, ori):
        """
.. method:: blit_center(psurf, cntr_pos, ori)

        Blit a :samp:`psurf` PlayerSurf object to SimScreen given surface desired center coordinates
        (as a tuple) and orientation (in radians).

        """
        top_left = psurf.cntr2tl(cntr_pos)
        if ori:
            dori = np.degrees(ori)
            if dori > 360:
                raise Exception
            pxh = psurf.dim[0]/2
            pyh = psurf.dim[1]/2
            if dori > 180:
                dori -= 180
                ori -= np.pi
            # rotated around center and traslated
            if dori < 90:
                tlc, trc = Point((-pxh, pyh)).rotate(ori), Point((pxh, pyh)).rotate(ori)
                top_left += Point((abs(-pxh - tlc.coords[0]), -pyh + trc.coords[1]))
            else:
                trc, brc = Point((pxh, pyh)).rotate(ori), Point((pxh, -pyh)).rotate(ori)
                top_left += Point((abs(-pxh - trc.coords[0]), -pyh + brc.coords[1]))
        self._screen.blit(psurf.surf, self._pgs2ss_coords( top_left ) )
