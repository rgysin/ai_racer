import pyglet
from . import util


class PhysicalObject(pyglet.sprite.Sprite):
    """A sprite with physical properties such as velocity"""

    def __init__(self, max_x, max_y, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)

        """ Boundaries are walls """
        self.min_x = -self.image.width / 2
        self.min_y = -self.image.height / 2
        self.max_x = max_x + self.image.width / 2
        self.max_y = max_y + self.image.height / 2

        self.dead = False;

        # Velocity
        self.velocity_x, self.velocity_y = 0.0, 0.0

        # Tell the game handler about any event handlers
        # Only applies to things with keyboard/mouse input
        self.event_handlers = []

    def update(self, dt):
        """This method should be called every frame."""

        # Update position according to velocity and time
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        # Wrap around the screen if necessary
        self.check_bounds()

    def check_bounds(self):
        if self.x < self.min_x:
            self.x = self.max_x
        if self.y < self.min_y:
            self.y = self.max_y
        if self.x > self.max_x:
            self.x = self.min_x
        if self.y > self.max_y:
            self.y = self.min_y

    def collides_with(self, obj):
        collision_distance = self.image.width/2 + obj.image.width/2
        actual_distance = util.distance(self.position, obj.position)

        return (actual_distance <= collision_distance)

    def handle_collision_with(self):
        self.dead = True

    def delete(self):
        super(PhysicalObject, self).delete()

    def export(self):
        return f'{self.x},{self.y}'
