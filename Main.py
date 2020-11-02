import pygame as pg, time

from pygame.locals import *

from Class import *

from Sprites import Icono, proyectil, desarrollador 

from Blocks import  bloques 

from Constants import Ancho_pantalla, Alto_pantalla, Azul, Blanco, bertram

import sys


def mostrarTexto(ventana, fuente, texto, tamanio, color, x, y):

    tipoFuente= pg.font.Font(fuente, tamanio)
    superficie= tipoFuente.render(texto, True, color) #El True es para el 'Aliased', que hace que el texto quede liso y no pixelado
    rectangulo= superficie.get_rect()
    rectangulo.x=x
    rectangulo.y=y
    ventana.blit(superficie, rectangulo)
    

#Iniciando Pygame
if __name__=="__main__":

    pg.init()



#Creación de ventana + ícono de la misma
Ventana=pg.display.set_mode((Ancho_pantalla, Alto_pantalla))
pg.display.set_icon(Icono)
    

#FPS
Fps=30
Reloj= pg.time.Clock()

#Tiempo del juego
tiempo= 500

#grupos de Sprites
sprites= pg.sprite.Group()
enemigosBasicos= pg.sprite.Group()
magos= pg.sprite.Group()
bloquesBonus= pg.sprite.Group()
bloquesSimples= pg.sprite.Group()
bloquesDecoracion= pg.sprite.Group()
nuevaTuberias= pg.sprite.Group()
potenciadores= pg.sprite.Group()
proyectiles= pg.sprite.Group()


#======================Instanciaciones==========================00

#Instanciando personajePrincipalPrincipal principal
personajePrincipal=personaje()
sprites.add(personajePrincipal)


#Instanciación de enemigos    
nuevoEnemigo= Enemigo(1,700, 395)
enemigosBasicos.add(nuevoEnemigo)


#Magos
nuevoMago= Mago(0, 905, 320)
magos.add(nuevoMago)


#Instanciando Bloques
bonus= Bonus(bloques["Bonus"][0], 600, 275)
bloquesBonus.add(bonus)

#Instanciación de los potenciadores
hongos= Potenciador(desarrollador["Hongo"][0], bonus.rect.x, bonus.rect.y -3)
generacion=False

#Verfica que se cree un nuevo objeto
intanciacionArma=False

    
#Crear animación de subida y bajada bloque bonus (Pronto se pondrá en la clase para borrar este espacio)
animacionbonus=False
subir=-8
animacion=False


#Creando bloques en orden
distanciaX=0
distanciaY=435

for x in range(75):
    sueloBasico= Bloque(bloques["Suelo"], distanciaX, distanciaY)
    bloquesSimples.add(sueloBasico)
    distanciaX+=45


#Creación de bloques vacíos (solo por decoración)

distanciaX=0
distanciaY+=23
cont=0

for x in range(80):
    
    bloque=Decoracion(bloques["Suelo"],distanciaX, distanciaY)
    bloquesDecoracion.add(bloque)

    distanciaX+=25
    cont+=1

    if cont==40:

        distanciaY+=23
        distanciaX=0



#Tuberías
nuevaTuberia= Bloque(bloques["Tuberia"], 900, 320)
nuevaTuberias.add(nuevaTuberia)

#Montañas
nuevaMontania= Decoracion(bloques["Montanias"][0], 100, 395)
bloquesDecoracion.add(nuevaMontania)

nuevaMontania= Decoracion(bloques["Montanias"][1], nuevaMontania.rect.right, 360 )
bloquesDecoracion.add(nuevaMontania)

#Nubes
nuevaNube= Decoracion(bloques["Nubes"][0], 300, 50)
bloquesDecoracion.add(nuevaNube)

nube_2= Decoracion(bloques["Nubes"][1], 500, 50)
bloquesDecoracion.add(nuevaNube)

#Árboles
arbol= Decoracion(bloques["Arbol"], 300, 350)
bloquesDecoracion.add(arbol)


#========================== Bucle principal ===========================#

while True:

    Ventana.fill(Azul)
    
    for eventos in pg.event.get():

        if eventos.type == QUIT:

            pg.quit()
            sys.exit()
            

    #Actualización de los sprites
    sprites.update()
    enemigosBasicos.update()
    bloquesSimples.update()
    bloquesDecoracion.update()
    potenciadores.update()
    bloquesBonus.update()
    nuevaTuberias.update()
    proyectiles.update()
    magos.update()


    #Dibujando sprites
    bloquesDecoracion.draw(Ventana)
    potenciadores.draw(Ventana)
    proyectiles.draw(Ventana)
    enemigosBasicos.draw(Ventana)
    magos.draw(Ventana)
    bloquesBonus.draw(Ventana)
    nuevaTuberias.draw(Ventana)
    bloquesSimples.draw(Ventana)
    sprites.draw(Ventana)


    #Mostrando texto
    mostrarTexto(Ventana, bertram, "TIME", 30, Blanco, 10, 10)
    mostrarTexto(Ventana, bertram, str(int(tiempo)), 25, Blanco, 20, 40)
    mostrarTexto(Ventana, bertram, "SCORE", 30, Blanco, 870, 10)
    mostrarTexto(Ventana, bertram, str(personajePrincipal.puntuacion).zfill(5), 25, Blanco, 900, 40)

    tiempo-=.05
    

