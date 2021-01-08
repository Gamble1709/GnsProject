import pygame as pg
from pygame import *

ANCHO_PANTALLA=1000
ALTO_PANTALLA=512

AZUL=(82,216,183)
BLANCO=(255,255,255)
NEGRO=(0,0,0)
ROJO=(255,0,0)
VERDE=(0,255,0)

POSICIONES_LINEAS=[[360,12,665,12],[360,50,665,50],[360,12,360,50],[665,12,665,50]]

#Fuentes
bertram= pg.font.match_font('BERTRAM LET')

MENU= pg.image.load("Imagenes/Menu.png")
