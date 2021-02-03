import pygame as pg, time, sys, Collisions

from pygame.locals import *

from Class import *

from Sprites import Icono, proyectil, desarrollador, enemigos 

from Blocks import  bloques 

from Constants import ANCHO_PANTALLA, ALTO_PANTALLA, AZUL, BLANCO, ROJO, POSICIONES_LINEAS, bertram

from Sounds import *

from Functions import mostrarTexto, mostrarMenu, moverCamara 


#Iniciando Pygame
if __name__=="__main__":

    pg.init()


#Creación de ventana + ícono de la misma
VENTANA= pg.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pg.display.set_icon(Icono)
    

#FPS
Fps= 30
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
distanciaX= 0

#el ancho de la image es 46, lo usaremos para calcular la distancia entre bloques
for x in range(75):

    sueloBasico= Bloque(bloques["Suelo"], 46 * x, 447)     
    bloquesSimples.add(sueloBasico)
    distanciaX+= 45

#Creación de bloques vacíos (solo por decoración)

distanciaX= 0
distanciaY= 470

for x in range(150):
    
    bloque= Decoracion(bloques["Suelo"], distanciaX, distanciaY)
    bloquesDecoracion.add(bloque)

    distanciaX+= 46

    if x == 75:

        distanciaY+= 23
        distanciaX= 0



#Tuberías
nuevaTuberia= Bloque(bloques["Tuberia"], 900, 310)
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
personajePrincipal= Personaje()
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

#Crear animación de subida y bajada bloque bonus (Pronto se pondrá en la clase para borrar este espacio)

#Iniciar Menú
while not mostrarMenu(VENTANA):

    mostrarMenu(VENTANA)
    Reloj.tick(Fps)
    pg.display.update()



#Iniciar música de fondo
#pg.mixer.music.play()


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
    magos.update(personajePrincipal)


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

    tiempo-= .05

#======================================================================================================

    
    #"Movimiento" de la cámara
    if personajePrincipal.rect.x >= (ANCHO_PANTALLA / 2):

        moverCamara([goombas, magos, caracoles, tuberias, bloquesSimples, bloquesDecoracion,
            potenciadores, bloquesBonus], personajePrincipal) 

    #Si no está la cámara en "movimiento" cambiamos este atributo, si se quita el jugador no se moverá
    else: 

        if personajePrincipal.camara: personajePrincipal.camara= False


    #Generando proyectiles

    #Vericamos que el que ataque del personaje haya terminado y que esté listo para generar un proyectil
    if personajePrincipal.generar and not personajePrincipal.activo:
        
        #Hacemos que sea verdadero para saber que ek ataque ha iniciado
        personajePrincipal.activo= True

        #Indicamos que ya no puede generar otro proyectil hasta que acabe el ataque
        personajePrincipal.generar= False
        
        #Instanciamos el nuevo proyectil
        nuevoProyectil= Proyectil(personajePrincipal)

        #Lo agregamos a su grupo correspondiente
        proyectiles.add(nuevoProyectil)

            
#============================= Colisiones ==================================#
    
    #Método que se encarga de detectar todas las colisiones 
    Collisions.detectarColisiones(personajePrincipal, goombas, caracoles, magos, bloquesSimples, tuberias,
            bloquesBonus, potenciadores, proyectiles)



    #Dibuja un cuadrado alrededor del caracol (usado para hacer pruebas debido a un bug que aún está)
    
    """if caracoles:

        pg.draw.rect(VENTANA, ROJO, (caracoles.sprites()[0].rect.x + caracoles.sprites()[0].rect.w, caracoles.sprites()[0].rect.y, caracoles.sprites()[0].rect.w, caracoles.sprites()[0].rect.h))"""
        
    

        
#================================= Instanciación de otros objetos ===============================

    #Detecta si se activó la generación de un power up y lo instancia
    for bonus in bloquesBonus:

        if bonus.generar:

            nuevaArma= Potenciador(pg.transform.scale(desarrollador["Arma"][0], (50,14)), 
                    bonus.rect.x - 6, bonus.rect.top -3)

            potenciadores.add(nuevaArma)
            bonus.generar= False 



    #Detecta si el mago invocó a un nuevo caracol y lo instancia
    if nuevoMago.invocar:
        
        nuevoCaracol= Prueba(personajePrincipal.rect.x - 200, sueloBasico.rect.top - 28)
        caracoles.add(nuevoCaracol)


#====================== Otros ============================#

    #Verificamos sí el jugador está cayendo
    if not personajePrincipal.saltar and not Collisions.colisionBonus and not Collisions.colisionSuelo and not Collisions.colisionTuberia:

        personajePrincipal.saltar = True

        #A esta variable cuando ejecutamos el salto comenzamos a restarle, si está en 0 los valores serán
        #negativos y hará que el personaje caiga
        personajePrincipal.aumento=0
        


    Reloj.tick(Fps)
    pg.display.update()
