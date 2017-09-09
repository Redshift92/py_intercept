# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2017-09-09 09:59:21
# @Last Modified by:   lorenzo
# @Last Modified time: 2017-09-09 10:18:27

"""
.. module:: sensors_layers

**************
Sensors Layers
**************

Definitions of sensors layers updating retrieving players data with different sensors dynamics and
characteristics.

    """

class PerfectSensors:
    """
========================
The PerfectSensors class
========================

.. class:: PerfectSensors()

    Create a PerfectSensors instance: a sensors layer capable of retrieving player's position and
    acceleration with no noise or delay.

    """
    def __init__(self):
        pass

    def get_data(self, player):
        """
.. method:: get_data(player)

        Return player position and acceleration with no noise or delay,
        
        """
        return { 'position': player.pos, 'acceleration': player.acc }