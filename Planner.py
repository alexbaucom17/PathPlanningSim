import numpy as np

class Planner:

    def __init__(self, planner_type):
        if planner_type == 'Dstar':
            self.planner = DStarPlanner()
        elif planner_type == 'Astar':
            self.planner = AStarPlanner()
        else:
            raise ValueError('Unknown planner type')
        self.planner_type = planner_type

    def create_plan_discrete(self, start, end, occupancy_grid):
        if self.planner_type == 'Astar' or \
            self.planner_type == 'Dstar':
            self.planner.create_plan(start, end, occupancy_grid)
        else:
            raise ValueError('Planner type '+self.planner_type+ ' does not support discrete planning')


class AStarPlanner:

    def __init__(self):
        self.connection_type = 'four' #or eight

    def create_plan(self, start, end, occupancy_grid):
        """
        Generate a path through the occupancy grid that avoids obstacles
        :param start: 2d grid coordinates of start location
        :param end: 2d grid coordinates of end location
        :param occupancy_grid: boolean 2d numpy array where 0 is free space and 1 is blocked space
        :return: a list of coordinates which are the path from the start to the end. Returning an empty list means that no path was found
        """

        



class DStarPlanner:
    def __init__(self):
        pass

    def create_plan(self,start, end, occupancy_grid):
        pass