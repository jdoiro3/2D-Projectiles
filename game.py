from libs import *
import projectile_classes as p

def main():
    
    win = g.GraphWin('Projectile', 1000, 600)
    win.setCoords(0, 0, 10000, 10000)

    lan = p.Launcher(30,500)
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