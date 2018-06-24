import json
import numpy as np
import pydoc
import pygame

ID_NUMBER = 0

STEP_TIME = 0.02

#Pygame colors
WHITE =     (255, 255, 255)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 255,   0)
RED =       (255,   0,   0)
TEXTCOLOR = (  0,   0,  0)


def idGenerator():
    global ID_NUMBER
    ID_NUMBER = ID_NUMBER + 1
    return ID_NUMBER


class BaseEntity:
    """This is a base class for an entity that exists in the world
    It implements the position attribute in the base class since both the
    derived shape class and motion class need to reference it"""

    def __init__(self, position):
        self.pos = np.array(position)
        self.id = idGenerator()

    def get_id(self):
        return self.id

    def get_position(self):
        return self.pos


class Rectangle(BaseEntity):

    def __init__(self, shape_data, **kw):
        super(Rectangle, self).__init__(**kw)
        self.length = int(shape_data['Length'])
        self.height = int(shape_data['Height'])

    def draw(self, screen):
        x = self.pos[0] - self.length / 2.0
        y = self.pos[1] - self.height / 2.0
        window_size = screen.get_width()
        px_xy = world_to_pixel_frame(window_size, np.array([x,y]))
        pygame.draw.rect(screen, RED, (px_xy[0], px_xy[1], self.length, self.height), )


class Triangle(BaseEntity):

    def __init__(self, shape_data, **kw):
        super(Triangle, self).__init__(**kw)
        self.length = int(shape_data['Length'])
        self.height = int(shape_data['Height'])

    def draw(self, screen):
        top = self.pos + np.array([0, self.height / 2.0])
        bottom_left = self.pos + np.array([-self.length / 2.0, -self.height / 2.0])
        bottom_right = self.pos + np.array([self.length / 2.0, -self.height / 2.0])

        window_size = screen.get_width()
        px_top = world_to_pixel_frame(window_size, top)
        px_bottom_left = world_to_pixel_frame(window_size, bottom_left)
        px_bottom_right = world_to_pixel_frame(window_size, bottom_right)
        pygame.draw.polygon(screen, GREEN, [px_top, px_bottom_left, px_bottom_right])


class Circle(BaseEntity):

    def __init__(self, shape_data, **kw):
        super(Circle, self).__init__(**kw)
        self.radius = shape_data['Radius']

    def draw(self, screen):
        window_size = screen.get_width()
        px_pos = world_to_pixel_frame(window_size, self.pos)
        pygame.draw.circle(screen, BLUE, px_pos, self.radius)


class MotionBase(BaseEntity):

    def __init__(self, motion_data, **kw):
        super(MotionBase, self).__init__(**kw)
        self.vel = np.array(motion_data['InitialVelocity'])

    def update(self, dt):
        pass


class Static(MotionBase):

    def __init__(self, motion_data, **kw):
        super(Static, self).__init__(motion_data, **kw)

    def update(self, dt):
        self.pos = self.pos


class ConstVel(MotionBase):

    def __init__(self, motion_data, **kw):
        super(ConstVel, self).__init__(motion_data, **kw)

    def update(self, dt):
        self.pos = self.pos + self.vel * dt


def create_dynamic_object(motion_class, shape_class):
    """Generate entity classes based on the shape and motion profile provided"""

    class NewClass(motion_class, shape_class):
        def __init__(self, motion_data, shape_data, position):
            super(NewClass, self).__init__(motion_data=motion_data, shape_data=shape_data, position=position)

    NewClass.__name__ = "%s_%s" % (motion_class.__name__, shape_class.__name__)
    NewClass.__qualname__ = "%s_%s" % (motion_class.__name__, shape_class.__name__)
    return NewClass


def pixels_to_world_frame(window_size, pixel_coords):
    world_coords = np.array([0, 0])
    world_coords[0] = pixel_coords[0] - window_size/2
    world_coords[1] = -1 * (pixel_coords[1] - window_size/2)
    return world_coords

def world_to_pixel_frame(window_size, world_coords):
    pixel_coords = np.array([0, 0])
    pixel_coords[0] = world_coords[0] + window_size/2
    pixel_coords[1] = -1*world_coords[1] + window_size/2
    return pixel_coords

class World:
    """The world is a collection of entities that exist and may move around"""

    def __init__(self, descriptor_file, window_size=300, draw_window=True):
        self.entity_list = self.create_entities_from_file(descriptor_file)

        # initialize animation window
        pygame.init()
        self.window_size = window_size
        if draw_window:
            self.screen = pygame.display.set_mode((window_size, window_size))
            self.screen.fill(WHITE)
            self.draw()
            pygame.display.update()

    def create_entities_from_file(self, file):
        with open(file) as f:
            file_data = json.load(f)
        return [self.create_entity(entity_data) for entity_data in file_data['Entities']]

    @staticmethod
    def create_entity(entity_data):
        tmp_class = create_dynamic_object(pydoc.locate('World.'+entity_data['Motion']['Type']),
                                          pydoc.locate('World.'+entity_data['Shape']['Type']))
        return tmp_class(entity_data['Motion'],
                         entity_data['Shape'],
                         entity_data['Motion']['InitialPosition'])

    def step(self, dt):
        for entity in self.entity_list:
            entity.update(dt)

    def draw(self):
        self.screen.fill(WHITE)
        for entity in self.entity_list:
            entity.draw(self.screen)
        pygame.display.update()


# TODO: Maybe add scaling
# TODO: Write proper App/GUI wrapper
# TODO: Clear objects outside of window


# Testing GUI
if __name__ == '__main__':
    import sys
    w = World('D:\LocalFiles\Github\PathPlanningSim\sample_world.json',
              window_size = 750)
    target_fps = int(1/STEP_TIME)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(target_fps)
        w.step(clock.get_time()/1000.0)
        w.draw()
        print(clock.get_fps())




