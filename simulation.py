#!/usr/bin/env python

import sys, getopt, pyglet, random, math
from datetime import datetime
from game import player
from os import path
from simulation import resources, cone, util

# Set up a window
game_window = pyglet.window.Window(fullscreen=True)

main_batch = pyglet.graphics.Batch()

pyglet.gl.glLineWidth(2)

player_car = None
finish_line = \
    [game_window.width/4, game_window.height/3 - 75, game_window.height/3 + 75]
old_player_position = []

score = 0
game_objects = []
cones = []

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
    global score, player_car, old_player_position
    global game_objects, event_stack_size

    while event_stack_size > 0:
        game_window.pop_handlers()
        event_stack_size -= 1

    score = 0
    # Initialize the player sprite
    player_car = player.Player(
        max_x=game_window.width,
        max_y=game_window.height,
        x=game_window.width/4,
        y=game_window.height/3,
        batch=main_batch)
    old_player_position = [player_car.x, player_car.y]

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
    counter.draw()

    pyglet.gl.glColor3f(1, 0, 0)
    pyglet.graphics.draw(4, pyglet.gl.GL_LINES,
        ("v2f",
            (
            0, 0,
            0, 0,
            player_car.x, player_car.y,
            player_car.x + 50 * math.cos(-math.radians(player_car.rotation + player_car.target_steering)),
            player_car.y + 50 * math.sin(-math.radians(player_car.rotation + player_car.target_steering))
            )
        )
    )

    pyglet.gl.glColor3f(1, 1, 1)
    pyglet.graphics.draw(4, pyglet.gl.GL_LINES,
        ("v2f",
            (
            0, 0,
            0, 0,
            finish_line[0], finish_line[1],
            finish_line[0], finish_line[2]
            )
        )
    )

    main_batch.draw()

def add_cone(position):
        new_cone = cone.Cone(
            x=position[0],
            y=position[1],
            max_x=game_window.width,
            max_y=game_window.height,
            batch=main_batch)

        cones.extend([new_cone])

@game_window.event
def on_mouse_press(x, y, button, modifiers):
    global cones

    if (button == pyglet.window.mouse.LEFT):
        add_cone([x, y])

    elif (button == pyglet.window.mouse.RIGHT):
        if not cones:
            return

        closest = [util.distance([x, y], [cones[0].x, cones[0].y]), cones[0]]
        for cone in cones[1:]:
            distance = util.distance([x, y], [cone.x, cone.y])
            if (closest[0] > distance):
                closest = [distance, cone]

        if (closest[0] < 20):
            closest[1].delete()
            cones.remove(closest[1])

    elif (button == pyglet.window.mouse.MIDDLE):
        if not cones:
            return

        now = datetime.now()
        filename = path.join(
            'courses',
            f'{now.year}{now.month}{now.day}' + \
                f'_{now.hour}{now.minute}{now.second}.csv')
        with open(filename, "a") as save_file:
            for to_export in cones:
                save_file.write(f'{to_export.export()}\n')
                to_export.delete()

        cones = []

def update(dt):
    global score, old_player_position

    for obj in game_objects:
        obj.update(dt)

    for cone in cones:
        if cone.collides_with(player_car):
            player_car.reset()
            score = 0

    score += math.floor(player_car.speed)**2 * dt;

    # Finish line check
    x_passing_finish = old_player_position[0] < finish_line[0] \
        and player_car.x >= finish_line[0]
    y_passing_finish = player_car.y >= finish_line[1] \
        and player_car.y <= finish_line[2]


    if (x_passing_finish and y_passing_finish):
        score += 10000000
    old_player_position = [player_car.x, player_car.y]

    score_label.text = score_text + str(math.floor(score))
    target_speed_label.text = \
        target_speed_text + str(math.floor(player_car.target_speed))

def parse_args(argv):
    help_line = 'simulation.py -c <coursefile>'
    try:
        opts, args = getopt.getopt(argv,"hc:",["course="])
    except getopt.GetoptError:
        print(help_line)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_line)
            sys.exit()
        elif opt in ("-c", "--course"):
            with open(arg) as course_file:
                for line in course_file:
                    new_cone = line.split(',')
                    add_cone(list(map(int, new_cone)))


if __name__ == "__main__":
    parse_args(sys.argv[1:])

    # Start it up!
    init()

    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()
