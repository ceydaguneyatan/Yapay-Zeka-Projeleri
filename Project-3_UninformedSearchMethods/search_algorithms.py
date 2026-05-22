import heapq
from collections import deque

"""Uninformed Search (Kör Arama Algoritmaları)"""

"""Uniform Cost Search - Öncelikli Arama"""
# en düşük maliyetli yolu bulur. burda maliyetler eşit olduğu için aynı BFS gibi davranır
def ucs(problem):
    # priority queue: öncelik kuyruğu
    pq = [(0, problem.start, [problem.start])] # maliyet, konum, şu ana kadarki yol
    visited_set = set() # hızlıca "visited in" kontrolü için
    visited_order = [] # Hangi düğüm önce genişletildi?

    while pq:
        cost, current, path = heapq.heappop(pq) # heappop, tuttuğu özel yapılı ağacın içinden en düşük maliyetli elemanı seçer

        if current not in visited_set:
        # daha önce geldiyse, daha az maliyet ile geldiği için yüksek maliyetliyi direk çöpe atar
            visited_set.add(current)
            visited_order.append(current)

            if current == problem.goal:
                return path, visited_order

            for neigh in problem.get_neighbors(current): # şuanki karenin komşuları
                new_cost = cost + 1
                new_path = path + [neigh]
                heapq.heappush(pq, (new_cost, neigh, new_path))
    return None, visited_order

"""Iterative Deepening Search - Kademeli Derinleşen Arama"""
# her seferinde derinliği 1 arttırarak aramaya baştan başlar
# bir yola girdi mi, duvara çarpana veya limite takılana kadar o yoldan dönmez
def ids(problem):
    depth = 0

    while True:
        visited_history = set()
        visited_order = []

        result = dls(problem, problem.start, depth, [problem.start], visited_history, visited_order)

        if result:
            return result, visited_order

        depth += 1
        if depth > 100:
            return None

"""Depth Limited Search - Derinlik Sınırlı Arama"""
def dls(problem, node, limit, path, visited_history, visited_order):
   # DLS, sadece kendisine verilen limit kadar ilerler. limiti gittikçe arttıran IDS'dir
    visited_history.add(node)
    visited_order.append(node)

    if node == problem.goal:
        return path

    if limit <= 0:
        return None

    for neigh in problem.get_neighbors(node):
        if neigh not in path: # gitmek istediğim komşu, geldiğim pathin üstünde ise oraya gitme
            # recursive kısmı
            result = dls(problem, neigh, limit - 1, path + [neigh], visited_history, visited_order) #buradaki limit - 1 ile elindeki hakkı tüketir
            if result:
                return result
           # geri dönerken (Backtracking) burası çalışır
    return None

"""Bidirectional Search - Çift Yönlü Arama"""
def bids(problem):
    # iki taraftan başlayıp ortada buluşur
    q_start = deque([(problem.start, [problem.start])])
    q_goal = deque([(problem.goal, [problem.goal])]) # sondan başlayıp geriye doğru gelir

    # dictionarydir çünkü : [path] ile buraya hangi yoldan geldim bilgisini tutar
    visited_start = {problem.start: [problem.start]}
    visited_goal = {problem.goal: [problem.goal]}

    visited_order = []

    while q_start and q_goal:
        if q_start:
            curr, path = q_start.popleft()
            visited_order.append((curr, 1))

            if curr in visited_goal: # karşı taraftan gelen ekip curr'a daha önce geldi mi
                path_from_goal = visited_goal[curr]
                return (path + path_from_goal[::-1][1:], visited_order) # ters çeviririz ([::-1]) ve buluşma noktasını 2 kere yazmayız ([1:])

            for neigh in problem.get_neighbors(curr):
                if neigh not in visited_start: # kendi tarafımda daha önce gelmediysem
                    new_path = path + [neigh]
                    visited_start[neigh] = new_path
                    q_start.append((neigh, new_path))

        if q_goal:
            curr_g, path_g = q_goal.popleft()
            visited_order.append((curr_g, 2))

            if curr_g in visited_start: # start ekibi buraya geldi mi ?
                path_from_start = visited_start[curr_g]
                return (path_from_start, path_g[::-1]), visited_order

            for neigh in problem.get_neighbors(curr_g):
                if neigh not in visited_goal:
                    new_path = path_g + [neigh]
                    visited_goal[neigh] = new_path
                    q_goal.append((neigh, new_path))
    return None, visited_order