import random

class Board:

    def __init__(self, size=8, state=None):
        self.size = size
        if state is None:
            self.state = [random.randint(0, size - 1) for _ in range(size)]
        else:
            self.state = list(state)

        self.conflicts = self.calculate_conflicts()

    def calculate_conflicts(self):
        # H(n): Birbiriyle çakışan vezir çifti sayısını hesaplar.
        conflicts = 0
        for i in range(self.size):
            for j in range(i + 1, self.size):
                # Aynı satırda mı?
                if self.state[i] == self.state[j]:
                    conflicts += 1
                # Çaprazda mı?
                elif abs(self.state[i] - self.state[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def get_neighbors(self):
        neighbors = []
        for col in range(self.size):
            original_row = self.state[col]
            for row in range(self.size):
                if row != original_row:
                    new_state = list(self.state)
                    new_state[col] = row
                    neighbors.append(Board(self.size, new_state))
        return neighbors

    def is_goal(self):
        return self.conflicts == 0

    def __lt__(self, other):
        # min() fonksiyonu kullanabilmek için karşılaştırma operatörü
        return self.conflicts < other.conflicts