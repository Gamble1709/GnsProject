import pygame as pg
from pygame.locals import *

pg.mixer.init()

pg.mixer.music.load('Soundtracks/Theme.mp3')

shoot= pg.mixer.Sound('Soundtracks/Shoot.wav')
jump= pg.mixer.Sound('Soundtracks/Jump.wav')
