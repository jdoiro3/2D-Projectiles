from graphics import *
from graphics import _root
from math import cos, sin, tan
from math import radians
import numpy as np
from graphics import *
import time

_gravity = 9.81


class Projectile(Circle):

    def __init__(self, v, theta, pos_x=0.0, pos_y=0.0):
        self.theta = theta
        self.v = v
        self.v_x = v * cos(radians(theta))
        self.v_y = v * sin(radians(theta))
        self.time_of_flight = (2 * v * sin(radians(theta))) / _gravity
        self.range = ((v**2)*(sin(2*radians(theta)))) / _gravity
        self.max_height = ((v**2)*sin(radians(theta))**2) / 2*_gravity
        self.pos_x = pos_x
        self.pos_y = pos_y
        Circle.__init__(self, Point(self.pos_x, self.pos_y), 2)

    def __str__(self):
        return "Projectile instance located at ({self.pos_x},{self.pos_y})".format(self=self)

# NEED TO FIX THIS PART
    def move(self, t):
        canvas = self.canvas
        if canvas and not canvas.isClosed():
            trans = canvas.trans
            self.pos_x = self.v_x * t

            if self.pos_x > self.range:
                self.pos_x = self.range / trans.xscale
                self.pos_y = 0.0
            else:
                self.pos_y = (tan(radians(self.theta))*self.pos_x) - \
                     (_gravity / (2*(self.v**2)*(cos(radians(self.theta))**2))*(self.pos_x**2)) / trans.yscale



    def move(self, t):
        self.update_position(t)
        canvas = self.canvas
        if canvas and not canvas.isClosed():
            trans = canvas.trans
            if trans:
                x = self.pos_x
                y = -self.pos_y
            else:
                x = self.pos_x
                y = self.pos_y
            self.canvas.move(self.id, x, y)
            if canvas.autoflush:
                _root.update()


def main(velocity, angle):
    cir1 = Projectile(100, 20)
    cir1.setFill("black")
    win = GraphWin('Back and Forth', 1000, 1000)
    win.setCoords(0, 0, cir1.range, cir1.max_height)

    cir1.draw(win)

    delta_t = 0.0
    while cir1.getCenter().getX() <= cir1.range:
        delta_t += .1
        cir1.move(delta_t)
        time.sleep(1)

    win.getMouse()
    win.close()




main(100,50)
