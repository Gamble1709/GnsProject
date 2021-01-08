import pygame as pg, os

from pygame.locals import *

#Directorios
carpetaPrincipal= os.path.dirname(__file__)
carpetaJugador= os.path.join(carpetaPrincipal, "Imagenes/Personaje")
sniper= os.path.join(carpetaJugador, "Sniper")
carpetaGoomba= os.path.join(carpetaPrincipal, "Imagenes/Enemigos/Goomba")
carpetaMago= os.path.join(carpetaPrincipal, "Imagenes/Enemigos/Mago")
carpetaCaracol= os.path.join(carpetaPrincipal, "Imagenes/Enemigos/Caracol")

dirPotenciadores= os.path.join(carpetaPrincipal, "Imagenes/Potenciadores") 


#ícono del juego
Icono= pg.image.load("Imagenes/Icono.png")


#Imágenes de dirección del personaje
Derecha=os.path.join(carpetaJugador, "Derecha")
Izquierda=os.path.join(carpetaJugador, "Izquierda")
sniperDer= os.path.join(carpetaJugador, "Sniper/Derecha")
sniperIzq= os.path.join(carpetaJugador, "Sniper/Izquierda")


movimiento={"Quieto": [], "Derecha": [], "Izquierda": [], "Salto": [], "sniperDer": [], "sniperIzq": [], "ataqueDer": [], "ataqueIzq": []}
for x in range(1,5):

    archivo= "Mario{}.png".format(x)
    imagen= pg.image.load(os.path.join(Derecha, archivo))
    imagen2= pg.image.load(os.path.join(sniperDer, archivo))
    movimiento["Derecha"].append(imagen)
    movimiento["sniperDer"].append(imagen2)


for x in range(1,5):

    archivo= "Mario{}.png".format(x)
    imagen= pg.image.load(os.path.join(Izquierda, archivo))
    imagen2= pg.image.load(os.path.join(sniperIzq, archivo))
    movimiento["Izquierda"].append(imagen)
    movimiento["sniperIzq"].append(imagen2)


#Imágenes ataque del sniper
for x in range(3):

    archivo= "Sniper{}.png".format(x)
    imagen= pg.image.load(os.path.join(sniperDer, "Atacar/"+archivo))
    imagen2= pg.image.load(os.path.join(sniperIzq, "Atacar/"+archivo))
    movimiento["ataqueDer"].append(imagen)
    movimiento["ataqueIzq"].append(imagen2)


#Salto del personaje
movimiento["Salto"].append(pg.image.load(os.path.join(carpetaJugador, "Derecha/Salto.png")))
movimiento["Salto"].append(pg.image.load(os.path.join(carpetaJugador, "Izquierda/Salto.png")))

#Modo Sniper
movimiento["Salto"].append(pg.image.load(os.path.join(sniperDer, "Salto.png")))
movimiento["Salto"].append(pg.image.load(os.path.join(sniperIzq, "Salto.png")))

#Imágenes de cuando está quieto el jugador

movimiento["Quieto"].append(pg.image.load(os.path.join(carpetaJugador,"Derecha/Mario0.png")))
movimiento["Quieto"].append(pg.image.load(os.path.join(carpetaJugador,"Izquierda/Mario0.png")))

#Modo Sniper
movimiento["Quieto"].append(pg.image.load(os.path.join(carpetaJugador,"Sniper/Derecha/Mario0.png")))
movimiento["Quieto"].append(pg.image.load(os.path.join(carpetaJugador,"Sniper/Izquierda/Mario0.png")))

#Imágen de muerte
movimiento["Muerte"]=pg.image.load("Imagenes/Personaje/Muerte.png")


#Imágenes del proyectil
proyectil= [pg.image.load("Imagenes/Items/proyectil.png"),
        pg.image.load("Imagenes/Items/proyectil2.png")]

#=============== Potenciadores ========================

desarrollador= {"Hongo": [], "Arma": []}

#Pronto se añadirán más sprites al hongo y uno más al arma
for x in range(1):

    archivo= "Hongo{}.png".format(x)
    imagen= pg.image.load(os.path.join(dirPotenciadores, archivo))
    desarrollador["Hongo"].append(imagen)

    archivo= "Arma{}.png".format(x)
    imagen= pg.image.load(os.path.join(dirPotenciadores, archivo))
    desarrollador["Arma"].append(imagen)
   

#=========================== Sprites Enemigos ===========================

enemigos= {"Goomba": [], "Mago": [[],[]], "Caracol": [], "Prueba": [[],[]]}

for x in range(3):

    archivo= f"Goomba{x}.png"
    enemigos["Goomba"].append(pg.image.load(os.path.join(carpetaGoomba, archivo)))
    archivo= f"Caracol{x}.png"
    enemigos["Caracol"].append(pg.image.load(os.path.join(carpetaCaracol, archivo)))
       

mago= pg.image.load(os.path.join(carpetaMago, "MagoP1.png"))
cuadrado= mago.get_rect()
widthImage=  int(cuadrado.w / 6) 
heightImage= int(cuadrado.h / 2)


rect= pg.Rect(0, heightImage + 14, widthImage - 40, heightImage -14)
enemigos["Mago"][0].append(mago.subsurface(rect))
rect= pg.Rect(0, 0, widthImage - 40, heightImage -14)
enemigos["Mago"][1].append(mago.subsurface(rect))

inicio=50

#Recortando imagenes de ataque
for columna in range(5):

    if columna == 4:

        rect= pg.Rect(inicio + 46, heightImage + 14, widthImage - 20, heightImage -14)

    else:

        rect= pg.Rect(inicio + 46, heightImage + 14, widthImage - 40, heightImage -14)


    rect2= pg.Rect(inicio + 46, 0, widthImage - 40, heightImage - 14)
    inicio+= 46 + 50 
    enemigos["Mago"][0].append(mago.subsurface(rect))
    enemigos["Mago"][1].append(mago.subsurface(rect2))


caracol= pg.image.load(os.path.join(carpetaCaracol, "Caracol.png")) 
cuadrado= caracol.get_rect()
widthImage= int(cuadrado.w / 10)
heightImage= int(cuadrado.h / 4)

for column in range(10):

    rect= pg.Rect(column * widthImage, 1 * heightImage + 18, widthImage, heightImage - 22)
    enemigos["Prueba"][0].append(caracol.subsurface(rect))

    rect= pg.Rect(column * widthImage, 3 * heightImage + 18, widthImage, heightImage - 19) 
    enemigos["Prueba"][1].append(caracol.subsurface(rect))
