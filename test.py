import pygame
import pygame.gfxdraw

screen = pygame.display.set_mode((600, 600))
controls = [

]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 0))
    pygame.display.update()
pygame.quit()