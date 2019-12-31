from graphics import *
from graphics import _root
from math import cos, sin, tan, sqrt, pow, radians
import keyboard
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
        Circle.__init__(self, Point(self.x, self.y), 55)

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
        dt = .5
        while self.x <= self.range and self.x <= 10000:
            self.move(t, dt)
            t += dt
            time.sleep(.05)

class Cannon(Rectangle):

    def __init__(self):
        pass


def main():

    win = GraphWin('Projectile', 1000, 800)
    win.setCoords(0, 0, 10000, 10000)
    theta = 45
    x2 = 1000*cos(radians(theta))
    y2 = 1000*sin(radians(theta))
    ln = Line(Point(0,0),Point(x2,y2))
    ln.draw(win)

    mouse = None
    while mouse == None:
        if keyboard.is_pressed('w'):
            ln.undraw()
            theta += 1
            x2 = 1000*cos(radians(theta))
            y2 = 1000*sin(radians(theta))
            print(x2)
            ln = Line(Point(0,0), Point(x2,y2))
            ln.draw(win)
            time.sleep(.1)
        if keyboard.is_pressed('s'):
            ln.undraw()
            theta -= 1
            x2 = 1000*cos(radians(theta))
            y2 = 1000*sin(radians(theta))
            ln = Line(Point(0, 0), Point(x2, y2))
            ln.draw(win)
            time.sleep(.1)
        if keyboard.is_pressed('f'):
            p = Projectile(200, theta, x=ln.getP2().getX(), y=ln.getP2().getY())
            p.launch(win)

        mouse = win.checkMouse()

main()
