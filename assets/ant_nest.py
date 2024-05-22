from random import randint, choice
from math import dist

import pygame


class Ant:
    def __init__(self, nest, game, pos):
        self.game = game

        self.nests = [nest]
        self.current_nest = self.nests[0]

        self.in_nest = True
        self.pos = pygame.Vector2(*pos)
        self.walking_direction = pygame.Vector2()

        self.pheromones = []

        self.trail_index = 0
        self.pheromones_to_food = []

        self.total_steps = 0
        self.steps = 0
        self.col = (randint(0, 255), randint(0, 255), randint(0, 255))

        self.max_health = 10
        self.health = self.max_health

        # standard is 60FPS so 60 * 30 should roughly be 30 seconds
        one_second = 60
        self.max_eat_interval = one_second * 15
        self.eat_interval = self.max_eat_interval
        self.total_ate = 0

        self.fighting_skill = randint(1, 10)

        self.has_food = False

    def look_for_food(self):
        """
        looks at the ants adjacent tiles for food
        and returns the food if found, else it returns None
        :returns: Food if food is found, else None
        """
        for ix in range(-1, 2):
            for iy in range(-1, 2):
                if (ix, iy) != (0, 0):
                    jx = (self.pos.x + ix)
                    jy = (self.pos.y + iy)
                    for food in self.game.foods:
                        if food.pos == (jx, jy):
                            return food
        return None

    def look_for_nest(self, nests):
        for ix in range(-1, 2):
            for iy in range(-1, 2):
                if (ix, iy) != (0, 0):
                    jx = (self.pos.x + ix)
                    jy = (self.pos.y + iy)
                    for nest in nests:
                        # if it has, the ant will go inside
                        if (jx, jy) == nest.pos:
                            if nest.unclaimed:
                                if self.current_nest.col != nest.col:
                                    nest.col = self.current_nest.col
                                    nest.unclaimed = False

                            self.current_nest = nest
                            self.in_nest = True
                            self.steps = 0
                            return

    def look_for_ant(self):
        for ix in range(-1, 2):
            for iy in range(-1, 2):
                if (ix, iy) != (0, 0):
                    jx = (self.pos.x + ix)
                    jy = (self.pos.y + iy)
                    for nest in self.game.nests:
                        if nest.col != self.current_nest.col:
                            for ant in nest.ants:
                                if (jx, jy) == ant.pos:
                                    if randint(1, self.fighting_skill) == 1:
                                        ant.health -= 1
                                        return True
        return  False

    def remove_loops(self, line):
        return line[:line.index(self.pos * self.game.tile_size) + 1]

    def move(self) -> None:
        """
        this function controls the "random" movement of the ant
        """
        # chance to change x direction
        if randint(1, 4) == 1:
            if self.walking_direction.x == 0:
                self.walking_direction.x = choice((-1, 1))
            else:
                self.walking_direction.x = 0

        # chance to change y direction
        if randint(1, 4) == 1:
            if self.walking_direction.y == 0:
                self.walking_direction.y = choice((-1, 1))
            else:
                self.walking_direction.y = 0

        # chance to move the ant in its facing direction
        # if randint(1, 8) == 1:
        if 0 <= (self.pos.x + self.walking_direction.x) * self.game.tile_size < self.game.SCREEN_WIDTH:
            if 0 <= (self.pos.y + self.walking_direction.y) * self.game.tile_size < self.game.SCREEN_HEIGHT:
                if self.walking_direction.x or self.walking_direction.y:
                    self.pos += self.walking_direction

                    self.total_steps += 1
                    self.steps += 1


                    # check if the ant has landed on a path that leads to food
                    for nest in self.nests:
                        for ant in nest.ants:
                            if ant.pheromones_to_food:
                                if self.pos * self.game.tile_size in ant.pheromones_to_food:
                                    for food in self.game.foods:
                                        if ant.pheromones_to_food in food.paths_to:

                                        # if it has, it will now follow the path

                                            # if randint(1, 4) == 1:
                                                self.pheromones_to_food.clear()

                                                self.trail_index = ant.pheromones_to_food.index(
                                                    self.pos * self.game.tile_size)

                                                self.pheromones_to_food.extend(self.pheromones.copy() + ant.pheromones_to_food.copy()[self.trail_index:])

                                                self.trail_index = len(self.pheromones_to_food) - len(ant.pheromones_to_food) + self.trail_index
                                                self.pheromones.clear()
                                                return

                    # check to see if the ant has landed on an unclaimed nest
                    self.look_for_nest(self.game.unclaimed_nests)

                    # check to see if the ant has landed on a nest
                    self.look_for_nest(self.nests)

                    # will leave a pheromone every N steps (1 by default)
                    if not self.pheromones_to_food:
                        self.pheromones.append((self.pos * self.game.tile_size))
                        self.pheromones = self.remove_loops(self.pheromones)
                        self.trail_index = len(self.pheromones)

                    if self.current_nest.stored_food >= 200:
                        if all(dist(nest.pos, self.pos) >= 30 for nest in self.nests):
                            if randint(1, 2) == 1:
                                new_nest = AntNest(self.game, self.pos.x, self.pos.y, 1, self.current_nest.col)
                                for nest in self.nests:
                                    for ant in nest.ants:
                                        ant.nests.append(new_nest)

                                self.game.nests.append(new_nest)
                                self.current_nest.stored_food -= 200

    def move_on_path(self, direction, path) -> None:
        """
        this function is used to move the ant up and down
        its pheromone path to food

        :param direction: 1 to move up the path and -1 to move down
        :param path: the pheromone path you want the ant to follow
        """
        # chance to move
        # self.pheromones = self.remove_loops(self.pheromones)
        # if randint(1, 4) == 1:
        self.trail_index += direction
        self.pos = path[self.trail_index] // self.game.tile_size

    def eat(self):
        if self.health < self.max_health:
            if self.current_nest.stored_food >= 1:
                if randint(1, 2) == 1:
                    self.health += 1
                    self.current_nest.stored_food -= 1

        if self.eat_interval:
            self.eat_interval -= 1

        else:
            if self.current_nest.stored_food >= 1:
                self.total_ate += 1
                self.current_nest.stored_food -= 1
            else:
                self.health -= 1

            self.eat_interval = self.max_eat_interval

    def die(self):
        if all(dist(nest.pos, self.pos) >= 5 for nest in self.nests):
            self.game.ants_to_die.append(self)
            self.game.foods.append(self.game.Food(self, ant.pos.x, ant.pos.y, int(ant.total_ate * 0.8)))
            return True
        return False

    def update(self) -> None:
        self.eat()

        # if the ant is outside a nest
        if self.in_nest is False:

            if self.health <= 0:
                if self.die():
                    return




            # if the ant is following a path to food
            if self.pheromones_to_food:

                # if the ant has no food
                if self.has_food is False:

                    # if ant isn't at the end of the food path
                    if self.trail_index + 1 < len(self.pheromones_to_food):
                        self.move_on_path(1, self.pheromones_to_food)
                        if self.look_for_ant():
                            return

                    # if ant is at the end of food path
                    else:
                        food = self.look_for_food()

                        # if food is found
                        if food:
                            if food.chunks > 0:
                                # take a piece of food
                                self.has_food = True
                                food.chunks -= 1
                        else:
                            # self.pheromones.clear()
                            self.pheromones.extend(self.pheromones_to_food.copy())
                            self.pheromones_to_food.clear()

                # if the ant has food
                else:
                    if self.trail_index - 1 >= 0:
                        self.move_on_path(-1, self.pheromones_to_food)
                        if self.look_for_ant():
                            return

                    else:
                        self.steps = 0
                        self.in_nest = True
                        self.has_food = False
                        self.current_nest.stored_food += 1
                        return

            # if the ant is not following a path to food
            else:
                if self.steps > 15:
                    if self.trail_index == 0:
                        self.in_nest = True
                        self.steps = 0
                        self.pheromones.clear()
                        # self.pos = self.current_nest.pos.copy()
                        return

                    self.move_on_path(-1, self.pheromones)
                    self.look_for_ant()
                    return

                food = self.look_for_food()
                if food:
                    # grab food and start following path to food
                    food.chunks -= 1
                    self.has_food = True
                    self.pheromones_to_food.extend([self.current_nest.pos * self.game.tile_size] + self.pheromones.copy())
                    food.paths_to.append(self.pheromones_to_food)
                    self.pheromones.clear()
                    self.trail_index = len(self.pheromones_to_food)
                    return

                self.move()
                if self.look_for_ant():
                    return

        # if the ant is inside the nest
        else:
            # clear pheromones
            if self.pheromones:
                self.pheromones.clear()

            # chance to leave the nest
            if randint(1, 100) == 1:
                self.in_nest = False

    def draw(self):
        if len(self.pheromones) > 1:
            pygame.draw.lines(self.game.screen, self.current_nest.col, False, self.pheromones)

        if len(self.pheromones_to_food) > 1:
            pygame.draw.lines(self.game.screen, self.current_nest.col, False, self.pheromones_to_food)

        if self.in_nest is False:
            pygame.draw.rect(self.game.screen, self.current_nest.col,  # (200, 0, 0)
                             (self.pos.x * self.game.tile_size, self.pos.y * self.game.tile_size,
                              self.game.tile_size, self.game.tile_size))


