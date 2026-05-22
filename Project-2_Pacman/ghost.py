import pygame as pg
import random
import collections
from settings import *
from character import Character

class Ghost(Character):
    def __init__(self, game, grid_x, grid_y):
        super().__init__(game, grid_x, grid_y, WHITE)
        self.original_color = self.color
        self.original_pos = pg.math.Vector2(grid_x, grid_y)
        self.mode = GHOST_MODE_NORMAL
        self.scared_timer = 0

        self.radius = self.game.cell_width // 2
        self.speed = MOB_SPEED * 0.8

    def update(self):
        self.pixel_pos += self.current_direction * self.speed

        if self.mode == GHOST_MODE_SCARED:
            self.scared_timer -= 1
            if self.scared_timer <= 0:
                self.return_to_normal()

        if self.is_at_grid_center():
            self.change_direction()

    def start_scared(self):
        self.mode = GHOST_MODE_SCARED
        self.color = Scared_GHOST_COLOR
        self.scared_timer = POWER_PELLET_TIME
        self.speed = MOB_SPEED * 0.5

    def return_to_normal(self):
        self.mode = GHOST_MODE_NORMAL
        self.color = self.original_color
        self.speed = MOB_SPEED * 0.8

    def reset_position(self):
        self.grid_pos = self.original_pos.copy()
        self.pixel_pos = self.get_pixel_pos_from_grid(self.grid_pos)
        self.current_direction = pg.math.Vector2(0, 0)
        self.return_to_normal()

    def change_direction(self):
        direction = [
            pg.math.Vector2(-1, 0), pg.math.Vector2(1, 0),
            pg.math.Vector2(0, -1), pg.math.Vector2(0, 1)
        ]
        valid_direction = []

        for d in direction:
            if d == self.current_direction * -1:
                continue
            if self.can_move(d):
                valid_direction.append(d)

        if valid_direction:
            if self.mode == GHOST_MODE_NORMAL:
                self.current_direction = random.choice(valid_direction)
            elif self.mode == GHOST_MODE_SCARED:
                best_flee_dir = valid_direction[0]
                max_dist = -1

                pacman_grid_pos = self.game.player.get_current_grid_cell()

                for d in valid_direction:
                    next_pixel_x = self.pixel_pos.x + (d.x * self.game.cell_width)
                    next_pixel_y = self.pixel_pos.y + (d.y * self.game.cell_height)

                    next_grid_x = int(next_pixel_x // self.game.cell_width)
                    next_grid_y = int(next_pixel_y // self.game.cell_height)

                    dist = self.get_bfs_distance((next_grid_x, next_grid_y), pacman_grid_pos)

                    if dist > max_dist:
                        max_dist = dist
                        best_flee_dir = d
                self.current_direction = best_flee_dir

        elif self.can_move(self.current_direction * -1):
            self.current_direction = self.current_direction * -1

    def get_bfs_distance(self, start_pos, target_pos):
        queue = collections.deque([(start_pos[0], start_pos[1], 0)])
        visited = set()
        visited.add(start_pos)

        while queue:
            curr_x, curr_y, dist = queue.popleft()
            if curr_x == target_pos[0] and curr_y == target_pos[1]:
                return dist

            neighbors = [
                (curr_x + 1, curr_y), (curr_x - 1, curr_y),
                (curr_x, curr_y + 1), (curr_x, curr_y - 1)
            ]

            for nx, ny in neighbors:
                if 0 <= nx < len(self.game.map[0]) and 0 <= ny < len(self.game.map):
                    if self.game.map[ny][nx] != 1 and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny, dist + 1))

        return 0

    def draw(self):
        pg.draw.circle(self.game.screen, self.color, (int(self.pixel_pos.x), int(self.pixel_pos.y - 2)), self.radius)
        pg.draw.rect(self.game.screen, self.color,
                     (int(self.pixel_pos.x - self.radius), int(self.pixel_pos.y - 2), self.radius * 2, self.radius + 2))

        eye_color = BLACK
        pupil_color = BLUE
        if self.mode == GHOST_MODE_SCARED:
            pupil_color = WHITE
            eye_color = BLACK

        eye_radius = int(self.radius * 0.3)
        pupil_radius = int(self.radius * 0.15)
        offset_x = int(self.radius * 0.35)
        offset_y = int(self.radius * 0.35)

        pupil_dx = int(self.current_direction.x * 2)
        pupil_dy = int(self.current_direction.y * 2)

        pg.draw.circle(self.game.screen, eye_color,
                       (int(self.pixel_pos.x - offset_x), int(self.pixel_pos.y - offset_y)), eye_radius)
        pg.draw.circle(self.game.screen, eye_color,
                       (int(self.pixel_pos.x + offset_x), int(self.pixel_pos.y - offset_y)), eye_radius)

        pg.draw.circle(self.game.screen, pupil_color,
                       (int(self.pixel_pos.x - offset_x + pupil_dx), int(self.pixel_pos.y - offset_y + pupil_dy)),
                       pupil_radius)
        pg.draw.circle(self.game.screen, pupil_color,
                       (int(self.pixel_pos.x + offset_x + pupil_dx), int(self.pixel_pos.y - offset_y + pupil_dy)),
                       pupil_radius)