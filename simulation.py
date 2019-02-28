#!/usr/bin/env python

import pyglet, random, math
from game import player
from simulation import resources

# Set up a window
game_window = pyglet.window.Window(fullscreen=True)

main_batch = pyglet.graphics.Batch()

pyglet.gl.glLineWidth(2)


player_car = None
score = 0
game_objects = []

score_text = "Score: "
score_label = pyglet.text.Label(
    text=score_text + str(0),
    x=10,
    y=game_window.height-25,
    batch=main_batch)

target_speed_text = "Target Speed: "
target_speed_label = pyglet.text.Label(
    text=target_speed_text + str(0),
    x=10,
    y=game_window.height-50,
    batch=main_batch)

counter = pyglet.clock.ClockDisplay()

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

    pyglet.graphics.draw(4, pyglet.gl.GL_LINES,
        ("v2f", (0, 0, 0, 0, player_car.x, player_car.y,
        player_car.x + 50 * math.cos(-math.radians(player_car.rotation + player_car.target_steering)),
        player_car.y + 50 * math.sin(-math.radians(player_car.rotation + player_car.target_steering))))
    )

def update(dt):
    global score

    for obj in game_objects:
        obj.update(dt)

    score += dt;
    score_label.text = score_text + str(math.floor(score))
    target_speed_label.text = \
        target_speed_text + str(math.floor(player_car.target_speed))

if __name__ == "__main__":
    # Start it up!
    init()

    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()
