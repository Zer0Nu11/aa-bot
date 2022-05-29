import gym
from gym import spaces
import math
import random
import numpy as np
import pygame

PLANE_NUM = 3 # max planes in same moment
WIDTH = 1280
HEIGHT = 720
TICKS = 60 # ticks per second

random.seed()
plane_img = pygame.image.load('src/assets/plane.png')
plane_img = pygame.transform.scale(plane_img, (WIDTH//15, HEIGHT//15))
plane_img_reverse = pygame.transform.flip(plane_img.copy(), True, False)

class airplane():
    def __init__(self, inited=False):
        self.direction = random.randint(0,1)
        if inited:
            self.x = random.randint(-WIDTH/10, WIDTH)
        else:
            self.x = WIDTH if self.direction else -WIDTH/10
        self.y = random.randint(int(0.1*HEIGHT), int(0.4*HEIGHT))
        self.speed = (-1 if self.direction else 1) * WIDTH/(TICKS*10)

    def update(self):
        self.x += self.speed

    def debug(self):
        print(f"({self.x},{self.y}), speed=={self.speed}")

class projectile():
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.radius = 10
        self.speed = 10
        self.speed_v = self.speed * math.sin(math.radians(self.angle))
        self.speed_h = self.speed * math.cos(math.radians(self.angle))

    def update(self):
        self.y += self.speed_v
        self.x += self.speed_h
        self.speed_v += 0.085

class AntiAirEnv(gym.Env):
    def __init__(self):
        super(AntiAirEnv, self).__init__()
        self.action_space = spaces.Discrete(3) # left \ right \ shoot
        self.observation_space = spaces.Box(low=0, high=255,
                                        shape=(HEIGHT//4, WIDTH//4, 3), dtype=np.uint8)

        self.done = False

        self.airplanes = [airplane(True) for i in range(PLANE_NUM)]
        self.projectiles = []
        self.angle = -90
        self.alpha = 1 # degress per step
        self.bullets = 5
        self.bulletBonus = 3

        self.screen = None
        self.clock = None

    def step(self, action=None):
        reward = 0
        for plane in self.airplanes:
            plane.update()
            if plane.x > WIDTH or plane.x < -WIDTH/10:
                self.airplanes[self.airplanes.index(plane)] = airplane()
        for proj in self.projectiles:
            proj.update()
            if (proj.x > WIDTH or proj.x < 0) or (proj.y > HEIGHT or proj.y < 0):
                self.projectiles.pop(self.projectiles.index(proj))
                reward = -1

        for plane in self.airplanes:
            for proj in self.projectiles:
                if (plane.x <= proj.x and plane.x + plane_img.get_width() >= proj.x) and (plane.y <= proj.y and plane.y + plane_img.get_height() >= proj.y):
                    self.airplanes.pop(self.airplanes.index(plane))
                    self.projectiles.pop(self.projectiles.index(proj))
                    self.bullets += self.bulletBonus
                    reward = 1

        if len(self.airplanes) < PLANE_NUM:
            self.airplanes.append(airplane())

        if action==0:
            if(self.bullets>0):
                self.projectiles.append(projectile(0.5*WIDTH, 0.87*HEIGHT, self.angle))
                self.bullets -= 1
        elif action==1 and self.angle>-180:
            self.angle -= self.alpha
        elif action==2 and self.angle<0:
            self.angle += self.alpha
        else:
            # Invalid action
            pass
        if self.bullets == 0 and len(self.projectiles) == 0:
            self.done = True

        info = {}

        observation = self.render(mode="rgb_array")
        return observation, reward, self.done, info

    def reset(self):
        self.angle = -90
        self.airplanes = [airplane(True) for i in range(PLANE_NUM)]
        self.projectiles = []
        self.bullets = 5
        self.done = False
        observation = self.render(mode="rgb_array")
        return observation

    def render(self, mode="human"):
        if self.screen is None:
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        if self.clock is None:
            self.clock = pygame.time.Clock()

        self.screen.fill((0, 0, 0))

        for plane in self.airplanes:
            if plane.direction:
                self.screen.blit(plane_img_reverse,(plane.x,plane.y))
            else:
                self.screen.blit(plane_img,(plane.x,plane.y))
        for proj in self.projectiles:
            pygame.draw.circle(self.screen, (255,0,0),(proj.x, proj.y), proj.radius)

        font = pygame.font.SysFont(None, 60)
        scoreText = font.render('Bullets='+str(self.bullets), True, (255,255,255))
        self.screen.blit(scoreText, (int(0.42*WIDTH), int(0.945*HEIGHT)))
        
        pygame.draw.line(self.screen,(255,255,255),(0,0.9*HEIGHT),(WIDTH,0.9*HEIGHT)) # ground line
        
        # AA-gun
        gun_len = 0.11*HEIGHT
        end_pos = (0.5*WIDTH + math.cos(math.radians(self.angle)) * gun_len, 
                0.87*HEIGHT + math.sin(math.radians(self.angle)) * gun_len)
        pygame.draw.line(
            self.screen,(0,0,255),
            (0.5*WIDTH, 0.87*HEIGHT),
            end_pos,
            10
            )
        pygame.draw.rect(self.screen,(0,0,255),(0.47*WIDTH, 0.87*HEIGHT, 0.06*WIDTH, 0.03*HEIGHT))

        if mode == "human":
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(TICKS)
            
        if mode == "rgb_array":
            image_array = np.transpose(np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2))            
            return image_array[::4, ::4]


    def close(self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()
        