import pygame as pg, time

from pygame.locals import *

from Sprites import Camina_Derecha, Camina_Izquierda,Saltos, Icono, Quieto, Muerte, Enemigo_1, mago, sniperDerecha, sniperIzquierda, sniperSalto, ataqueIzquierda, ataqueDerecha, hongo, arma, proyectil

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
        self.Estatico= Quieto[0]

        #Controlar muerte
        self.muerte=False
 
        #Cargar imagen
        self.image= Quieto[0]

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


    def mover(self):
        
        if self.conteo:

            if personajePrincipal.Dir == 0:
                
                self.dir=10

            else:

                self.image= proyectil[1]
                self.dir=-10

            self.conteo=False


        self.rect.x+=self.dir
    

    def comprobarPosicion(self):

        if nuevoProyectil.rect.x > 950 or nuevoProyectil.rect.x < 0:

            nuevoProyectil.kill()
            personajePrincipal.generar=False
            personajePrincipal.numero=0



#Clase para los enemigos básicos
class Enemigo(pg.sprite.Sprite):

    def __init__(self):

        super().__init__()

        #Gravedad
        self.caida=3
        self.caer=True

        #Dibujar cuadros
        self.Pasos=0

        #Controlar muerte del enemigo
        self.muerte=False
        self.continua=False
        self.retraso=0
        self.ahora=0

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




class OtroEnemigo(pg.sprite.Sprite):

    def __init__(self, imagen, x, y, cuadros):

        super().__init__()

        self.image= imagen[0]
        self.rect= self.image.get_rect()
        self.rect.x= x
        self.rect.y= y

        #Control de número de imagenes (ya que se usa una lista) 
        self.cuadros= cuadros

        self.mover=False

        #Control de ataque
        self.conteo=0
        self.bandera=False

        #Variable de prueba
        self.tiempo=0
        self.accion=False

        #Dependiendo el enemigo, ajustamos su moviento
        self.x= 0
        self.y= 0


    def moverX(self):
        
        self.rect.x+=3


    def moverY(self, direccion):

        if direccion == 0:

            self.rect.y-= 3

        else:

            self.rect.y+=3
    

    def atacar(self):

        if self.conteo >= 30.0 and self.conteo < 60:

            self.image= mago[1]

        elif self.conteo > 60 and self.conteo < 100:
            
            self.rect.x = 885 
            self.image= mago[2]

        
        elif self.conteo > 100:

            self.conteo=0
            self.mover= False
            self.bandera= True

            print(True)

        

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
magos= pg.sprite.Group()
bloquesBonus= pg.sprite.Group()
bloquesSimples= pg.sprite.Group()
bloquesDecoracion= pg.sprite.Group()
tuberias= pg.sprite.Group()
potenciadores= pg.sprite.Group()
proyectiles= pg.sprite.Group()

#Instanciación de enemigos    
nuevoEnemigo= Enemigo()
nuevoEnemigo.Posicion(700, 395)
enemigosBasicos.add(nuevoEnemigo)


#Magos
nuevoMago= OtroEnemigo(mago, 905, 320, 3)
magos.add(nuevoMago)


#Instanciando personajePrincipalPrincipal principal
personajePrincipal=personaje()
sprites.add(personajePrincipal)

#Instanciando Bloques
bonus= Bloque(600, 275, bloqueBonus)
bloquesBonus.add(bonus)

#Instanciación de los potenciadores

hongos= Potenciador(bonus.rect.x, bonus.rect.y -3, hongo)
armas= Potenciador(bonus.rect.x, bonus.rect.y -3, arma)

    
#Crear animación de subida y bajada bloque bonus (Pronto se pondrá en la clase para borrar este espacio)
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



