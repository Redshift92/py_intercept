# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2017-08-21 13:24:31
# @Last Modified by:   Lorenzo
# @Last Modified time: 2017-09-14 20:27:09

"""

*********
Simulator
*********

Simulate a missile-target intercept scenario.

    """

import time
import threading
import argparse

import numpy as np

import unit_converter as uc
import players
import png
import data_handlers as dh
import visualizer as viz
import sensors_layers


class Simulator:
    """
===================
The Simulator class
===================

.. class:: Simulator(sscreen, plt, m0, t0, dt, rtf, tol, player_dim=(50,10))

    Create a Simulator instance.
    To have the Simulator correctly running the following parameters are needed:

        * :samp:`sscreen` SimScreen instance to output Simulation animation;
        * :samp:`plt`  Plotter instance to output Simulation data;
        * :samp:`m0` Missile configuration info passed as a dictionary composed of the following keys:
          ['pos', 'he', 'vel', 'guidance'] paired respectively with an (x,y) start position tuple,
          heading error angle in degrees, start velocity and a string for desired guidance method;
        * :samp:`t0` Target configuration info passed as a dictionary composed of the following keys:
          ['pos', 'vel', 'acc'] paired respectively with an (x,y) start position tuple,
          start velocity and acceleration;
        * :samp:`dt` scalar value used as both integration and simulation step;
        * :samp:`rtf` realtime factor with a value less than 1 to slow down the simulation without 
          reducing the simulation step (i.e. a rft of 0.5 and a dt of 0.01 will make the simulation
          animation run like a 2ms step one while the integration step is still 1ms);
        * :samp:`tol` allowed tolerance on Missile/Target position difference to consider the
          interception ended;
        * :samp:`player_dim` a tuple representing Missile and Target representations dimensions in 
          pixels. 

    """
    def __init__(self, sscreen, plt, m0, t0, dt, rtf, tol, player_dim=(50,10)):
        self._sscreen = sscreen
        self._plt = plt
        self.dt = dt
        self.realtime_factor = rtf
        self.tolerance = tol

        guidance_data = {
            'guidance': m0['guidance'],
            'guidance_gain': m0['guidance_gain'],
        }

        losangle0 = np.arctan2(t0['pos'][1] - m0['pos'][1], t0['pos'][0] - m0['pos'][0])
        self.m = { 'player': players.Missile(m0['pos'], 
                                             losangle0 + np.radians(m0['he']),
                                             m0['vel'], 0, guidance_data,
                                             sensors_layers.PerfectSensors) }
        self.t = { 'player': players.Target(t0['pos'] , losangle0, t0['vel'], t0['acc']) }

        self.m['surface'] = viz.PlayerSurf(player_dim, losangle0 + np.radians(m0['he']))
        self.t['surface'] = viz.PlayerSurf(player_dim, losangle0)

        self.quit_event    = threading.Event()
        self.resume_event  = threading.Event()
        self.resume_event.set()


    def loop(self):
        """
.. method:: loop()

        Start simulation loop:

            * let the Missile acquire sensors data and consequently update its acceleration;
            * evaluate new Missile and Target position;
            * save meaningful data, update plots and Players positions on screen;
            * if collision is detected exit the loop and quit the simulation;
            * sleep and repeat.
        """
        while True:
            self._sscreen.clear()

            # pass target true coordinates to missile sensor layer and retrieve sensed values
            # "corrupted" by sensors dynamics and noise
            sensed = self.m['player'].sensors_layer.get_data(self.t['player'])

            # update missile acceleration through sensed data
            nacc   = self.m['player'].update_acc(sensed, self.dt)

            # update Missile and Target navigation data and animation surface orientation
            for p in [self.m, self.t]:
                p['player'].update_nav(self.dt)
                p['surface'].update_ori(p['player'].ori)

            if nacc:
                self.m['player'].acc = nacc

            # log and draw line of sight

            dh.history['los'].append((
                 viz.Point(self.pos2pix(self.m['player'].pos)), 
                 viz.Point(self.pos2pix(self.t['player'].pos))
            ))

            for los in dh.history['los'][:-1]:
                self._sscreen.draw_line('green', los[0], los[1])
            self._sscreen.draw_line('red', dh.history['los'][-1][0], dh.history['los'][-1][1])


            # place Missile and Target surfaces on screen
            for p in [self.m, self.t]:
                self._sscreen.blit_center(p['surface'], 
                                          self.pos2pix(p['player'].pos),
                                          p['player'].ori)
            if self.check_collision():
                break

            # log and plot
            if self.m['player'].acc:
                dh.history['acc'].append(round(self.m['player'].acc, 2))

            for los_d in ['los_rate', 'los_angle', 'closing_velocity']:
                if hasattr(self.m['player'], los_d):
                    dh.history[los_d].append(round(getattr(self.m['player'], los_d), 5))

            for plt_id in plt.plots():
                plt.set_data(plt_id, dh.history[plt_id])

            self._sscreen.display_text('> missile acceleration: ' + 
                                       str(round(self.m['player'].acc, 2)))
            self._sscreen.display_text('(s/r) to suspend/resume simulation', 1)
            self._sscreen.display_text('  (q) to quit simulation', 2)
            self._sscreen.update()

            time.sleep(self.dt/self.realtime_factor)
            self.resume_event.wait()

            if self.quit_event.is_set():
                break

        self.quit_event.wait()
        self._plt.quit()

    def key_listener(self):
        """
.. method:: key_listener()

        Listen to keyboard and ui events.
        """
        while not self.quit_event.is_set():
            for event in self._sscreen.event.get():
                if event.type == viz.event_type('QUIT'):
                    self.quit_event.set()
                    self.resume_event.set()
                if event.type == viz.event_type('KEYDOWN'):
                    if event.key == viz.event_key('s'):
                        self.resume_event.clear()
                    if event.key == viz.event_key('r'):
                        self.resume_event.set()
                    if event.key == viz.event_key('q'):
                        self.quit_event.set()
                        self.resume_event.set()
            time.sleep(0.01)

    def check_collision(self):
        """
.. method:: check_collision()

        Check missile and target collision under allowed tolerance condition.
        """
        return (self.m['player'].pos[0] > self.t['player'].pos[0] - self.tolerance and 
                self.m['player'].pos[0] < self.t['player'].pos[0] + self.tolerance and 
                self.m['player'].pos[1] > self.t['player'].pos[1] - self.tolerance and 
                self.m['player'].pos[1] < self.t['player'].pos[1] + self.tolerance)

    def pos2pix(self, pos):
        """
.. method:: pos2pix(pos)

        Conver a position tuple expressed in meters to a pixels tuple.
        """
        return tuple([int(uc.meters_to_pix(ppos)) for ppos in pos])


