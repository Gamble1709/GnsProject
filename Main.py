import pygame as pg, time

from pygame.locals import *

from Sprites import Camina_Derecha, Camina_Izquierda,Saltos, Icono, Quieto, Muerte, Enemigo_1, sniperDerecha, sniperIzquierda, sniperSalto, ataqueIzquierda, ataqueDerecha, hongo, arma

from Blocks import bloqueBonus, bloqueBonus_2, suelo

from Constants import Ancho_pantalla, Alto_pantalla, Azul, Blanco

import sys



class personaje(pg.sprite.Sprite):

    def __init__(self):

        super().__init__()

        #Control de sprites
        self.pasos=0

        #Activar - Desactivar Sniper
        self.francotirador= False

        #Controla ataque
        self.ataque=False
        self.numeroImagenes=0
        self.tiempo=0

        #Controla el alto del salto
        self.aumento=-30

        self.Saltar= False

        #Dirección mientras está quieto
        self.Dir=0
        self.Estatico= Quieto[0]
        
        #Cargar imagen
        self.image= Quieto[0]

        #obtiene el rectangulo del sprite 
        self.rect= self.image.get_rect()
        
        #Coordenadas del rectangulo
        self.rect.x=50
        self.rect.y= 375

        
     

    def Movimiento(self):

        global Tecla

        #Controlar eventos del teclado
        Tecla=pg.key.get_pressed()


        #Margenes de movimiento

        if self.rect.x <=0:

            self.rect.x=1
            

        elif self.rect.x >=950:
            
            self.rect.x=950



        #Movimiento

        if Tecla[K_d]:

            #Evitar movimiento mientras se ejecute el salto
            if self.Saltar:
                pass


            #Salto combinado
            elif Tecla[K_d] and Tecla[K_w]:

                self.rect.x+=2
                self.Saltar=True


            #Evitar movimiento mientras dispara

            if self.ataque:

                pass
            
            
            #Caminar derecha 
            else:

                self.rect.x +=10
                
                if self.pasos >4:

                    self.pasos=0
                    

                if self.francotirador:

                    self.image= sniperDerecha[self.pasos]

                    self.pasos+=1

                    self.Dir=0


                else:
                    
                    self.image= Camina_Derecha[self.pasos]

                    self.pasos+=1

                    self.Dir=0



        #izquierda

        elif Tecla[K_a]:

            #Evitar movimiento mientras se ejecute el salto
            if self.Saltar:
                pass

            
            #Salto combinado
            elif Tecla[K_a] and Tecla[K_w]:

                self.rect.x-=2
                self.Saltar=True


            #Evitar movimiento mientras dispara
            if self.ataque:

                pass
            

            #Caminar Izquierda
            else:
                
                self.rect.x -=10

     
                if self.pasos > 4:
                    
                    self.pasos=0


                if self.francotirador:

                    self.image= sniperIzquierda[self.pasos]

                    self.pasos+=1

                    self.Dir=1

                
                else:
                    self.image= Camina_Izquierda[self.pasos]

                    self.pasos+=1

                    self.Dir=1



        #Activar salto
        elif Tecla[K_w]:

            self.Saltar= True


                 
        #Quieto
        else:

            if self.francotirador:

                if self.Dir == 0:

                    self.image= sniperDerecha[self.Dir]


                else:

                    self.image= sniperIzquierda[self.Dir-1]


            else:
                
                self.image= Quieto[self.Dir]




        #Ataque
        if Tecla[K_SPACE]:

            if self.francotirador:

                #Activamos ataque
                self.ataque=True


        
    def salto(self):

        #Restamos a la posición Y el aumento
        self.rect.y+= self.aumento


        #Dibujamos el salto
        if self.francotirador:

            self.image= sniperSalto[self.Dir]


        else:
            
            self.image= Saltos[self.Dir]
            

        #Aplicamos gravedad
        self.aumento+=3


        #Mover a la derecha durante el salto
        if Tecla[K_d]:
            self.rect.x+=2
            self.Dir=0

        #Mover a la izquierda durante el salto
        elif Tecla[K_a]:
            self.rect.x-=2
            self.Dir=1

            
            personajePrincipal.Dir=1
            



    def disparar(self):

        #Controlar número de imagenes
        if self.numeroImagenes > 2:

            self.numeroImagenes=0

            if self.Dir==0:
                
                self.image= sniperDerecha[0]

            else:

                self.image= sniperIzquierda[0]
                
                
            self.ataque=False



        else:
            
            #Dirección
            if self.Dir == 0:

                self.image= ataqueDerecha[self.numeroImagenes]
                self.tiempo+=1


            else:

                self.image= ataqueIzquierda[self.numeroImagenes]
                self.tiempo+=1

                
        if self.tiempo == 5:

            self.numeroImagenes+=1
            self.tiempo=0
            

        
    

