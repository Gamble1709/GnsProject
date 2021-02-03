import pygame as pg, os

from pygame.locals import *

from Sprites import movimiento, proyectil, enemigos, carpetaCaracol

from Blocks import bloques

from Sounds import jump, shoot 


class Personaje(pg.sprite.Sprite):

    def __init__(self):

        super().__init__()

        #Control de sprites
        self.pasos=0

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
        self.activo= False

        #Controla el alto del salto
        self.aumento= -30

        #Activa el salto del personaje
        self.saltar= False

        #Controlar velocidad mientras salta
        self.velocidad= 2

        #Si el personaje está cayendo se activa
        self.caida= False

        #Dirección mientras está quieto
        self.direccion= 0

        #Controla la velocidad mientras haya movimiento de cámara
        self.camara= False

        #Controlar muerte
        self.muerte=False
        self.inicio= 0
 
        #Cargar imagen
        self.image= movimiento["Quieto"][0]

        #obtiene el rectangulo del sprite 
        self.rect= self.image.get_rect()
        
        #Coordenadas del rectangulo
        self.rect.x= 50
        self.rect.y= 379


    def update(self):

        global Tecla

        #Controlar eventos del teclado
        Tecla=pg.key.get_pressed()

        #Si no está muerto el jugador
        if not self.muerte:

            #Margenes de movimiento
            if self.rect.x <=0:

                self.rect.x= 1
                

            elif self.rect.x >= 950:
                
                self.rect.x= 950

            
            #Si el jugador está inactivo "quieto", mostramos la imagen correspondiente
            if not Tecla[K_a] and not Tecla[K_d] and not self.saltar:

                #Verificamos si está en el modo Sniper o Francotirador para elegir la imagen
                if self.francotirador: self.image= movimiento["Quieto"][self.direccion + 2]

                else: self.image= movimiento["Quieto"][self.direccion]


            #Movimiento

            #Si la tecla "d" es presionada
            if Tecla[K_d]:

                #Evitar movimiento mientras se ejecute el salto
                if self.saltar:

                    pass

                #Salto combinado
                elif Tecla[K_d] and Tecla[K_w]:

                    #Si no estaba saltando ejecutamos el sonido de salto
                    if not self.saltar: 

                        jump.play()

                    #Activamos el salto
                    self.saltar= True


                #Evitar movimiento mientras dispara
                if self.ataque: pass

                #Caminar derecha 
                else:

                    #Si la "cámara" está activada evitamos que se mueva para evitar errores 
                    if self.camara: pass

                    #Si no, movemos al personaje
                    else: self.rect.x += 10

                    #Verificamos si el número que controla las imágenes supera el límite máximo 
                    if self.pasos > 3:

                        #Si es así reiniciamos los pasos (controla que imagen se mostrará de cierta lista)
                        self.pasos= 0
                        

                    #Si el modo Sniper o francotirador está activado la imagen será distinta
                    if self.francotirador:

                        self.image= movimiento["sniperDer"][self.pasos]

                        self.pasos+= 1


                    #Si no, entonces mostramos la imagen normal
                    else:
                        
                        self.image= movimiento["Derecha"][self.pasos]

                        self.pasos+= 1

                    
                    #Cambiando dirección (útil para saber cual es la dirección del personaje)
                    self.direccion= 0



            #izquierda

            elif Tecla[K_a]:

                #Evitar movimiento mientras se ejecute el salto
                if self.saltar: pass

                #Salto combinado
                elif Tecla[K_a] and Tecla[K_w]:
                    
                    if not self.saltar:

                        jump.play()

                    self.saltar=True


                #Evitar movimiento mientras dispara
                if self.ataque: pass
                
                #Caminar Izquierda
                else:

                    #Se encarga de restarle a la posición en X del personaje
                    self.rect.x -= 10

                    #Mismo procedimiento que con la tecla "d" 
                    if self.pasos > 3:
                        
                        self.pasos=0


                    if self.francotirador:

                        self.image= movimiento["sniperIzq"][self.pasos]

                        self.pasos+= 1

                    else:
                        self.image= movimiento["Izquierda"][self.pasos]

                        self.pasos+= 1

                    
                    #Cambiando dirección
                    self.direccion= 1



            #Activar salto
            elif Tecla[K_w]:
                
                #Si el salto no estaba activado entonces reproducimos el soundtrack correspondiente
                if not self.saltar:

                    jump.play()


                if self.caida: pass

                else:
                    
                    #Cambiamos el estado del atributo que controla el salto
                    self.saltar= True



            #Ataque
            if Tecla[K_SPACE]:

                #Si está en modo francotirador y su último ataque ha terminado
                if not self.activo and self.francotirador:

                    #Ejecutamos el sountrack de ataque
                    shoot.play()

                    #Activamos ataque
                    self.ataque=True

                    #Indicamos que se generará un nuevo proyectil
                    self.generar=True

                
                #if self.activo: pass


        #Ejecutar Salto
        if self.saltar:

            #Llama al método que ejecuta el salto
            self.salto()


        #Ejecutar disparo
        if self.ataque:

            #Llama al método que se encarga de mostrar la imágenes de ataque
            self.disparar()


        
    def salto(self):

        #Restamos a la posición Y el aumento
        self.rect.y+= self.aumento


        #Dibujamos el salto verificando si está en el modo francotirador o Sniper
        if self.francotirador:

            self.image= movimiento["Salto"][self.direccion + 2]


        #Si no, mostramos la imagen normal
        else:
            
            self.image= movimiento["Salto"][self.direccion]
            

        #Aplicamos gravedad
        self.aumento+= 3


        #Mover a la derecha durante el salto
        if Tecla[K_d]:

            #Verificamos si el modo "cámara" está activado para evitar errores al mover
            if self.camara: pass

            else:
                
                self.rect.x+= 2

                #Indica la dirección que tiene o tuvo el personaje (izquierda= 0 o derecha= 1)
                self.direccion= 0
                

        #Mover a la izquierda durante el salto
        elif Tecla[K_a]:

            self.rect.x-= 2
            self.direccion= 1



    def disparar(self):

        #Controlar número de imágenes  
        if self.numeroImagenes > 2:

            self.numeroImagenes= 0

            #Verificamos cual es la dirección que lleva para mostrar la imagen correspondiente una
            #vez que el ataque ha terminado
            if self.direccion == 0: self.image= movimiento["sniperDer"][0]

            else: self.image= movimiento["sniperIzq"][0]
                
            #Terminamos el ataque y dejamos de mostrar las imágenes del mismo
            self.ataque=False


        else:
            
            #Dirección

            #Si la dirección del personaje es hacia la derecha, mostramos las imágenes correspondientes
            if self.direccion == 0:

                self.image= movimiento["ataqueDer"][self.numeroImagenes]

                #Contamos cuanto tiempo durará la imagen
                self.tiempo+= 1


            #Si está mirando hacia la izquierda mostramos las imágenes correspondientes
            else:

                self.image= movimiento["ataqueIzq"][self.numeroImagenes]
                self.tiempo+= 1

                
        #Si el contador llegó a 5 significa que es momento de cambiar la imagen
        if self.tiempo == 5:

            self.numeroImagenes+= 1

            #Reiniciamos el tiempo
            self.tiempo= 0



    def tiempoDeMuerte(self):

        #Dibujamos la imagen de muerte
        self.image= movimiento["Muerte"]
        
        #Si ya han pasado 2 segundo desde que murió, eliminamos el personaje
        if (pg.time.get_ticks() - self.inicio > 2000):

            self.kill()



