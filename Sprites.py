import pygame as py, os

from pygame.locals import *

#Directorios
carpetaPrincipal= os.path.dirname(__file__)
carpetaJugador= os.path.join(carpetaPrincipal, "Imagenes/Personaje")
sniper= os.path.join(carpetaJugador, "Sniper")
carpetaGoomba= os.path.join(carpetaPrincipal, "Imagenes/Enemigos/Goomba")
carpetaMago= os.path.join(carpetaPrincipal, "Imagenes/Enemigos/Mago")

dirPotenciadores= os.path.join(carpetaPrincipal, "Imagenes/Potenciadores") 


#ícono del juego
Icono= py.image.load("Imagenes/Icono.png")


#Imágenes de dirección del personaje
Derecha=os.path.join(carpetaJugador, "Derecha")
Izquierda=os.path.join(carpetaJugador, "Izquierda")
sniperDer= os.path.join(carpetaJugador, "Sniper/Derecha")
sniperIzq= os.path.join(carpetaJugador, "Sniper/Izquierda")


movimiento={"Quieto": [], "Derecha": [], "Izquierda": [], "Salto": [], "sniperDer": [], "sniperIzq": [], "ataqueDer": [], "ataqueIzq": []}

for x in range(1,5):

    archivo= "Mario{}.png".format(x)
    imagen= py.image.load(os.path.join(Derecha, archivo))
    imagen2= py.image.load(os.path.join(sniperDer, archivo))
    movimiento["Derecha"].append(imagen)
    movimiento["sniperDer"].append(imagen2)


for x in range(1,5):

    archivo= "Mario{}.png".format(x)
    imagen= py.image.load(os.path.join(Izquierda, archivo))
    imagen2= py.image.load(os.path.join(sniperIzq, archivo))
    movimiento["Izquierda"].append(imagen)
    movimiento["sniperIzq"].append(imagen2)


#Imágenes ataque del sniper
for x in range(3):

    archivo= "Sniper{}.png".format(x)
    imagen= py.image.load(os.path.join(sniperDer, "Atacar/"+archivo))
    imagen2= py.image.load(os.path.join(sniperIzq, "Atacar/"+archivo))
    movimiento["ataqueDer"].append(imagen)
    movimiento["ataqueIzq"].append(imagen2)


#Salto del personaje
movimiento["Salto"].append(py.image.load(os.path.join(carpetaJugador, "Derecha/Salto.png")))
movimiento["Salto"].append(py.image.load(os.path.join(carpetaJugador, "Izquierda/Salto.png")))

#Modo Sniper
movimiento["Salto"].append(py.image.load(os.path.join(sniperDer, "Salto.png")))
movimiento["Salto"].append(py.image.load(os.path.join(sniperIzq, "Salto.png")))

#Imágenes de cuando está quieto el jugador

movimiento["Quieto"].append(py.image.load(os.path.join(carpetaJugador,"Derecha/Mario0.png")))
movimiento["Quieto"].append(py.image.load(os.path.join(carpetaJugador,"Izquierda/Mario0.png")))

#Modo Sniper
movimiento["Quieto"].append(py.image.load(os.path.join(carpetaJugador,"Sniper/Derecha/Mario0.png")))
movimiento["Quieto"].append(py.image.load(os.path.join(carpetaJugador,"Sniper/Izquierda/Mario0.png")))

#Imágen de muerte
movimiento["Muerte"]=py.image.load("Imagenes/Personaje/Muerte.png")


#Imágenes del proyectil
proyectil= [py.image.load("Imagenes/Items/proyectil.png"),
        py.image.load("Imagenes/Items/proyectil2.png")]

#=============== Potenciadores ========================

desarrollador= {"Hongo": [], "Arma": []}

#Pronto se añadirán más sprites al hongo y uno más al arma
for x in range(1):

    archivo= "Hongo{}.png".format(x)
    imagen= py.image.load(os.path.join(dirPotenciadores, archivo))
    desarrollador["Hongo"].append(imagen)

    archivo= "Arma{}.png".format(x)
    imagen= py.image.load(os.path.join(dirPotenciadores, archivo))
    desarrollador["Arma"].append(imagen)
   

#=========================== Sprites Enemigos ===========================

enemigos= {"Goomba": [], "Mago": []}

for x in range(3):

    archivo= "Goomba{}.png".format(x)
    archivo2= "Mago{}.png".format(x)
    enemigos["Goomba"].append(py.image.load(os.path.join(carpetaGoomba, archivo)))
    enemigos["Mago"].append(py.image.load(os.path.join(carpetaMago, archivo2)))
       

