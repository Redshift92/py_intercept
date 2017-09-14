# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2017-08-21 13:24:23
# @Last Modified by:   Lorenzo
# @Last Modified time: 2017-09-14 20:24:30

"""
.. module:: players

*******
Players
*******

Players are generic simulation objects.

    """

import types
import numpy as np

#TODO: acceleration only perpendicular to velocity in current implementation, make generic

class Player:
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
    This method directly updates objects' attributes.
    Velocity is updated integrating Players' acceleration and considering this acceleration always 
    perpendicular to velocity vector.

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

.. class:: Missile(pos, ori, vel, acc, guidance_data, sensors_layer)

    Create a Missile instance.
    A Missile is a player capable of updating its acceleration based on a certain guidance law and 
    detecting a Target through a sensors layer modeling sensors' dynamics and noise.

    For its initialization the following parameters are needed:

        * :samp:`pos`, :samp:`ori`, :samp:`vel`, :samp:`acc` with the same meaning of Player base 
           class;

        * :samp:`guidance_data` is a dictionary with 'guidance' and 'guidance_gain' keys:
          'guidance' value must be a function representing a desired guidance law used to update
          Missile acceleration before the navigation integration step.
          A valid :samp:`guidance` function is a Python function taking three arguments::

            def guidance_example(obj, sensed, dt):
                # do something to evaluate acceleration value
                obj.acc = new_acceleration

          where :samp:`obj`, :samp:`sensed` and :samp:`dt` are respectively a reference to Missile 
          instance, a dictionary containing data returned by the sensor layer and integration step.
          The aim of :samp:`guidance` function should be updating :samp:`acc` object attribute.
          'guidance_gain' value should be a number which will become available inside guidance
          function as obj.guidance_gain attribute;

        * :samp:`sensors_layer` is a class modeling sensors' dynamics and noise.
          A valid :samp:`sensors_layer` is a Python class having a :samp:`get_data` method taking a 
          player object as argument and returning a dictionary representing sensed data::

            class MySensors:

                def __init__(self):
                    pass

                def get_data(self, player):
                    ...
                    return { 'position': player.pos + some_noise, 'acceleration': player.acc }

    """
    def __init__(self, pos, ori, vel, acc, guidance_data, sensors_layer):
        Player.__init__(self, pos, ori, vel, acc)
        self.sensors_layer = sensors_layer()
        self.guidance_gain = guidance_data['guidance_gain']
        self.update_acc = types.MethodType(guidance_data['guidance'], self)

class Target(Player):
    """
=================
The Target class
=================

.. class:: Target(pos, ori, vel, acc)

    Create a Missile instance.
    In current implementation a Target is a simple Player with no additional methods or attributes.

    """
    def __init__(self, pos, ori, vel, acc):
        Player.__init__(self, pos, ori, vel, acc)
