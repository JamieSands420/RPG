import pygame
import os
import math

# Pygame init #
scr = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
pygame.init()
font = pygame.font.SysFont(None, 36)

# Variables init #
playerCor = [0, 0]

worldData = []
worldRects = []
x_offset = 0
y_offset = 0

TEXTURES = []

# load textures #

print("Loading textures..")
for file_name in os.listdir(f"{__file__[:-7]}/Resources/Textures"):
    TEXTURES.append(pygame.transform.scale(pygame.image.load(f"{__file__[:-7]}/Resources/Textures/{file_name}").convert(), (40, 40)))
    print(f"{file_name} loaded..")

# Fill world #
for x in range(19):
    row = []
    for y in range(19):
        row.append(pygame.Rect(x * 40, y * 40, 40, 40))
    worldRects.append(row)
    
# Functions init #
def load_level(level):
    with open(f"{__file__[:-7]}/Resources/Levels/{level}.txt", "r") as file:
        for line in file:
            row = [int(char) for char in line.strip()]
            worldData.append(row)
            
# load initial level
load_level("4")


fps = 0
# MAIN GAME LOOP #
run = True
while run:

    fpstext = font.render(str(math.ceil(fps)), True, (255, 255, 255))

    # Move #
    for y in range(len(worldRects)):
        for x in range(len(worldRects[y])):
            i = y * 19 + x
            
            x_offset = i % 19 + playerCor[0] // 40
            y_offset = i // 19 + playerCor[1] // 40

            worldRects[x][y].x = 0 - playerCor[0] + x_offset * 40 
            worldRects[x][y].y = 0 - playerCor[1] + y_offset * 40
        
    # Controls #
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerCor[1] -= 2

    elif keys[pygame.K_s]:
        playerCor[1] += 2

    if keys[pygame.K_a]:
        playerCor[0] -= 2

    elif keys[pygame.K_d]:
        playerCor[0] += 2

    # Draw loop #
    scr.fill((0, 0, 0))

    # draws the world
    for x in range(len(worldRects)):
        for y in range(len(worldRects[x])):

            # clamp for edges (also stops negative x,y offset from wrapping the world)
            if 0 <= y + y_offset < len(worldData) and 0 <= x + x_offset < len(worldData[0]):
                try:
                    tile = worldData[y + y_offset][x + x_offset]
                except IndexError:
                    continue
            else:
                continue

            scr.blit(TEXTURES[tile], worldRects[x][y])
    
    pygame.draw.rect(scr, (0, 255, 0), ((350, 350), (40, 40)))
    
    scr.blit(fpstext, (0, 0))
    pygame.display.flip()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    clock.tick(120)
    fps = clock.get_fps()
