import pygame
pygame.init()
#use this to integrate into Tic Tac Toe game
# Create the game window
Background = pygame.display.set_mode((900, 900))

# Draw the grid
for i in range(0, 900, 300):
    pygame.draw.line(Background, (255, 255, 255), (0, i), (900, i))  # Horizontal lines
    pygame.draw.line(Background, (255, 255, 255), (i, 0), (i, 900))  # Vertical lines

pygame.display.update()

# Keep the display active
while pygame.event.wait().type != pygame.QUIT:
    pass

