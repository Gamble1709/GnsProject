import pygame as pg

from pygame.locals import *

from Sounds import jump


"""En muchas líneas de código puede que veas algo como colisionObjeto[0].método, esto es gracias a que cuandocreamos la variable de colisión como por ejemplo ColisionObjeto, esta al ser verdadera retorna una lista con los objetos que colisionó; con esto podemos saber un objeto en específico y además usar sus métodos y atributos sin problema.

Sabemos que en una lista el índice inicia en 0 y en la lista que retorna la variable colisionObjeto esto nos ayuda a saber el objeto con el que colisionó ya que por lo general los elementos de la lista se eliminan solos y siempre el índice 0 obtendrá un objeto, también podríamos usar el índice -1 ya que sería el último, aunque personalmente NO LO HE PROBADO, pienso que sería bastante útil esta última cuando la usemos con múltiples colisiones.

Ahora sabes la razón, por lo que si ves algo como colisionGoomba[0].iniciarMuerte() ya sabes que significa que la variable ColisionGoomba retorna una lista con los objetos tipo GOOMBA que haya encontrado o dependiendo de con quien quieres que colisione un objeto, posteriormente toma ese objeto de la lista y usa su atributo, por lo que si el objeto se llamara primerGoomba, usar la forma anterior es como si escribieramos primerGoomba.iniciarMuerte()"""


#nuevoProyectil=0

