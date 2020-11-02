import pygame as pg, os
from pygame import *

directorio= os.path.dirname(__file__)
dirBloques= os.path.join(directorio, "Bloques")
Especiales= os.path.join(dirBloques, "Especiales")
decoracion= os.path.join(dirBloques, "Decoracion")


bloques= {"Bonus": [], "Montanias": [], "Nubes": [], 
        "Suelo": pg.image.load(os.path.join(decoracion, "Suelo.png")), 
        "Arbol": pg.image.load(os.path.join(decoracion, "arboles.png")) ,
        "Tuberia": pg.image.load(os.path.join(Especiales, "tuberia.png"))}


for x in range(2):

    archivo= "montania{}.png".format(x)
    imagen= pg.image.load(os.path.join(decoracion, archivo))
    bloques["Montanias"].append(imagen)

    archivo= "bloqueBonus{}.png".format(x)
    imagen= pg.image.load(os.path.join(Especiales, archivo))
    bloques["Bonus"].append(imagen)

    archivo= "nube{}.png".format(x)
    imagen= pg.image.load(os.path.join(decoracion, archivo))
    bloques["Nubes"].append(imagen)