class Proyectil(pg.sprite.Sprite):

    def __init__(self, personaje):

        super().__init__()

        #Según la dirección del personaje será la imagen del proyectil
        self.image= proyectil[personaje.direccion]
        self.rect= self.image.get_rect()

        #Según la dirección del personaje será la dirección del proyectil
        if personaje.direccion == 0: 

            #Si la dirección es 0 (mirando hacia la derecha), hacemos que aumente positivamente la pos X
            self.dir= 20

            #Hacemos que la posición de inicio sea del lado donde está el arma que sostiene el personaje
            #pues si mira a la izquierda el lado de donde está el arma cambia
            self.rect.x= personaje.rect.right

        else: 

            #Si está mirando a la izquierda hacemos que la posición en X se reste
            self.dir= -20

            #Hacemos que la posición de inicio sea del lado donde está el arma que sostiene el personaje
            self.rect.x= personaje.rect.x 

        #Hacemos que la posición Y del enemigo sea la misma que la del arma
        self.rect.y= personaje.rect.centery + 5



    def update(self, personaje):

        self.comprobarPosicion(personaje)

        #Cambiamos la posición en X según la dirección (positiva o negativa)
        self.rect.x+= self.dir
    

    def comprobarPosicion(self, personaje):

        #Si el proyectil supera los márgenes de la pantalla
        if self.rect.x > 950 or self.rect.x < 0:

            #Lo eliminamos
            self.kill()

            #Cambiamos el atributo del personaje que indica que puede volver a lanzar otro proyectil
            personaje.activo=False