#======================================================================================================

    #Generando proyectiles
    if personajePrincipal.generar:
        
        if personajePrincipal.numero == 0:

            nuevoProyectil= Proyectil(proyectil[0], personajePrincipal.rect.right, (personajePrincipal.rect.centery + 5))
            proyectiles.add(nuevoProyectil)
            personajePrincipal.numero+=1

        nuevoProyectil.mover(personajePrincipal)


    #Movimiento y ataque del mago    
    if personajePrincipal.rect.right >= (nuevaTuberia.rect.left - 200):

        if not nuevoMago.mover and nuevoMago.rect.y == 320:

            if nuevoMago.accion and nuevoMago.tiempo == int(tiempo):

                nuevoMago.mover= True
                nuevoMago.tiempo=0
                nuevoMago.accion=False

            elif nuevoMago.accion:

                pass

            else:

                nuevoMago.mover= True


    if nuevoMago.mover:

        if nuevoMago.rect.y >= 230:

            nuevoMago.rect.y-=3
        
        else:

           nuevoMago.atacar()
           nuevoMago.conteo+=1

    else:

        if nuevoMago.bandera:

            nuevoMago.rect.x = 905
            nuevoMago.image= enemigos["Mago"][0]

            nuevoMago.rect.y+=3

            if nuevoMago.rect.y == 320:

                nuevoMago.bandera= False
                nuevoMago.tiempo= (int(tiempo) - 5)
                nuevoMago.accion= True


