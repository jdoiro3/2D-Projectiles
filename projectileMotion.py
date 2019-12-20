from graphics import *
import time






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
