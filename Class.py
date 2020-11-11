import pygame as pg

from pygame.locals import *

from Sprites import movimiento, proyectil, enemigos

from Blocks import bloques


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

        #Activa el salto del personaje
        self.Saltar= False

        #Controlar velocidad mientras salta
        self.velocidad=2

        #Si el personaje está cayendo se activa
        self.caida= False

        #Dirección mientras está quieto
        self.Dir=0
        self.Estatico= movimiento["Quieto"][0]

        #Controlar muerte
        self.muerte=False
 
        #Cargar imagen
        self.image= movimiento["Quieto"][0]
        self.image2= movimiento["Salto"][0]

        #obtiene el rectangulo del sprite 
        self.rect= self.image2.get_rect()
        
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

            if self.caida:

                pass

            else:

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



    def tiempoDeMuerte(self, inicio):

        self.ahora= pg.time.get_ticks()
        self.image= movimiento["Muerte"]
        
        if (self.ahora - inicio > 2000):

            self.kill()



class Proyectil(pg.sprite.Sprite):

    def __init__(self, imagen, x, y):

        super().__init__()

        self.image= imagen
        self.rect= self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

        #Para mover el proyectil
        self.conteo=True
        self.dir=0


    def mover(self, personaje):
        
        if self.conteo:

            if personaje.Dir == 0:
                
                self.dir=10

            else:

                self.image= proyectil[1]
                self.dir=-10

            self.conteo=False


        self.rect.x+=self.dir
    

    def comprobarPosicion(self, personaje):

        if self.rect.x > 950 or self.rect.x < 0:

            self.kill()
            personaje.generar=False
            personaje.numero=0



#Clase para los enemigos básicos
class Enemigo(pg.sprite.Sprite):

    def __init__(self,maxPasos,x,y):

        super().__init__()

        #Gravedad
        self.caida=3
        self.caer=True

        #Dibujar cuadros
        self.Pasos=0
        self.maximosPasos= maxPasos

        #Controlar muerte del enemigo
        self.muerte=False

        #Imagen inicial
        self.imagen= enemigos 
        self.image= self.imagen["Goomba"][self.Pasos]

        #obtenemos el rectángulo de la imagen
        self.rect= self.image.get_rect()

        #Posición
        self.rect.x =x
        self.rect.y =y

        #controlar rebote por velocidad o velocidad del enemigo
        self.Velocidad=3

        #controlar tiempo de cambio entre sprites o cuadros
        self.Contador=0

        

    def mover(self):
        
        self.rect.x-= self.Velocidad
        self.image= self.imagen["Goomba"][self.Pasos]

        self.Contador+=1

        if self.Contador ==10:
            self.Pasos+=1
            self.Contador=0

        if self.Pasos > self.maximosPasos:
            self.Pasos=0

        """Si se desea usar rebote

        if self.rect.x < 0:
            self.Velocidad=-3


        elif self.rect.x > 950:
            self.Velocidad=3

        """


    def Caer(self):

        self.rect.y+= self.caida


    def tiempoDeMuerte(self, inicio):

        self.image= enemigos["Goomba"][2]
        self.ahora= pg.time.get_ticks()

        if (self.ahora -inicio > 2000):

            self.kill()



class Mago(Enemigo):

    def __init__(self, maxPasos, x, y):

        
        super().__init__(maxPasos, x, y)

        self.image= self.imagen["Mago"][0]

        self.movimiento=False

        #Control de ataque
        self.conteo=0
        self.bandera=False

        self.inicio=0

        #Variable de prueba
        self.tiempo=0
        self.accion=False


    def mover(self):

        if self.rect.y > 230 and not self.atacar(pg.time.get_ticks()):

            self.rect.y-= 3 
            self.inicio= pg.time.get_ticks()

        elif self.atacar(pg.time.get_ticks()):

            if self.rect.y < 320:

                self.rect.y+= 3

            else:

                self.movimiento= False

        else:

            self.atacar(pg.time.get_ticks())



    def atacar(self, ahora):

        if ahora - self.inicio >= 1000 and ahora - self.inicio <= 2000:

            self.image= self.imagen["Mago"][1]
            return False

        elif ahora - self.inicio >= 2000 and ahora - self.inicio <= 3000: 
            self.rect.x = 885 
            self.image= self.imagen["Mago"][2]
            return False

        
        elif ahora - self.inicio >= 3000: 

            self.rect.x= 905
            self.image= self.imagen["Mago"][0]
            return True

        else:

            return False
    

    def tiempoDeMuerte(self, inicio):

        #self.image= enemigos["Mago"][2]
        self.ahora= pg.time.get_ticks()

        if (self.ahora -inicio > 2000):

            self.kill()

        





#Clase para los bloques
class Bloque(pg.sprite.Sprite):
    
    def __init__(self, imagen, posX, posY): 
        super().__init__()

        self.image= imagen
        self.rect= self.image.get_rect()
        self.rect.x= posX
        self.rect.y= posY




#Clase para los potenciadores
class Potenciador(Bloque):
    

    def __init__(self, x, y, imagen):
    
        super().__init__(x,y,imagen)

        #Movimiento
        self.mover=True

        #Caída
        self.caida=True


    def moverPotenciador(self):

        self.rect.x+=2


    def caer(self):

        self.rect.y+=5




#Clase para los Bloque bonus
class Bonus(Bloque):

    def __init__(self, imagen, posX, posY):

        super().__init__(imagen, posX, posY)
        
        self.pixeles=1


    def mover(self, inicio):

        ahora= pg.time.get_ticks() 
        self.rect.y-= self.pixeles
         
        if(ahora - inicio > 500):

            self.image= bloques["Bonus"][1] 
            self.pixeles=-1

        if(ahora - inicio > 1000):

            return True 



#Clase para los elementos de decoración
class Decoracion(Bloque):

    def __init__(self, imagen, posX, posY):

        super().__init__(imagen, posX,posY)

