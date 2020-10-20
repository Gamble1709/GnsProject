import pygame as py, os

from pygame.locals import *

#Directorios
carpetaPrincipal= os.path.dirname(__file__)
carpetaJugador= os.path.join(carpetaPrincipal, "Imagenes/Personaje")
sniper= os.path.join(carpetaJugador, "Sniper")

#ícono del juego
Icono= py.image.load("Imagenes/Icono.png")


#Imágenes de dirección del personaje
Camina_Derecha=[py.image.load(os.path.join(carpetaJugador, "Derecha/Mario.png")),
                py.image.load(os.path.join(carpetaJugador, "Derecha/Mario-1.png")),
                py.image.load(os.path.join(carpetaJugador, "Derecha/Mario-2.png")),
                py.image.load(os.path.join(carpetaJugador, "Derecha/Mario-3.png")),
                py.image.load(os.path.join(carpetaJugador, "Derecha/Mario-4.png"))]



Camina_Izquierda=[py.image.load(os.path.join(carpetaJugador, "Izquierda/Mario2.png")),
                py.image.load(os.path.join(carpetaJugador, "Izquierda/Mario3.png")),
                py.image.load(os.path.join(carpetaJugador, "Izquierda/Mario4.png")),
                py.image.load(os.path.join(carpetaJugador, "Izquierda/Mario5.png")),
                py.image.load(os.path.join(carpetaJugador, "Izquierda/Mario6.png"))]


#Imagenes de salto
Saltos= [py.image.load(os.path.join(carpetaJugador, "Derecha/Salto.png")),
         py.image.load(os.path.join(carpetaJugador, "Izquierda/Salto.png"))]
         

#Imágenes de cuando está quieto el jugador
Quieto= [py.image.load(os.path.join(carpetaJugador,"Derecha/Mario.png")),
         py.image.load(os.path.join(carpetaJugador,"Izquierda/Mario6.png"))]


#Imágen de muerte
Muerte=py.image.load("Imagenes/Personaje/Muerte.png")


#=============== Sprites sniper =====================

sniperDerecha= [py.image.load(os.path.join(sniper, "Derecha/Mario.png")),
                py.image.load(os.path.join(sniper, "Derecha/Mario-1.png")),
                py.image.load(os.path.join(sniper, "Derecha/Mario-2.png")),
                py.image.load(os.path.join(sniper, "Derecha/Mario-3.png")),
                py.image.load(os.path.join(sniper, "Derecha/Mario-4.png"))]


sniperIzquierda= [py.image.load(os.path.join(sniper, "Izquierda/Mario.png")),
                  py.image.load(os.path.join(sniper, "Izquierda/Mario-1.png")),
                  py.image.load(os.path.join(sniper, "Izquierda/Mario-2.png")),
                  py.image.load(os.path.join(sniper, "Izquierda/Mario-3.png")),
                  py.image.load(os.path.join(sniper, "Izquierda/Mario-4.png"))]


sniperSalto=[py.image.load(os.path.join(sniper, "Derecha/Salto.png")),
             py.image.load(os.path.join(sniper, "Izquierda/Salto.png"))]


#Imágenes ataque del sniper
ataqueIzquierda= [py.image.load(os.path.join(sniper, "Izquierda/Disparar/Sniper.png")),
                  py.image.load(os.path.join(sniper, "Izquierda/Disparar/Sniper1.png")),
                  py.image.load(os.path.join(sniper, "Izquierda/Disparar/Sniper2.png"))]


ataqueDerecha= [py.image.load(os.path.join(sniper, "Derecha/Disparar/Sniper.png")),
                py.image.load(os.path.join(sniper, "Derecha/Disparar/Sniper1.png")),
                py.image.load(os.path.join(sniper, "Derecha/Disparar/Sniper2.png"))]


#Imágenes del proyectil
proyectil= [py.image.load("Imagenes/Items/proyectil.png"),
        py.image.load("Imagenes/Items/proyectil2.png")]

#=============== Potenciadores ========================

hongo= py.image.load("Imagenes/Potenciadores/Hongo.png")
arma= py.image.load("Imagenes/Potenciadores/Arma.png")


#=========================== Sprites Enemigos ===========================

Enemigo_1=[py.image.load("Imagenes/Enemigos/Enemy_1.png"),
           py.image.load("Imagenes/Enemigos/Enemy_2.png"),
           py.image.load("Imagenes/Enemigos/Muerte.png")]
        

mago= [py.image.load("Imagenes/Enemigos/Mago/Mago1.png"),
        py.image.load("Imagenes/Enemigos/Mago/Mago2.png"),
        py.image.load("Imagenes/Enemigos/Mago/Mago3.png"),]