#Clase para los enemigos básicos
class Enemigo(pg.sprite.Sprite):

    def __init__(self, x,y):

        super().__init__()

        #Gravedad
        self.caer=True

        #Dibujar cuadros
        self.pasos=0
        self.maximosPasos= 1

        #Controlar muerte del enemigo
        self.muerte=False
        self.inicio=0

        #Imagen inicial
        self.imagen= enemigos 
        self.image= enemigos["Goomba"][self.pasos]

        #obtenemos el rectángulo de la imagen
        self.rect= self.image.get_rect()

        #Posición
        self.rect.x =x
        self.rect.y =y

        #controlar rebote por velocidad o velocidad del enemigo
        self.velocidad=3

        #controlar tiempo de cambio entre sprites o cuadros
        self.contador=0

        

    def update(self):

        #Si el Goomba no ha muerto
        if not self.muerte:
        
            #Aumento a su posición en X
            self.rect.x-= self.velocidad

            #Dibujamos cada imagen
            self.image= enemigos["Goomba"][self.pasos]

            self.contador+=1

            #Si el contador llega a 10 cambiamos el número de imagen, esto debido a que solo son dos
            #imágenes y al mostrarlas sin un contador pasan demasiado rápido
            if self.contador == 10:

                self.pasos+=1
                self.contador=0

            
            #Si el número que se encarga de mostrar cada imagen es mayor al máximo reiniciamos los pasos
            if self.pasos > self.maximosPasos: self.pasos=0

            """Si se desea usar rebote:

            if self.rect.x < 0:
                self.Velocidad=-3


            elif self.rect.x > 950:
                self.Velocidad=3

            """

            #Si está en el aire hacemos que comienze a caer 
            if self.caer:

                self.rect.y+= 3 

            #Si sale de la pantalla se elimina
            if self.rect.x < 0:

                self.kill()

        else:

            self.tiempoDeMuerte()




    def iniciarMuerte(self):

        #Obtenemos el tiempo en que inició la muerte
        self.inicio= pg.time.get_ticks()

        #Cambiamos el atributo de muerte a True
        self.muerte= True

        #Mostramos la imagen de muerte
        self.image= enemigos["Goomba"][2]

        #Subimos su posición en Y pues al cambiar de imagen esta queda muy abajo sobrepasando el suelo 
        self.rect.bottom += 2 



    def tiempoDeMuerte(self):

        #Verficamos si desde que inició el tiempo de muere han pasado 2 segundos (2000) milésimas 
        if (pg.time.get_ticks()  - self.inicio > 2000):

            #Si es verdadero eliminamos el objeto
            self.kill()



