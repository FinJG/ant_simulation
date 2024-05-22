import pygame
from random import randint
import sys

import assets


class Settings:
    def __init__(self):
        # classes
        self.Food = assets.Food
        self.Ant = assets.Ant
        self.AntNest = assets.AntNest

        # display settings
        self.FPS = 60
        self.SCREEN_WIDTH = 896
        self.SCREEN_HEIGHT = 896
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        self.dt = 1

        # game settings
        self.grid_size = 128
        self.tile_size = self.SCREEN_HEIGHT / self.grid_size

        self.nests = []
        self.unclaimed_nests = []

        self.ants_to_die = []
        self.foods = []

        self.paths_to_food = set()
        self.displaying_path_index = 0
        self.running = False

        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

    def new_game(self):
        self.nests.clear()
        self.foods.clear()

        col = ((255, 0, 0), (0, 0, 255))
        for i in range(1):
            self.nests.append(self.AntNest(self,
                                           randint(0, self.grid_size),
                                           randint(0, self.grid_size),
                                           1,
                                           col[i]
                                           ))

        for i in range(3200):
            self.foods.append(self.Food(self,
                                        randint(0, self.grid_size),
                                        randint(0, self.grid_size),
                                        5))

    def controls(self, event):
        if event.key == pygame.K_ESCAPE:
            self.quit()

        if event.key == pygame.K_SPACE:
            self.running = not self.running

        if event.key == pygame.K_r:
            self.new_game()

        if event.key == pygame.K_LEFTBRACKET:
            if self.displaying_path_index - 1 >= 0:
                self.displaying_path_index -= 1

        if event.key == pygame.K_RIGHTBRACKET:
            if self.displaying_path_index + 1 < len(self.paths_to_food):
                self.displaying_path_index += 1

    def select_path(self):
        self.paths_to_food = []
        for nest in self.nests:
            for ant in nest.ants:
                if ant.pheromones_to_food:
                    self.paths_to_food.append(ant.pheromones_to_food)

        if self.displaying_path_index > len(self.paths_to_food) - 1:
            self.displaying_path_index = len(self.paths_to_food) - 1

    def select_food(self):
        for food in self.foods:
            if food.pos == (self.mouse_pos[0] // self.tile_size, self.mouse_pos[1] // self.tile_size):
                pygame.display.set_caption(
                    f'{food.chunks} ants: {[[ant.health for ant in nest.ants] for nest in self.nests]}')


