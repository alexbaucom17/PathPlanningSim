import json
import numpy as np
import pydoc
import pygame

ID_NUMBER = 0

#Pygame colors
WHITE =     (255, 255, 255)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 255,   0)
RED =       (255,   0,   0)
TEXTCOLOR = (  0,   0,  0)


def idGenerator():
    """Generate a globally unique ID number for an entity"""
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
    """A derived shape class for a rectangle"""

    def __init__(self, shape_data, **kw):
        super(Rectangle, self).__init__(**kw)
        self.length = int(shape_data['Length'])
        self.height = int(shape_data['Height'])

    def draw(self, screen, window_size, world_scale):
        x = self.pos[0] - self.length / 2.0
        y = self.pos[1] - self.height / 2.0
        px_xy = world_to_pixel_frame(np.array([x,y]), window_size, world_scale)
        #TODO: Fix scaling of length/height
        pygame.draw.rect(screen, RED, (px_xy[0], px_xy[1], self.length, self.height), )


class Triangle(BaseEntity):
    """Derived shape class for a triangle"""

    def __init__(self, shape_data, **kw):
        super(Triangle, self).__init__(**kw)
        self.length = int(shape_data['Length'])
        self.height = int(shape_data['Height'])

    def draw(self, screen, window_size, world_scale):
        top = self.pos + np.array([0, self.height / 2.0])
        bottom_left = self.pos + np.array([-self.length / 2.0, -self.height / 2.0])
        bottom_right = self.pos + np.array([self.length / 2.0, -self.height / 2.0])

        px_top = world_to_pixel_frame(top, window_size, world_scale)
        px_bottom_left = world_to_pixel_frame(bottom_left, window_size, world_scale)
        px_bottom_right = world_to_pixel_frame(bottom_right, window_size, world_scale)
        pygame.draw.polygon(screen, GREEN, [px_top, px_bottom_left, px_bottom_right])


class Circle(BaseEntity):
    """Derived shape class for a circle"""

    def __init__(self, shape_data, **kw):
        super(Circle, self).__init__(**kw)
        self.radius = shape_data['Radius']

    def draw(self, screen, window_size, world_scale):
        px_pos = world_to_pixel_frame(self.pos, window_size, world_scale)
        #TODO: fix radius scaling
        pygame.draw.circle(screen, BLUE, px_pos, self.radius)


class MotionBase(BaseEntity):
    """Implements basic motion parameters and functions"""

    def __init__(self, motion_data, **kw):
        super(MotionBase, self).__init__(**kw)
        self.vel = np.array(motion_data['InitialVelocity'])

    def update(self, dt):
        pass


class Static(MotionBase):
    """Derived motion class for static object"""

    def __init__(self, motion_data, **kw):
        super(Static, self).__init__(motion_data, **kw)

    def update(self, dt):
        self.pos = self.pos


class ConstVel(MotionBase):
    """Derived motion class for constant velocity object"""

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

#TODO: make coordinate conversions into scalar functions and then provide 2d wrappers
def pixels_to_world_frame(pixel_coords, window_size, world_scale):
    """
    Coinvert pixel coordinates into world coordinates
    :param pixel_coords: 2d pixel coordinates
    :param window_size: size of display window in pixels
    :param world_scale: scaling value of pixels/meter
    :return: Numpy vector of world coordinates
    """
    world_coords = np.array([0, 0])
    world_coords[0] = (pixel_coords[0] - window_size/2) / world_scale
    world_coords[1] = -1*(pixel_coords[1] - window_size/2) / world_scale
    return world_coords

def world_to_pixel_frame(world_coords, window_size, world_scale ):
    """
    Convert world coordinates to pixel coordiantes
    :param world_coords: 2d world coordinates in meters
    :param window_size: size of display window in pixels
    :param world_scale: scaling value of pixels/meter
    :return: Numpy vector of pixel coordinates
    """
    pixel_coords = np.array([0, 0])
    pixel_coords[0] = world_scale*world_coords[0] + window_size/2
    pixel_coords[1] = -1*world_scale*world_coords[1] + window_size/2
    return pixel_coords