parser = argparse.ArgumentParser(description='Simulator and plotter.')
parser.add_argument('-mp', '--missilepos', dest='m0pos', nargs=2, type=int,
                    metavar=('x','y'), help='missile start position', default=(10,5))
parser.add_argument('-mv', '--missilevel', dest='m0vel', type=int,
                    metavar='vel', help='missile start velocity', default=40)
parser.add_argument('-mhe', '--missilehe', dest='m0he', type=int,
                    metavar='HE (degrees)', help='missile heading error', default=-20)
parser.add_argument('-mg', '--missileguidance', dest='missile_guidance', type=str,
                    metavar='guidance', help='chosen guidance (ppn/apng)', default='ppn')
parser.add_argument('-mgg', '--mguidancegain', dest='missile_guidance_gain', type=int,
                    metavar='guidance', help='chosen guidance gain', default=3)


parser.add_argument('-tp', '--targetpos', dest='t0pos', nargs=2, type=int,
                    metavar=('x','y'), help='target start position', default=(50,30))
parser.add_argument('-tv', '--targetvel', dest='t0vel', type=int,
                    metavar='vel', help='target start velocity', default=5)
parser.add_argument('-ta', '--targetacc', dest='t0acc', type=int,
                    metavar='acceleration', help='target acceleration', default=0)

args = parser.parse_args()

data_ids = ['acc', 'los_rate', 'los_angle', 'los', 'closing_velocity']
plt = dh.Plotter('Data Plotting', (800,800))
plt.add_plots([[data_ids[0], 'Missile Acceleration Plot', ['y']],
               [data_ids[1], 'Los Rate Plot', ['y']],
               'next_row',
               [data_ids[2], 'Los Angle Plot', ['y']],
               [data_ids[4], 'Closing Velocity Plot', ['y']]])

dh.make_history(data_ids)

m0 = {
    'guidance': getattr(png, args.missile_guidance),
    'guidance_gain': args.missile_guidance_gain,
    'pos': args.m0pos,
    'vel': args.m0vel,
    'he':  args.m0he
}

t0 = {
    'pos': args.t0pos,
    'vel': args.t0vel,
    'acc': args.t0acc
}

sscreen = viz.SimScreen((800, 600), 15)
simulator = Simulator(sscreen, plt, m0, t0, dt = 0.005, rtf = 0.5, tol = 0.5)

threading.Thread(target=simulator.key_listener).start()
threading.Thread(target=simulator.loop).start()
# plotter object must run inside main thread
plt.run()
