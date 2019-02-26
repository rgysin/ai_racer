import pyglet, random, math
from game import load, player, resources

# Set up a window
game_window = pyglet.window.Window(800, 600)

main_batch = pyglet.graphics.Batch()

# Set up the two top labels
score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)

counter = pyglet.clock.ClockDisplay()

player_ship = None
score = 0
game_objects = []

# We need to pop off as many event stack frames as we pushed on
# every time we reset the level.
event_stack_size = 0


def init():
    global score

    score = 0
    score_label.text = "Score: " + str(score)

    reset_level()


def reset_level():
    global player_ship, game_objects, event_stack_size

    # Initialize the player sprite
    player_ship = player.Player(x=400, y=300, batch=main_batch)

    # Store all objects that update each frame in a list
    game_objects = [player_ship]

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

if __name__ == "__main__":
    # Start it up!
    init()

    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()
