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
        self.unclaimed_nests = []

        self.ants_to_die = []
        self.foods = []

        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

        self.paths_to_food = set()
        self.displaying_path_index = 0
        self.running = False