class Mago(pg.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()

        self.image= enemigos["Mago"][0][0]
        self.rect= self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

        #Indica si es necesario voltear la imagen
        self.flip= False

        self.movimiento=False

        #Control de ataque
        self.numeroImagenes=0
        self.inicio=0
        self.retraso=0 
        self.tiempo=1000

        #Ataque
        self.invocar= False

        #Evita que se generen múltiples enemigos
        self.invocado= False

        #Variable de prueba
        self.accion=False

        self.imagenesMuerte=0 #controlar número de imágenes de muerte
        self.muerte= False



    def update(self, personaje):

        #Si ha activado la muerte
        if self.muerte:

            #Si se estaba moviendo lo detenemos
            if self.movimiento: self.movimiento= False

            #Si la imagen de muerte es 0 es que apenas inició la muerte
            if self.imagenesMuerte == 0: self.tiempo=1000

            #Llamamos al método que se encarga de mostrar las imágenes de muerte y de eliminar el objeto
            self.tiempoDeMuerte()


        else:

            #Movimiento y ataque del mago    
            if personaje.rect.x > (self.rect.x - 300) or personaje.rect.x < (self.rect.x + 300) and (not 
                    personaje.muerte and not self.muerte):

                #Si el Mago no se ha movido del punto de inicio y ya pasó el tiempo de retraso 
                #del último ataque
                 if self.rect.y == 352 and self.comprobarMovimiento():

                     #Verificamos si la posición X del jugador es mayor para así saber voltear la imagen
                     if personaje.rect.x > self.rect.centerx: self.flip= True

                     #Nos ayuda a saber en que momento inició el ataque
                     self.inicio= pg.time.get_ticks()

                     #Iniciamos el movimiento
                     self.movimiento= True


            #Verificamos si el atributo movimiento es True o verdadero y llamamos al método que mueve
            #el objeto
            if self.movimiento: self.mover()



    def mover(self):

        #Sí aún no ha llegado al top de la tubería y además sabemos que no está bajando, hacemos que suba
        if self.rect.y > 230 and not self.atacar():

            #Evita que se generen múltiples enemigos
            self.invocado= False

            self.rect.y-= 3 
            self.inicio= pg.time.get_ticks()

        # y cuando retorne verdadero comenzamos a bajar
        elif self.atacar():

            #Mientras no lleguemos a la posición de origen, bajamos
            if self.rect.y < 352:

                self.rect.y+= 3

            #Sí ya llegamos, evitamos el movimiento
            else:

                self.movimiento= False

        #Llamamos el ataque + invocación
        else:

            self.atacar()



    def comprobarMovimiento(self):

        #Comprobamos si ya han pasado 5 segundos desque se hizo el último ataque
        if (pg.time.get_ticks()) - self.retraso >= 5000:

            return True

        #Si no, retornamos False
        return False



    def atacar(self):

        #Este condicional ayuda a que cuando inicie el ataque haya un segundo de retraso o de pausa
        #para que el personaje pueda ver al Mago antes de que ataque
        if not pg.time.get_ticks() - self.inicio > self.tiempo: pass 

        #Verificamos si cada imagen está entre su rango de tiempo, es decir, cada imagen se muestra
        #por 0.3 segundos, cuando pasen mostramos la siguiente imagen
        if pg.time.get_ticks() - self.inicio >= self.tiempo and (pg.time.get_ticks() - self.inicio 
                <= (self.tiempo + 300)):


            #En 2500 milésimas o en 2.5 segundos se muestran todas las, imágenes si ya pasaron significa
            #que todas las imágenes se mostraron, si no, seguimos mostrandolas
            if self.tiempo <= 2500:

                #Verificamos si debemos voltear la imagen y si es verdad lo hacemos
                if self.flip: self.image= pg.transform.flip(enemigos["Mago"][0][self.numeroImagenes], 
                        True, False)

                #Si no, mostramos la imagen sin voltear
                else: self.image= enemigos["Mago"][0][self.numeroImagenes]

                self.numeroImagenes+=1
                self.tiempo+=300


        #Cuando termine el tiempo de ataque
        if pg.time.get_ticks() - self.inicio > 2800: 

            #Reinciamos el tiempo para cuando vuelva a atacar
            self.tiempo= 1000

            #Si no ha invocado el enemigo, hacemos que lo invoque
            if not self.invocado and not self.invocar:

                self.invocar= True
                self.invocado= True

            #Si ya fue invocado, evitamos que genere uno nuevo
            else:

                self.invocar= False

            
            #self.rect.x= 908

            #Cuando haya terminado el ataque hacemos que tenga la imagen inicial
            self.image= enemigos["Mago"][0][0]

            #Este retraso evita que en cuanto termine el ataque vuelva a empezar, da un tiempo de espera
            self.retraso= pg.time.get_ticks()

            #Restaura el número de imágenes  
            self.numeroImagenes=0

            #Indicamos que el ataque terminó
            return True


        return False
    


    def tiempoDeMuerte(self):

        self.ahora= pg.time.get_ticks()

        #Controla el tiempo que se mostrará cada imagen
        if (self.ahora - self.inicio > self.tiempo) and self.ahora - self.inicio < (self.tiempo + 400):

            #Mientras no pasen 3.4 segundos, se mostrarán todas las imágenes de muerte
            #3.4 segundos es lo que tardan en mostrarse
            if self.tiempo < 3400:

                self.image= enemigos["Mago"][1][self.imagenesMuerte]
                self.tiempo+=400

            else:

                #Si ya pasó ese tiempo eliminamos el objeto
                self.kill()


            self.imagenesMuerte+=1



class Prueba(pg.sprite.Sprite):
    
    def __init__(self, x, y):

        super().__init__()

        self.image= enemigos["Caracol"][0][0]
        self.rect= self.image.get_rect()
        self.rect.y= y
        self.rect.x= x

        #Atributos que controlan el cuadro que se mostrará y la dirección que tendrá
        self.cuadros= 0
        self.direccion= 0

        #Controla la velocidad del caracol
        self.velocidad= 3

        #Cuando está escondido en su caparazón podrá soportar 3 golpes del personaje y luego morirá
        self.golpes= 0
        
        #Atributo que se contiene el tiempo que se escondio el objeto
        self.inicioTiempoEscondido= 0

        #Atributo que indica cuando si el objeto está escondido o no
        self.escondido= False

        self.tiempoMuerte= 0
        self.muerte= False



    def update(self, personajePrincipal):

        #Si el Caracol no ha muerto
        if not self.muerte:

            if self.golpes > 2:

                self.iniciarMuerte()

            if not self.escondido:

                #Verificamos que el número de cuadros (frames) esté entre el rango de número de imagenes
                if self.cuadros > 8:

                    #Si es así reiniciamos el número de cuadros
                    self.cuadros= 0
                
                #Dibujamos la imagen según la dirección del personaje
                self.image= enemigos["Caracol"][self.direccion][self.cuadros]

                #El caracol seguirá a el jugador, según la posición del jugador así será la dirección 
                if personajePrincipal.rect.x > self.rect.x:
                    
                    #Si la dirección que llevaba no era la correcta la cambiamos
                    if self.direccion != 0: self.direccion= 0

                    #Aumentamos la posición en X
                    self.rect.x+= self.velocidad 

                else:
                    
                    if self.direccion != 1: self.direccion= 1

                    self.rect.x-= self.velocidad 

                #Esta controla los 'frames' o que imagen se mostrará
                self.cuadros+= 1


            #Si el caracol si está escondido
            else:

               self.esconderse() 

        else:

            #Si se activa el atributo de muerte llamamos al método que destruye al objeto caracol
            self.destruirObjeto()


    
    def esconderse(self):

        self.image= enemigos["Caracol"][2][self.direccion]

        if pg.time.get_ticks() - self.inicioTiempoEscondido > 3000:

            self.escondido= False 
            self.velocidad+= 1



    def iniciarMuerte(self):

        #Obtenemos el tiempo en que inició la muerte
        self.tiempoMuerte= pg.time.get_ticks()

        #Activamos el atributo que indica que el caracol ha muerto
        self.muerte=True



    def destruirObjeto(self):

        #Verificamos si desde el tiempo desde que inició la muerte hasta ahora han pasado 3 segundos
        if pg.time.get_ticks() - self.tiempoMuerte > 3000:

            #Si es así, eliminamos el objeto
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

        #Caída
        self.caida= False
        


    def update(self):

        #Movemos el objeto a la derecha
        self.rect.x+= 2

        #Verifica si el objeto está cayendo
        if self.caida:

            #Hacemos que su posición en Y incremente
            self.rect.y+= 5



#Clase para los Bloque bonus
class Bonus(Bloque):

    def __init__(self, imagen, posX, posY):

        super().__init__(imagen, posX, posY)
        
        self.rect= self.image.get_rect()
        self.rect.x= posX
        self.rect.y=posY
        self.pixeles=1

        #Variable que obtendrá el inicio de un evento (en milisegundos)
        self.inicio=0

        #Mostrar animación
        self.animacion= False
        
        #Evita que se ejecute varias veces
        self.activado= False

        #Sí el bloque genera un objeto se activa
        self.generar= False 



    def update(self):

        #Si se activó la animación de colisión
        if self.animacion:

            #Movemos al objeto y verificamos si terminó la animación
            if self.mover(self.inicio):

                #Si es así detenemos la animación
                self.animacion= False

                #Luego cambiamos este atributo que indica que se generará un potenciador
                self.generar= True



    def mover(self, inicio):

        ahora= pg.time.get_ticks() 
        self.rect.y-= self.pixeles
         

        #Verificamos si el tiempo desde que inició el movimiento es mayor a 0.5 segundos
        if(ahora - inicio > 500):

            #Si es así entonces cambiamos la imagen del objeto  
            self.image= bloques["Bonus"][1] 

            #Y cambiamos la dirección en que se moverá
            self.pixeles=-1

        #Si el tiempo desde que inició el movimiento es mayor a 1 segundo, indicamos que ya terminó
        if(ahora - inicio > 1000):

            return True 



#Clase para los elementos de decoración
class Decoracion(Bloque):

    def __init__(self, imagen, posX, posY):

        super().__init__(imagen, posX,posY)