class AntNest:
    def __init__(self, game, x, y, num_of_ants=10, col=(randint(0, 255), randint(0, 255), randint(0, 255))):
        self.game = game
        self.pos = pygame.Vector2(x, y)
        self.ants = set(Ant(self, self.game, self.pos) for _ in range(num_of_ants))
        self.stored_food = 0

        self.col = col
        self.time_passed = 0

        self.ant_cost = 5
        self.unclaimed = False

        self.unclaim_timer_max = 60 * 30
        self.unclaim_timer = self.unclaim_timer_max

    def update(self):
        self.time_passed += 1

        if all([not ant.in_nest for ant in self.ants]):
            self.unclaim_timer -= 1

        else:
            self.unclaim_timer = self.unclaim_timer_max

        if self.unclaim_timer == 0:
            self.unclaimed = True
            self.game.unclaimed_nests.append(self)



            for ant in self.ants:
                if self in ant.nests:
                    ant.nests.remove(self)
                    break


        if self.stored_food >= self.ant_cost:
            if randint(1, 60 * 10) == 1:
                self.stored_food -= self.ant_cost

                if len(self.ants) <= 10:
                    self.ants.add(Ant(self, self.game, self.pos))

    def draw(self):
        pygame.draw.rect(self.game.screen, (139, 69, 19),
                         (self.pos.x * self.game.tile_size, self.pos.y * self.game.tile_size,
                          self.game.tile_size, self.game.tile_size))
