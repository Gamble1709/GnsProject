import pygame as pg

from pygame.locals import *

from Sounds import jump


"""En muchas líneas de código puede que veas algo como colisionObjeto[0].método, esto es gracias a que cuandocreamos la variable de colisión como por ejemplo ColisionObjeto, esta al ser verdadera retorna una lista con los objetos que colisionó; con esto podemos saber un objeto en específico y además usar sus métodos y atributos sin problema.

Sabemos que en una lista el índice inicia en 0 y en la lista que retorna la variable colisionObjeto esto nos ayuda a saber el objeto con el que colisionó ya que por lo general los elementos de la lista se eliminan solos y siempre el índice 0 obtendrá un objeto, también podríamos usar el índice -1 ya que sería el último, aunque personalmente NO LO HE PROBADO, pienso que sería bastante útil esta última cuando la usemos con múltiples colisiones.

Ahora sabes la razón, por lo que si ves algo como colisionGoomba[0].iniciarMuerte() ya sabes que significa que la variable ColisionGoomba retorna una lista con los objetos tipo GOOMBA que haya encontrado o dependiendo de con quien quieres que colisione un objeto, posteriormente toma ese objeto de la lista y usa su atributo, por lo que si el objeto se llamara primerGoomba, usar la forma anterior es como si escribieramos primerGoomba.iniciarMuerte()"""


nuevoProyectil=0

def detectarColisiones(personajePrincipal, goombas, caracoles, magos, bloquesSimples, tuberias, 
        bloquesBonus):

    global colisionSuelo, nuevoProyectil, colisionBonus

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
                personajePrincipal.aumento=-30
                jump.play()
                colisionGoomba[0].iniciarMuerte()


        else:

            #Si colisionamos con el enemigo, pero el ya está muerto, no hacemos nada
            #Evita que la colisión continua se genere un bucle donde nunca desaparece
            if colisionGoomba[0].muerte or personajePrincipal.muerte:

                pass

            #Si el enemigo está vivo y colisiona de forma directa, destruimos el personajePrincipal
            else:

                if personajePrincipal.francotirador:

                    personajePrincipal.francotirador= False
                    colisionGoomba[0].iniciarMuerte()

                else:

                    personajePrincipal.muerte=True
                    personajePrincipal.inicio=pg.time.get_ticks()



    colisionCaracol= pg.sprite.spritecollide(personajePrincipal, caracoles, False)

    if colisionCaracol:

        if colisionCaracol[0].muerte:

            pass

        else:

            if personajePrincipal.rect.bottom < colisionCaracol[0].rect.bottom:

                if not colisionCaracol[0].escondido:

                    colisionCaracol[0].escondido=True
                    colisionCaracol[0].tiempoEscondido= pg.time.get_ticks()
                    personajePrincipal.aumento= -30

                else:

                    colisionCaracol[0].iniciarMuerte()                    

            else:

                if not colisionCaracol[0].escondido:

                    personajePrincipal.muerte= True
                    personajePrincipal.inicio= pg.time.get_ticks()

                else:

                    colisionCaracol[0].iniciarMuerte()



    #colisión del personaje con el mago
    colisionMago= pg.sprite.spritecollide(personajePrincipal, magos, False) 

    if colisionMago:

        if colisionMago[0].muerte or personajePrincipal.muerte:

            pass

        else:

            if personajePrincipal.francotirador:

                personajePrincipal.francotirador= False
                colisionMago[0].iniciarMuerte()
                #nuevoMago.muerte= True
                #nuevoMago.inicio= pg.time.get_ticks()

            else:
               
                personajePrincipal.muerte= True
                personajePrincipal.inicio= pg.time.get_ticks()



    #Colisiones del proyectil mientrás esté activo
    if personajePrincipal.activo:

        colisionProyectil= pg.sprite.spritecollide(nuevoProyectil, goombas, False)
        proyectilMago= pg.sprite.spritecollide(nuevoProyectil, magos, False)
        proyectilTuberia= pg.sprite.spritecollide(nuevoProyectil, tuberias, False)
        proyectilBonus= pg.sprite.spritecollide(nuevoProyectil, bloquesBonus, False)

        if colisionProyectil:

            personajePrincipal.activo= False
            nuevoProyectil.kill()
            colisionProyectil[0].iniciarMuerte()

        if proyectilMago:

            if proyectilMago[0].rect.top <= 320:

                personajePrincipal.activo= False
                nuevoProyectil.kill()
                proyectilMago[0].iniciarMuerte()
                personajePrincipal.puntuacion+=1000


        if proyectilTuberia or proyectilBonus:

            personajePrincipal.activo= False
            nuevoProyectil.kill()


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
