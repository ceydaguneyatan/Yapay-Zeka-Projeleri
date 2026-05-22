import pygame as pg
import math
from settings import *
from character import Character
from ai_agent import AIAgent

class Pacman(Character):
    def __init__(self, game):
        super().__init__(game, 9, 4, YELLOW)

        self.radius = self.game.cell_width // 2 - 2

        self.control_type = "human"
        self.next_direction = None

        self.ai_agent = AIAgent(game)

        self.mouth_angle = 0
        self.animation_speed = 4
        self.mouth_opening = True
        self.last_direction_angle = 0

    def update(self):
        if self.is_at_grid_center():
            self.eat()

            if self.control_type == "ai":
                self.ai_move()

            if self.next_direction and self.can_move(self.next_direction):
                self.current_direction = self.next_direction.copy()
                self.next_direction = None

            elif not self.can_move(self.current_direction):
                self.current_direction= pg.math.Vector2(0, 0)

        self.pixel_pos += self.current_direction * self.speed

        if self.current_direction.length() > 0:
            if self.mouth_opening:
                self.mouth_angle += self.animation_speed
                if self.mouth_angle >= 45:
                    self.mouth_angle = 45
                    self.mouth_opening = False
            else:
                self.mouth_angle -= self.animation_speed
                if self.mouth_angle <= 0:
                    self.mouth_angle = 0
                    self.mouth_opening = True
        else:
            self.mouth_angle = 10

    def human_move(self, key):
        if self.control_type != "human":
            return

        new_direction = None

        if key == pg.K_LEFT:
            new_direction = pg.math.Vector2(-1, 0)
        elif key == pg.K_RIGHT:
            new_direction = pg.math.Vector2(1, 0)
        elif key == pg.K_UP:
            new_direction = pg.math.Vector2(0, -1)
        elif key == pg.K_DOWN:
            new_direction = pg.math.Vector2(0, 1)

        if new_direction:
            if new_direction == self.current_direction * -1: # Geri dönme → anında
                self.current_direction = new_direction.copy()
                self.next_direction = None
            else: # Diğer yönler → kontrol edilene kadar bekle
                self.next_direction = new_direction

    def eat(self):
        current_cell_x, current_cell_y = self.get_current_grid_cell()

        if self.game.map[current_cell_y][current_cell_x] == 0:
            self.game.map[current_cell_y][current_cell_x] = 2
            self.game.score += 10
            if self.game.chomp_sound:
                self.game.chomp_sound.play()

        elif self.game.map[current_cell_y][current_cell_x] == 3:
            self.game.map[current_cell_y][current_cell_x] = 2

            for ghost in self.game.ghosts:
                ghost.start_scared()

            if self.game.power_sound:
                self.game.power_channel.play(self.game.power_sound, loops=-1)

    def draw(self):
        if self.current_direction.x == 1:
            direction_angle = 0
        elif self.current_direction.x == -1:
            direction_angle = 180
        elif self.current_direction.y == -1:
            direction_angle = 270
        elif self.current_direction.y == 1:
            direction_angle = 90
        else:
            direction_angle = self.last_direction_angle

        if self.current_direction.length() > 0:
            self.last_direction_angle = direction_angle

        start_angle = direction_angle + self.mouth_angle
        end_angle = direction_angle + 360 - self.mouth_angle

        center = (int(self.pixel_pos.x), int(self.pixel_pos.y))
        points = [center]

        for angle in range(int(start_angle), int(end_angle) + 1, 10):
            rad = math.radians(angle)
            x = center[0] + self.radius * math.cos(rad)
            y = center[1] + self.radius * math.sin(rad)
            points.append((int(x), int(y)))

        rad_end = math.radians(end_angle)
        points.append(
            (int(center[0] + self.radius * math.cos(rad_end)), int(center[1] + self.radius * math.sin(rad_end))))

        pg.draw.polygon(self.game.screen, YELLOW, points)

    def ai_move(self):
        self.next_direction = self.ai_agent.get_best_move(self, self.game.ghosts)