#Tuberías
tuberia= Bloque(900, 320, tuberiaBasica)
tuberias.add(tuberia)

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
    tuberias.update()
    proyectiles.update()
    magos.update()


    #Dibujando sprites
    bloquesDecoracion.draw(Ventana)
    potenciadores.draw(Ventana)
    proyectiles.draw(Ventana)
    enemigosBasicos.draw(Ventana)
    magos.draw(Ventana)
    bloquesBonus.draw(Ventana)
    tuberias.draw(Ventana)
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

        nuevoProyectil.mover()


    #Movimiento y ataque del mago    
    if personajePrincipal.rect.right >= (tuberia.rect.left - 200):

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

            nuevoMago.moverY(0)
        
        else:

           nuevoMago.atacar()
           nuevoMago.conteo+=1

    else:

        if nuevoMago.bandera:

            nuevoMago.rect.x = 905
            nuevoMago.image= mago[0]

            nuevoMago.moverY(1)

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

            if nuevoEnemigo.muerte:

                pass


            else:

                personajePrincipal.puntuacion+=500
                personajePrincipal.aumento=-30
                nuevoEnemigo.image=Enemigo_1[2]
                nuevoEnemigo.rect.bottom=450
                nuevoEnemigo.muerte=True
                nuevoEnemigo.ahora= pg.time.get_ticks()
                nuevoEnemigo.retraso= nuevoEnemigo.ahora + 2000 
            

        else:

            if nuevoEnemigo.muerte:

                pass

            else:
                
                personajePrincipal.muerte=True
                personajePrincipal.ahora=pg.time.get_ticks()
                personajePrincipal.retraso=personajePrincipal.ahora + 2000

        
    if nuevoEnemigo.muerte:

        #Tiempo que se mostrará la imagen antes de eliminar el objeto
        if nuevoEnemigo.ahora >= nuevoEnemigo.retraso:
                
            nuevoEnemigo.kill()

        else:

            nuevoEnemigo.ahora+=50


    #Mostrar muerte, aunque colisione con un objeto
    if personajePrincipal.muerte or (personajePrincipal.muerte and colisionSuelo):

        personajePrincipal.image=Muerte
        sprites.draw(Ventana)

        #Tiempo que se mostrará la imagen antes de eliminar el objeto
        if personajePrincipal.muerte:
            
            personajePrincipal.ahora+=100

            if personajePrincipal.ahora ==  personajePrincipal.retraso:

                personajePrincipal.kill()
                personajePrincipal.conteo=0

        
        
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

    personajeArmas= pg.sprite.spritecollide(personajePrincipal, potenciadores, False)

    if personajeArmas:

        personajePrincipal.puntuacion+=1000
        personajePrincipal.francotirador=True
        armas.kill()


    #Colisión del enemigo con proyectil
    
    if personajePrincipal.generar:

        colisionProyectil= pg.sprite.spritecollide(nuevoProyectil, enemigosBasicos, False)

        if colisionProyectil:

            nuevoProyectil.kill() 
            personajePrincipal.generar=False
            nuevoEnemigo.kill()


    #Eliminar proyectil al salir de la pantalla
    if personajePrincipal.generar:

        nuevoProyectil.comprobarPosicion()

    

    #Colisión tubería

    colisionTuberia= pg.sprite.spritecollide(personajePrincipal, tuberias, False)

    if colisionTuberia:

        #Comprobamos si está encima de la tubería
        if personajePrincipal.rect.bottom >= tuberia.rect.top and (personajePrincipal.rect.centery - 10) < tuberia.rect.top:

            personajePrincipal.rect.bottom = tuberia.rect.top +1
            personajePrincipal.Saltar=False
            personajePrincipal.aumento= -30

        
        #Si no lo está, verificamos si ha colisionado con uno de los lados del sprite (left, right)
        else:
            
            if personajePrincipal.rect.right >= tuberia.rect.left:

                 personajePrincipal.rect.right= tuberia.rect.left
        

#========================== Movimiento de los personajes ====================================#
        
    
    #Mover personajePrincipal y enemigos

    if not personajePrincipal.muerte:
        personajePrincipal.Movimiento()

    if not nuevoEnemigo.muerte:
        nuevoEnemigo.Mover()


    #Movimiento de potenciadores
    if armas.mover:

        armas.moverPotenciador()

    if armas.caida:

        armas.caer()
        

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
