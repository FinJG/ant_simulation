import sys
from random import randint

import pygame

import assets


class Game(assets.Settings):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.new_game()

    def new_game(self):
        self.nests.clear()
        self.foods.clear()

        col = ((255, 0, 0), (0, 0, 255))
        for i in range(1):
            self.nests.append(assets.AntNest(self,
                                             randint(0, self.grid_size),
                                             randint(0, self.grid_size),
                                             1,
                                             col[i]
                                             ))

        for i in range(3200):
            self.foods.append(assets.Food(self,
                                          randint(0, self.grid_size),
                                          randint(0, self.grid_size),
                                          5))



    def events(self):
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

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

        if self.keys[pygame.K_w]:
            self.FPS += 0.1 * self.dt

        if self.keys[pygame.K_s]:
            self.FPS -= 0.1 * self.dt

        # pygame.display.set_caption(f' ants: {[[ant.health for ant in nest.ants] for nest in self.nests]}')

        for food in self.foods:
            if food.pos == (self.mouse_pos[0] // self.tile_size, self.mouse_pos[1] // self.tile_size):
                pygame.display.set_caption(f'{food.chunks} ants: {[[ant.health for ant in nest.ants] for nest in self.nests]}')
            # else:
        self.paths_to_food = []
        for nest in self.nests:
            for ant in nest.ants:
                if ant.pheromones_to_food:
                    self.paths_to_food.append(ant.pheromones_to_food)

        if self.displaying_path_index > len(self.paths_to_food) - 1:
            self.displaying_path_index = len(self.paths_to_food) - 1


    def update(self):
        for nest in self.nests:
            for ant in nest.ants:
                ant.update()
            nest.update()

        for nest in self.nests:
            for ant in self.ants_to_die:
                self.foods.append(assets.Food(self, ant.pos.x, ant.pos.y, int(ant.total_ate * 0.8)))
                if ant in nest.ants:
                    nest.ants.remove(ant)

        self.ants_to_die.clear()

        for food in self.foods:
            food.update()

        self.dt = self.clock.tick(self.FPS)

        # debug tools
        pygame.display.set_caption(f'{self.clock.get_fps():.1f} {self.FPS}')
        # pygame.display.set_caption(f'ants: {sum([len(nest.ants) for nest in self.nests])}, total_food: {[nest.stored_food for nest in self.nests]}')
        # pygame.display.set_caption(f'total_food: {[nest.stored_food for nest in self.nests]} ants: {[ant.health for ant in nest.ants for nest in self.nests]}')

    def draw(self):
        self.screen.fill((235, 235, 235))

        for nest in self.nests:
            for ant in nest.ants:
                ant.draw()
            nest.draw()

        for food in self.foods:
            food.draw()

        if self.paths_to_food:
            if len(self.paths_to_food[self.displaying_path_index]) > 2:
                pygame.draw.lines(self.screen, (0, 255, 0), False, self.paths_to_food[self.displaying_path_index], 2)

        pygame.display.update()

    def run(self):
        while True:
            self.events()
            if self.running:
                self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
