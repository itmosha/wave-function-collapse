import json
import random

import pygame.image


class WFC:
    def __init__(self, set_number, x_tiles_count, y_tiles_count):
        f = open(f'tile_sets/set{set_number}/tile_config.json')

        self.set_number = set_number
        self.x_tiles_count = x_tiles_count
        self.y_tiles_count = y_tiles_count
        tiles_info = json.load(f)

        self.tiles_cnt = tiles_info['tiles_cnt']

        self.all_tiles_connections = []
        for i in range(self.tiles_cnt):
            self.all_tiles_connections.append(tiles_info['tiles'][f'tile{i + 1}'])

        self.tiles = [None] * self.tiles_cnt
        self.entropy = [[self.tiles_cnt for i in range(x_tiles_count)] for j in range(y_tiles_count)]
        self.connections = [[[-1, -1, -1, -1] for i in range(x_tiles_count)] for j in range(y_tiles_count)]
        self.render_grid = [[None for i in range(x_tiles_count)] for j in range(y_tiles_count)]

        f.close()

    def load_tiles(self):
        for i in range(self.tiles_cnt):
            self.tiles[i] = pygame.image.load(f'tile_sets/set{self.set_number}/tiles/tile{i + 1}.png')

    def all_possible_tiles(self, x, y):
        self.entropy[y][x] = 0

        tile_connections = [-1] * 4
        options = []

        if y > 0:
            tile_connections[0] = self.connections[y - 1][x][2]
        if x < self.x_tiles_count - 1:
            tile_connections[1] = self.connections[y][x + 1][3]
        if y < self.y_tiles_count - 1:
            tile_connections[2] = self.connections[y + 1][x][0]
        if x > 0:
            tile_connections[3] = self.connections[y][x - 1][1]
        for i in range(self.tiles_cnt):
            fits = True
            for j in range(4):
                if not (tile_connections[j] == self.all_tiles_connections[i][j] or tile_connections[j] == -1):
                    fits = False
                    break
            if fits:
                options.append(self.tiles[i])

        if len(options) == 0:
            options.append(self.tiles[0])

        return options

    def add_tile(self):
        min_entropy = self.tiles_cnt + 1

        for i in range(len(self.entropy)):
            min_entropy = min(min_entropy, min(self.entropy[i]))

        if min_entropy == self.tiles_cnt + 1:
            return False

        min_entropy_cells = []

        for i in range(self.y_tiles_count):
            for j in range(self.x_tiles_count):
                if self.entropy[i][j] == min_entropy:
                    min_entropy_cells.append((j, i))

        x, y = min_entropy_cells[random.randint(0, len(min_entropy_cells) - 1)]

        possible_tiles_list = self.all_possible_tiles(x, y)

        if not possible_tiles_list:
            return True

        chosen_tile = possible_tiles_list[random.randint(0, len(possible_tiles_list) - 1)]

        self.render_grid[y][x] = chosen_tile

        for i in range(self.tiles_cnt):
            if chosen_tile == self.tiles[i]:
                self.connections[y][x] = self.all_tiles_connections[i]

        self.entropy[y][x] = self.tiles_cnt + 1

        if x > 0:
            if self.entropy[y][x - 1] < self.tiles_cnt + 1:
                self.entropy[y][x - 1] = len(self.all_possible_tiles(x - 1, y))

        if y > 0:
            if self.entropy[y - 1][x] < self.tiles_cnt + 1:
                self.entropy[y - 1][x] = len(self.all_possible_tiles(x, y - 1))

        if x < self.x_tiles_count - 1:
            if self.entropy[y][x + 1] < self.tiles_cnt + 1:
                self.entropy[y][x + 1] = len(self.all_possible_tiles(x + 1, y))

        if y < self.y_tiles_count - 1:
            if self.entropy[y + 1][x] < self.tiles_cnt + 1:
                self.entropy[y + 1][x] = len(self.all_possible_tiles(x, y + 1))

        return True
