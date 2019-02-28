import pyglet

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2

# Tell pyglet where to find the resources
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

car_image = pyglet.resource.image("yellow_car.png")
center_image(car_image)
