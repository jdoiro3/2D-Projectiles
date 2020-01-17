from libs import *
from graphics import _root

_gravity = 9.81

class Projectile(Circle):
    '''A projectile that can be fired by a launcher'''

    # class attribute that represents the difference in time between each call to move()
    _dt = .5

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

    def __init__(self, theta, length):
        self.theta = theta
        self.text = str(theta)+" degrees"
        self.length = length
        self.position_x = length*cos(radians(theta))
        self.position_y = length*sin(radians(theta))
        self.power = 0.0
        self.projectiles_airborn = []
        Line.__init__(self, Point(0,0), Point(self.position_x, self.position_y))


    def _update_theta(self, theta):
        self.position_x = self.length*cos(radians(theta))
        self.position_y = self.length*sin(radians(theta))
        Line.__init__(self, Point(0,0), Point(self.position_x, self.position_y))

    def _update_text(self, new_text):
        self.text = new_text

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
        if self.power > 1000:
            pass
        else:
            self.power += 20.0
            # draw to the power bar

    def decrease_power(self):
        if self.power < 0.0:
            self.power = 0.0
        else:
            self.power -= 20.0
            # draw to power bar

    def decrease_power(self):
        self.power += -1
        # draw to the power bar

    def launch(self, win):
        p = Projectile(self.power, self.theta)
        p.draw(win)
        self.projectiles_airborn.append(p)

    def drop_grounded_projectiles(self):
        self.projectiles_airborn = [p for p in self.projectiles_airborn if p.grounded != True]

    def update_projectiles(self):
        self.drop_grounded_projectiles()
        for p in self.projectiles_airborn:
            p.move()
        




def main():

    win = GraphWin('Projectile', 1000, 600)
    win.setCoords(0, 0, 10000, 10000)

    lan = Launcher(30,500)
    lan.draw(win)

    mouse = None
    while mouse == None:

        time.sleep(.05)

        if keyboard.is_pressed('w'):
            lan.move_up(win)
        if keyboard.is_pressed('s'):
            lan.move_down(win)
        if keyboard.is_pressed('f'):
            lan.launch(win)
        if keyboard.is_pressed('d'):
            lan.increase_power()
        if keyboard.is_pressed('a'):
            lan.decrease_power()
        
        lan.update_projectiles()
        mouse = win.checkMouse()

main()