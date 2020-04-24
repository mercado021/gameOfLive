import sys, pygame
import numpy as np
import time

pygame.init()

width, height = 700, 700
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25 #color
screen.fill(bg)# Pinta la pantalla del color de la variable bg
nCy, nCx = 60,60

anchuraC = width / nCx
alturaC = height / nCy

#Matris de Estados de cada celada en el tablero. Vivas = 1; Muertas = 0
gameState = np.zeros((nCx, nCy))


gameState[5,3] = 1
gameState[5,4] = 1
gameState[5,5] = 1
gameState[1,3] = 1
gameState[21,21] = 1
gameState[22,22] = 1
gameState[22,23] = 1
gameState[21,23] = 1
gameState[20,23] = 1
gameState[8,8] = 1
gameState[8,7] = 1
gameState[8,9] = 1

#variable para el control del flujo de ejecución
pauseExect = False
while True:
#    pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    time.sleep(0.01)
    newGameState = np.copy(gameState)
    screen.fill(bg)
   
    ev = pygame.event.get()
    for event in ev:
        mouseClick = pygame.mouse.get_pressed()
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
            
        if sum(mouseClick) > 0: 
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / anchuraC)), int(np.floor(posY / alturaC))
            newGameState[celX, celY] = not mouseClick[2]

        

    for y in range(0,nCy):
        for x in range(0,nCx):
            if not pauseExect:
                #Calculamos el número de vecinos cercanos
                n_neigh = gameState[(x - 1) % nCx, (y - 1) % nCy] + \
                        gameState[(x + 1) % nCx, (y - 1) % nCy] + \
                        gameState[(x + 1) % nCx, (y + 1) % nCy] + \
                        gameState[(x - 1) % nCx, (y + 1) % nCy] + \
                        gameState[(x) % nCx    , (y + 1) % nCy] + \
                        gameState[(x) % nCx    , (y - 1) % nCy] + \
                        gameState[(x + 1) % nCx, (y) % nCy] +  \
                        gameState[(x - 1) % nCx, (y) % nCy]  
                #Reglas del juego 
                #regla 1: Una Célula Muerta, Con exactamente 3 vecinas vivas, "Revive"
                if gameState[x,y] == 0 and n_neigh == 3:
                    newGameState[x,y] = 1
                #Regla 2: Una Célula viva con menos de 2 o con mas de 3 vecinas vivas "Muere"
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x,y] = 0
            #Se crea el tablero
            poly = [((x)    * anchuraC,  y * alturaC),
                    ((x+1)  * anchuraC, y * alturaC),
                    ((x+1)  * anchuraC, (y+1) * alturaC),
                    ((x)    * anchuraC, (y+1) * alturaC)]
            if newGameState[x,y] == 0:
                pygame.draw.polygon(screen, (128,128,128), poly , 1)     
            else:
                pygame.draw.polygon(screen, (255,255,255), poly , 0)
    #actualizamos el estado del juego
    gameState = np.copy(newGameState)
    pygame.display.flip()
