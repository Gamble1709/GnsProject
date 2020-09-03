import pygame as pg, time

from pygame.locals import *

from Sprites import Camina_Derecha, Camina_Izquierda,Saltos, Icono, Quieto, Muerte, Enemigo_1

from Blocks import bloqueBonus, bloqueBonus_2, suelo

from Constants import Ancho_pantalla, Alto_pantalla, Azul, Blanco

import sys



class personaje(pg.sprite.Sprite):

    def __init__(self):

        super().__init__()

        #Control de sprites
        self.pasos=0

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

                self.rect.x+=10
                self.Saltar=True


            #Caminar derecha 
            else:

                self.rect.x +=10
                

                if self.pasos >4:

                    self.pasos=0

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

                self.rect.x-=10
                self.Saltar=True


            #Caminar derecha
            else:
                
                self.rect.x -=10
                

                if self.pasos > 4:
                    
                    self.pasos=0

                self.image= Camina_Izquierda[self.pasos]

                self.pasos+=1

                self.Dir=1



        #Activar salto
        elif Tecla[K_w]:

            self.Saltar= True

                 
        #Quieto
        else:
            self.image= Quieto[self.Dir]






class Enemigo(pg.sprite.Sprite):

    def __init__(self):

        super().__init__()

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
        
        
   

if __name__=="__main__":

    pg.init()

    

#FPS
Fps=30
Reloj= pg.time.Clock()



#grupos de Sprites
sprites= pg.sprite.Group()
enemigosBasicos= pg.sprite.Group()
bloquesBonus= pg.sprite.Group()
bloquesSimples= pg.sprite.Group()


#Instanciando Enemigo + posición
Enemigo_Basico= Enemigo()
Enemigo_Basico.Posicion(700, 395)
enemigosBasicos.add(Enemigo_Basico)

#Instanciando personajePrincipalPrincipal principal
personajePrincipal=personaje()
sprites.add(personajePrincipal)
N=0


#Instanciando Bloques
Bonus= Bloque(600, 275, bloqueBonus)
bloquesBonus.add(Bonus)


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

distanciaX=0

cont=0
#Creación de bloques vacíos (solo por decoración)

for x in range(50):
    sueloBasico= Bloque(distanciaX, distanciaY, suelo)
    distanciaX+=45

    if cont == 25:

        distanciaX=0
        distanciaY+=25


#Creación de ventana + ícono de la misma
Ventana=pg.display.set_mode((Ancho_pantalla, Alto_pantalla))
pg.display.set_icon(Icono)



#Muerte de enemigo
Contar=False
Contador=0
Continua=False
Mover=True
Bajar=True



#Muerte del personajePrincipal principal
Muerte_personajePrincipal=False
Mover_personajePrincipal=True
contar=False


#Bucle principal
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


    #Dibujando sprites
    enemigosBasicos.draw(Ventana)
    sprites.draw(Ventana)
    bloquesBonus.draw(Ventana)
    bloquesSimples.draw(Ventana)



    #Creando colisión con enemigos
    
    Colision= pg.sprite.spritecollide(personajePrincipal, enemigosBasicos, False)

    if Colision:

        #Sí la posición en Y es menor al enemigo, significa que el personajePrincipal colisionó estando en el aire y cayendo encima del enemigo
        if personajePrincipal.Saltar or (personajePrincipal.rect.y + 20 < Enemigo_Basico.rect.y):

            personajePrincipal.aumento=-30
            Enemigo_Basico.Velocidad=0
            Enemigo_Basico.image=Enemigo_1[2]
            Mover=False
            Continua=True

            if Bajar:
                for x in range(0,5):
                    Enemigo_Basico.rect.y+=3

                Bajar=False



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
                Enemigo_Basico.kill()
                Contador=0



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

    colisionSuelo= pg.sprite.spritecollide(personajePrincipal, bloquesSimples, False)


    if animacionBonus:

        Bonus.rect.y+=subir
        subir+=1

        if subir == 8:
            
            Bonus.image= bloqueBonus_2
            animacionBonus=False
            subir=-8
    
    #Colsisión con el suelo
    if colisionSuelo:

        if personajePrincipal.rect.bottom >= sueloBasico.rect.top:

            personajePrincipal.Saltar=False
            personajePrincipal.aumento=-30
            personajePrincipal.rect.bottom= sueloBasico.rect.top+3


    else:

        if not personajePrincipal.Saltar:

            personajePrincipal.rect.y+=5
        


    #Mover personajePrincipal y enemigos

    if Mover_personajePrincipal:
        personajePrincipal.Movimiento()

    if Mover:
        Enemigo_Basico.Mover()

    #Morir al salir de la pantalla
    if Enemigo_Basico.rect.x<=0:
        Enemigo_Basico.kill()


    #Salto
    if personajePrincipal.Saltar:
                
        personajePrincipal.rect.y+=personajePrincipal.aumento
        personajePrincipal.image= Saltos[N]
        personajePrincipal.aumento+=3


        #Mover a la derecha durante el salto
        if Tecla[K_d]:
            personajePrincipal.rect.x+=10
            N=1

            personajePrincipal.Dir=0

        #Mover a la izquierda durante el salto
        elif Tecla[K_a]:
            personajePrincipal.rect.x-=10
            N=0

            
            personajePrincipal.Dir=1



    Reloj.tick(Fps)
    pg.display.update()
