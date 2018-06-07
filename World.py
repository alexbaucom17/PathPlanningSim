import json
import numpy as np

ID_NUMBER = 0


def idGenerator():
    global ID_NUMBER
    ID_NUMBER = ID_NUMBER + 1
    return ID_NUMBER


class BaseEntity:
    """This is a base class for an entity that exists in the world"""

    def __init__(self, position):
        self.pos = np.array(position)
        self.id = idGenerator()

    def update(self, dt):
        pass


class Rectangle(BaseEntity):

    def __init__(self, shape_data, **kw):
        super(Rectangle, self).__init__(**kw)
        self.length = int(shape_data['Length'])
        self.height = int(shape_data['Height'])


class Circle(BaseEntity):

    def __init__(self, shape_data, **kw):
        super(Circle, self).__init__(**kw)
        self.radius = shape_data['Radius']


class MotionBase(BaseEntity):

    def __init__(self, motion_data, **kw):
        super(MotionBase, self).__init__(**kw)
        self.vel = motion_data['InitialVelocity']


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


def createDynamicObject(motion_class, shape_class):
    class NewClass(motion_class, shape_class):
        def __init__(self, motion_data, shape_data, position):
            super(NewClass, self).__init__(motion_data=motion_data, shape_data=shape_data, position=position)

    NewClass.__name__ = "%s_%s" % (motion_class.__name__, shape_class.__name__)
    return NewClass


class World:
    """The world is a collection of entities that exist and may move around"""

    def __init__(self, descriptor_file):
        self.entity_list = self.createEntitiesFromFile(descriptor_file)

    def createEntitiesFromFile(self, file):
        with open(file) as f:
            file_data = json.load(f)
        return [self.createEntity(entity_data) for entity_data in file_data['Entities']]

    @staticmethod
    def createEntity(entity_data):
        if entity_data['Type'] == 'Rectangle':
            return Rectangle(entity_data)
        elif entity_data['Type'] == 'Circle':
            return Circle(entity_data)
        else:
            raise KeyError('Type '+entity_data['Type']+' is unsupported')

    def step(self, dt):
        pass

    def draw(self):
        pass

