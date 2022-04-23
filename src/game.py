import pygame as py
import math
import random

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
L = 350 # line
W = 900 # pixel screensize
H = 400
FPS = 20 # tickrate
speed = 5 # speed of planes
last_time = 0
x = W//2
y = H//2
a = 0
score = 0
x0 = 200+(math.cos(a*math.pi/180))
y0 = L-10+(math.sin(a*math.pi/180))
alpha = 5 # angle per button press
flLeft = flRight = False # button long-press flags
air = py.image.load('src/plane.png')

random.seed()

class airplanes():
    def __init__(self, x,y, width, height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 5
    def draw(self,win):
        win.blit(air,(self.x,self.y))

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

# existing entities
bullets = []
air_planes = []
# plane spawn
def random_spawn():
    air_planes.append(airplanes(1, random.randint(30,220), 30,30, WHITE))
    
# primary data loop
while True:
    if(py.time.get_ticks()-last_time > random.randint(2000,3000)):
        random_spawn()
        last_time = py.time.get_ticks()
    # update planes coordinates
    for airplane in air_planes:
        if airplane.x < W and airplane.x > 0 and airplane.y < H and airplane.y > 0:
            airplane.x += airplane.speed
        if airplane.x >= W:
            air_planes.pop(air_planes.index(airplane))
    # update shells coordinates
    for bullet in bullets:
        if bullet.x < W and bullet.x > 0 and bullet.y < H and bullet.y > 0 and bullet.y < L:
            bullet.x = x0 +  bullet.vel*(math.cos(bullet.grad*math.pi/180))*bullet.time
            bullet.y = y0 - (bullet.vel*(-math.sin(bullet.grad*math.pi/180))*bullet.time - 1/2*(bullet.time**2))
            bullet.time+=1
        else:
            bullets.pop(bullets.index(bullet))
    # event handler (user controller)
    for event in py.event.get():
        if event.type == py.QUIT:
            exit()
        elif event.type == py.KEYDOWN:
            if event.key == py.K_a:
                flLeft = True
            if event.key == py.K_d:
                flRight = True
            if event.key == py.K_SPACE:
                bullets.append(projectile(200+(math.cos(a*math.pi/180)*50),L - 10+(math.sin(a*math.pi/180)*50),10,WHITE,300,a))
        elif event.type == py.KEYUP:
            if event.key in [py.K_a, py.K_d]:
                flLeft = flRight = False
    if flLeft and a>-180:
        a-= alpha 
    elif flRight and a<0:
        a+= alpha

    screen = py.display.set_mode((W,H))
    clock = py.time.Clock()

    for bullet in bullets:
        bullet.draw(screen)
    for airplane in air_planes:
        airplane.draw(screen)
    # check hits
    for bullet in bullets:
        for airplane in air_planes:
            if (airplane.x <= bullet.x and airplane.x + air.get_width() >= bullet.x) and (airplane.y <= bullet.y and airplane.y + air.get_height() >= bullet.y):
                air_planes.pop(air_planes.index(airplane))
                bullets.pop(bullets.index(bullet))
                score+=1

    # UI objects
    font = py.font.SysFont(None, 24)
    img = font.render('Score='+str(score), True, WHITE)
    screen.blit(img, (W//2-90, H-30))

    py.draw.line(screen,WHITE,(0,L),(W,L))
    py.draw.line(screen,WHITE,(200,L - 10),(200+(math.cos(a*math.pi/180)*50),L - 10+(math.sin(a*math.pi/180)*50)),10)
    py.draw.rect(screen,WHITE,(190,L - 20,20,20))
    py.display.flip()

    clock.tick(FPS)