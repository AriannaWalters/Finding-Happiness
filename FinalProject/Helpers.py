import os, sys
import pygame
from pygame.locals import *

def load_image(name, colorkey=None):
    fullname = os.path.join('Data', 'Images')
    fullname = os.path.join(fullname, name)
    try:
        image = pygame.image.load(fullname)
        print("hi")
    except pygame.error:
        print ("Cannot load image:", fullname)
        raise SystemExit
    image = image.convert()
    print(image, colorkey)
    print(image.get_rect())
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
