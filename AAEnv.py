import pygame as py
from telnetlib import XASCII
import math

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
i = 1
W = 900
H = 400
FPS = 20
speed = 5
x = W//2
y = H//2
a = 0
x0 = 200+(math.cos(a*math.pi/180))
y0 = 340+(math.sin(a*math.pi/180))
alpha = 5
flLeft = 0
flRight = 0

class airplanes():
    def __init__(self, x,y, width, height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 5
    def draw(self,win):
        py.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))

class projectile():
    def __init__(self, x, y, radius, color, facing, grad):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.grad = grad
        self.vel = 0.1*self.facing
        self.time = 1
    def draw(self, win):
        py.draw.circle(win, self.color,(self.x, self.y), self.radius)

py.init()
bullets = []
air_planes = []

while(len(air_planes)!= 4):
        air_planes.append(airplanes(100*i, 40, 30,30, WHITE))
        i+=1
while True:
    for airplane in air_planes:
        if airplane.x < W and airplane.x > 0 and airplane.y < H and airplane.y > 0:
            airplane.x += airplane.speed
        if airplane.x >= W:
            airplane.x = 0 + airplane.speed
    for bullet in bullets:
        if bullet.x < W and bullet.x > 0 and bullet.y < H and bullet.y > 0:
            bullet.x = x0 +  bullet.vel*(math.cos(bullet.grad*math.pi/180))*bullet.time
            bullet.y = y0 - (bullet.vel*(-math.sin(bullet.grad*math.pi/180))*bullet.time - 1/2*(bullet.time**2))
            bullet.time+=1
        else:
            bullets.pop(bullets.index(bullet))
    for event in py.event.get():
        if event.type == py.QUIT:
            exit()
        elif event.type == py.KEYDOWN:
            if event.key == py.K_a:
                flLeft = True
            if event.key == py.K_d:
                flRight = True
            if event.key == py.K_SPACE:
                bullets.append(projectile(200+(math.cos(a*math.pi/180)*50),340+(math.sin(a*math.pi/180)*50),10,WHITE,300,a))
        elif event.type == py.KEYUP:
            if event.key in [py.K_a, py.K_d]:
                flLeft = flRight = False
    if flLeft:
        a-= alpha 
    elif flRight:
        a+= alpha
    screen = py.display.set_mode((W,H))
    
    clock = py.time.Clock()
    for bullet in bullets:
        bullet.draw(screen)
    for airplane in air_planes:
        airplane.draw(screen)
    for bullet in bullets:
        for airplane in air_planes:
            if (airplane.x <= bullet.x and airplane.x + airplane.width >= bullet.x) and (airplane.y <= bullet.y and airplane.y + airplane.height >= bullet.y):
                air_planes.pop(air_planes.index(airplane))
                bullets.pop(bullets.index(bullet))
    py.draw.line(screen,WHITE,(0,350),(W,350))
    py.draw.line(screen,WHITE,(200,340),(200+(math.cos(a*math.pi/180)*50),340+(math.sin(a*math.pi/180)*50)),10)
    py.draw.rect(screen,WHITE,(190,330,20,20))
    py.display.flip()

    clock.tick(FPS)