#============================= Colisiones ==================================#
    

    #Creando colisión con enemigos + Muerte del enemigo
    
    Colision= pg.sprite.spritecollide(personajePrincipal, enemigosBasicos, False)

    if Colision:

     #Sí la posición en Y es menor al enemigo, significa que el personajePrincipal colisionó estando en el aire y cayendo encima del enemigo
        if personajePrincipal.Saltar or (personajePrincipal.rect.bottom < nuevoEnemigo.rect.y):


            #Si el enemigo ya está muriendo(mostrando animación de muerte) no hacemos nada
            if nuevoEnemigo.muerte:

                pass


            #Si no, eliminamos al enemigo
            else:

                personajePrincipal.puntuacion+=500
                personajePrincipal.aumento=-30
                nuevoEnemigo.muerte=True
                ahora= pg.time.get_ticks()


        else:

            #Si colisionamos con el enemigo, pero el ya está muerto, no hacemos nada
            if nuevoEnemigo.muerte:

                pass

            else:
                
                #Si el enemigo está vivo y colisiona de forma directa, destruimos el personaje
                personajePrincipal.muerte=True
                ahora=pg.time.get_ticks()



    #colisión del personaje con el mago
    colisionMago= pg.sprite.spritecollide(personajePrincipal, magos, False) 

    if colisionMago:

        if personajePrincipal.rect.bottom < nuevoMago.rect.centery:

           nuevoMago.muerte= True
           ahora= pg.time.get_ticks()


        else:

            personajePrincipal.muerte= True
            personajePrincipal.ahora= pg.time.get_ticks()



   #Condicional que se encarga del tiempo antes de morir y de destruir el objeto
    if personajePrincipal.muerte:

        personajePrincipal.tiempoDeMuerte(ahora)

        
    if nuevoEnemigo.muerte:

       nuevoEnemigo.tiempoDeMuerte(ahora) 

    
    if nuevoMago.muerte:

        nuevoMago.tiempoDeMuerte(ahora)


            
    #Colisión del personaje con el bloque bonus (left y right)

    if (personajePrincipal.rect.x + 63 >= bonus.rect.left and personajePrincipal.rect.top <= bonus.rect.bottom -3)\
       and personajePrincipal.rect.x < bonus.rect.right:
           

        personajePrincipal.rect.x= personajePrincipal.posX


    elif (personajePrincipal.rect.x <= bonus.rect.right and personajePrincipal.rect.top <= bonus.rect.bottom -3) \
         and personajePrincipal.rect.x > bonus.rect.left:

        personajePrincipal.rect.x= personajePrincipal.posX


    else:

        personajePrincipal.posX= personajePrincipal.rect.x

        
        

    #Colisión con bloque Bonus (bottom)
    colisionbonus= pg.sprite.spritecollide(personajePrincipal, bloquesBonus, False)


    if colisionbonus:

        if personajePrincipal.rect.y <= bonus.rect.bottom and personajePrincipal.rect.x + 63 > bonus.rect.left:
            
            #Esto para que al colisionar baje y no continue subiendo
            personajePrincipal.rect.y+=3
            personajePrincipal.aumento=0

            if not animacion:
                
                animacionbonus=True
                inicio= pg.time.get_ticks()
                animacion=True

            else:

                personajePrincipal.rect.y+=3


    #Animación de bonus
    if animacionbonus:

        if bonus.mover(inicio):

            animacionbonus=False
            nuevaArma= Potenciador(desarrollador["Arma"][0], bonus.rect.x, bonus.rect.top -3)
            potenciadores.add(nuevaArma)
            generacion=True


    
    #Colisión del arma con el bloque bonus
    if generacion:
        armabonus= pg.sprite.spritecollide(nuevaArma, bloquesBonus, False)

        if armabonus:

            #Evitar que el sprite traspase el bloque bonus
            if nuevaArma.rect.bottom >= bonus.rect.top:

                nuevaArma.rect.bottom = bonus.rect.top+3
                nuevaArma.caida=False 

            else: 
                nuevaArma.caida=True




    #Colisión del arma con el suelo
    if generacion:
        armaSuelo= pg.sprite.spritecollide(nuevaArma, bloquesSimples, False)

        if armaSuelo:

            if nuevaArma.rect.bottom >= sueloBasico.rect.top:
                
                nuevaArma.rect.bottom= sueloBasico.rect.top+3
                nuevaArma.caida=False
            

        else:

            nuevaArma.caida= True
    


    #Colsisión del personaje con el suelo
    colisionSuelo= pg.sprite.spritecollide(personajePrincipal, bloquesSimples, False)

    if colisionSuelo and not personajePrincipal.muerte:
 
        if personajePrincipal.rect.bottom >= sueloBasico.rect.top:

            personajePrincipal.Saltar=False
            personajePrincipal.aumento=-30
            personajePrincipal.rect.bottom= sueloBasico.rect.top+1


        #Si el personaje no está saltando ni hay colisión con el suelo, significa que está cayento
        
        else:
            
            if not personajePrincipal.Saltar:

                personajePrincipal.rect.y+=5
        


    #Colisión del enemigo con el suelo
            
    colisionSueloEnemigo= pg.sprite.spritecollide(nuevoEnemigo, bloquesSimples, False)

    if colisionSueloEnemigo:
        
        if nuevoEnemigo.rect.bottom >= sueloBasico.rect.top:

            caida=False
            nuevoEnemigo.rect.bottom = sueloBasico.rect.top+1


    else:
        caida=True



    #Colisión con potenciadores

    personajeArmas= pg.sprite.spritecollide(personajePrincipal, potenciadores, True)

    if personajeArmas:

        personajePrincipal.puntuacion+=1000
        personajePrincipal.francotirador=True
        nuevaArma.kill()


    #Colisión del enemigo con proyectil
    
    if personajePrincipal.generar:

        colisionProyectil= pg.sprite.spritecollide(nuevoProyectil, enemigosBasicos, False)

        if colisionProyectil:

            nuevoProyectil.kill() 
            personajePrincipal.generar=False
            nuevoEnemigo.kill()


    #Eliminar proyectil al salir de la pantalla
    if personajePrincipal.generar:

        nuevoProyectil.comprobarPosicion(personajePrincipal)

    

    #Colisión tubería

    colisionTuberia= pg.sprite.spritecollide(personajePrincipal, nuevaTuberias, False)

    if colisionTuberia:

        #Comprobamos si está encima de la tubería
        if personajePrincipal.rect.bottom >= nuevaTuberia.rect.top and (personajePrincipal.rect.centery - 10) < tuberia.rect.top:

            personajePrincipal.rect.bottom = nuevaTuberia.rect.top +1
            personajePrincipal.Saltar=False
            personajePrincipal.aumento= -30

        
        #Si no lo está, verificamos si ha colisionado con uno de los lados del sprite (left, right)
        else:
            
            if personajePrincipal.rect.right >= nuevaTuberia.rect.left:

                 personajePrincipal.rect.right= nuevaTuberia.rect.left
        

#========================== Movimiento de los personajes ====================================#
        
    
    #Mover personajePrincipal y enemigos

    if not personajePrincipal.muerte:
        personajePrincipal.Movimiento()

    if not nuevoEnemigo.muerte:
        nuevoEnemigo.mover()


    #Movimiento de potenciadores
    if generacion:

        if nuevaArma.mover:

            nuevaArma.moverPotenciador()

        if nuevaArma.caida:

            nuevaArma.caer()
            

#====================== Otros ============================#
        
    #Morir al salir de la pantalla
    if nuevoEnemigo.rect.x<=0:
        nuevoEnemigo.kill()


    #Gravedad del enemigo
    if nuevoEnemigo.caer:
        nuevoEnemigo.Caer()

        
    #Salto
    if personajePrincipal.Saltar:

        personajePrincipal.salto()


    #Disparar
    if personajePrincipal.ataque:

        personajePrincipal.disparar()


    Reloj.tick(Fps)
    pg.display.update()
