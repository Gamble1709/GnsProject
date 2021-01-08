import pygame as pg, time, sys, Collisions

from pygame.locals import *

from Class import *

from Sprites import Icono, proyectil, desarrollador, enemigos 

from Blocks import  bloques 

from Constants import ANCHO_PANTALLA, ALTO_PANTALLA, AZUL, BLANCO, ROJO, POSICIONES_LINEAS, bertram

from Sounds import *

from Functions import mostrarTexto, mostrarMenu 


#Iniciando Pygame
if __name__=="__main__":

    pg.init()


#Creación de ventana + ícono de la misma
VENTANA=pg.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pg.display.set_icon(Icono)
    

#FPS
Fps=30
Reloj= pg.time.Clock()

#Tiempo del juego
tiempo= 500

#grupos de Sprites
sprites= pg.sprite.Group()
goombas= pg.sprite.Group()
magos= pg.sprite.Group()
caracoles= pg.sprite.Group()
bloquesBonus= pg.sprite.Group()
bloquesSimples= pg.sprite.Group()
bloquesDecoracion= pg.sprite.Group()
tuberias= pg.sprite.Group()
potenciadores= pg.sprite.Group()
proyectiles= pg.sprite.Group()


#======================Instanciaciones==========================00

#Creando bloques en orden
distanciaX=0
distanciaY=447

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
tuberias.add(nuevaTuberia)

#Montañas
nuevaMontania= Decoracion(bloques["Montanias"][0], 100, 407)
bloquesDecoracion.add(nuevaMontania)

nuevaMontania= Decoracion(bloques["Montanias"][1], nuevaMontania.rect.right, 372 )
bloquesDecoracion.add(nuevaMontania)

#Nubes
nuevaNube= Decoracion(bloques["Nubes"][0], 300, 150)
bloquesDecoracion.add(nuevaNube)

nuevaNube= Decoracion(bloques["Nubes"][1], 500, 150)
bloquesDecoracion.add(nuevaNube)

#Árboles
arbol= Decoracion(bloques["Arbol"], 300, 350)
bloquesDecoracion.add(arbol)



#Instanciando personajePrincipalPrincipal principal
personajePrincipal=personaje()
sprites.add(personajePrincipal)


#Instanciación de enemigos    
nuevoEnemigo= Enemigo(700, 395)
goombas.add(nuevoEnemigo)


#Magos
nuevoMago= Mago(nuevaTuberia.rect.left + 13, 352)
magos.add(nuevoMago)


#Instanciando Bloques
bonus= Bonus(bloques["Bonus"][0], 600, 287)
bloquesBonus.add(bonus)

#Instanciación de los potenciadores
#hongos= Potenciador(desarrollador["Hongo"][0], bonus.rect.x, bonus.rect.y -3)
generacion=False


#Crear animación de subida y bajada bloque bonus (Pronto se pondrá en la clase para borrar este espacio)
animacionbonus=False
subir=-8
animacion=False


#Iniciar Menú
while not mostrarMenu(VENTANA):

    mostrarMenu(VENTANA)
    Reloj.tick(Fps)
    pg.display.update()



#Iniciar música de fondo
pg.mixer.music.play()


#========================== Bucle principal ===========================#

while True:

    VENTANA.fill(AZUL)
    
    for eventos in pg.event.get():

        if eventos.type == QUIT:

            pg.quit()
            sys.exit()
            

    #Actualización de los sprites
    sprites.update()
    goombas.update()
    bloquesSimples.update()
    bloquesDecoracion.update()
    potenciadores.update()
    bloquesBonus.update()
    tuberias.update()
    proyectiles.update(personajePrincipal)
    magos.update()
    caracoles.update(personajePrincipal)


    #Dibujando sprites
    bloquesDecoracion.draw(VENTANA)
    potenciadores.draw(VENTANA)
    proyectiles.draw(VENTANA)
    goombas.draw(VENTANA)
    magos.draw(VENTANA)
    bloquesBonus.draw(VENTANA)
    tuberias.draw(VENTANA)
    bloquesSimples.draw(VENTANA)
    sprites.draw(VENTANA)
    caracoles.draw(VENTANA)


    #Mostrando texto
    pg.draw.rect(VENTANA,(0,0,0), (350,5,325,53))

    for x in range(4):

        pg.draw.line(VENTANA, ROJO, (POSICIONES_LINEAS[x][0], POSICIONES_LINEAS[x][1]), ( POSICIONES_LINEAS[x][2], POSICIONES_LINEAS[x][3]), 3)

    mostrarTexto(VENTANA, bertram, "TIME", 25, BLANCO, 370, 23)
    mostrarTexto(VENTANA, bertram, str(int(tiempo)), 25, BLANCO, 430, 23)
    mostrarTexto(VENTANA, bertram, "SCORE", 25, BLANCO, 525, 23)
    mostrarTexto(VENTANA, bertram, str(personajePrincipal.puntuacion).zfill(5), 25, BLANCO, 605, 23)

    tiempo-=.05

#======================================================================================================

    #Generando proyectiles
    if personajePrincipal.generar and personajePrincipal.activo == False:
        
        personajePrincipal.activo= True
        personajePrincipal.generar= False
        
        nuevoProyectil= Proyectil(personajePrincipal.rect.right, personajePrincipal.rect.centery + 5)

        #Hacemos que la variable nuevoProyectil del archivo Collisions contenga el objeto creado, esto para las colisiones
        Collisions.nuevoProyectil= nuevoProyectil

        proyectiles.add(nuevoProyectil)

        #Controla la dirección del proyectil 
        if personajePrincipal.Dir == 0:

            nuevoProyectil.dir= 20

        else:

            nuevoProyectil.dir= -20

    

    #Movimiento y ataque del mago    
    if personajePrincipal.rect.right >= (nuevaTuberia.rect.left - 200) and not personajePrincipal.muerte:

        if (nuevoMago.rect.y == 352 and nuevoMago.comprobarMovimiento()) and not nuevoMago.muerte:

            nuevoMago.inicio= pg.time.get_ticks()
            nuevoMago.movimiento= True



            
