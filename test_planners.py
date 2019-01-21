import unittest
import numpy as np
import Planner
import World


class TestAStarPlanner(unittest.TestCase):

    sample_grid = [[0, 0, 0, 0, 0],
                   [0, 1, 1, 1, 0],
                   [0, 0, 0, 1, 0],
                   [1, 0, 1, 1, 0],
                   [0, 0, 0, 0, 0]]
    sample_grid_bool = np.array(sample_grid, dtype=bool)
    occ_grid = World.occupancy_grid_from_numpy_array(sample_grid_bool)

    def test_createPlan_WhenStartBlocked_ReturnsEmptyPath(self):
        start = [1,1]
        end = [0,1]
        p = Planner.AStarPlanner()
        path = p.create_plan(start, end, self.occ_grid)
        self.assertFalse(path)

    def test_createPlan_WhenEndBlocked_ReturnsEmptyPath(self):
        end = [1,1]
        start = [0,1]
        p = Planner.AStarPlanner()
        path = p.create_plan(start, end, self.occ_grid)
        self.assertFalse(path)

    def test_createPlan_WhenStartAndEndMatch_ReturnsSinglePoint(self):
        end = [0,1]
        start = [0,1]
        p = Planner.AStarPlanner()
        path = p.create_plan(start, end, self.occ_grid)
        self.assertTrue(np.all(path == start))

    def test_createPlan_EasyPath(self):
        start = [0,0]
        end = [1,4]
        expected_path = [[0,0],[0,1],[0,2],[0,3],[0,4],[1,4]]
        p = Planner.AStarPlanner()
        path = p.create_plan(start, end, self.occ_grid)
        self.assertEqual(len(expected_path), len(path))
        path_match = [np.all(path[i] == expected_path[i]) for i in range(len(path))]
        self.assertTrue(np.all(path_match))

    def test_createPlan_MediumPath(self):
        start = [2,2]
        end = [4,3]
        expected_path = [[2,2],[2,1],[3,1],[4,1],[4,2],[4,3]]
        p = Planner.AStarPlanner()
        path = p.create_plan(start, end, self.occ_grid)
        self.assertEqual(len(expected_path), len(path))
        path_match = [np.all(path[i] == expected_path[i]) for i in range(len(path))]
        self.assertTrue(np.all(path_match))

    def test_createPlan_HardPath(self):
        start = [4,0]
        end = [0,4]
        expected_path = [[4,0],[4,1],[4,2],[4,3],[4,4],[3,4],[2,4],[1,4],[0,4]]
        p = Planner.AStarPlanner()
        path = p.create_plan(start, end, self.occ_grid)
        self.assertEqual(len(expected_path), len(path))
        path_match = [np.all(path[i] == expected_path[i]) for i in range(len(path))]
        self.assertTrue(np.all(path_match))