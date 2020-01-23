from libs import *
import projectile_classes as p


def main():
    
    win = GraphWin('Projectile', 1000, 600)
    win.setCoords(0, 0, 10000, 10000)

    lan = p.Launcher(30,500)
    lan.draw(win)

    power_bar = p.Power_Bar(win, screen_cords=10000, color="red")

    num = 0

    mouse = None
    while mouse == None:

        time.sleep(.01)

        if keyboard.is_pressed('w'):
            lan.move_up(win)
        if keyboard.is_pressed('s'):
            lan.move_down(win)
            
        if keyboard.is_pressed('f'):
            # limit the amount of shots that are fired
            # if the 'F' key is held down.
            if num == 0:
                lan.launch(win)
            num += 1
            if num > 10:
                num = 0
            
        if keyboard.is_pressed('d'):
            lan.increase_power()
            power_bar.move_power_level(lan.power, win)
        if keyboard.is_pressed('a'):
            lan.decrease_power()
            power_bar.move_power_level(lan.power, win)
        
        lan.update_projectiles()
        mouse = win.checkMouse()

main()
