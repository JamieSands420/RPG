import pygame
import math

scr = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
pygame.init()

playerCor = [0, 0]

x_offset = 0
y_offset = 0

loaded_world = []

for i in range(19 * 19):
    loaded_world.append(pygame.Rect((0, 0), (40, 40)))

run = True
while run:
    
    # move the world
    for i in range(len(loaded_world)):
        x_offset = i % 19 + math.floor(playerCor[0] / 40)
        y_offset = i // 19 + math.floor(playerCor[1] / 40)

        loaded_world[i].x = 0 - playerCor[0] + x_offset * 40 + 0
        loaded_world[i].y = 0 - playerCor[1] + y_offset * 40 + 0

    x_offset = 0
    y_offset = 0

    # controls
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        playerCor[1] -= 1

    if keys[pygame.K_s]:
        playerCor[1] += 1

    if keys[pygame.K_a]:
        playerCor[0] -= 1

    if keys[pygame.K_d]:
        playerCor[0] += 1

    # draw
    scr.fill((0, 0, 0))

    switch = True
    for i in range(len(loaded_world)):
        if switch == True:
            pygame.draw.rect(scr, (255, 0, 0), loaded_world[i])
        else:
            pygame.draw.rect(scr, (0, 0, 255), loaded_world[i])
        switch = not switch

    pygame.draw.rect(scr, (0, 255, 0), ((350, 350), (40, 40)))

    pygame.display.flip()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    clock.tick(120)

pygame.quit()
