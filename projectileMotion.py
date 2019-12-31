from graphics import *
from graphics import _root
from math import cos, sin, tan, sqrt, pow, radians
import numpy as np
import time

_gravity = 9.81


class Projectile(Circle):

    def __init__(self, v, theta, x=0.0, y=0.0):
        self.initial_v = v
        self.v = v
        self.v_x = self.v * cos(radians(theta)) # constant
        self.v_y = self.v * sin(radians(theta)) # changes with time
        self.theta = theta
        self.x = x
        self.y = y
        self.max_height = (pow(self.initial_v,2) * pow(sin(radians(theta)),2))/(2*_gravity)
        self.range = (pow(self.initial_v,2) * (sin(radians(2*theta)))) / _gravity
        Circle.__init__(self, Point(self.x, self.y), 25)

    def __str__(self):
        return "Projectile instance located at ({self.x},{self.pos_y})".format(self=self)

    def _update_position(self, time):
        self.x = self.initial_v * time * cos(radians(self.theta))
        self.y = (self.initial_v * time * sin(radians(self.theta))) - (.5 * _gravity * pow(time,2))

    def move(self, time, dt):

        self._update_position(time-dt)
        x_before = self.x
        y_before = self.y
        self._update_position(time)

        dx = self.x - x_before
        dy = self.y - y_before

        canvas = self.canvas
        if canvas and not canvas.isClosed():
            trans = canvas.trans
            if trans:
                x = dx/ trans.xscale 
                y = -dy / trans.yscale
            else:
                x = dx
                y = dy
            self.canvas.move(self.id, x, y)
            if canvas.autoflush:
                _root.update()

    def launch(self, win):

        self.draw(win)
        self.setFill("black")

        time.sleep(1)

        t = 0.0
        dt = .1
        while (self.x <= self.range and self.x <= 10000):
            self.move(t, dt)
            t += dt
            time.sleep(.01)

                


def main():

    win = GraphWin('Projectile', 900, 400)
    win.setCoords(0, 0, 10000, 10000)

    p = Projectile(320, 40)
    p2 = Projectile(200,80)
    p3 = Projectile(500,85)

    p.launch(win)
    p2.launch(win)
    p3.launch(win)


main()
