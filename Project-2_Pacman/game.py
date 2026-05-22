import pygame as pg
import sys
import copy
import array
import math
from settings import *
from pacman import Pacman
from ghost import Ghost

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.pre_init(44100, -16, 1, 1024)
        pg.mixer.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Pac-Man AI Projesi")
        self.clock = pg.time.Clock()
        self.running = True
        self.state = "RUNNING"

        self.map = copy.deepcopy(MAP)

        self.cell_width = WIDTH // len(self.map[0])
        self.cell_height = HEIGHT // len(self.map)

        self.player = Pacman(self)
        self.score = 0
        self.font_name = pg.font.match_font(TEXT_FONT)
        self.start_time = pg.time.get_ticks()

        self.chomp_sound = self.make_sound(frequency=400, duration=0.1)
        self.death_sound = self.make_sound(frequency=150, duration=1.0)
        self.power_sound = self.make_siren_sound()
        self.power_channel = pg.mixer.Channel(1)

        self.ghosts = [
            Ghost(self, 9, 3),
            Ghost(self, 18, 1),
            Ghost(self, 1, 5),
            Ghost(self, 18, 5)
        ]

    def make_sound(self, frequency, duration):
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buffer = array.array('h', [int(32767 * 0.5 * ((i * frequency // sample_rate) % 2 * 2 - 1)) for i in
                                   range(n_samples)])
        return pg.mixer.Sound(buffer=buffer)

    def make_siren_sound(self):
        sample_rate = 44100
        duration = 0.6
        n_samples = int(sample_rate * duration)
        buffer = array.array('h')
        phase = 0

        for i in range(n_samples):
            t = i / sample_rate
            freq = 450 + 150 * math.sin(2 * math.pi * 3 * t)
            phase += 2 * math.pi * freq / sample_rate
            value = int(32767 * 0.2 * math.sin(phase))
            buffer.append(value)

        return pg.mixer.Sound(buffer=buffer)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        while self.running:
            if self.state == "RUNNING":
                self.events()
                self.update()
                self.draw()
            else:
                self.running = False

            self.clock.tick(60)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                self.player.human_move(event.key)

    def update(self):
        self.player.update()

        any_scared = False
        for g in self.ghosts:
            g.update()
            if g.mode == GHOST_MODE_SCARED:
                any_scared = True

            # Çarpışma Kontrolü
            distance = self.player.pixel_pos.distance_to(g.pixel_pos)
            if distance < self.player.radius + g.radius:
                if g.mode == GHOST_MODE_SCARED:
                    g.reset_position()
                    self.score += 200
                else:
                    self.state = "GAMEOVER"
                    self.power_channel.stop()
                    if self.death_sound:
                        self.death_sound.play()

        if self.check_win():
            self.state = "WIN"

        if not any_scared:
            self.power_channel.stop()

    def check_win(self):
        dot_count = sum(row.count(0) for row in self.map)

        if dot_count == 0:
            return True
        return False

    def show_unified_results(self, results, current_mode):
        pg.mixer.stop()
        blink_timer = 0

        if self.state == "WIN":
            title_text = "YOU WIN! ALL CLEARED!"
            title_color = GREEN
        else:
            title_text = "GAME OVER! GHOST HIT!"
            title_color = RED

        while True:
            self.screen.fill(BLACK)
            blink_timer += 1

            # 1. DIŞ ÇERÇEVE (NEON STYLE)
            rect = pg.Rect(10, 10, WIDTH - 20, HEIGHT - 20)
            pg.draw.rect(self.screen, title_color, rect, 4, border_radius=10)
            pg.draw.rect(self.screen, (20, 20, 20), (16, 16, WIDTH - 32, HEIGHT - 32), 0, border_radius=8)

            # 2. BAŞLIK
            self.draw_text_3d(title_text, 45, title_color, WIDTH // 2, 80)

            # 3. SKOR TABLOSU (ORTA ALAN)
            headers_y = 150
            col1, col2, col3, col4 = 140, 300, 420, 540

            pg.draw.line(self.screen, GREY, (50, headers_y + 25), (WIDTH - 50, headers_y + 25), 2)

            self.draw_text_3d("MODE", 22, YELLOW, col1, headers_y)
            self.draw_text_3d("SCORE", 22, YELLOW, col2, headers_y)
            self.draw_text_3d("TIME", 22, YELLOW, col3, headers_y)
            self.draw_text_3d("PERF", 22, YELLOW, col4, headers_y)

            # İnsan Verileri
            h_res = results["human"]
            h_color = WHITE if current_mode != "human" else ORANGE
            self.draw_text_3d("HUMAN", 20, h_color, col1, headers_y + 50)
            self.draw_text(str(h_res['score']), 20, h_color, col2, headers_y + 50)
            self.draw_text(f"{h_res['time']:.1f}s", 20, h_color, col3, headers_y + 50)
            self.draw_text(f"{h_res['perf']:.2f}", 20, h_color, col4, headers_y + 50)

            # AI Verileri
            a_res = results["ai"]
            a_color = WHITE if current_mode != "ai" else (0, 255, 255)
            self.draw_text_3d("AI BOT", 20, a_color, col1, headers_y + 90)
            self.draw_text(str(a_res['score']), 20, a_color, col2, headers_y + 90)
            self.draw_text(f"{a_res['time']:.1f}s", 20, a_color, col3, headers_y + 90)
            self.draw_text(f"{a_res['perf']:.2f}", 20, a_color, col4, headers_y + 90)

            # Kazanan Mesajı
            winner_text = ""
            if h_res['perf'] > 0 and a_res['perf'] > 0:
                if h_res['perf'] > a_res['perf']:
                    winner_text = "WINNER: HUMAN PLAYER!"
                elif a_res['perf'] > h_res['perf']:
                    winner_text = "WINNER: AI AGENT!"
                else:
                    winner_text = "DRAW!"
            else:
                winner_text = "Play both modes to compare!"

            self.draw_text(winner_text, 24, GREY, WIDTH // 2, 320)

            # --- DÜZELTİLEN BÖLÜM: ALT BUTONLAR ---
            btn_y = HEIGHT - 80  # Yazıların Y koordinatı
            icon_y = btn_y - 50  # İkonların yazıların tam üstünde durması için Y koordinatı

            human_btn_x = WIDTH // 2 - 150
            ai_btn_x = WIDTH // 2 + 150

            # Human Button (Pacman İkonu Üstte)
            self.draw_pacman_icon(human_btn_x, icon_y, 20)
            self.draw_text_3d("[1] HUMAN REPLAY", 22, ORANGE, human_btn_x, btn_y, font_name="arial")

            # AI Button (Robot İkonu Üstte)
            self.draw_robot_icon(ai_btn_x, icon_y, 18)
            self.draw_text_3d("[2] AI REPLAY", 22, (0, 255, 255), ai_btn_x, btn_y, font_name="arial")

            if (blink_timer // 40) % 2 == 0:
                self.draw_text("PRESS [ESC] TO QUIT", 18, (100, 100, 100), WIDTH // 2, HEIGHT - 30)

            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                    return "quit"
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        return "human"
                    elif event.key == pg.K_2:
                        return "ai"
                    elif event.key == pg.K_ESCAPE:
                        self.quit()
                        return "quit"

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.player.draw()

        for g in self.ghosts:
            g.draw()

        current_time = (pg.time.get_ticks()- self.start_time)/ 1000

        self.draw_text(f"SCORE: {self.score}", TEXT_SIZE, WHITE, 50, 15)
        self.draw_text(f"TIME: {current_time:.1f}", TEXT_SIZE, WHITE, 250, 15)

        pg.display.update()

    def quit(self):
        pg.mixer.stop()
        pg.mixer.music.stop()
        pg.quit()
        sys.exit()

    def draw_grid(self):
        for row_index, row in enumerate(self.map):
            for col_index, cell in enumerate(row):
                if cell == 1:
                    pg.draw.rect(self.screen, BLUE, (col_index * self.cell_width, row_index * self.cell_height, self.cell_width, self.cell_height))
                elif cell == 0:
                    pg.draw.circle(self.screen, YELLOW, (col_index * self.cell_width + self.cell_width//2, row_index * self.cell_height + self.cell_height//2), 3)
                elif cell == 3:
                    pg.draw.circle(self.screen, ORANGE, (col_index * self.cell_width + self.cell_width // 2,
                                                         row_index * self.cell_height + self.cell_height // 2), 8)

    def draw_text_3d(self, text, size, color, x, y, font_name=None):
        if not font_name:
            font_name = self.font_name
        try:
            font = pg.font.SysFont("arialblack", size)
        except:
            font = pg.font.Font(font_name, size)

        # Gölge
        text_surface_shadow = font.render(text, True, (30, 30, 150))
        text_rect_shadow = text_surface_shadow.get_rect(center=(x + 4, y + 4))
        self.screen.blit(text_surface_shadow, text_rect_shadow)

        # Asıl Yazı
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_pacman_icon(self, x, y, size):
        pg.draw.circle(self.screen, YELLOW, (x, y), size)
        points = [(x, y), (x + size, y - size // 1.5), (x + size, y + size // 1.5)]
        pg.draw.polygon(self.screen, BLACK, points)

    def draw_ghost_icon(self, x, y, size, color):
        rect = pg.Rect(x - size, y - size, size * 2, size * 2)
        pg.draw.ellipse(self.screen, color, rect)
        pg.draw.rect(self.screen, color, (x - size, y, size * 2, size))
        for i in range(3):
            sub_x = (x - size) + (i * size * 2 // 3)
            pg.draw.circle(self.screen, color, (int(sub_x) + size // 3, y + size), size // 3)
        pg.draw.circle(self.screen, WHITE, (x - size // 2, y - size // 4), size // 3)
        pg.draw.circle(self.screen, WHITE, (x + size // 2, y - size // 4), size // 3)
        pg.draw.circle(self.screen, BLUE, (x - size // 3, y - size // 4), size // 6)
        pg.draw.circle(self.screen, BLUE, (x + size // 3 + 2, y - size // 4), size // 6)

    def draw_robot_icon(self, x, y, size):
        """AI Modu için Robot kafası"""
        rect = pg.Rect(x - size, y - size, size * 2, size * 1.8)
        pg.draw.rect(self.screen, (0, 200, 200), rect, border_radius=5)
        pg.draw.rect(self.screen, BLACK, (x - size + 4, y - size // 2, size * 2 - 8, size // 1.5))
        pg.draw.circle(self.screen, RED, (x - size // 2, y - size // 6), 3)
        pg.draw.circle(self.screen, RED, (x + size // 2, y - size // 6), 3)
        pg.draw.line(self.screen, GREY, (x, y - size), (x, y - size - 10), 3)
        pg.draw.circle(self.screen, RED, (x, y - size - 10), 4)

    def start_screen(self):
        blink_timer = 0
        while True:
            self.screen.fill(BLACK)
            blink_timer += 1

            # 1. ÇERÇEVE
            border_rect = pg.Rect(10, 10, WIDTH - 20, HEIGHT - 20)
            pg.draw.rect(self.screen, BLUE, border_rect, 4, border_radius=10)
            pg.draw.rect(self.screen, (0, 0, 100), (16, 16, WIDTH - 32, HEIGHT - 32), 2, border_radius=8)

            # 2. BAŞLIK
            self.draw_text_3d("PAC-MAN", 70, YELLOW, WIDTH // 2, HEIGHT // 4 - 20)
            self.draw_text_3d("AI PROJECT", 40, WHITE, WIDTH // 2, HEIGHT // 4 + 40)

            # 3. SEÇENEKLER (HİZALAMA)
            row1_y = HEIGHT // 2
            row2_y = HEIGHT // 2 + 70

            icon_x = WIDTH // 2 - 170
            num_x = WIDTH // 2 - 100
            text_x = WIDTH // 2 + 70

            # SEÇENEK 1
            self.draw_pacman_icon(icon_x, row1_y, 22)
            self.draw_text_3d("1.", 35, ORANGE, num_x, row1_y)
            self.draw_text_3d("PLAYER MODE", 32, ORANGE, text_x, row1_y)

            # SEÇENEK 2
            self.draw_robot_icon(icon_x, row2_y, 20)
            self.draw_text_3d("2.", 35, (0, 255, 255), num_x, row2_y)
            self.draw_text_3d("AI AGENT MODE", 32, (0, 255, 255), text_x, row2_y)

            if (blink_timer // 30) % 2 == 0:
                self.draw_text("PRESS [1] or [2] TO START", 20, GREY, WIDTH // 2, HEIGHT - 80)

            pg.display.update()
            self.clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                    return "quit"
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        return "human"
                    elif event.key == pg.K_2:
                        return "ai"
                    elif event.key == pg.K_ESCAPE:
                        self.quit()
                        return "quit"

    def quit_for_restart(self):
        pg.mixer.stop()