# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2017-08-23 17:29:39
# @Last Modified by:   lorenzo
# @Last Modified time: 2017-09-06 13:47:59

import numpy as np

def ppn(self, sensed, dt):
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
