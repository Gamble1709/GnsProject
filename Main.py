import pygame as pg, time

from pygame.locals import *

from Sprites import Camina_Derecha, Camina_Izquierda,Saltos, Icono, Quieto, Muerte, Enemigo_1, sniperDerecha, sniperIzquierda, sniperSalto, ataqueIzquierda, ataqueDerecha, hongo, arma

from Blocks import bloqueBonus, bloqueBonus_2, suelo, montaniaPequenia, montaniaGrande, nubeGrande, nubePequenia, arboles, tuberiaBasica

from Constants import Ancho_pantalla, Alto_pantalla, Azul, Blanco, bertram

import sys



class personaje(pg.sprite.Sprite):

    def __init__(self):

        super().__init__()

        #Control de sprites
        self.pasos=0

        #control del colisión con bloque bonus
        self.posX=0

        self.puntuacion=0
        self.puntuacion2=""

        #Activar - Desactivar Sniper
        self.francotirador= False

        #Controla ataque
        self.ataque=False
        self.numeroImagenes=0
        self.tiempo=0

        #Controla el alto del salto
        self.aumento=-30

        self.Saltar= False

        #Controlar velocidad mientras salta
        self.velocidad=2

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



    def obtenerPuntuacion(self):

        puntuacion= str(self.puntuacion)
        
        #Creamos la lista según el puntaje máximo
        lista=['0' for x in range(5)]
        
        #Esto nos permite iniciar desde la última posición de la lista
        indice=-1
        
        #Según el tamaño se ejecuta for n veces
        tamanio= len(puntuacion)

        for x in range(tamanio):

            #Reemplazamos el índice de la lista con el índice de la puntuación
            lista[indice]= puntuacion[indice]
            
            #Restamos para ir una posición hacia atrás
            indice-=1
        
        #Convertimos la lista en string
        self.puntuacion2= "".join(lista)
        

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

            if self.velocidad == 0:

                pass

            else:
                
                self.rect.x+= self.velocidad
                self.Dir=0
                

        #Mover a la izquierda durante el salto
        elif Tecla[K_a]:
            self.rect.x-= self.velocidad
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

        #Gravedad
        self.caida=3

        #Dibujar cuadros
        self.Pasos=0

        #Controlar personaje principal al morir el enemigo
        self.muerte=False

        #Imagen inicial
        self.image= Enemigo_1[self.Pasos]

        #obtenemos el rectángulo de la imagen
        self.rect= self.image.get_rect()

        #controlar rebote por velocidad o velocidad del enemigo
        self.Velocidad=3

        #controlar tiempo de cambio entre sprites o cuadros
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

def mostrarTexto(ventana, fuente, texto, tamaño, color, x, y):

    tipoFuente= pg.font.Font(fuente, tamaño)
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
bloquesBonus= pg.sprite.Group()
bloquesSimples= pg.sprite.Group()
bloquesDecoracion= pg.sprite.Group()
potenciadores= pg.sprite.Group()

#Instanciación de enemigos    
primerEnemigo= Enemigo()
primerEnemigo.Posicion(700, 395)
enemigosBasicos.add(primerEnemigo)

#Instanciando personajePrincipalPrincipal principal
personajePrincipal=personaje()
sprites.add(personajePrincipal)


#Instanciando Bloques
bonus= Bloque(600, 275, bloqueBonus)
bloquesBonus.add(bonus)


#Instanciación de los potenciadores

hongos= Potenciador(bonus.rect.x, bonus.rect.y -3, hongo)
armas= Potenciador(bonus.rect.x, bonus.rect.y -3, arma)


#Crear animación de subida y bajada bloque bonus
animacionbonus=False
subir=-8
animacion=False


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
    
    bloque=Decoracion(distanciaX, distanciaY, suelo)
    bloquesDecoracion.add(bloque)

    distanciaX+=25
    cont+=1

    if cont==40:

        distanciaY+=23
        distanciaX=0



#Montañas
montania_1= Decoracion(100, 395, montaniaPequenia)
bloquesDecoracion.add(montania_1)

montania_2= Decoracion(montania_1.rect.right, 360 ,montaniaGrande)
bloquesDecoracion.add(montania_2)

#Nubes
nube_1= Decoracion(300, 50, nubeGrande)
bloquesDecoracion.add(nube_1)

nube_2= Decoracion(500, 50, nubePequenia)
bloquesDecoracion.add(nube_2)

#Árboles
arbol= Decoracion(300, 350, arboles)
bloquesDecoracion.add(arbol)

