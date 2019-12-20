from math import cos, sin, tan
from math import radians

_gravity = 9.81


class projectile:

    def __init__(self, v, theta, pos_x=0.0, pos_y=0.0):
        self.theta = theta
        self.v = v
        self.v_x = v * cos(radians(theta))
        self.v_y = v * sin(radians(theta))
        self.time_of_flight = (2 * v * sin(radians(theta))) / _gravity
        self.range = ((v**2)*(sin(radians(theta))**2)) / 2*_gravity
        self.max_height = ((v**2)*sin(radians(theta))) / _gravity
        self.pos_x = pos_x
        self.pos_y = pos_y

    def __str__(self):
        return "Projectile instance located at ({self.v_x},{self.v_y})".format(self=self)

    def update_position(self, t):
        self.pos_x = self.v_x*t
        self.pos_y = (tan(radians(self.theta))*self.pos_x) - \
                     (_gravity / (2*(self.v**2)*(cos(radians(self.theta))**2))*(self.pos_x**2))




p = projectile(100,20)

print(p)

p.update_position(2)

print(p)
