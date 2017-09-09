# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2017-08-21 13:24:23
# @Last Modified by:   lorenzo
# @Last Modified time: 2017-09-09 10:06:02

import types
import numpy as np

import sensors_layers

#TODO: acceleration only perpendicular to velocity in current 
#      implementation, make generic

class Player():
    """
================
The Player class
================

.. class:: Player(pos, ori, vel, acc)

    Create a Player instance given its start:

        * :samp:`pos` position
        * :samp:`ori` orientation
        * :samp:`vel` velocity
        * :samp:`acc` acceleration

    """
    def __init__(self, pos, ori, vel, acc):
        self.pos, self.ori, self.vel, self.acc = list(pos), ori, [vel*np.cos(ori), vel*np.sin(ori)], acc

    def update_nav(self, dt):
        """
.. method:: update_nav(dt)

    A Player is an entity capable of updating its navigation coordinates (position, orientation,
    velocity) with a :samp:`dt` integration step.
    This method directly updates self attributes.

        """
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        if self.acc:
            self.ori += (self.acc/np.sqrt(self.vel[0]**2 + self.vel[1]**2)) * dt
            while self.ori < 0:
                self.ori = np.pi * 2 - self.ori
            while self.ori > np.pi * 2:
                self.ori -= np.pi * 2

            vel_inc = self.acc * dt # has to be distributed along x,y axis since
                                    # this value represents the value perpendicular
                                    # to velocity vector (with angle ori)
            self.vel[0] += vel_inc * np.cos(self.ori + np.pi/2)
            self.vel[1] += vel_inc * np.sin(self.ori + np.pi/2)


class Missile(Player):
    """
=================
The Missile class
=================

.. class:: Missile(pos, ori, vel, acc, update_fn)


    """
    def __init__(self, pos, ori, vel, acc, update_fn):
        Player.__init__(self, pos, ori, vel, acc)
        self.sensors_layer = sensors_layers.PerfectSensors()
        self.update_acc =  types.MethodType(update_fn, self)

class Target(Player):
    """
=================
The Target class
=================

.. class:: Target(pos, ori, vel, acc)


    """
    def __init__(self, pos, ori, vel, acc):
        Player.__init__(self, pos, ori, vel, acc)