#Tuberías
tuberia= Bloque(900, 320, tuberiaBasica)
bloquesDecoracion.add(tuberia)


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
    bloquesBonus.update()


    #Dibujando sprites
    bloquesDecoracion.draw(Ventana)
    enemigosBasicos.draw(Ventana)
    potenciadores.draw(Ventana)
    bloquesBonus.draw(Ventana)
    bloquesSimples.draw(Ventana)
    sprites.draw(Ventana)


    #Mostrando texto
    mostrarTexto(Ventana, bertram, "TIME", 30, Blanco, 10, 10)
    mostrarTexto(Ventana, bertram, str(int(tiempo)), 25, Blanco, 20, 40)
    mostrarTexto(Ventana, bertram, "SCORE", 30, Blanco, 870, 10)
    personajePrincipal.obtenerPuntuacion()
    mostrarTexto(Ventana, bertram, str(personajePrincipal.puntuacion2), 25, Blanco, 900, 40)

    tiempo-=.05


#============================= Colisiones ==================================#
    

    #Creando colisión con enemigos + Muerte del enemigo
    
    Colision= pg.sprite.spritecollide(personajePrincipal, enemigosBasicos, False)

    if Colision:

        #Sí la posición en Y es menor al enemigo, significa que el personajePrincipal colisionó estando en el aire y cayendo encima del enemigo
        if personajePrincipal.Saltar or (personajePrincipal.rect.bottom < primerEnemigo.rect.y):

            if primerEnemigo.muerte:

                pass


            else:

                personajePrincipal.puntuacion+=500
                personajePrincipal.aumento=-30
                primerEnemigo.Velocidad=0
                primerEnemigo.image=Enemigo_1[2]
                primerEnemigo.rect.bottom=450
                Mover=False
                Continua=True
                primerEnemigo.muerte=True
            
            

        else:

            if primerEnemigo.muerte:

                pass

            else:
                
                Mover_personajePrincipal=False
                Muerte_personajePrincipal=True
                Contar=True


        
    if Continua:

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

        
        
    #Colisión del personaje con el bloque bonus

    if (personajePrincipal.rect.x + 63 >= bonus.rect.left and personajePrincipal.rect.top <= bonus.rect.bottom -3)\
       and personajePrincipal.rect.x < bonus.rect.right:
           

        personajePrincipal.rect.x= personajePrincipal.posX


    elif (personajePrincipal.rect.x <= bonus.rect.right and personajePrincipal.rect.top <= bonus.rect.bottom -3) \
         and personajePrincipal.rect.x > bonus.rect.left:

        personajePrincipal.rect.x= personajePrincipal.posX


    else:

        personajePrincipal.posX= personajePrincipal.rect.x

        
        
    colisionbonus= pg.sprite.spritecollide(personajePrincipal, bloquesBonus, False)


    if colisionbonus:

        if personajePrincipal.rect.y <= bonus.rect.bottom and personajePrincipal.rect.x + 63 > bonus.rect.left:
            
            #Esto para que al colisionar baje y no continue subiendo
            personajePrincipal.rect.y+=3
            personajePrincipal.aumento=0

            if not animacion:
                
                animacionbonus=True

            else:

                personajePrincipal.rect.y+=3


    #Animación de bonus
    if animacionbonus:

        bonus.rect.y+=subir
        subir+=1

        if subir == 8:
            
            bonus.image= bloqueBonus_2
            animacionbonus=False
            subir=-8

            potenciadores.add(armas)
            armas.mover=True
            armas.caida=True
            animacion=True


    
    #Colisión del arma con el bloque bonus
    armabonus= pg.sprite.spritecollide(armas, bloquesBonus, False)

    if armabonus:

        #Evitar que el sprite traspase el bloque bonus
        if armas.rect.bottom >= bonus.rect.top:

            armas.rect.bottom = bonus.rect.top+3
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
    


    #Colsisión del personaje con el suelo
    colisionSuelo= pg.sprite.spritecollide(personajePrincipal, bloquesSimples, False)

    if colisionSuelo:
 
        if personajePrincipal.rect.bottom >= sueloBasico.rect.top:

            personajePrincipal.Saltar=False
            personajePrincipal.aumento=-30
            personajePrincipal.rect.bottom= sueloBasico.rect.top+1


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

        personajePrincipal.puntuacion+=1000
        personajePrincipal.francotirador=True
        armas.kill()

    #Colisión tubería
    if personajePrincipal.rect.right >= tuberia.rect.left:

        personajePrincipal.rect.right = tuberia.rect.left


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
