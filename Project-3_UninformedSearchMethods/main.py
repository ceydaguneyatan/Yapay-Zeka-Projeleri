from pacman_game import PacmanProblem
from search_algorithms import ucs, ids, bids
from visualization import visualize_path

if __name__ == "__main__":
    game = PacmanProblem()
    try:
        print("--- 1. UCS (Uniform Cost Search) ---")
        result_ucs = ucs(game)
        visualize_path(game, result_ucs, "Uniform Cost Search")

        print("--- 2. IDS (Iterative Deepening Search) ---")
        result_ids = ids(game)
        visualize_path(game, result_ids, "Iterative Deepening Search")

        print("--- 3. BiDS (Bidirectional Search) ---")
        result_bids = bids(game)
        visualize_path(game, result_bids, "Bidirectional Search", is_last=True)
    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından sonlandırıldı. (Çıkış yapılıyor...)")