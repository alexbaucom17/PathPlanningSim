import unittest
import numpy as np
import World


# class TestBaseEntity(unittest.TestCase):
#
#     def test_update(self):
#         pos = [2, 1]
#         vel = [3, 5]
#         motion_profile = {'Type': "Static"}
#         entity = World.BaseEntity(pos, vel, motion_profile)
#         entity.update(1)
#         self.assertTrue(np.all(entity.pos == [5, 6]))
#
# class TestWorld(unittest.TestCase):
#
#     def test_initialization(self):
#         w = World.World('D:\LocalFiles\Github\PathPlanningSim\sample_world.json')
#         self.assertTrue(1)

class TestDynamicObjects(unittest.TestCase):

    def test_object_creation(self):
        const_vel_rectangle_class = World.createDynamicObject(World.ConstVel, World.Rectangle)
        self.assertTrue(type(const_vel_rectangle_class) == type)
        self.assertTrue(const_vel_rectangle_class.__name__ == 'ConstVel_Rectangle')
        static_circle_class = World.createDynamicObject(World.Static, World.Circle)
        self.assertTrue(type(static_circle_class) == type)
        self.assertTrue(static_circle_class.__name__ == 'Static_Circle')

    def test_object_instantiation1(self):
        static_circle_class = World.createDynamicObject(World.Static, World.Circle)
        motion_data = {'InitialVelocity': [5, 2]}
        shape_data = {'Radius': 2}
        position = [2, 1]
        static_circle_instance = static_circle_class(motion_data, shape_data, position)
        self.assertTrue(np.all(static_circle_instance.pos == [2, 1]))
        self.assertTrue(np.all(static_circle_instance.vel == [5, 2]))
        self.assertTrue(static_circle_instance.radius == 2)
        self.assertTrue(static_circle_instance.id == 1)

    def test_object_instantiation2(self):
        const_vel_rectangle_class = World.createDynamicObject(World.ConstVel, World.Rectangle)
        motion_data = {'InitialVelocity': [1, 1]}
        shape_data = {'Length': 2, 'Height': 7}
        position = [4, 2]
        const_vel_rectangle_instance = const_vel_rectangle_class(motion_data, shape_data, position)
        self.assertTrue(np.all(const_vel_rectangle_instance.pos == [4, 2]))
        self.assertTrue(np.all(const_vel_rectangle_instance.vel == [1, 1]))
        self.assertTrue(const_vel_rectangle_instance.length == 2)
        self.assertTrue(const_vel_rectangle_instance.height == 7)
        self.assertTrue(const_vel_rectangle_instance.id == 2)
        const_vel_rectangle_instance.update(1)
        self.assertTrue(np.all(const_vel_rectangle_instance.pos == [5, 3]))


