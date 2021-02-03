import pygame as pg, sys
from pygame.locals import *

from Constants import MENU

from Sprites import desarrollador


def mostrarTexto(ventana, fuente, texto, tamanio, color, x, y):

    tipoFuente= pg.font.Font(fuente, tamanio)
    superficie= tipoFuente.render(texto, True, color) #El True es para el 'Aliased', que hace que el texto quede liso y no pixelado
    rectangulo= superficie.get_rect()
    rectangulo.x=x
    rectangulo.y=y
    ventana.blit(superficie, rectangulo)


posicion= 300

def mostrarMenu(ventana):

    global posicion

    for eventos in pg.event.get():

        if eventos.type == QUIT:

            pg.quit()
            sys.exit()


    tecla= pg.key.get_pressed()

    ventana.blit(pg.transform.scale(MENU, (1000,512)), (0,0))
    ventana.blit(desarrollador["Hongo"][0], (360, posicion))
        
    if tecla[K_UP]:

        posicion=300

    elif tecla[K_DOWN]:

        posicion=337

    elif tecla[K_RETURN]:

        return True



def moverCamara(grupos, personajePrincipal):

    personajePrincipal.camara= True

    tecla= pg.key.get_pressed()

    if tecla[K_d]:

        mover= -10

    else:

        mover=0


    for grupo in grupos:

        for objeto in grupo:

            objeto.rect.x+= mover  
