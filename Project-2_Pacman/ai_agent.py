import pygame as pg
import collections
from settings import *

class AIAgent():
    def __init__(self, game):
        self.game = game
        # son 10 adım
        self.location_history = collections.deque(maxlen=10)

    def get_best_move(self, pacman, ghosts):
        directions = [
            pg.math.Vector2(0, -1), pg.math.Vector2(0, 1),
            pg.math.Vector2(-1, 0), pg.math.Vector2(1, 0),
        ]

        best_score = -float("inf")
        best_direction = pg.math.Vector2(0, 0)

        current_x, current_y = pacman.get_current_grid_cell()

        # titremeyi önlemek için yönün tersi
        if pacman.current_direction.length() > 0:
            reverse_direction = pacman.current_direction * -1
        else:
            reverse_direction = None

        total_food_left = sum(row.count(0) + row.count(3) for row in self.game.map)

        little_food = (total_food_left < 20)

        food_search_limit = 200 if little_food else 40

        min_ghost_dist = float('inf')

        for g in ghosts:
            if g.mode == GHOST_MODE_NORMAL:
                gx, gy = g.get_current_grid_cell()
                d = abs(gx - current_x) + abs(gy - current_y)
                if d < min_ghost_dist:
                    min_ghost_dist = d

        # yönler değerlendiriliyor
        for direction in directions:
            if not pacman.can_move(direction): #duvar varsa geç
                continue

            next_x = current_x + int(direction.x)
            next_y = current_y + int(direction.y)

            score = 0

            # hayalet analizi
            for g in ghosts:
                g_grid = g.get_current_grid_cell()

                manhattan_dist = abs(g_grid[0] - next_x) + abs(g_grid[1] - next_y)
                # eğer kuş uçuşnda bile 10'dan fazla ise hiç hesaplama
                if manhattan_dist > 10:
                    continue

                # bfs ile gerçek yolu hesaplıyoruz
                true_dist = self.bfs_limited_distance((next_x, next_y), g_grid, limit=10)

                if true_dist is None:
                    continue

                # ghost çok yakınsa kaç
                if g.mode == GHOST_MODE_NORMAL:
                    if true_dist < 3:
                        score -= 1000000

                    if true_dist <= 7:
                        score += (true_dist * 40000)
                    else:
                        score -= 5000 / (true_dist + 0.1)

                # ghost korkmuşsa ona yaklaş
                elif g.mode == GHOST_MODE_SCARED:
                    if true_dist < 15:
                        score += 3000 / (true_dist + 1)

            dist_to_food = self.bfs_food((next_x, next_y), limit=food_search_limit)

            if dist_to_food is not None:
                if little_food:
                    multiplier = 25000
                else:
                    multiplier = 3000
                score += multiplier / (dist_to_food + 1)
            else:
                score -= 50

            # geri dönme cezası
            if reverse_direction and direction == reverse_direction:
                score -= 10000

            # daha önce visit edilen yerlere gitmek ceza
            visit_count = self.location_history.count((next_x, next_y))
            # oyun sonunda ise eski yolların cezasını azalt
            penalty = 200 if little_food else 1000
            score -= visit_count * penalty

            if score > best_score:
                best_score = score
                best_direction = direction

        # güncel visit listesi
        self.location_history.append((current_x, current_y))
        return best_direction

    def bfs_limited_distance(self, start_pos, target_pos, limit = 12):
        # Sadece belirli bir derinliğe kadar arama yapar.
        if start_pos == target_pos: # zaten hedefin üstündeysek
            return 0

        # queue: (x,y,gidilen mesafe). fifo
        queue = collections.deque([(start_pos[0], start_pos[1], 0)])

        # kontrol edilen kareler
        visited = set()
        visited.add(start_pos)

        while queue:
            curr_x, curr_y, dist = queue.popleft()

            # limiti aştıysak
            if dist >= limit:
                return None

            # hedefin üstündeysek değil de ghost ile hesapladığı karenin arasındaki mesafe.
            if (curr_x, curr_y) == target_pos:
                return dist

            # olduğumuz karenin 4 yanı
            neighbors = [
                (curr_x + 1, curr_y), (curr_x - 1, curr_y),
                (curr_x, curr_y + 1), (curr_x, curr_y - 1)
            ]

            for nx, ny in neighbors:
                if 0 <= nx < len(self.game.map[0]) and 0 <= ny < len(self.game.map): # harita sınırları içinde mi
                    if self.game.map[ny][nx] != 1 and (nx, ny) not in visited:
                        visited.add((nx, ny)) # kuyruğa atıldığı için ziyaret edildi işaretliyoruz ki tekrar eklemeyelim
                        queue.append((nx, ny, dist + 1))

        return None

    def bfs_food(self, start_pos, limit=40):
        # kuyruk: x, y, gidilen mesafe
        queue = collections.deque([(start_pos[0], start_pos[1], 0)])

        visited = set()
        visited.add(start_pos)
        # max bakacağımız mesafe
        max_search_depth = 40

        while queue:
            curr_x, curr_y, dist = queue.popleft()

            if dist >= max_search_depth:
                return None

            tip = self.game.map[curr_y][curr_x]
            # küçük veya büyük yem ise
            if tip == 0 or tip == 3:
                return dist

            neighbors = [
                (curr_x + 1, curr_y), (curr_x - 1, curr_y),
                (curr_x, curr_y + 1), (curr_x, curr_y - 1)
            ]

            for nx, ny in neighbors:
                if 0 <= nx < len(self.game.map[0]) and 0 <= ny < len(self.game.map):
                    if self.game.map[ny][nx] != 1 and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        # komşusu, kareden +1 adım uzaklıktadır
                        queue.append((nx, ny, dist + 1))

        return None