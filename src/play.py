import pygame
from aaEnv import AntiAirEnv
import numpy as np
from matplotlib import pyplot as plt

flLeft = flRight = False

def event_to_action(eventlist):
    global run, key, flLeft, flRight
    for event in eventlist:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if  event.key == pygame.K_r:
                env.reset()
            elif event.key == pygame.K_a:
                flLeft = True
            elif event.key == pygame.K_d:
                flRight = True
            elif event.key == pygame.K_SPACE:
                key = 0
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_d]:
                flLeft = flRight = False
    if flLeft:
        key = 1
    elif flRight:
        key = 2

env = AntiAirEnv()

# human render
env.render()
run = True
while run:
    key = None
    get_event = pygame.event.get()
    event_to_action(get_event)
    env.step(action=key)
    env.render()
    run = not env.done and run


# numpy array output
# for i in range(50):
#     env.step(action=1)
#     if i%10==0:
#         obs, reward, done, _ = env.step(action=0)
#         plt.imshow(obs, interpolation='nearest')
#         plt.show()

pygame.quit()