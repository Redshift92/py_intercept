# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2017-08-23 17:29:39
# @Last Modified by:   Lorenzo
# @Last Modified time: 2017-09-13 16:45:41

"""
.. module:: png

***
PNG
***

Implementation of Proportitonal Navigation Guidance laws to be chosen as acceleration update methods
for a Missile object.

    """

import numpy as np

def ppn(self, sensed, dt):
    """
.. function:: ppn(self, sensed, dt)

    Implementation of an Pure Proportional Navigation Guidance law.

    """
    tpos = sensed['position']
    self.range = np.sqrt((tpos[1] - self.pos[1])**2 + (tpos[0] - self.pos[0])**2)
    if abs(tpos[0] - self.pos[0]) > 0.01:
        self.los_angle = np.arctan2(tpos[1] - self.pos[1], tpos[0] - self.pos[0])
    try:
        self.closing_velocity = - (self.range - self.prev_range) / dt
        self.los_rate  = (self.los_angle - self.prev_los_angle) / dt
        if abs(np.cos(self.ori - self.los_angle)) > 0.01:
            self.acc = ((5/(np.cos(self.ori - self.los_angle))) *
                         self.closing_velocity * self.los_rate)
    except AttributeError:
        pass
    finally:
        self.prev_range = self.range
        self.prev_los_angle = self.los_angle

def apng(self, sensed, dt):
    """
.. function:: apng(self, sensed, dt)

    Implementation of an Augmented Proportional Navigation Guidance law.

    """
    tpos, tacc = sensed['position'], sensed['acceleration']
    self.range = np.sqrt((tpos[1] - self.pos[1])**2 + (tpos[0] - self.pos[0])**2)
    if abs(tpos[0] - self.pos[0]) > 0.01:
        self.los_angle = np.arctan2(tpos[1] - self.pos[1], tpos[0] - self.pos[0])
    try:
        self.closing_velocity = - (self.range - self.prev_range) / dt
        self.los_rate  = (self.los_angle - self.prev_los_angle) / dt
        if abs(np.cos(self.ori - self.los_angle)) > 0.01:
            self.acc = ((5/(np.cos(self.ori - self.los_angle))) *
                         self.closing_velocity * self.los_rate) + 2.5*tacc
    except AttributeError:
        pass
    finally:
        self.prev_range = self.range
        self.prev_los_angle = self.los_angle
