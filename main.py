import pygame

from settings import Settings


class Game(Settings):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.new_game()

    def events(self):
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.KEYDOWN:
                self.controls(event)

        if self.keys[pygame.K_w]:
            self.FPS += 0.1 * self.dt

        if self.keys[pygame.K_s]:
            self.FPS -= 0.1 * self.dt

        # self.select_food()
        self.select_path()

    def update(self):
        for nest in self.nests:
            for ant in nest.ants:
                ant.update()
            nest.update()

        for nest in self.nests:
            for ant in self.ants_to_die:
                self.foods.append(self.Food(self, ant.pos.x, ant.pos.y, int(ant.total_ate * 0.8)))
                if ant in nest.ants:
                    nest.ants.remove(ant)

        self.ants_to_die.clear()

        for food in self.foods:
            food.update()

        self.dt = self.clock.tick(self.FPS)

        # debug tools
        pygame.display.set_caption(f'{self.clock.get_fps():.1f} {self.FPS}')

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
