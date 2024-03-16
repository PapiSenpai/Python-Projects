#import pygame_widgets
#import pygame
#from pygame_widgets.toggle import Toggle

#pygame.init()
#win = pygame.display.set_mode((1000, 600))

#toggle = Toggle(win, 100, 100, 100, 20) #(display, x, y, barlength, dot size)

#run = True
#while run:
#    events = pygame.event.get()
#    for event in events:
#        if event.type == pygame.QUIT:
#            pygame.quit()
#            run = False
#            quit()

#    win.fill((255, 255, 255))

#    pygame_widgets.update(events)
#    pygame.display.update()

import pygame

class Cell:
    def __init__(self):
        self.clicked = False

grid_size = 50 #use this to implement user options to make grid as large as they would like
board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]

pygame.init()
window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.MOUSEBUTTONDOWN:    
            if event.button == 1:
                row = event.pos[1] // 20
                col = event.pos[0] // 20
                board[row][col].clicked = True

    window.fill(0)
    for iy, rowOfCells in enumerate(board):
        for ix, cell in enumerate(rowOfCells):
            color = (64, 64, 64) if cell.clicked else (164, 164, 164) #makes it possible for boxes to change color (make it so that it changes to x or O)
            pygame.draw.rect(window, color, (ix*20+1, iy*20+1, 18, 18)) #mess with this to change the size of boxes
    pygame.display.flip()

pygame.quit()
exit()