def detectarColisiones(personajePrincipal, goombas, caracoles, magos, bloquesSimples, tuberias, 
        bloquesBonus, potenciadores, proyectiles):

    #Variables que deben ser globales ya que se usan en el archivo Main.py
    global colisionSuelo, colisionBonus, colisionTuberia

    #Creando colisión con enemigos + Muerte del enemigo
    colisionGoomba= pg.sprite.spritecollide(personajePrincipal, goombas, False)

    if colisionGoomba:

         #Sí la posición en Y es menor al enemigo, significa que el personajePrincipal colisionó estando en el aire y cayendo encima del enemigo
        if personajePrincipal.saltar or (personajePrincipal.rect.bottom < colisionGoomba[0].rect.y):

            #Si el enemigo ya está muriendo(mostrando animación de muerte) no hacemos nada
            if colisionGoomba[0].muerte:

                pass


            #Si no, eliminamos al enemigo
            else:

                personajePrincipal.puntuacion+=500
                personajePrincipal.aumento= -30
                jump.play()
                colisionGoomba[0].iniciarMuerte()


        else:

            #Si colisionamos con el enemigo, pero el ya está muerto, no hacemos nada
            #Evita que la colisión continua se genere un bucle donde nunca desaparece
            if colisionGoomba[0].muerte or personajePrincipal.muerte:

                pass

            #Si el enemigo está vivo y colisiona de forma directa, destruimos el personajePrincipal
            else:

                #Si el personaje está en modo Sniper desactivamos ese modo y no eliminamos al jugador
                if personajePrincipal.francotirador:

                    personajePrincipal.francotirador= False

                    #Eliminamos el enemigo con el que colisionó
                    colisionGoomba[0].iniciarMuerte()

                else:

                    #Indicamos que el personaje va a ser destruido
                    personajePrincipal.muerte=True

                    #Obtenemos el tiempo en que inicia la muerte
                    personajePrincipal.inicio=pg.time.get_ticks()



    #Colisión del personaje con el caracol
    colisionCaracol= pg.sprite.spritecollide(personajePrincipal, caracoles, False)

    if colisionCaracol:

        for caracol in colisionCaracol:

            #Verificamos la forma en que colisionó el personaje con el caracol, si la posición Y del 
            #personaje es mayor a la del caracol entonces es que el jugador saltó sobre él
            if personajePrincipal.saltar:

                caracol.golpes+= 1
                personajePrincipal.puntuacion+= 200

                #Hacemos que el personaje salte de nuevo para que se muestre que colisionó
                personajePrincipal.rect.y-= 3
                personajePrincipal.aumento= -30

                #Verificamos si el caracol no estaba escondido antes
                if not caracol.escondido:

                    #Si es así, iniciamos el atributo que hace que se esconda el caracol
                    caracol.escondido= True

                    #Obtenemos el tiempo de inicio en que se escondió el caracol
                    caracol.inicioTiempoEscondido= pg.time.get_ticks()


            else:

                #Verificamos si el caracol estaba escondido, pues de no ser así el personaje será 
                #destruido pues colisionó de frente con el caracol
                if not caracol.escondido and not personajePrincipal.muerte:

                    personajePrincipal.muerte= True
                    personajePrincipal.inicio= pg.time.get_ticks()


                #Si el caracol estaba escondido 
                else:

                    #Solo podrá destruir el personaje al caracol si salta sobre él. si no
                    #hacemos que choque con él pero que nada pase

                    if not personajePrincipal.saltar:

                        if personajePrincipal.rect.right < caracol.rect.centerx:

                            personajePrincipal.rect.right= caracol.rect.left

                        else: personajePrincipal.rect.left= caracol.rect.right



    #colisión del personaje con el mago
    colisionMago= pg.sprite.spritecollide(personajePrincipal, magos, False) 

    if colisionMago:

        if colisionMago[0].muerte or personajePrincipal.muerte:

            pass

        else:

            if personajePrincipal.francotirador:

                personajePrincipal.francotirador= False
                colisionMago[0].muerte= True
                colisionMago[0].inicio= pg.time.get_ticks()

            else:
               
                personajePrincipal.muerte= True
                personajePrincipal.inicio= pg.time.get_ticks()



    #Colisiones del proyectil mientrás esté activo
    if personajePrincipal.activo:

        proyectil= proyectiles.sprites()[0]

        proyectilGoomba= pg.sprite.spritecollide(proyectil, goombas, False)
        proyectilMago= pg.sprite.spritecollide(proyectil, magos, False)
        proyectilCaracol= pg.sprite.spritecollide(proyectil, caracoles, False)
        proyectilTuberia= pg.sprite.spritecollide(proyectil, tuberias, False)
        proyectilBonus= pg.sprite.spritecollide(proyectil, bloquesBonus, False)


        #Colisión del proyectil con un objeto del grupo goombas 
        if proyectilGoomba:

            colisionProyectil[0].iniciarMuerte()

        
        #Colisión del proyectil con un objeto del grupo magos 
        if proyectilMago and not proyectilMago[0].muerte:

            personajePrincipal.puntuacion+=1000
            proyectilMago[0].muerte= True
            proyectilMago[0].inicio= pg.time.get_ticks()


        #Colisión del proyectil con objeto del grupo caracoles
        if proyectilCaracol:

            for caracol in proyectilCaracol:

                #Si el caracol no está muriendo entonces llamamos al método que inicia su muerte
                if not caracol.muerte: caracol.iniciarMuerte()


        #Colisión del proyectil con cualquier objeto
        if proyectilTuberia or proyectilBonus or proyectilGoomba or proyectilMago or proyectilCaracol:

            personajePrincipal.activo= False
            proyectil.kill()


   #Condicional que se encarga del tiempo antes de morir y de destruir el objeto
    if personajePrincipal.muerte:

        personajePrincipal.tiempoDeMuerte()



    #Colisión con Bloque colisionBonus            
    colisionBonus= pg.sprite.spritecollide(personajePrincipal, bloquesBonus, False)

    if colisionBonus:

        if (personajePrincipal.rect.right < colisionBonus[0].rect.centerx and 
                personajePrincipal.rect.top < colisionBonus[0].rect.centery + 5):

            personajePrincipal.rect.right= colisionBonus[0].rect.left

        if (personajePrincipal.rect.left > colisionBonus[0].rect.centerx and 
                personajePrincipal.rect.top < colisionBonus[0].rect.centery - 5):

            personajePrincipal.rect.left= colisionBonus[0].rect.right

        if personajePrincipal.rect.top > colisionBonus[0].rect.centery :

            #Esto para que al colisionar baje y no continue subiendo
            personajePrincipal.rect.y += 10
            personajePrincipal.aumento=0

            if not colisionBonus[0].animacion and not colisionBonus[0].activado:
                
                colisionBonus[0].animacion=True
                colisionBonus[0].activado= True
                colisionBonus[0].inicio= pg.time.get_ticks()

        if personajePrincipal.rect.bottom < colisionBonus[0].rect.centery - 8:

            personajePrincipal.saltar=False
            personajePrincipal.rect.bottom=colisionBonus[0].rect.top + 1
            personajePrincipal.aumento= -30



    #Colisión del personaje con el suelo
    colisionSuelo= pg.sprite.spritecollide(personajePrincipal, bloquesSimples, False)

    if colisionSuelo and not personajePrincipal.muerte or colisionSuelo and not personajePrincipal.muerte and colisionCaracol:

        personajePrincipal.saltar=False
        personajePrincipal.aumento=-30
        personajePrincipal.rect.bottom= colisionSuelo[0].rect.top+1


    #Prueba

    #if colisionCaracol and colisionSuelo:

    #    personajePrincipal.rect.bottom = colisionSuelo[0].rect.top + 3

    if potenciadores:
    
        for arma in potenciadores:

            #Colisión del arma con el bloque bonus
            armaBonus= pg.sprite.spritecollide(arma, bloquesBonus, False)

            if armaBonus:

                #Evitar que el sprite traspase el bloque bonus
                if arma.rect.bottom >= armaBonus[0].rect.top:

                    arma.rect.bottom = armaBonus[0].rect.top - 3
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

    if goombas: #Verificamos que el grupo no esté vacío

        for enemigo in goombas: #Iteramos en el grupo obteniendo cada objeto

            colisionSueloEnemigo= pg.sprite.spritecollide(enemigo, bloquesSimples, False)

            if colisionSueloEnemigo and not enemigo.muerte: #Si hay colisión se retorna una lista con los objetos colisionados. (Verificamos que el enemigo no esté muerto para evitar cambios de posición) 
                
                if enemigo.rect.bottom >= colisionSueloEnemigo[0].rect.top:

                    enemigo.caer=False 
                    enemigo.rect.bottom = colisionSueloEnemigo[0].rect.top + 1

            else:

                enemigo.caer=True



    #Colisión con potenciadores
    personajeArmas= pg.sprite.spritecollide(personajePrincipal, potenciadores, True)

    if personajeArmas:

        personajePrincipal.puntuacion+=1000
        personajePrincipal.francotirador=True
        #personajeArmas[0].kill()



    #Colisión tubería
    colisionTuberia= pg.sprite.spritecollide(personajePrincipal, tuberias, False)

    if colisionTuberia:

        #Comprobamos si está encima de la tubería
        if personajePrincipal.rect.bottom < colisionTuberia[0].rect.centery - 5:

            personajePrincipal.rect.bottom = colisionTuberia[0].rect.top +1
            personajePrincipal.saltar=False
            personajePrincipal.aumento= -30

        
        #Si no lo está, verificamos si ha colisionado con uno de los lados del sprite (left, right)
        else:

            if personajePrincipal.rect.right <= (colisionTuberia[0].rect.left + 20): 

                #print(colisionTuberia[0].rect.left)

                personajePrincipal.rect.right= colisionTuberia[0].rect.left


            elif personajePrincipal.rect.left >= (colisionTuberia[0].rect.right - 20):

                personajePrincipal.rect.left= colisionTuberia[0].rect.right