class World:
    """The world is a collection of entities that exist and may move around"""

    def __init__(self, descriptor_file, screen=None, world_scale=1, physics_limit=100):
        """
        Initialize the world
        :param descriptor_file: Full path to JSON file describing the world entities
        :param screen: pygame screen to draw on. If not provided, nothing will be drawn
        :param world_scale: scaling value used for drawing on the screen. Units are pixels/meter
        :param physics_limits: distance (in meters) from world origin to simulate physics. Objects that leave this region will be deleted. Used for world discritization. If not specified, it is set to 100 meters or 20% larger than the pygame screen
        """

        self.entity_list = self.create_entities_from_file(descriptor_file)

        # initialize animation window
        if screen:
            self.display_mode = 'Screen'
            self.screen = screen
            self.screen.fill(WHITE)
            self.window_size = self.screen.get_width()
            self.world_scale = world_scale
            self.physics_limit = self.get_physicis_limit_from_screen(0.2)
            self.draw()
        else:
            self.display_mode = 'None'
            self.screen = None
            self.window_size = None
            self.world_scale = None
            self.physics_limit = physics_limit

    def create_entities_from_file(self, file):
        """Open a JSON file an generate world entities from the file"""
        with open(file) as f:
            file_data = json.load(f)
        return [self.create_entity(entity_data) for entity_data in file_data['Entities']]

    def get_physicis_limit_from_screen(self, buffer_fraction):
        """Generates the physicis limits from the pygame screen size"""
        screen_size_in_pixels = [self.window_size/2, self.window_size/2]
        screen_size_in_meters = pixels_to_world_frame(screen_size_in_pixels, self.window_size, self.world_scale)
        return screen_size_in_meters[0] * (1+buffer_fraction)

    @staticmethod
    def create_entity(entity_data):
        """Create an entity based on struct of entity data loaded from JSON"""
        tmp_class = create_dynamic_object(pydoc.locate('World.'+entity_data['Motion']['Type']),
                                          pydoc.locate('World.'+entity_data['Shape']['Type']))
        return tmp_class(entity_data['Motion'],
                         entity_data['Shape'],
                         entity_data['Motion']['InitialPosition'])

    def step(self, dt):
        """Perform a physics time step for each entity in the world"""
        for entity in self.entity_list:
            entity.update(dt)

        # TODO: Clear objects outside physics limit

    def draw(self):
        """Draw the world"""
        if self.display_mode == 'None':
            raise ValueError('Specify a pygame screen in order to draw the world')

        self.screen.fill(WHITE)
        for entity in self.entity_list:
            entity.draw(self.screen, self.window_size, self.world_scale)


    def get_occupancy_grid(self, resolution):
        """Get a discritized representation of the world with the given resolution
        Resolution parameter should be in meters/cell. Returns an object of type OccupancyGrid
        """
        occ_grid = OccupancyGrid(2*self.physics_limit, resolution)
        for entity in self.entity_list:
            occ_grid.add_entity(entity)
        return occ_grid


class OccupancyGrid:
    """Stores and provides world information as a 2d boolean numpy array"""

    def __init__(self, size, resolution):
        """
        Creates an occupancy grid to store world information
        :param size: scalar value representing the length of the grid in meters on one size
        :param resolution: scalar value representing the size mapping of meters to cells. Units are meters/cell
        """

        self.size = size
        self.resolution = resolution
        self.n_cells = round(size/resolution)
        self.grid = np.zeros((self.n_cells,self.n_cells), dtype=np.bool)

    def add_entity(self, entity):
        blocked_cells = entity.get_blocked_cells(self.resolution)
        self.fill_blocked_cells(blocked_cells)

    def fill_blocked_cells(self, blocked_cells):
        pass

    def get_grid(self):
        return self.grid

    def index_to_meters(self, index):
        pass

    def meters_to_index(self, meters):
        pass

    def position_to_2d_index(self, position):
        pass

    def index_to_2d_position(self, index):
        pass






