import sys
import World
import Agent
import pygame

#Configuration
TARGET_FPS = 60
WINDOW_SIZE = 750
FILE_NAME =  'D:\LocalFiles\Github\PathPlanningSim\sample_world.json'

#Initialization
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
W = World.World(FILE_NAME, window_size=WINDOW_SIZE, screen=screen)
A = Agent.Agent(screen=screen)

clock = pygame.time.Clock()

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
