import numpy as np
import pygame


class Agent:

    def __init__(self, screen=None):
        if screen:
            self.screen = screen

    def step(self, dt):
        pass

    def draw(self):
        pass