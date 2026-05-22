class PacmanProblem:
    def __init__(self):
        self.grid_str = [
            "%%%%%%%%%%%%%%%%%%%%%%%",
            "%P....................%",
            "%.%%%%.%%%%.%%%%.%%%%.%",
            "%....%.%..%.%..%.%....%",
            "%.%%.%.%..%.%..%.%.%%.%",
            "%.....................%",
            "%.%%.%.%%%%.%%%%.%.%%.%",
            "%....%..............%.%",
            "%.%%%%.%%%%.%%%%.%%.%.%",
            "%....................G%",
            "%%%%%%%%%%%%%%%%%%%%%%%"
        ]

        self.rows = len(self.grid_str)
        self.cols = len(self.grid_str[0])
        self.start = self.find_pos('P')
        self.goal = self.find_pos('G')

    def find_pos(self, char):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid_str[r][c] == char:
                    return (r, c)
        return None

    def get_neighbors(self, state):
        r, c = state
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid_str[nr][nc] != '%':
                neighbors.append((nr, nc))
        return neighbors