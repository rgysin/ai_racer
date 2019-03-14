import pyglet, math
from pyglet.window import key
from simulation import physicalobject, resources

# Constants - TODO: Move these to either class privates or expose to user
scaling_factor = 50.0 # Pixel to real world scaling
STEPPER_SLEW = 378.0 / 4.0 # Speed of the stepper motor in degrees/second
LIDAR_FOV = 240 # Lidar's field of view in degrees
LIDAR_RANGE = 10000 # Lidar's filter range in millimeters
STEERING_RANGE = 45.0 # Maximum steering wheel angle
WHEEL_RANGE = 35.0 # Maximum wheel angle
VEHICLE_ACCELERATION = 5 # Max acceleration in m/s^2
VEHICLE_DECELERATION = 5 # Max deceleration in m/s^2
L = 942.0 #Wheel base in mm
MAX_SPEED = 50.0 # Arbitrary max speed
MIN_SPEED = 0.0 # Racecars don't go backwards

class Car(physicalobject.PhysicalObject):
    def __init__(self, *args, **kwargs):
        super(Car, self).__init__(img=resources.car_image, *args, **kwargs)

        # Initial Position
        self.initial_position = [ kwargs['x'], kwargs['y'] ]

        # Vehicle params
        self.wheel_angle = 0
        self.steering = 0
        self.speed = 0;

        self.target_steering = 0
        self.target_speed = 0

        # Tell the game handler about any event handlers
        self.event_handlers = []

    def update(self, dt):
        # Do all the normal physics stuff
        super(Car, self).update(dt)
        self.checkTargetLimits()
        self.updateActuators(dt)

    def checkTargetLimits(self):
        if self.target_steering > STEERING_RANGE:
            self.target_steering = STEERING_RANGE
        elif self.target_steering < -STEERING_RANGE:
            self.target_steering = -STEERING_RANGE

        if self.target_speed > MAX_SPEED:
            self.target_speed = MAX_SPEED
        elif self.target_speed < MIN_SPEED:
            self.target_speed = MIN_SPEED

    def updateActuators(self, dt):
        '''
        Updates vehicle actuators. Used to model mechanical lag in the system.
        '''

        # Updates steering angle and wheel angle
        if abs(self.target_steering - self.steering) < (STEPPER_SLEW*dt):
            self.steering = self.target_steering
        elif self.target_steering - self.steering < 0:
            self.steering = self.target_steering + (STEPPER_SLEW*dt)
        else:
            self.steering = self.target_steering - (STEPPER_SLEW*dt)

        self.wheel_angle = self.steering * WHEEL_RANGE / STEERING_RANGE

        # Update vehicle speed
        if self.speed > self.target_speed:
            if self.speed - (VEHICLE_DECELERATION * dt) > self.target_speed:
                self.speed = self.speed - (VEHICLE_DECELERATION * dt)
            else:
                self.speed = self.target_speed
        else:
            if self.speed + (VEHICLE_ACCELERATION * dt) < self.target_speed:
                self.speed = self.speed + (VEHICLE_ACCELERATION * dt)
            else:
                self.speed = self.target_speed

        # TODO: Add vehicle position and angle change
        self.rotation += 1000.0 * math.floor(self.speed) * \
            self.wheel_angle * dt / L

        if self.rotation > 360.:
            self.rotation -= 360.
        elif self.rotation < -360.:
            self.rotation+= 360.

        angle_radians = -math.radians(self.rotation)
        self.velocity_x = math.cos(angle_radians) * \
            math.floor(self.speed) * scaling_factor
        self.velocity_y = math.sin(angle_radians) * \
            math.floor(self.speed) * scaling_factor

    def reset(self):
        self.x = self.initial_position[0]
        self.y = self.initial_position[1]

        self.wheel_angle = 0
        self.steering = 0
        self.speed = 0;

        self.target_steering = 0
        self.target_speed = 0

        self.velocity_x = 0
        self.velocity_y = 0

        self.rotation = 0
