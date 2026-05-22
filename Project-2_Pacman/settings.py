# Ekran Ayarları
WIDTH, HEIGHT = 670, 670
FPS = 60
TOP_BOTTOM_BUFFER = 50

# Renkler (RGB Formatı)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (208, 22, 22)
GREY = (107, 107, 107)
YELLOW = (255, 255, 0)     # Pacman rengi
BLUE = (25, 25, 112)       # Duvar rengi
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

Scared_GHOST_COLOR = (0, 0, 255)
POWER_PELLET_TIME = 420

# Oyun Ayarları
MOB_SPEED = 2              # Karakterlerin hızı

# Font Ayarları
TEXT_FONT = 'Times New Roman'
TEXT_SIZE = 20

GHOST_MODE_NORMAL = "normal"
GHOST_MODE_SCARED = "scared"

# Harita (Grid)
# 1: Duvar
# 0: Yenen yem (Coin)
# 2: Boş koridor (Yem yenmiş veya yok)
# 3: Enerji Topu (Power pellet)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1],
    [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]