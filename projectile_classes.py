from libs import *
from graphics import _root

_gravity = 9.81

class Projectile(Circle):
    '''A projectile that can be fired by a launcher'''

    # class attribute that represents the difference in time between each call to move()
    _dt = .1

    def __init__(self, v, theta, size=30, x=0.0, y=0.0):
        # set the time to dt for each instance. This is private...
        self._time = self._dt

        # public data members (attributes)
        self.v = v
        self.v_x = self.v * cos(radians(theta)) # constant
        self.v_y = self.v * sin(radians(theta)) # changes with time
        self.theta = theta
        self.x = x
        self.y = y
        self.dx = 0.0
        self.dy = 0.0
        self.max_height = (pow(self.v,2) * pow(sin(radians(theta)),2))/(2*_gravity)
        self.range = (pow(self.v,2) * (sin(radians(2*theta)))) / _gravity

        # after launching a projectile, this value is set to True once the projectile's x position
        # is greater than the range.
        self.grounded = False

        # call the super class's __init__ to create all the attributes of the Circle class
        Circle.__init__(self, Point(self.x, self.y), size)

    def __str__(self):
        return "Projectile instance located at ({self.x},{self.pos_y})".format(self=self)

    # internal method that is called by _move()
    # updates the x and y position of the projectile
    def _update_position(self):
        self.x = self.v * self._time * cos(radians(self.theta))
        self.y = (self.v * self._time * sin(radians(self.theta))) - (.5 * _gravity * pow(self._time,2))
        
        # each time the method is called, this projectile's instance moves further in it's flight time
        self._time += self._dt

    def _move(self):
        # don't move the projectile anymore once it reaches it's range
        # grounded tells other methods this projectile is done moving
        if self.x > self.range:
            self.grounded = True
        else:
            x_before = self.x
            y_before = self.y

            self._update_position()

            self.dx = self.x - x_before
            self.dy = self.y - y_before


    def move(self):

        self._move()

        if self.grounded:
            pass
        else:
            # same as in graphics.py except for self.dx and self.dy
            canvas = self.canvas
            if canvas and not canvas.isClosed():
                trans = canvas.trans
                if trans:
                    x = self.dx/ trans.xscale 
                    y = -self.dy / trans.yscale
                else:
                    x = self.dx
                    y = self.dy
                self.canvas.move(self.id, x, y)
                if canvas.autoflush:
                    _root.update()

class Launcher(Line):

    max_power = 1000

    def __init__(self, theta, length):
        self.theta = theta
        self.length = length
        self.x2 = length*cos(radians(theta))
        self.y2 = length*sin(radians(theta))
        self.power = 0.0
        self.projectiles_airborn = []
        Line.__init__(self, Point(0,0), Point(self.x2, self.y2))


    def _update_theta(self, theta):
        self.x2 = self.length*cos(radians(theta))
        self.y2 = self.length*sin(radians(theta))
        Line.__init__(self, Point(0,0), Point(self.x2, self.y2))

    def move_up(self, win):
        self.undraw()
        self.theta += 1
        self._update_theta(self.theta)
        self.draw(win)

    def move_down(self, win):
        self.undraw()
        self.theta -= 1
        self._update_theta(self.theta)
        self.draw(win)

    def increase_power(self):
        if self.power+10.0 > self.max_power:
            pass
        else:
            self.power += 10.0
            # draw to the power bar

    def decrease_power(self):
        if self.power-10.0 < 0.0:
            self.power = 0.0
        else:
            self.power -= 10.0
            # draw to power bar

    def launch(self, win):
        p = Projectile(self.power, self.theta)
        p.draw(win)
        self.projectiles_airborn.append(p)

    def drop_grounded_projectiles(self):
        self.projectiles_airborn = [proj for proj in self.projectiles_airborn if proj.grounded != True]

    def update_projectiles(self):
        self.drop_grounded_projectiles()
        for p in self.projectiles_airborn:
            p.move()


class Power_Bar(Rectangle):

    max_power = 1000

    def __init__(self, win, screen_cords, color, start_pos=1, end_pos=2):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.win = win
        self.x_start = (self.start_pos/4)*screen_cords
        self.x_end = (end_pos/4)*screen_cords

        Rectangle.__init__(self, Point(self.x_start, 200), Point(self.x_end, 400))
        self.draw(self.win)

        self.power_level = Rectangle(self.getP1(), Point(self.p1.getX(), self.p1.getY()))
        if self.color:
            self.power_level.setFill(self.color)
        self.power_level.draw(self.win)

    def move_power_level(self, power, win):
        middle = ((self.x_end - self.x_start)/2)+self.x_start
        const = 2*(middle - self.x_start)
        x = ((power/self.max_power)*const)+self.x_start
        y = self.p2.getY()
        self.power_level.undraw()
        self.power_level.p2 = Point(x,y)
        self.power_level.draw(self.win)