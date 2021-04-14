import pygame as pg 
from time import sleep
from random import random
from math import sin, cos, pi, sqrt
from win32api import GetSystemMetrics


rm_pt  = lambda  : random() * 650  #returns a random number between 0 and 650
to_rad = lambda a: a * (pi / 180)  #deg -> rad
dist   = lambda p1, p2: sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) #Distance between two points

class Boundary:
    def __init__(self, x1, y1, x2, y2, color = (255,0 ,0)):
        self.a = [x1, y1]
        self.b = [x2, y2]
        self.color = color
    def show(self, surface):
        pg.draw.line(surface, self.color, self.a, self.b, width = 2)

class Ray:
    def __init__(self, angle: float):
        self.focus = None
        self.dir = [cos(angle), sin(angle)]
    def set_posittion(self, mouse):
        self.focus = mouse
    def cast(self, wall):
        x1, y1 = wall.a[0], wall.a[1]
        x2, y2 = wall.b[0], wall.b[1]

        x3 = self.focus[0]
        y3 = self.focus[1]
        x4 = self.focus[0] + self.dir[0]
        y4 = self.focus[1] + self.dir[1]

        #line intersection: https://en.wikipedia.org/wiki/Line-line_intersection
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return
        t =  ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        if t > 0 and t < 1 and u > 0:
            intersection = []
            intersection.append(x1 + t * (x2 - x1))
            intersection.append(y1 + t * (y2 - y1))

            return intersection
        else:
            return

def main():
    y_height   = GetSystemMetrics(1) - 100 #screen height
    delay      = 0.01
    bg_color   = (0,0,0)
    running    = True
    line_color = (255, 255, 255)
    size       = (y_height, y_height)
    #---------------
    num_walls  = 7
    num_rays   = 72 
    #---------------
    walls = []
    for i in range(num_walls):
        walls.append(Boundary(rm_pt(), rm_pt(), rm_pt(), rm_pt()))
    
    walls.append(Boundary(     0 ,      0 , size[0],      0,  bg_color))
    walls.append(Boundary(size[0],      0 , size[0], size[0], bg_color))
    walls.append(Boundary(size[0], size[0],      0 , size[0], bg_color))
    walls.append(Boundary(     0 , size[0],      0 ,      0,  bg_color)) 

    rays = []
    for i in range(0, 360, int(360 / num_rays)):
        rays.append(Ray(to_rad(i)))

    pg.init()
    screen = pg.display.set_mode(size)

    # main loop
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill(bg_color)
        for wall in walls:
            wall.show(screen)

        for ray in rays:
            closest = None
            aux     = 1e3
            for wall in walls:
                ray.set_posittion(pg.mouse.get_pos())
                coll_pt = ray.cast(wall)
                if coll_pt:
                    d = dist(ray.focus, coll_pt)
                    if d < aux:
                        aux = d
                        closest = coll_pt 
                    aux = min(d, aux)
            if closest:
                pg.draw.line  (screen, line_color, ray.focus, closest, width=1)
                pg.draw.circle(screen, line_color, ray.focus, 5, width=1)

        sleep(delay)
        pg.display.update()
    pg.quit()

if __name__ == "__main__":
    main()
