import pyglet, random, math
from game import load, player, resources

# Set up a window
game_window = pyglet.window.Window(fullscreen=True)

main_batch = pyglet.graphics.Batch()

# Set up the two top labels
score_label = pyglet.text.Label(
    text="Score: 0", x=10, y=game_window.height-25, batch=main_batch)
target_speed_label = pyglet.text.Label(
    text="Target Speed: 0", x=10, y=game_window.height-50, batch=main_batch)
speed_label = pyglet.text.Label(
    text="Actual Speed: 0", x=10, y=game_window.height-75, batch=main_batch)
steering_label = pyglet.text.Label(
    text="Steering Angle: 0", x=10, y=game_window.height-100, batch=main_batch)
wheel_angle_label = pyglet.text.Label(
    text="Wheel Angle: 0", x=10, y=game_window.height-125, batch=main_batch)
vehicle_angle_label = pyglet.text.Label(
    text="Vehicle Angle: 0", x=10, y=game_window.height-150, batch=main_batch)

counter = pyglet.clock.ClockDisplay()

player_car = None
score = 0
game_objects = []

# We need to pop off as many event stack frames as we pushed on
# every time we reset the level.
event_stack_size = 0

def init():
    reset_level()


def reset_level():
    global score, player_car, game_objects, event_stack_size

    while event_stack_size > 0:
        game_window.pop_handlers()
        event_stack_size -= 1

    score = 0
    # Initialize the player sprite
    player_car = player.Player(
        max_x=game_window.width,
        max_y=game_window.height,
        x=game_window.width/2,
        y=game_window.height/2,
        batch=main_batch)

    # Store all objects that update each frame in a list
    game_objects = [player_car]

    # Add any specified event handlers to the event handler stack
    for obj in game_objects:
        for handler in obj.event_handlers:
            game_window.push_handlers(handler)
            event_stack_size += 1

@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()
    counter.draw()


def update(dt):
    global score

    for obj in game_objects:
        obj.update(dt)

    score += dt;
    score_label.text = "Score: " + str(math.floor(score))
    target_speed_label.text = "Target Speed: " + str(player_car.target_speed)
    speed_label.text = "Actual Speed: " + str(player_car.speed)

    steering_label.text="Steering Angle: " + str(player_car.steering)
    wheel_angle_label.text="Wheel Angle: " + str(player_car.wheel_angle)
    vehicle_angle_label.text="Vehicle Angle: " + str(player_car.rotation)

if __name__ == "__main__":
    # Start it up!
    init()

    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()
