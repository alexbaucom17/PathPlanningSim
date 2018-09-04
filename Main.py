import sys
import World
import Agent
import pygame
import os
import matplotlib.pyplot as plt

#Configuration
TARGET_FPS = 60
WINDOW_SIZE = 750
FILE_NAME =  'D:\LocalFiles\Github\PathPlanningSim\sample_world.json'
WINDOW_START_POS_X = 500
WINDOW_START_POS_Y = 100

#Initialization
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WINDOW_START_POS_X,WINDOW_START_POS_Y)
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
W = World.World(FILE_NAME, screen=screen, world_scale = 3)
A = Agent.Agent(screen=screen)
clock = pygame.time.Clock()

grid = W.get_occupancy_grid(1)
grid.debug_draw()
plt.show(block=False)
plt.pause(0.1)


#Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #Manage clock
    clock.tick(TARGET_FPS)
    dt = clock.get_time() / 1000.0

    #Perform physics updates
    W.step(dt)
    A.step(dt)

    #Draw
    W.draw()
    A.draw()
    pygame.display.update()

    #Debug draw
    grid = W.get_occupancy_grid(1)
    grid.debug_draw()
    plt.show(block=False)
    plt.pause(0.01)

