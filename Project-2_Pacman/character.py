import pygame as pg
from settings import *

class Character():
    def __init__(self, game, grid_x, grid_y, color):
        self.game = game
        self.grid_pos = pg.math.Vector2(grid_x, grid_y)
        self.pixel_pos = self.get_pixel_pos_from_grid(self.grid_pos)
        self.current_direction = pg.math.Vector2(0, 0)

        self.color = color
        self.radius = self.game.cell_width // 2 - 2
        self.speed = MOB_SPEED

    def get_pixel_pos_from_grid(self, grid_pos):
        x = grid_pos.x * self.game.cell_width + (self.game.cell_width // 2)
        y = grid_pos.y * self.game.cell_height + (self.game.cell_height // 2)
        return pg.math.Vector2(x, y)

    def get_current_grid_cell(self):
        grid_x = int((self.pixel_pos.x - self.game.cell_width // 2 ) // self.game.cell_width)
        grid_y = int((self.pixel_pos.y - self.game.cell_height // 2 ) // self.game.cell_height)
        return grid_x, grid_y

    def draw(self):
        pg.draw.circle(
            self.game.screen,
            self.color,
            (int(self.pixel_pos.x), int(self.pixel_pos.y)),
            self.radius
        )

    def can_move(self, direction):
        if direction is None or direction.length() == 0:
            return False

        current_cell_x, current_cell_y = self.get_current_grid_cell()
        next_cell_x = current_cell_x + int(direction.x)
        next_cell_y = current_cell_y + int(direction.y)

        if not (0 <= next_cell_x < len(self.game.map[0]) and 0 <= next_cell_y < len(MAP)):
            return False

        if self.game.map[next_cell_y][next_cell_x] == 1:
                return False

        return True

    def is_at_grid_center(self):
        if self.current_direction.length() == 0:
            return True

        current_cell_x, current_cell_y = self.get_current_grid_cell()
        center_x = current_cell_x * self.game.cell_width + self.game.cell_width // 2
        center_y = current_cell_y * self.game.cell_height + self.game.cell_height // 2

        if self.current_direction.x != 0:
            if abs(self.pixel_pos.y - center_y) > 1:
                self.pixel_pos.y = center_y
            return abs(self.pixel_pos.x - center_x) < self.speed

        if self.current_direction.y != 0:
            if abs(self.pixel_pos.x - center_x) > 1:
                self.pixel_pos.x = center_x
            return abs(self.pixel_pos.y - center_y) < self.speed

        return False