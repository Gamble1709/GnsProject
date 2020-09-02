import pygame as pg, time

from pygame.locals import *

from Sprites import Camina_Derecha, Camina_Izquierda,Saltos, Icono, Quieto, Muerte, Enemigo_1

from Blocks import Bloque_Bonus

from Constants import Ancho_pantalla, Alto_pantalla, Azul, Blanco

import sys



class Personajes(pg.sprite.Sprite):

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






class Enemigos(pg.sprite.Sprite):

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



class Bloques(pg.sprite.Sprite):

    def __init__(self, X, Y):

        super().__init__()

        #Asignando imagen
        self.image= Bloque_Bonus

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



#Sprites
sprites= pg.sprite.Group()
Enemigos_group= pg.sprite.Group()
Bonus_group= pg.sprite .Group()



#Instanciando Enemigo + posición
Enemigo_Basico= Enemigos()
Enemigo_Basico.Posicion(700, 395)
Enemigos_group.add(Enemigo_Basico)

#Instanciando personaje principal
Personaje=Personajes()
sprites.add(Personaje)
N=0

#Instanciando Bloques
Bonus= Bloques(600, 275)
Bonus_group.add(Bonus)



#Creación de ventana + ícono de la misma
Ventana=pg.display.set_mode((Ancho_pantalla, Alto_pantalla))
pg.display.set_icon(Icono)



#Muerte de enemigo
Contar=False
Contador=0
Continua=False
Mover=True
Bajar=True



#Muerte del personaje principal
Muerte_Personaje=False
Mover_Personaje=True
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
    Enemigos_group.update()


    #Dibujando sprites
    Enemigos_group.draw(Ventana)
    sprites.draw(Ventana)
    Bonus_group.draw(Ventana)


    #Creando colisión con enemigos
    
    Colision= pg.sprite.spritecollide(Personaje, Enemigos_group, False)

    if Colision:

        #Sí la posición en Y es menor al enemigo, significa que el personaje colisionó estando en el aire y cayendo encima del enemigo
        if Personaje.Saltar or (Personaje.rect.y + 20 < Enemigo_Basico.rect.y):

            Enemigo_Basico.Velocidad=0
            Enemigo_Basico.image=Enemigo_1[2]
            Mover=False
            Continua=True

            if Bajar:
                for x in range(0,5):
                    Enemigo_Basico.rect.y+=3

                Bajar=False



        else:

            Mover_Personaje=False
            Muerte_Personaje=True
            Contar=True

        
    if Continua:
        
        Enemigos_group.draw(Ventana)
        Contar=True

        #Tiempo que se mostrará la imagen antes de eliminar el objeto
        if Contar:
            Contador+=1

            if Contador >=50:
                Enemigo_Basico.kill()
                Muerte=False
                Contador=0



    if Muerte_Personaje:

        Personaje.image=Muerte
        sprites.draw(Ventana)

        #Tiempo que se mostrará la imagen antes de eliminar el objeto
        if Contar:
            
            Contador+=1

            if Contador >=50:

                Personaje.kill()
                Contador=0
        


    Colision_bonus= pg.sprite.spritecollide(Personaje, Bonus_group, False)

    if Colision_bonus:

        if Personaje.rect.top == Bonus.rect.bottom:

            Bonus.rect.y-=10
        

    #Mover personaje y enemigos

    if Mover_Personaje:
        Personaje.Movimiento()

    if Mover:
        Enemigo_Basico.Mover()

    #Morir al salir de la pantalla
    if Enemigo_Basico.rect.x<=0:
        Enemigo_Basico.kill()


    #Salto
    if Personaje.Saltar:
                
        Personaje.rect.y+=Personaje.aumento
        Personaje.image= Saltos[N]
        Personaje.aumento+=3


        #Mover a la derecha durante el salto
        if Tecla[K_d]:
            Personaje.rect.x+=10
            N=1

            Personaje.Dir=0

        #Mover a la izquierda durante el salto
        elif Tecla[K_a]:
            Personaje.rect.x-=10
            N=0

            
            Personaje.Dir=1

        #límite de caída
        if Personaje.aumento >= 33:
            Personaje.Saltar=False
            Personaje.aumento=-30


    Reloj.tick(Fps)
    pg.display.update()



