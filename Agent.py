import numpy as np
import pygame

MAX_ACC_DELTA = 10

class Agent:

    def __init__(self, screen=None):

        self._pos = np.array([0,0])
        self._vel = np.array([0,0])
        self._acc = np.array([0,0])

        if screen:
            self.screen = screen

    def get_pos(self):
        return self._pos

    def get_vel(self):
        return self._vel

    def get_acc(self):
        return self._acc

    def set_acc(self, acc):
        #da = np.abs(acc - self.get_acc())
        #TODO: Add jerk lims
        self._acc = acc

    def step(self, dt):
        self._vel = self._vel + self._acc * dt
        #TODO: Add vel lims
        self._pos = self._pos + self._vel * dt
        #TODO: Add pos lims

    def draw(self):
        pass

#TODO: Consider splitting agent into discrete and continous agent children