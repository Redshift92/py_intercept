# -*- coding: utf-8 -*-
# @Author: lorenzo
# @Date:   2017-08-21 21:54:00
# @Last Modified by:   Lorenzo
# @Last Modified time: 2017-09-17 16:10:03

# Copyright 2017 Lorenzo Rizzello
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import pygame
import numpy as np

def rotate(point, angle):
    new_x = np.cos(angle) * point[0] - np.sin(angle) * point[1]
    new_y = np.sin(angle) * point[0] + np.cos(angle) * point[1]
    return new_x, new_y

def point_diff(point1, point2):
    return (int(point1[0] - point2[0]), int(point1[1] - point2[1]))

def point_sum(point1, point2):
    return (int(point1[0] + point2[0]), int(point1[1] + point2[1]))

def point_int(point):
    return (int(point[0]), int(point[1]))

GREY = (  90,  90,  90)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
screen.fill(WHITE)


def pos_to_screen(pos):
    return (pos[0], screen_size[1] - pos[1])

def cntr2tl(cntr_pos):
    return (cntr_pos[0] - 100, cntr_pos[1] + 20)

def blit_center(surf, cntr_pos, ori):
    top_left = cntr2tl( cntr_pos )
    if ori:
        dori = np.degrees(ori)
        if dori > 360:
            raise Exception
        if dori > 180:
            dori -= 180
            ori -= np.pi
        if dori < 90:
            top_left = point_sum(top_left, (abs(-100 - rotate((-100, +20), ori)[0]), -20 + rotate((100, 20), ori)[1]) )
        else:
            top_left = point_sum(top_left, (abs(-100 - rotate((+100, +20), ori)[0]), -20 + rotate((100, -20), ori)[1]) )


        # rotated around top right
        # top_left = point_sum(top_left, (200 - rotate((200,0), -ori)[0], 0) )

        # rotated around center and traslated
        print('> trasl x: ', -100 - rotate((-100,-20), ori)[0])
        print('> trasl y: ', -20 + rotate((100, 20), ori)[1] )
    screen.blit(surf, pos_to_screen( top_left ) )

ang = 0

# if ang > 90:
#     ang = 180 - ang

surf = pygame.Surface((200,40))
surf.set_colorkey((255, 0, 0))
surf = pygame.transform.rotate(surf, ang)

surf2 = pygame.Surface((200,40))
surf2.set_colorkey((255, 0, 0))
surf2.fill(BLUE)

screen.blit(surf2, (0,0))
screen.blit(surf, (0,0))
# 
# screen.blit(surf, (0,0))
# screen.blit(surf, point_sum((0,0), point_diff( surf.get_rect().center, rotate((100,20), np.radians(ang)) )) )
screen.blit(surf, point_sum((0,0), point_int((200 - rotate((200,0), np.radians(-ang))[0], 0)) ))

blit_center(surf2, (200,100), np.radians(0  ))
blit_center(surf,  (200,100), np.radians(ang))

pygame.draw.circle(screen, RED, pos_to_screen((200,100)), 1)

pygame.draw.circle(screen, GREEN, point_sum((0,0), point_diff( surf.get_rect().center, rotate((100,20), np.radians(ang)) )), 1)

pygame.draw.circle(screen, RED, surf.get_rect().center, 1)
pygame.draw.circle(screen, RED, surf2.get_rect().center, 1)
pygame.draw.circle(screen, RED, (1,1), 1)

pygame.draw.circle(screen, GREEN, point_int(rotate((200,40), np.radians(ang))), 1)
pygame.draw.circle(screen, GREEN, point_int(rotate((100,20), np.radians(ang))), 1)

pygame.display.flip()

from time import sleep
while ang < 360:
    screen.fill(WHITE)
    ang += 1
    surf = pygame.Surface((200,40))
    surf.set_colorkey((255, 0, 0))
    surf = pygame.transform.rotate(surf, ang)
    blit_center(surf,  (200,100), np.radians(ang))
    pygame.display.flip()
    print(ang)
    sleep(0.02)

while True:
    sleep(1)
