import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np


def visualize_path(problem, result_data, algorithm_name="Algoritma", is_last=False):
    # 1. VERİYİ AYIKLAMA
    visited_order = []

    if isinstance(result_data, tuple):
        path_data = result_data[0]
        visited_order = result_data[1]
    else:
        path_data = result_data

    if not visited_order and not path_data:
        print("Çözüm veya gezilen düğüm yok!")
        return

    # 2. HARİTAYI OLUŞTURMA
    rows, cols = problem.rows, problem.cols
    map_matrix = np.zeros((rows, cols))

    for r in range(rows):
        for c in range(cols):
            char = problem.grid_str[r][c]
            if char == '%':
                map_matrix[r][c] = 1
            else:
                map_matrix[r][c] = 0

    # Arkaplan renkleri
    cmap = colors.ListedColormap(['white', '#2c3e50'])
    fig, ax = plt.subplots(figsize=(10, 6))
    if not is_last:
        fig.text(0.5, 0.02,
                 "İPUCU: Animasyonu atlamak ve diğer algoritmaya geçmek için pencereyi kapatınız (X)",
                 ha='center', fontsize=10, color='red', style='italic')

    ax.imshow(map_matrix, cmap=cmap)
    ax.set_xticks([]);
    ax.set_yticks([])

    # Start/Goal harfleri
    ax.text(problem.start[1], problem.start[0], "S", color='green', fontweight='bold', ha='center', va='center',
            fontsize=12, zorder=5)
    ax.text(problem.goal[1], problem.goal[0], "G", color='red', fontweight='bold', ha='center', va='center',
            fontsize=12, zorder=5)

    title = ax.set_title(f"{algorithm_name} Başlıyor...", fontsize=12)

    # 3. ANİMASYON HAZIRLIĞI (İki farklı scatter kullanacağız)
    # Start tarafı (Cyan), Goal tarafı (Magenta)
    scat_start = ax.scatter([], [], c='#00FFFF', s=60, alpha=0.7, label='Start Araması')
    scat_goal = ax.scatter([], [], c='#FF00FF', s=60, alpha=0.7, label='Goal Araması')

    # --- KAFA (HEAD) - O an nerede? ---
    scat_head_start = ax.scatter([], [], c='blue', s=150, edgecolors='white', zorder=10, label='Konum (Start)')
    # Goal tarafından gelen kafa (Kırmızı) - Sadece BiDS kullanır
    scat_head_goal = ax.scatter([], [], c='#800020', s=150, edgecolors='white', zorder=10, label='Konum (Goal)')

    # Koordinat listeleri
    xs_start, ys_start = [], []
    xs_goal, ys_goal = [], []

    total_steps = len(visited_order)
    skip = 1
    if total_steps > 1000:
        skip = 50
    elif total_steps > 125:
        skip = 2
    elif total_steps > 50:
        skip = 1

    print(f"{algorithm_name}: {total_steps} adım oynatılıyor...")

    # --- ANİMASYON DÖNGÜSÜ ---
    for i, item in enumerate(visited_order):

        if not plt.fignum_exists(fig.number):
            print(f"{algorithm_name} animasyonu kullanıcı tarafından kesildi.")
            return  # Fonksiyondan çık, sonraki algoritmaya geç

        node = None
        side = 1

        # BiDS verisi kontrolü: ((r,c), side)
        if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], tuple):
            node = item[0]
            side = item[1]
        else:
            # Normal algoritma verisi: (r, c)
            node = item
            side = 1

        if node == problem.start: continue

        if side == 1:
            xs_start.append(node[1])
            ys_start.append(node[0])
        else:
            xs_goal.append(node[1])
            ys_goal.append(node[0])

        if i % skip == 0:
            if xs_start: scat_start.set_offsets(np.c_[xs_start, ys_start])
            if xs_goal: scat_goal.set_offsets(np.c_[xs_goal, ys_goal])

            if side == 1:
                scat_head_start.set_offsets(np.c_[[node[1]], [node[0]]])
            else:
                scat_head_goal.set_offsets(np.c_[[node[1]], [node[0]]])

            title.set_text(f"{algorithm_name}: Adım {i}/{total_steps}")
            plt.pause(0.02)

    # Son durumu çiz
    if xs_start: scat_start.set_offsets(np.c_[xs_start, ys_start])
    if xs_goal: scat_goal.set_offsets(np.c_[xs_goal, ys_goal])

    # 2. Mavi Kafayı Yerleştirme Mantığı
    if path_data:
        # EĞER BİR YOL BULUNDUYSA (ÇÖZÜM VARSA)

        if isinstance(path_data, tuple):
            # BiDS Durumu: Zaten yıldız var, kafayı ekrandan
            scat_head_start.set_offsets(np.empty((0, 2)))
            scat_head_goal.set_offsets(np.empty((0, 2)))

        else:
            # NORMAL ALGORİTMALAR (UCS, IDS, RBFS, SMA*)
            # Kafayı kesinlikle yolun bittiği yere (GOAL) ışınla!
            final_node = path_data[-1]  # Yolun sonu her zaman Hedef'tir.
            scat_head_start.set_offsets(np.c_[[final_node[1]], [final_node[0]]])

    elif visited_order:
        # EĞER ÇÖZÜM YOKSA ama gezilen yerler varsa son yere koy
        last_item = visited_order[-1]
        last_node = last_item if not (isinstance(last_item, tuple)) else last_item[0]
        scat_head_start.set_offsets(np.c_[[last_node[1]], [last_node[0]]])

    # 4. SONUÇ YOLUNU ÇİZME
    if path_data:
        if isinstance(path_data, tuple):
            # BiDS Çizimi
            path_s, path_g = path_data
            py_s, px_s = zip(*path_s)
            ax.plot(px_s, py_s, color='blue', linewidth=4, alpha=0.8, label='Start Yolu')
            py_g, px_g = zip(*path_g)
            ax.plot(px_g, py_g, color='red', linewidth=4, alpha=0.8, label='Goal Yolu')

            meet_node = path_s[-1]
            ax.scatter(meet_node[1], meet_node[0], marker='*', s=300, c='yellow', edgecolors='black', zorder=15,
                       label='Buluşma')

            title.set_text(f"{algorithm_name} Tamamlandı! Buluşma: {meet_node} | Oynatılan Adım: {total_steps}")
        else:
            # Normal Yol Çizimi
            py, px = zip(*path_data)
            ax.plot(px, py, color='red', linewidth=4, alpha=0.9)
            title.set_text(f"{algorithm_name} Tamamlandı! Yol: {len(path_data)} birim | Oynatılan Adım: {total_steps}")
    else:
        title.set_text(f"{algorithm_name}: Hedefe Ulaşılamadı!")

    if plt.fignum_exists(fig.number):
        plt.show()