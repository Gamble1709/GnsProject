import pygame as pg

from pygame.locals import *

from Sprites import movimiento


class personaje(pg.sprite.Sprite):

    def __init__(self):

        super().__init__()

        #Control de sprites
        self.pasos=0

        #control del colisión con bloque bonus
        self.posX=0

        #Puntuación
        self.puntuacion=0

        #Activar - Desactivar Sniper
        self.francotirador= False

        #Controla ataque
        self.ataque=False
        self.numeroImagenes=0
        self.tiempo=0

        #Cuando se crea un proyectil se activa
        self.generar=False
        self.numero=0

        #Controla el alto del salto
        self.aumento=-30

        self.Saltar= False

        #Controlar velocidad mientras salta
        self.velocidad=2

        #Dirección mientras está quieto
        self.Dir=0
        self.Estatico= movimiento["Quieto"][0]

        #Controlar muerte
        self.muerte=False
 
        #Cargar imagen
        self.image= movimiento["Quieto"][0]

        #obtiene el rectangulo del sprite 
        self.rect= self.image.get_rect()
        
        #Coordenadas del rectangulo
        self.rect.x=50
        self.rect.y= 379


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
                
                if self.pasos >3:

                    self.pasos=0
                    

                if self.francotirador:

                    self.image= movimiento["sniperDer"][self.pasos]

                    self.pasos+=1

                    self.Dir=0


                else:
                    
                    self.image= movimiento["Derecha"][self.pasos]

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

     
                if self.pasos > 3:
                    
                    self.pasos=0


                if self.francotirador:

                    self.image= movimiento["sniperIzq"][self.pasos]

                    self.pasos+=1

                    self.Dir=1

                
                else:
                    self.image= movimiento["Izquierda"][self.pasos]

                    self.pasos+=1

                    self.Dir=1



        #Activar salto
        elif Tecla[K_w]:

            self.Saltar= True


                 
        #Quieto
        else:

            if self.francotirador:

                if self.Dir == 0:

                    self.image= movimiento["Quieto"][self.Dir+2]


                else:

                    self.image= movimiento["Quieto"][self.Dir+2]


            else:
                
                self.image= movimiento["Quieto"][self.Dir]


        #Ataque
        if Tecla[K_SPACE]:
            
            if self.numero != 0:

                pass

            elif self.francotirador:
            
                #Activamos ataque
                self.ataque=True
                self.generar=True
                

        
    def salto(self):

        #Restamos a la posición Y el aumento
        self.rect.y+= self.aumento


        #Dibujamos el salto
        if self.francotirador:

            self.image= movimiento["Salto"][self.Dir+2]


        else:
            
            self.image= movimiento["Salto"][self.Dir]
            

        #Aplicamos gravedad
        self.aumento+=3


        #Mover a la derecha durante el salto
        if Tecla[K_d]:

            if self.velocidad == 0:

                pass

            else:
                
                self.rect.x+= self.velocidad
                self.Dir=0
                

        #Mover a la izquierda durante el salto
        elif Tecla[K_a]:
            self.rect.x-= self.velocidad
            self.Dir=1

            
            self.Dir=1
            



    def disparar(self):

        #Controlar número de imagenes
        if self.numeroImagenes > 2:

            self.numeroImagenes=0

            if self.Dir==0:
                
                self.image= movimiento["sniperDer"][0]

            else:

                self.image= movimiento["sniperIzq"][0]
                
                
            self.ataque=False



        else:
            
            #Dirección
            if self.Dir == 0:

                self.image= movimiento["ataqueDer"][self.numeroImagenes]
                self.tiempo+=1


            else:

                self.image= movimiento["ataqueIzq"][self.numeroImagenes]
                self.tiempo+=1

                
        if self.tiempo == 5:

            self.numeroImagenes+=1
            self.tiempo=0

