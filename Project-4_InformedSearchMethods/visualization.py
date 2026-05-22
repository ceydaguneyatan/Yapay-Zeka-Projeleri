import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np


def visualize_path(problem, result_data, algorithm_name="Algoritma"):

    visited_order = []

    if isinstance(result_data, tuple):
        path = result_data[0]
        visited_order = result_data[1]  # Animasyon listesi
    else:
        path = result_data  # Sadece yol döndüyse (eski tip)

    if not visited_order and not path:
        print(f"{algorithm_name}: Çözüm veya gezilen düğüm yok!")
        return

    # Harita Hazırlığı
    rows, cols = problem.rows, problem.cols
    map_matrix = np.zeros((rows, cols))

    for r in range(rows):
        for c in range(cols):
            char = problem.grid[r][c]  # Senin sınıfında grid veya grid_str olabilir, kontrol et
            if char == '%':
                map_matrix[r][c] = 1  # Duvar
            else:
                map_matrix[r][c] = 0  # Yol

    cmap = colors.ListedColormap(['white', '#2c3e50'])

    # Çizim Başlat
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(map_matrix, cmap=cmap)
    ax.set_xticks([]);
    ax.set_yticks([])

    ax.text(problem.start[1], problem.start[0], "S", color='green', fontweight='bold', ha='center',
                        va='center', fontsize=12)
    ax.text(problem.goal[1], problem.goal[0], "G", color='red', fontweight='bold', ha='center', va='center',
                       fontsize=12)

    title = ax.set_title(f"{algorithm_name} Başlıyor...", fontsize=12)

    # --- ANİMASYON ---
    # 1. GEÇMİŞ İZLER (Turuncu Noktalar)
    visited_x, visited_y = [], []
    scat_history = ax.scatter([], [], c='orange', s=60, alpha=0.5, label='Ziyaret Edilen')

    # 2. GÜNCEL KONUM (Mavi Büyük Nokta - KAFA)
    scat_head = ax.scatter([], [], c='blue', s=150, edgecolors='white', zorder=10, label='Güncel Konum')

    # Hız Ayarı (Adım sayısı çoksa kare atla)
    total_steps = len(visited_order)
    skip = 1
    if total_steps > 1000:
        skip = 10
    elif total_steps > 200:
        skip = 4
    elif total_steps > 50:
        skip = 1

    print(f"{algorithm_name}: {total_steps} adım oynatılıyor...")

    for i, node in enumerate(visited_order):
        if node == problem.start: continue

        visited_x.append(node[1])
        visited_y.append(node[0])

        if i % skip == 0:  # Ekranı güncelle
            scat_history.set_offsets(np.c_[visited_x, visited_y])
            scat_head.set_offsets(np.c_[[node[1]], [node[0]]])
            title.set_text(f"{algorithm_name}: Adım {i}/{total_steps}")
            plt.pause(0.001)  # Çok kısa bekle

    if visited_order:
        last_node = visited_order[-1]
        scat_history.set_offsets(np.c_[visited_x, visited_y])
        scat_head.set_offsets(np.c_[[last_node[1]], [last_node[0]]])

    # --- YOLU ÇİZ (SONUÇ) ---
    if path:
        py, px = zip(*path)
        ax.plot(px, py, color='red', linewidth=3, alpha=0.8)
        title.set_text(f"{algorithm_name} Bitti! Yol: {len(path)} br | Toplam Adım: {total_steps}")
    else:
        title.set_text(f"{algorithm_name}: Hedefe Ulaşılamadı! (Toplam Adım: {total_steps})")
    plt.show()