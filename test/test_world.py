import unittest
import numpy as np
import World
import pydoc


class TestDynamicObjects(unittest.TestCase):

    def test_object_creation(self):
        const_vel_rectangle_class = World.create_dynamic_object(World.ConstVel, World.Rectangle)
        self.assertTrue(type(const_vel_rectangle_class) == type)
        self.assertTrue(const_vel_rectangle_class.__name__ == 'ConstVel_Rectangle')
        static_circle_class = World.create_dynamic_object(World.Static, World.Circle)
        self.assertTrue(type(static_circle_class) == type)
        self.assertTrue(static_circle_class.__name__ == 'Static_Circle')

    def test_object_creation_from_string(self):
        cls1 = pydoc.locate('World.ConstVel')
        cls2 = pydoc.locate('World.Triangle')
        const_vel_triangle_class = World.create_dynamic_object(cls1, cls2)
        self.assertTrue(const_vel_triangle_class.__name__ == 'ConstVel_Triangle')

    def test_object_instantiation1(self):
        static_circle_class = World.create_dynamic_object(World.Static, World.Circle)
        motion_data = {'InitialVelocity': [5, 2]}
        shape_data = {'Radius': 2}
        position = [2, 1]
        static_circle_instance = static_circle_class(motion_data, shape_data, position)
        self.assertTrue(np.all(static_circle_instance.pos == [2, 1]))
        self.assertTrue(np.all(static_circle_instance.vel == [5, 2]))
        self.assertTrue(static_circle_instance.radius == 2)
        self.assertTrue(static_circle_instance.id == 1)

    def test_object_instantiation2(self):
        const_vel_rectangle_class = World.create_dynamic_object(World.ConstVel, World.Rectangle)
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


class TestWorld(unittest.TestCase):

    def test_initialization(self):
        w = World.World('D:\LocalFiles\Github\PathPlanningSim\world_for_unittests.json',
                        draw_window=False)
        self.assertTrue(type(w.entity_list[0]).__qualname__ == 'Static_Rectangle')
        self.assertTrue(type(w.entity_list[1]).__qualname__ == 'ConstVel_Circle')
        self.assertTrue(type(w.entity_list[2]).__qualname__ == 'Static_Triangle')

    def test_pixel_to_world(self):
        window = 300

        pc = np.array([150, 150])
        wc_act = np.array([0, 0])
        wc_test = World.pixels_to_world_frame(window,pc)
        self.assertTrue(np.all(wc_act == wc_test))

        pc = np.array([0, 0])
        wc_act = np.array([-150, 150])
        wc_test = World.pixels_to_world_frame(window, pc)
        self.assertTrue(np.all(wc_act == wc_test))

        pc = np.array([300, 0])
        wc_act = np.array([150, 150])
        wc_test = World.pixels_to_world_frame(window, pc)
        self.assertTrue(np.all(wc_act == wc_test))

        pc = np.array([0, 300])
        wc_act = np.array([-150, -150])
        wc_test = World.pixels_to_world_frame(window, pc)
        self.assertTrue(np.all(wc_act == wc_test))

        pc = np.array([300, 300])
        wc_act = np.array([150, -150])
        wc_test = World.pixels_to_world_frame(window, pc)
        self.assertTrue(np.all(wc_act == wc_test))

    def test_world_to_pixel(self):
        window = 300

        pc_act = np.array([150, 150])
        wc = np.array([0, 0])
        pc_test = World.world_to_pixel_frame(window,wc)
        self.assertTrue(np.all(pc_act == pc_test))

        pc_act = np.array([0, 0])
        wc = np.array([-150, 150])
        pc_test = World.world_to_pixel_frame(window, wc)
        self.assertTrue(np.all(pc_act == pc_test))

        pc_act = np.array([300, 0])
        wc = np.array([150, 150])
        pc_test = World.world_to_pixel_frame(window, wc)
        self.assertTrue(np.all(pc_act == pc_test))

        pc_act = np.array([0, 300])
        wc = np.array([-150, -150])
        pc_test = World.world_to_pixel_frame(window, wc)
        self.assertTrue(np.all(pc_act == pc_test))

        pc_act = np.array([300, 300])
        wc = np.array([150, -150])
        pc_test = World.world_to_pixel_frame(window, wc)
        self.assertTrue(np.all(pc_act == pc_test))



