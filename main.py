import pygame
import random
import time

SCREEN_WIDTH, SCREEN_HEIGHT = 960, 640
XLEN, YLEN = SCREEN_WIDTH // 32, SCREEN_HEIGHT // 32
TILES_CNT = 6

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wave function collapse')

tiles = [None] * TILES_CNT
entropy = [[6 for i in range(XLEN)] for j in range(YLEN)]
connections = [[[-1, -1, -1, -1] for i in range(XLEN)] for j in range(YLEN)]
tiles_grid = [[None for i in range(XLEN)] for j in range(YLEN)]


def load_tiles():
    for i in range(TILES_CNT):
        tiles[i] = pygame.image.load(f'tiles/tile{i+1}.png')


def refresh_entropy(x, y):
    cons = [-1] * 4
    entropy[y][x] = 0
    # Up, right, down, left

    if y > 0:
        cons[0] = connections[y - 1][x][2]
    if x < XLEN - 1:
        cons[1] = connections[y][x + 1][3]
    if y < YLEN - 1:
        cons[2] = connections[y + 1][x][0]
    if x > 0:
        cons[3] = connections[y][x - 1][1]

    # 4)
    # Select all the tiles that fit on that place

    options = []

    if (cons[0] == 1 or cons[0] == -1) and (cons[1] == 0 or cons[1] == -1) and (cons[2] == 0 or cons[2] == -1) and (
            cons[3] == 1 or cons[3] == -1):
        entropy[y][x] += 1
    if (cons[0] == 1 or cons[0] == -1) and (cons[1] == 1 or cons[1] == -1) and (cons[2] == 0 or cons[2] == -1) and (
            cons[3] == 0 or cons[3] == -1):
        entropy[y][x] += 1
    if (cons[0] == 0 or cons[0] == -1) and (cons[1] == 1 or cons[1] == -1) and (cons[2] == 1 or cons[2] == -1) and (
            cons[3] == 0 or cons[3] == -1):
        entropy[y][x] += 1
    if (cons[0] == 0 or cons[0] == -1) and (cons[1] == 0 or cons[1] == -1) and (cons[2] == 1 or cons[2] == -1) and (
            cons[3] == 1 or cons[3] == -1):
        entropy[y][x] += 1
    if (cons[0] == 0 or cons[0] == -1) and (cons[1] == 1 or cons[1] == -1) and (cons[2] == 0 or cons[2] == -1) and (
            cons[3] == 1 or cons[3] == -1):
        entropy[y][x] += 1
    if (cons[0] == 1 or cons[0] == -1) and (cons[1] == 0 or cons[1] == -1) and (cons[2] == 1 or cons[2] == -1) and (
            cons[3] == 0 or cons[3] == -1):
        entropy[y][x] += 1


def add_tile():
    # 1)
    # Find the cell with the least entropy.
    # Already filled cells are represented as tiles number + 1 (in this case 5 + 1 = 6)
    # Consider the case where all the cells are already filled, so we return in that case

    min_entropy = 7
    for i in range(len(entropy)):
        min_entropy = min(min_entropy, min(entropy[i]))

    if min_entropy == 7:
        return True

    # 2)
    # Take a random cell with the least entropy (its coords)

    min_entropy_cells = []
    for i in range(SCREEN_HEIGHT // 32):
        for j in range(SCREEN_WIDTH // 32):
            if entropy[i][j] == min_entropy:
                min_entropy_cells.append((j, i))
                break

    x, y = min_entropy_cells[random.randint(0, len(min_entropy_cells) - 1)]

    # 3)
    # Find out what shape fits every edge of the tile
    # 0 if is has no connections
    # 1 if it has a connection
    # -1 if there is no tile connected

    cons = [-1] * 4
    # Up, right, down, left

    if y > 0:
        cons[0] = connections[y - 1][x][2]
    if x < XLEN - 1:
        cons[1] = connections[y][x + 1][3]
    if y < YLEN - 1:
        cons[2] = connections[y + 1][x][0]
    if x > 0:
        cons[3] = connections[y][x - 1][1]

    # 4)
    # Select all the tiles that fit on that place

    options = []

    if (cons[0] == 1 or cons[0] == -1) and (cons[1] == 0 or cons[1] == -1) and (cons[2] == 0 or cons[2] == -1) and (
            cons[3] == 1 or cons[3] == -1):
        options.append(tiles[0])
    if (cons[0] == 1 or cons[0] == -1) and (cons[1] == 1 or cons[1] == -1) and (cons[2] == 0 or cons[2] == -1) and (
            cons[3] == 0 or cons[3] == -1):
        options.append(tiles[1])
    if (cons[0] == 0 or cons[0] == -1) and (cons[1] == 1 or cons[1] == -1) and (cons[2] == 1 or cons[2] == -1) and (
            cons[3] == 0 or cons[3] == -1):
        options.append(tiles[2])
    if (cons[0] == 0 or cons[0] == -1) and (cons[1] == 0 or cons[1] == -1) and (cons[2] == 1 or cons[2] == -1) and (
            cons[3] == 1 or cons[3] == -1):
        options.append(tiles[3])
    if (cons[0] == 0 or cons[0] == -1) and (cons[1] == 1 or cons[1] == -1) and (cons[2] == 0 or cons[2] == -1) and (
            cons[3] == 1 or cons[3] == -1):
        options.append(tiles[4])
    if (cons[0] == 1 or cons[0] == -1) and (cons[1] == 0 or cons[1] == -1) and (cons[2] == 1 or cons[2] == -1) and (
            cons[3] == 0 or cons[3] == -1):
        options.append(tiles[5])

    # 5)
    # Randomly choose a tile which will be placed on that spot

    assert len(options) > 0, 'Empty options list'

    chosen = options[random.randint(0, len(options) - 1)]
    tiles_grid[y][x] = chosen

    # 6)
    # Refresh the connections list for that cell

    if chosen == tiles[0]:
        connections[y][x] = [1, 0, 0, 1]
    elif chosen == tiles[1]:
        connections[y][x] = [1, 1, 0, 0]
    elif chosen == tiles[2]:
        connections[y][x] = [0, 1, 1, 0]
    elif chosen == tiles[3]:
        connections[y][x] = [0, 0, 1, 1]
    elif chosen == tiles[4]:
        connections[y][x] = [0, 1, 0, 1]
    elif chosen == tiles[5]:
        connections[y][x] = [1, 0, 1, 0]
    # 7)
    # Set the added cell entropy to 6 and refresh nearby cell's entropy

    entropy[y][x] = 7

    if x > 0:
        if entropy[y][x - 1] < 7:
            refresh_entropy(x - 1, y)
    if y > 0:
        if entropy[y - 1][x] < 7:
            refresh_entropy(x, y - 1)
    if x < XLEN - 1:
        if entropy[y][x + 1] < 7:
            refresh_entropy(x + 1, y)
    if y < YLEN - 1:
        if entropy[y + 1][x] < 7:
            refresh_entropy(x, y + 1)

    return True


if __name__ == "__main__":
    load_tiles()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        screen.fill((255, 255, 255))

        add_tile()
        time.sleep(0.02)

        for i in range(YLEN):
            for j in range(XLEN):
                if tiles_grid[i][j]:
                    screen.blit(tiles_grid[i][j], (j * 32, i * 32))

        pygame.display.update()
