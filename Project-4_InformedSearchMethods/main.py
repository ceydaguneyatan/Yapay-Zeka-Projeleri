from pacman_node import PacmanProblem
from search_algorithms import rbfs, sma_star
from visualization import visualize_path


if __name__ == "__main__":

    grid_map = [
        "%%%%%%%%%%%%%%%%%%%%",
        "%P..%.....%...%...G%",
        "%...%..%..%...%.%..%",
        "%.%.%..%......%.%..%",
        "%......%..%%%%%....%",
        "%%.%%%%%...........%",
        "%..........%.......%",
        "%%%%%%%%%%%%%%%%%%%%"
    ]

    prob = PacmanProblem(grid_map)

    try:
        # RBFS
        path_rbfs, visited_count = rbfs(prob) # yol, ziyaret sayısı

        stats_rbfs = f"Yol: {len(path_rbfs)} adım | Ziyaret Edilen Düğüm: {visited_count}"

        print(f"--- RBFS SONUÇLARI ---")
        result_rbfs = rbfs(prob)
        visualize_path(prob, result_rbfs, "1. RBFS Algoritması (Backtracking İzleme)")

        # SMA*
        path_sma, count_sma = sma_star(prob, max_memory=30)

        print(f"\n--- SMA* SONUÇLARI ---")
        if path_sma:
            result_sma = sma_star(prob, max_memory=50)

            visualize_path(prob, result_sma, "2. SMA* Algoritması")
        else:
            print("SMA* bu bellek miktarı ile çözüm bulamadı!")
    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından sonlandırıldı. (Çıkış yapılıyor...)")