#============================= Colisiones ==================================#
    
    Collisions.detectarColisiones(personajePrincipal, goombas, caracoles, magos, bloquesSimples, tuberias,
            bloquesBonus)
    


    #Colisión con Bloque bonus            
    """colisionBonus= pg.sprite.spritecollide(personajePrincipal, bloquesBonus, False)

    if colisionBonus:

        if personajePrincipal.rect.right < bonus.rect.centerx and personajePrincipal.rect.top < bonus.rect.centery + 5:

            personajePrincipal.rect.right= bonus.rect.left

        if personajePrincipal.rect.left > bonus.rect.centerx and personajePrincipal.rect.top < bonus.rect.centery - 5:

            personajePrincipal.rect.left= bonus.rect.right

        if personajePrincipal.rect.top > bonus.rect.centery :

            #Esto para que al colisionar baje y no continue subiendo
            personajePrincipal.rect.y += 10
            personajePrincipal.aumento=0

            if not bonus.animacion and not bonus.activado:
                
                bonus.animacion=True
                bonus.activado= True
                inicio= pg.time.get_ticks()

        if personajePrincipal.rect.bottom < bonus.rect.centery - 8:

            personajePrincipal.saltar=False
            personajePrincipal.rect.bottom=bonus.rect.top + 1
            personajePrincipal.aumento= -30
            """
        
    
    for bonus in bloquesBonus:

        if bonus.generar:

            nuevaArma= Potenciador(pg.transform.scale(desarrollador["Arma"][0], (50,14)), 
                    bonus.rect.x - 6, bonus.rect.top -3)

            potenciadores.add(nuevaArma)
            bonus.generar= False 



    if potenciadores:
    
        for arma in potenciadores:

            #Colisión del arma con el bloque bonus
            armaBonus= pg.sprite.spritecollide(arma, bloquesBonus, False)

            if armaBonus:

                #Evitar que el sprite traspase el bloque bonus
                if arma.rect.bottom >= armaBonus[0].rect.top:

                    arma.rect.bottom = armaBonus[0].rect.top+3
                    arma.caida=False 



            #Si no hay colision es que el objeto está cayendo
            else: 
                    
                arma.caida=True


            #Colisión del arma con el suelo
            armaSuelo= pg.sprite.spritecollide(arma, bloquesSimples, False)

            #Si hay colisión del arma con el suelo
            if armaSuelo:

                #Si la posición del arma en Y es mayor a la del bloque, la cambiamos para que no traspase el bloque
                if arma.rect.bottom >= armaSuelo[0].rect.top:
                
                    arma.rect.bottom= armaSuelo[0].rect.top+3
                    arma.caida=False

            else:

                arma.caida= True
    

    #Colisión del enemigo con el suelo
    colisionSueloEnemigo= pg.sprite.spritecollide(nuevoEnemigo, bloquesSimples, False)

    if colisionSueloEnemigo:
        
        if nuevoEnemigo.rect.bottom >= sueloBasico.rect.top:

            nuevoEnemigo.caer=False 
            nuevoEnemigo.rect.bottom = sueloBasico.rect.top+1


    else:

        nuevoEnemigo.caer=True


    #Colisión con potenciadores
    personajeArmas= pg.sprite.spritecollide(personajePrincipal, potenciadores, True)

    if personajeArmas:

        personajePrincipal.puntuacion+=1000
        personajePrincipal.francotirador=True
        nuevaArma.kill()



    #Colisión tubería
    colisionTuberia= pg.sprite.spritecollide(personajePrincipal, tuberias, False)

    if colisionTuberia:

        #Comprobamos si está encima de la tubería
        if personajePrincipal.rect.bottom < nuevaTuberia.rect.centery - 10:

            personajePrincipal.rect.bottom = nuevaTuberia.rect.top +1
            personajePrincipal.saltar=False
            personajePrincipal.aumento= -30

        
        #Si no lo está, verificamos si ha colisionado con uno de los lados del sprite (left, right)
        else:
            
            if personajePrincipal.rect.right >= nuevaTuberia.rect.left:

                 personajePrincipal.rect.right= nuevaTuberia.rect.left
        

    if nuevoMago.invocar:
        
        nuevoCaracol= Caracol(400, sueloBasico.rect.top, personajePrincipal)
        caracoles.add(nuevoCaracol)

    try:

        nuevoCaracol.comprobar(personajePrincipal)

    except:

        pass


#========================== Movimiento de los personajes ====================================#
        
    if nuevoMago.movimiento:
        nuevoMago.mover()

    #Movimiento de potenciadores
    if generacion:

        if nuevaArma.mover:

            nuevaArma.moverPotenciador()

        if nuevaArma.caida:

            nuevaArma.caer()
            

#====================== Otros ============================#

    if not personajePrincipal.saltar and not Collisions.colisionBonus and not Collisions.colisionSuelo and not colisionTuberia:

        personajePrincipal.saltar = True
        personajePrincipal.aumento=0
        


    Reloj.tick(Fps)
    pg.display.update()

    
