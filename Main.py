import pygame
import math

scr = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
pygame.init()

playerCor = [0, 0]

x_offset = 0
y_offset = 0

world_data = []
loaded_world = []

for y in range(19):
    row = []
    for x in range(19):
        row.append(pygame.Rect(x * 40, y * 40, 40, 40))
    loaded_world.append(row)


def load_level(level):
    with open(f"{__file__[:-7]}/Resources/Levels/{level}.txt", "r") as file:
        for line in file:
            row = [int(char) for char in line.strip()]
            world_data.append(row)

load_level("2")

run = True
while run:

    x_offset = 0
    y_offset = 0
    
    # move the world
    for y in range(len(loaded_world)):
        for x in range(len(loaded_world[y])):
            i = y * 19 + x
            
            x_offset = i % 19 + playerCor[0] // 40
            y_offset = i // 19 + playerCor[1] // 40

            loaded_world[x][y].x = 0 - playerCor[0] + x_offset * 40 + 150
            loaded_world[x][y].y = 0 - playerCor[1] + y_offset * 40 + 150

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

    # draws the world
    for y in range(len(loaded_world)):
        for x in range(len(loaded_world[y])):
            tile = world_data[y + x_offset][x + y_offset]
            
            if tile == 0:
                pygame.draw.rect(scr, (255, 0, 0), loaded_world[y][x])
                
            elif tile == 1:
                pygame.draw.rect(scr, (0, 0, 255), loaded_world[y][x])
                
            elif tile == 2:
                pygame.draw.rect(scr, (255, 0, 255), loaded_world[y][x])
                
            elif tile == 3:
                pygame.draw.rect(scr, (0, 255, 255), loaded_world[y][x])
                
            elif tile == 4:
                pygame.draw.rect(scr, (100, 100, 255), loaded_world[y][x])
    
    pygame.draw.rect(scr, (0, 255, 0), ((500, 500), (40, 40)))

    pygame.display.flip()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    clock.tick(120)

pygame.quit()
