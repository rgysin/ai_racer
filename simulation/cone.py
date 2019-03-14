import pyglet, math
from pyglet.window import key
from simulation import physicalobject, resources

class Cone(physicalobject.PhysicalObject):
    def __init__(self, *args, **kwargs):
        super(Cone, self).__init__(img=resources.cone_image, *args, **kwargs)
        self.event_handlers = []
