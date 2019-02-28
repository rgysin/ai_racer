import pyglet, math
from pyglet.window import key
from simulation import car

class Player(car.Car):
    """Physical object that responds to user input"""

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        # Set some easy-to-tweak constants
        self.thrust = 10
        self.rotate_speed = car.STEPPER_SLEW

        # Tell the game handler about any event handlers
        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

    def update(self, dt):
        # Do all the normal physics stuff
        super(Player, self).update(dt)

        if self.key_handler[key.LEFT]:
            self.target_steering -= self.rotate_speed * dt
        if self.key_handler[key.RIGHT]:
            self.target_steering += self.rotate_speed * dt
        if self.key_handler[key.UP]:
            self.target_speed += self.thrust * dt;
        if self.key_handler[key.DOWN]:
            self.target_speed -= self.thrust * dt;

    def delete(self):
        super(Player, self).delete()
