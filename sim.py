# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2017-08-21 13:24:31
# @Last Modified by:   lorenzo
# @Last Modified time: 2017-09-09 10:11:23

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
import pygame

import unit_converter as uc
import players
import png
import data_handlers as dh
import visualizer as viz


class Simulator:
    """
===================
The Simulator class
===================

.. class:: Simulator(sscreen, plt, m0, t0, dt, rtf, tol, player_dim=(50,10))


    """
    def __init__(self, sscreen, plt, m0, t0, dt, rtf, tol, player_dim=(50,10)):
        self._sscreen = sscreen
        self._plt = plt
        self.dt = dt
        self.realtime_factor = rtf
        self.tolerance = tol

        losangle0 = np.arctan2(t0['pos'][1] - m0['pos'][1], t0['pos'][0] - m0['pos'][0])
        self.m = { 'player': players.Missile(m0['pos'], 
                                             losangle0 + np.radians(m0['he']),
                                             m0['vel'], 0, m0['guidance']) }
        self.t = { 'player': players.Target(t0['pos'] , losangle0, t0['vel'], t0['acc']) }

        self.m['surface'] = viz.PlayerSurf(player_dim, losangle0 + np.radians(m0['he']))
        self.t['surface'] = viz.PlayerSurf(player_dim, losangle0)

        self.quit_event    = threading.Event()
        self.resume_event  = threading.Event()
        self.resume_event.set()


    def loop(self):
        """
.. method:: loop()

        
        """
        while True:
            self._sscreen.clear()
            sensed = self.m['player'].sensors_layer.get_data(self.t['player'])
            nacc   = self.m['player'].update_acc(sensed, self.dt)
            for p in [self.m, self.t]:
                p['player'].update_nav(self.dt)
                p['surface'].update_ori(p['player'].ori)
            if nacc:
                self.m['player'].acc = nacc
            
            dh.history['los'].append((
                 viz.Point(self.pos2pix(self.m['player'].pos)), 
                 viz.Point(self.pos2pix(self.t['player'].pos))
            ))

            for los in dh.history['los'][:-1]:
                self._sscreen.draw_line('green', los[0], los[1])
            self._sscreen.draw_line('red', dh.history['los'][-1][0], dh.history['los'][-1][1])
            for p in [self.m, self.t]:
                self._sscreen.blit_center(p['surface'], 
                                          self.pos2pix(p['player'].pos),
                                          p['player'].ori)
            if self.check_collision():
                break

            if self.m['player'].acc:
                dh.history['acc'].append(abs(round(self.m['player'].acc, 2)))

            for los_d in ['los_rate', 'los_angle', 'closing_velocity']:
                if hasattr(self.m['player'], los_d):
                    dh.history[los_d].append(abs(round(getattr(self.m['player'], los_d), 5)))

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

        
        """
        while not self.quit_event.is_set():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_event.set()
                    self.resume_event.set()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.resume_event.clear()
                    if event.key == pygame.K_r:
                        self.resume_event.set()
                    if event.key == pygame.K_q:
                        self.quit_event.set()
                        self.resume_event.set()
            time.sleep(0.01)

    def check_collision(self):
        """
.. method:: check_collision()

        
        """
        return (self.m['player'].pos[0] > self.t['player'].pos[0] - self.tolerance and 
                self.m['player'].pos[0] < self.t['player'].pos[0] + self.tolerance and 
                self.m['player'].pos[1] > self.t['player'].pos[1] - self.tolerance and 
                self.m['player'].pos[1] < self.t['player'].pos[1] + self.tolerance)

    def pos2pix(self, pos):
        """
.. method:: pos2pix(pos)

        
        """
        return [int(uc.meters_to_pix(ppos)) for ppos in pos]


parser = argparse.ArgumentParser(description='Simulator and plotter.')
parser.add_argument('-mp', '--missilepos', dest='m0pos', nargs=2, type=int,
                    metavar =('x','y'), help='missile start position', default=(10,5))
parser.add_argument('-mv', '--missilevel', dest='m0vel', type=int,
                    metavar = 'vel', help='missile start velocity', default=40)
parser.add_argument('-mhe', '--missilehe', dest='m0he', type=int,
                    metavar = 'HE (degrees)', help='missile heading error', default=30)
parser.add_argument('-mg', '--missileguidance', dest='missile_guidance', type=str,
                    metavar = 'guidance', help='chosen guidance (ppn/apng)', default='ppn')


parser.add_argument('-tp', '--targetpos', dest='t0pos', nargs=2, type=int,
                    metavar = ('x','y'), help='target start position', default=(50,30))
parser.add_argument('-tv', '--targetvel', dest='t0vel', type=int,
                    metavar = 'vel', help='target start velocity', default=5)
parser.add_argument('-ta', '--targetacc', dest='t0acc', type=int,
                    metavar = 'acceleration', help='target acceleration', default=0)

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
