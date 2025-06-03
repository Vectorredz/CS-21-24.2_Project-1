import pyxel
from collections import deque 
from dataclasses import dataclass
from typing import Literal

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 200
DIM = 10
DELAY = 2
@dataclass
class Snake:
    x: int
    y: int 
    facing: Literal['N', 'E', 'W', 'S'] = 'E'

@dataclass
class Segment:
    x: int 
    y: int
    segments: list[tuple[int, int]]


class Game:
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.snake_x = 20
        self.snake_y = 10
        self.coords = deque([])
        self.snake = Snake(self.snake_x, self.snake_y)
        self.segment = []
        self.segments = Segment(self.snake_x, self.snake_y, segments=[])

        pyxel.init(self.screen_width, self.screen_height, fps=7)
        pyxel.run(self.update, self.draw)

    def update(self):
        # self.update_snake(self.snake.x, self.snake.y)
        self.dy = self.snake.y
        self.dx = self.snake.x
        if (pyxel.btn(pyxel.KEY_D)):
            self.dx += 10
            self.snake = Snake(self.dx, self.snake.y) if self.out_of_bounds(self.dx, self.snake.y) else Snake(self.snake.x, self.snake.y)
            self.coords.append((self.snake.x, self.snake.y))
            self.snake.facing = 'E'
            self.update_segment()
        elif (pyxel.btn(pyxel.KEY_W)):
            self.dy -= 10
            self.snake = Snake(self.snake.x, self.dy) if self.out_of_bounds(self.snake.x, self.dy) else Snake(self.snake.x, self.snake.y)
            self.coords.append((self.snake.x, self.snake.y))
            self.snake.facing = 'N'
            self.update_segment()
        elif (pyxel.btn(pyxel.KEY_S)):
            self.dy += 10
            self.snake = Snake(self.snake.x, self.dy) if self.out_of_bounds(self.snake.x, self.dy) else Snake(self.snake.x, self.snake.y)
            self.coords.append((self.snake.x, self.snake.y))
            self.snake.facing = 'S'
            self.update_segment()
        elif (pyxel.btn(pyxel.KEY_A)):
            self.dx -= 10
            self.snake = Snake(self.dx, self.snake.y) if self.out_of_bounds(self.dx, self.snake.y) else Snake(self.snake.x, self.snake.y)
            self.coords.append((self.snake.x, self.snake.y))
            self.snake.facing = 'W'
            self.update_segment()
        

        # self.update_segment(self.segment.x, self.segment.y)

    def out_of_bounds(self, x, y):
        # return True if 0 < x <= self.screen_width and 0 < y <= self.screen_height else False
        if (x < 0 or x >= self.screen_width):
            return False
        if (y < 0 or y >= self.screen_height):
            return False
        return True

    def update_segment(self):
        for i in range(len(self.coords)):
            self.segments[i] = (self.coords[(i-1) * DELAY], self.coords[i * DELAY])
            self.segment = Segment(self.segments[i][0], self.segments[i][1])
            # print((coords[0], coords[1]))
            # self.segment = Segment(self.new_coords[0], self.new_coords[1])
            
    def draw(self):
        pyxel.cls(0)
        self.draw_snake(self.snake.x, self.snake.y)  
        self.draw_segment(self.segments.x, self.segments.y)

    def draw_snake(self, x, y): 
        pyxel.rect(x, y, DIM, DIM, 12)

    def draw_segment(self, x, y):
        pyxel.rect(x, y, DIM, DIM, 6)
        pyxel.rect(x-DIM, y, DIM, DIM, 6)

Game()


