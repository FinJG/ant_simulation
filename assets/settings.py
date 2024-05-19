import pygame


class Settings:
    def __init__(self):
        self.FPS = 60
        self.SCREEN_WIDTH = 896
        self.SCREEN_HEIGHT = 896
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        self.dt = 1

        self.grid_size = 128
        self.tile_size = self.SCREEN_HEIGHT / self.grid_size

        self.nests = []
        self.foods = []

        self.keys = pygame.key.get_pressed()
        self.running = False
