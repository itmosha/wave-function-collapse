import pygame
import time
from wfc import WFC

SCREEN_WIDTH, SCREEN_HEIGHT = 960, 640
X_CELLS_COUNT, Y_CELLS_COUNT = SCREEN_WIDTH // 32, SCREEN_HEIGHT // 32
SET_NUMBER = 1

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Wave function collapse')

    wfc = WFC(SET_NUMBER, X_CELLS_COUNT, Y_CELLS_COUNT)
    wfc.load_tiles()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        screen.fill((255, 255, 255))
        wfc.add_tile()

        for i in range(Y_CELLS_COUNT):
            for j in range(X_CELLS_COUNT):
                if wfc.render_grid[i][j]:
                    screen.blit(wfc.render_grid[i][j], (j * 32, i * 32))

        pygame.display.update()
        time.sleep(0.01)
