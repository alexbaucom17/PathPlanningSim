import numpy as np
import math
import heapq

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


def computeEuclideanDistance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


class AStarPlanner:

    def __init__(self):
        self.connection_type = 'four' #or eight

    def get_neighbors(self, grid, point):
        if self.connection_type == 'four':
            a = [np.array([0, 1]),
                 np.array([1, 0]),
                 np.array([-1, 0]),
                 np.array([0, -1])]
        else:
            a = [np.array([0, 1]),
                 np.array([1, 0]),
                 np.array([-1, 0]),
                 np.array([0, -1]),
                 np.array([-1, -1]),
                 np.array([-1, 1]),
                 np.array([1, 1]),
                 np.array([1, -1])]

        new_points = []
        for direction in a:
            p = point + direction
            if not (grid.is_out_of_bounds(p) or grid.is_blocked(p)):
                new_points.append(p)

        return new_points

    def create_plan(self, start, end, grid):
        """
        Generate a path through the occupancy grid that avoids obstacles
        :param start: 2d grid coordinates of start location
        :param end: 2d grid coordinates of end location
        :param grid: boolean 2d numpy array where 0 is free space and 1 is blocked space
        :return: a list of coordinates which are the path from the start to the end. Returning an empty list means that no path was found
        """

        # Ensure start and end are numpy arrays
        start = np.array(start)
        end = np.array(end)

        # If start or end is blocked, there is no feasible path
        if grid.is_blocked(start) or grid.is_blocked(end):
            return [],[]

        # If the start position and the end are the same point, return that point as the path
        if np.all(start == end):
            return start,[]

        # Initialize queue with start position
        queue = []
        explored_points = []
        score = computeEuclideanDistance(start, end)
        counter = 0 # unique counter for points to ensure tuple comparison functions correctly
        entry = (score, counter, (start, [list(start)], 0))
        counter += 1
        heapq.heappush(queue, entry)

        while True:

            # if there are no points left to pop, then there is no feasible path
            if len(queue) == 0:
                return [], explored_points

            # Get next entry from heap
            score, count, node = heapq.heappop(queue)
            point = node[0]
            path = node[1]
            path_cost = node[2]
            explored_points.append(list(point))

            # If the point we pop is the goal, then we are done and can return the path
            if np.all(point == end):
                return path, explored_points

            # Expand neighbors of the current point
            neighbors = self.get_neighbors(grid, point)

            for n in neighbors:
                # Compute scores for current neighbor
                new_path_cost = path_cost + computeEuclideanDistance(point, n)
                estimated_goal_cost = computeEuclideanDistance(n, end)
                new_score = new_path_cost + estimated_goal_cost
                # Append neighbor to path
                new_path = path.copy()
                new_path.append(list(n))
                # Create node and entry
                node = (n, new_path, new_path_cost)
                entry = (new_score, counter, node)
                counter += 1
                # Push onto heap
                heapq.heappush(queue, entry)



class DStarPlanner:
    def __init__(self):
        pass

    def create_plan(self,start, end, occupancy_grid):
        pass