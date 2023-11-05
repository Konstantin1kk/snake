import pygame as pg
import sys
from random import randrange


class Apple:
    def __init__(self, game_obj):
        self.apple = randrange(0, game_obj.field_size[0]), randrange(0, game_obj.field_size[1])


class Snake:
    def __init__(self, game_obj):
        self.start_pos = game_obj.field_size[0] // 2, game_obj.field_size[1] // 2
        self.body = [self.start_pos]


class Game:
    def __init__(self):
        pg.init()
        self.width = 800
        self.height = 800
        self.screen = pg.display.set_mode((self.width, self.height))
        self.fps = 5
        self.block_size = 40
        self.field_size = self.width // self.block_size, self.height // self.block_size
        self.running = True
        self.DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
        self.direction = 0
        self.snake = Snake(self)
        self.apple = Apple(self)
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 50)
        self.alive = False
        self.font_space = self.font.render('enter "SPACE" to restart', False, pg.Color('yellow'))

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if self.alive:
                        if event.key == pg.K_LEFT and self.direction != 1:
                            self.direction = 0
                        elif event.key == pg.K_RIGHT and self.direction != 0:
                            self.direction = 1
                        elif event.key == pg.K_UP and self.direction != 3:
                            self.direction = 2
                        elif event.key == pg.K_DOWN and self.direction != 2:
                            self.direction = 3

                    else:
                        if event.key == pg.K_SPACE:
                            self.alive = True
                            self.snake.body = [self.snake.start_pos]
                            self.apple.apple = randrange(0, self.field_size[0]), randrange(0, self.field_size[1])
                            self.fps = 5

            self.screen.fill(pg.Color('black'))
            text1 = self.font.render(f'score: {str(len(self.snake.body))}', False, pg.Color('yellow'))
            self.screen.blit(text1, ((self.width // 2) - 50, 0))

            if self.alive:
                for elem in self.snake.body:
                    pg.draw.rect(self.screen, 'green', (elem[0] * self.block_size, elem[1] * self.block_size, self.block_size - 1, self.block_size - 1))
                pg.draw.rect(self.screen, 'red', (self.apple.apple[0] * self.block_size, self.apple.apple[1] * self.block_size, self.block_size - 1, self.block_size - 1))

                self.new_pos = self.DIRECTIONS[self.direction][0] + self.snake.body[0][0], self.DIRECTIONS[self.direction][1] + self.snake.body[0][1]

                if self.new_pos == self.apple.apple or self.apple.apple == self.snake.body:
                    self.apple.apple = randrange(0, self.field_size[0] - 1), randrange(0, self.field_size[1] - 1)
                    self.snake.body.append(self.new_pos)
                    self.fps += 1

                elif not(0 <= self.snake.body[0][0] < self.field_size[0] and 0 <= self.snake.body[0][1] < self.field_size[1]) or self.new_pos in self.snake.body:
                    self.alive = False

                self.snake.body.insert(0, self.new_pos)
                self.snake.body.pop(-1)

            else:
                self.text2 = self.screen.blit(self.font_space, (230, 50))

            pg.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