#Clase para los enemigos
class Enemigo(pg.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.caida=3
        self.Pasos=0
        self.image= Enemigo_1[self.Pasos]
        self.rect= self.image.get_rect()

        #controlar rebote por velocidad
        self.Velocidad=3

        #controlar tiempo de cambio entre sprites
        self.Contador=0


    def Posicion(self, X, Y):

        self.rect.x =X
        self.rect.y =Y


    def Mover(self):
        
        self.rect.x-= self.Velocidad
        self.image= Enemigo_1[self.Pasos]

        self.Contador+=1

        if self.Contador ==10:
            self.Pasos+=1
            self.Contador=0

        if self.Pasos >1:
            self.Pasos=0

        """Si se desea usar rebote

        if self.rect.x < 0:
            self.Velocidad=-3


        elif self.rect.x > 950:
            self.Velocidad=3

        """


    def Caer(self):

        self.rect.y+= self.caida



        

#Clase para los bloques
class Bloque(pg.sprite.Sprite):

    def __init__(self, X, Y, imagen):

        super().__init__()

        #Asignando imagen
        self.image= imagen

        #Obteniendo cuadrado del sprite
        self.rect= self.image.get_rect()

        #Posición
        self.rect.x= X
        self.rect.y= Y




#Clase para los elementos de decoración
class Decoracion(Bloque):

    def __init__(self, posx, posy, imagen):

        super().__init__(posx,posy, imagen)




#Clase para los potenciadores
class Potenciador(Bloque):
    

    def __init__(self, x, y, imagen):
    
        super().__init__(x,y,imagen)

        #Movimiento
        self.mover=False

        #Caída
        self.caida=False


    def moverPotenciador(self):

        self.rect.x+=2


    def caer(self):

        self.rect.y+=5


    def potenciar(self, personaje ,imagenPersonaje):

        personaje.image= imagenPersonaje

        
#=================== Salimos de las clases ========================#

        
#Iniciando Pygame
if __name__=="__main__":

    pg.init()



#Creación de ventana + ícono de la misma
Ventana=pg.display.set_mode((Ancho_pantalla, Alto_pantalla))
pg.display.set_icon(Icono)
    

#FPS
Fps=30
Reloj= pg.time.Clock()



#grupos de Sprites
sprites= pg.sprite.Group()
enemigosBasicos= pg.sprite.Group()
bloquesBonus= pg.sprite.Group()
bloquesSimples= pg.sprite.Group()
bloquesDecoracion= pg.sprite.Group()
potenciadores= pg.sprite.Group()


#Instanciando Enemigo + posición
primerEnemigo= Enemigo()
primerEnemigo.Posicion(700, 395)
enemigosBasicos.add(primerEnemigo)

#Instanciando personajePrincipalPrincipal principal
personajePrincipal=personaje()
sprites.add(personajePrincipal)


#Instanciando Bloques
Bonus= Bloque(600, 275, bloqueBonus)
bloquesBonus.add(Bonus)


#Instanciación de los potenciadores

hongos= Potenciador(Bonus.rect.x, Bonus.rect.y -3, hongo)
armas= Potenciador(Bonus.rect.x, Bonus.rect.y -3, arma)


#Crear animación de subida y bajado
animacionBonus=False
subir=-8


#Creando bloques en orden
distanciaX=0
distanciaY=435

for x in range(75):
    sueloBasico= Bloque(distanciaX, distanciaY, suelo)
    bloquesSimples.add(sueloBasico)
    distanciaX+=45


#Creación de bloques vacíos (solo por decoración)

distanciaX=0
distanciaY+=23
cont=0

for x in range(80):
    
    bloque=Decoracion(distanciaX, distanciaY,suelo)
    bloquesDecoracion.add(bloque)

    distanciaX+=25
    cont+=1

    if cont==40:

        distanciaY+=23
        distanciaX=0



#Muerte de enemigo
Contar=False
Contador=0
Continua=False
Mover=True
Bajar=True

#Gravedad del enemigo
caida=True

#Muerte del personajePrincipal principal
Muerte_personajePrincipal=False
Mover_personajePrincipal=True
contar=False



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


    #Dibujando sprites
    enemigosBasicos.draw(Ventana)
    sprites.draw(Ventana)
    bloquesBonus.draw(Ventana)
    bloquesSimples.draw(Ventana)
    bloquesDecoracion.draw(Ventana)
    potenciadores.draw(Ventana)


#============================= Colisiones ==================================# 

    #Creando colisión con enemigos + Muerte del enemigo
    
    Colision= pg.sprite.spritecollide(personajePrincipal, enemigosBasicos, False)

    if Colision:

        #Sí la posición en Y es menor al enemigo, significa que el personajePrincipal colisionó estando en el aire y cayendo encima del enemigo
        if personajePrincipal.Saltar or (personajePrincipal.rect.y + 20 < primerEnemigo.rect.y):

            personajePrincipal.aumento=-30
            primerEnemigo.Velocidad=0
            primerEnemigo.image=Enemigo_1[2]
            Mover=False
            Continua=True
         
            

        else:
            
            Mover_personajePrincipal=False
            Muerte_personajePrincipal=True
            Contar=True


        
    if Continua:

        enemigosBasicos.draw(Ventana)
        Contar=True

        #Tiempo que se mostrará la imagen antes de eliminar el objeto
        if Contar:
            Contador+=1

            if Contador >=50:
                
                primerEnemigo.kill()
                Contador=0
                Continua=False



    #Mostrar muerte, aunque colisione con un objeto
    if Muerte_personajePrincipal or (Muerte_personajePrincipal and colisionSuelo):

        personajePrincipal.image=Muerte
        sprites.draw(Ventana)

        #Tiempo que se mostrará la imagen antes de eliminar el objeto
        if Contar:
            
            Contador+=1

            if Contador >=50:

                personajePrincipal.kill()
                Contador=0
        


    #Colisión con bloque bonus
    Colision_bonus= pg.sprite.spritecollide(personajePrincipal, bloquesBonus, False)

    if Colision_bonus:

        if personajePrincipal.rect.top <= Bonus.rect.bottom:
            
            #Esto para que al colisionar baje y no continue subiendo
            personajePrincipal.aumento=0

            animacionBonus=True



    #Animación de Bonus
    if animacionBonus:

        Bonus.rect.y+=subir
        subir+=1

        if subir == 8:
            
            Bonus.image= bloqueBonus_2
            animacionBonus=False
            subir=-8

            potenciadores.add(armas)
            armas.mover=True
            armas.caida=True
            



    #Colisión del arma con el bloque bonus
    armaBonus= pg.sprite.spritecollide(armas, bloquesBonus, False)

    if armaBonus:

        #Evitar que el sprite traspase el bloque bonus
        if armas.rect.bottom >= Bonus.rect.top:

            armas.rect.bottom = Bonus.rect.top+3
            armas.caida=False

    else:

        armas.caida=True




    #Colisión del arma con el suelo
    armaSuelo= pg.sprite.spritecollide(armas, bloquesSimples, False)

    if armaSuelo:

        if armas.rect.bottom >= sueloBasico.rect.top:
            
            armas.rect.bottom= sueloBasico.rect.top+3
            armas.caida=False
        

    else:

        armas.caida= True
    


    #Colsisión con el suelo
    colisionSuelo= pg.sprite.spritecollide(personajePrincipal, bloquesSimples, False)

    if colisionSuelo:

        if personajePrincipal.rect.bottom >= sueloBasico.rect.top:

            personajePrincipal.Saltar=False
            personajePrincipal.aumento=-30
            personajePrincipal.rect.bottom= sueloBasico.rect.top+3


    else:

        #Si el personaje no está saltando ni hay colisión con el suelo, significa que está cayento
        
        if not personajePrincipal.Saltar:

            personajePrincipal.rect.y+=5
        


    #Colisión del enemigo con el suelo
            
    colisionSueloEnemigo= pg.sprite.spritecollide(primerEnemigo, bloquesSimples, False)

    if colisionSueloEnemigo:
        
        if primerEnemigo.rect.bottom >= sueloBasico.rect.top:

            caida=False
            primerEnemigo.rect.bottom = sueloBasico.rect.top+3


    else:
        caida=True



    #Colisión con potenciadores

    personajeArmas= pg.sprite.spritecollide(personajePrincipal, potenciadores, False)

    if personajeArmas:

        personajePrincipal.francotirador=True
        armas.kill()



#========================== Movimiento de los personajes ====================================#
        
    
    #Mover personajePrincipal y enemigos

    if Mover_personajePrincipal:
        personajePrincipal.Movimiento()

    if Mover:
        primerEnemigo.Mover()


    #Movimiento de potenciadores
    if armas.mover:

        armas.moverPotenciador()

    if armas.caida:

        armas.caer()
        



#====================== Otros ============================#
        
    #Morir al salir de la pantalla
    if primerEnemigo.rect.x<=0:
        primerEnemigo.kill()


    #Gravedad del enemigo
    if caida:
        primerEnemigo.Caer()

        
    #Salto
    if personajePrincipal.Saltar:

        personajePrincipal.salto()


    #Disparar
    if personajePrincipal.ataque:

        personajePrincipal.disparar()
        

    Reloj.tick(Fps)
    pg.display.update()
