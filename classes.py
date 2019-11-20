
# import datetime as dt
import math
import random
import matplotlib.pyplot as plt

class Projectile:

    gravity = 9.8

    def __init__(self, position_x=0.0, position_y=10.0, velocity=0.0, angle=0.0):

        self.__position_x = position_x
        self.__position_y = position_y
        self.__velocity = velocity
        self.__angle = angle
        self.__history = []
        # private members that can never be accessed
        self.__v_x = self.__velocity*math.cos(math.radians(self.__angle))
        self.__v_y = self.__velocity*math.sin(math.radians(self.__angle))

    @property
    def position_x(self):
        return self.__position_x
    @property
    def position_y(self):
        return self.__position_y
    @property
    def velocity(self):
        return self.__velocity
    @property
    def angle(self):
        return self.__angle
    @property
    def history(self):
        return self.__history

    def updatePosition(self, delta_t):

        delta_x = self.__v_x *delta_t
        delta_y = self.__v_y *delta_t - (.5 *Projectile.gravity *(delta_t**2))

        new_x = self.__position_x +delta_x
        new_y = self.__position_y +delta_y

        if new_y < 0.0:
            new_y = 0.0

        self.__position_x = new_x
        self.__position_y = new_y

    def recordPosition(self):
        self.__history.append((self.__position_x, self.__position_y))

    def showPosition(self):
        plt.scatter(self.__position_x, self.__position_y, color='r')
        plt.show()



class Gun:
    # firingRate is the number of bullets that can be fired per second
    def __init__(self, muzzleVelocity=0.0, direction=0.0, firingRate=1.0, bullets=0):

        self.__muzzleVelocity = muzzleVelocity
        self.__direction = direction
        self.__firingRate = firingRate
        self.__bullets = bullets

    def fire(self, triggerHoldLength):
        # if you don't have bullets, you must reload.
        if self.__bullets == 0:
            print("Reload.")
        # if you have bullets, proceed with firing
        else:
            # triggerHoldLength (sec) and firingRate (bullets/sec)
            bullet_num = int(triggerHoldLength*self.__firingRate)
            # if the amount of bullets that can be fired exceeds the amount in the mag, decrease to amount in mag
            if bullet_num > self.__bullets:
                bullet_num = self.__bullets
                # let user know they need to reload
                print("Reload.")
            # create list of bullet instances to fire
            bullets = [Projectile(velocity=self.__muzzleVelocity, angle=self.__direction+random.uniform(-.1, 2)) for i in range(bullet_num)]
            # fire each bullet, calculate the trajectory, and keep a history of the previous positions
            for i in range(bullet_num):
                # change in time after each recorded position
                delta_t = .01
                # we have bullets but let's take one away since we fired
                self.__bullets -= 1
                # the bullet moves until it makes contact with the ground
                while bullets[i].position_y != 0.0:
                    # update the bullets position
                    bullets[i].updatePosition(delta_t)
                    # update the position history
                    bullets[i].recordPosition()
                    # move forward in time
                    delta_t += .01

                # these two variables are used for plotting
                x_val = [x[0] for x in bullets[i].history]
                y_val = [x[1] for x in bullets[i].history]

                plt.scatter(x=x_val, y=y_val, color='r', alpha=.5)

            plt.show()

    def reload(self, magCapacity):
        self.__bullets += magCapacity

    def aim(self, direction_chg):
        self.__direction += direction_chg

    @property
    def direction(self):
        return self.__direction




