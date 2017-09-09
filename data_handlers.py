# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2017-08-29 21:10:17
# @Last Modified by:   lorenzo
# @Last Modified time: 2017-08-30 11:15:36

"""
.. module:: data_handlers

*************
Data Handlers
*************

Handle useful simulation data: plot and keep history.

    """

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

class Plotter:
    """
=================
The Plotter class
=================

.. class:: Plotter(title, size)

        Creates a Plotter instance with window title :samp:`title` and window size :samp:`size`.

    """
    def __init__(self, title, size):
        self._win = pg.GraphicsWindow(title=title)
        self._win.resize(*size)
        self._plots = {}
        self._curves = {}
        self._app_inst = QtGui.QApplication.instance()

    def add_plots(self, plots_list):
        """
.. method:: add_plots(plots_list)

        Add plots to Plotter window.

        * :samp:`plots_list` is a list containing:

            * a list describing a desired plot, this list is composed of:

                * plot id string to access plot and add data to it subsequently
                * plot title string
                * curves list: a list composed of n elements corresponing to desired curves colors
        """
        for plot in plots_list:
            if plot == 'next_row':
                self._win.nextRow()
                continue
            self._plots[plot[0]] = self._win.addPlot(title=plot[1])
            self._curves[plot[0]] = []
            for curve in plot[2]:
                self._curves[plot[0]].append(self._plots[plot[0]].plot(pen=curve))

    def plots(self):
        """
.. method:: plots(plots_list)

        Return plot ids.
        """
        return list(self._plots.keys())

    def set_data(self, plot, data, curve_index=0):
        """
.. method:: set_data(plot, data, curve_index = 0)

        Plot :samp:`data` list to curve :samp:`curve_index` inside plot :samp:`plot`.
        """
        self._curves[plot][curve_index].setData(data)

    def run(self):
        """
.. method:: run()

        Start Qt Plotter Application.
        """
        self._app_inst.exec()

    def quit(self):
        """
.. method:: quit()

        Quit Qt Plotter Application.
        """
        self._app_inst.exit()


history = None
def make_history(ids):
    """
.. function:: make_history(ids)

    Prepare a history dictionary with ids as keys and empty lists as values to keep data logs.
    """
    global history
    history = {mid: [] for mid in ids}
