class Node:

    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent

        self.g = g # cost: başlangıçtan buraya gelene kadar harcanan adım sayısı
        self.h = h # heuristic: buradan hedefe kuş uçuşu ne kadar kaldı
        self.f = g + h # total score: bu yolun toplam maliyeti

        self.children = [] # sma* için çocukları hafızada tutmak

    def __lt__(self, other): # less than
        if self.f == other.f:
            return self.g > other.g # hedefe daha yakın olanı alırız
        return self.f < other.f # eğer self daha küçükse True döndürür, büyükse False döndürür

    def __repr__(self):
        return f"Node({self.state}, f={self.f})"

class PacmanProblem:

    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        # haritada P ve G sembollerini bul
        self.start = self._find_symbol('P')
        self.goal = self._find_symbol('G')

    def _find_symbol(self, symbol):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == symbol:
                    return (r, c)
        return None

    def get_neighbors(self, state):
        r, c = state
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Yukarı, Aşağı, Sol, Sağ
        neighbors = []

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] != '%':
                    neighbors.append((nr, nc))
        return neighbors

    def heuristic(self, state):
        x1, y1 = state
        x2, y2 = self.goal
        # manhattan mesafesi (öklid kullanmayız, yolu L şeklinde hesaplarız)
        return abs(x1 - x2) + abs(y1 - y2)

# başlangıca giden yolu bulur
def reconstruct_path(node):
    path = []
    current = node
    while current:
        path.append(current.state) # şuanki konumu pathe ekle
        current = current.parent # ebeveynine git
    # döngü bittiğinde liste terstir
    return path[::-1]  # tersini çevir