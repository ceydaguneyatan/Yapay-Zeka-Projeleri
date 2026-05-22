import random
from board import Board

class HillClimbingSolver:

    def __init__(self, size=8):
        self.size = size

    def steepesst_ascent(self, start_board):
        current = start_board
        path = [current]

        while not current.is_goal():
            neighbors = current.get_neighbors()
            if not neighbors:
                break

            # Tüm komşular arasından EN İYİSİNİ seç
            best_neighbor = min(neighbors, key=lambda x: x.conflicts)

            # Eğer en iyi komşu bile şu anki durumdan daha iyi değilse (Local Optimum)
            if best_neighbor.conflicts >= current.conflicts:
                break

            current = best_neighbor
            path.append(current)

        return current, path

    def stochastic(self, start_board):
        current = start_board
        path = [current]
        max_steps = 2000  # Sonsuz döngü koruması

        for _ in range(max_steps):
            if current.is_goal():
                break

            neighbors = current.get_neighbors()
            # Mevcut durumdan DAHA İYİ olan komşuları filtrele
            better_neighbors = [n for n in neighbors if n.conflicts < current.conflicts]

            if not better_neighbors:
                break

            current = random.choice(better_neighbors)
            path.append(current)

        return current, path

    def random_restart(self, start_board=None):
        # İlk denemeyi verilen tahta ile yap
        current_start = start_board if start_board else Board(self.size)
        full_path = []
        restarts = 0
        max_restarts = 50

        while restarts < max_restarts:
            final_state, path = self.steepesst_ascent(current_start)
            full_path.extend(path)

            if final_state.is_goal():
                return final_state, full_path, restarts

            restarts += 1
            current_start = Board(self.size)  # Rastgele yeni tahta
            full_path.append(current_start)  # Yeni başlangıcı yola ekle

        return final_state, full_path, restarts
