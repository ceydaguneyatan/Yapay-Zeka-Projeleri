from pacman_node import Node, reconstruct_path

"""Informed Search (Bilgili/Sezgisel Arama)"""

"""Recursive Best-First Search - Özyinelemeli En İyi Öncelikli Arama"""

def rbfs(problem):
    visited_order = []

    def recursive(node, f_limit):
        visited_order.append(node.state)

        if node.state == problem.goal:# hedefte isek
            return reconstruct_path(node), node.f # geriye doğru yol oluşturarak maliyeti dön

        successors = [] # çocukları oluşturur: burdan nereye gidebilirim
        for next_state in problem.get_neighbors(node.state):
            if node.parent and next_state == node.parent.state:
                # node.parent varsa ve next_state, demin geldiğimiz yol ise (node.parent.state)
                continue
            g = node.g + 1 # adım sayısı arttı
            h = problem.heuristic(next_state) # yeni h değeri oluşur
            child = Node(next_state, node, g, h)
            child.f = max(child.f, node.f) # çocuğun maliyeti ebeveyninden düşük olamaz.
            successors.append(child)

        if not successors: # gidecek bir yeri yoksa (her yer duvar veya sadece geldiğim yer var)
            return None, float('inf')

        # rbfs burada çalışır. sürekli en iyi çocuğu seçer, dener, olmazsa fikrini değiştirir
        while True:
            successors.sort(key=lambda x: x.f) # çocukları maliyetlerine göre küçükten büyüğe sırala
            best = successors[0] # en düşük maliyetli

            if best.f > f_limit: # bu bile limiti aştıysa
                return None, best.f

            if len(successors) > 1:
                alternative = successors[1].f # ikinci en iyi çocuğun sadece MALİYETİNİ tutuyoruz
            else: # tek çocuk varsa
                alternative = float('inf') # maliyeti sonsuzdur yani min aldığımız için bu maliyet asla seçilmez

            result, best.f = recursive(best, min(f_limit, alternative))

            if result is not None: return result, best.f

    start_node = Node(problem.start, None, 0, problem.heuristic(problem.start))
    path, _ = recursive(start_node, float('inf'))

    return path, visited_order


"""Simplified Memory-Bounded A* - Basitleştirilmiş Bellek Sınırlı A*"""

def sma_star(problem, max_memory=100):
    start_node = Node(problem.start, None, 0, problem.heuristic(problem.start))
    queue = [start_node] # gidebilceğimiz yolların listesi
    explored = {start_node.state: start_node.f} # {koordinat: maliyet} tutan hafıza defteri
    visited_order = []

    while queue:
        queue.sort(key=lambda x: (x.f, -x.g))
        # öncelik x.f: toplam maliyeti düşük olan
        # maliyetler eşitse daha çok yol gideni (g>) öne al
        # başına eksi koyduk ki büyük olanı küçük görsün çünkü sort küçükten büyüğe sıralar

        best = queue.pop(0) # en düşük f'li olanı kuyruktan aldık
        visited_order.append(best.state)

        if best.state == problem.goal:
            return reconstruct_path(best), visited_order

        # komşuları gez
        for succ_state in problem.get_neighbors(best.state):
            # geldiğimiz yere geri dönmeyelim
            if best.parent and succ_state == best.parent.state:
                continue

            g = best.g + 1
            h = problem.heuristic(succ_state)
            child = Node(succ_state, best, g, h) # yeni değerleri paketledik

            # hafıza defterinde daha önce varsa ve şuanki maliyeti eşit veya daha yüksekse
            if succ_state in explored and explored[succ_state] <= child.f:
                continue

            queue.append(child)
            explored[succ_state] = child.f

            # sma* nın öenmli kısmı: bellek yönetimi
            if len(queue) > max_memory: # limitimize ulaştıysak
                queue.sort(key=lambda x: (x.f, -x.g)) # tekrar düzgünce sırala

                # listenin en sonu (en kötü yani f en yüksek) olanı:
                worst_node = queue.pop(-1) # kuyruktan çıkar

                if worst_node.state in explored: # hafızadan da silmeyi unutma
                    del explored[worst_node.state] # bu düğümü artık sil

    return None, visited_order

"""explored ve queue mantığı"""
# hafızadan da sileriz çünkü diyelim ilerde belki bu daha az maliyetli sandığımız yolların hepsi duvara çıktı, geri sardık ve bu kareye geri döndük,
# kuyruktan sildik ama exploreddan silmediğimiz için kontrol ettiğimizde exploredda var sandık ama aslında kuyruktan silmiştik, yani şuan elimizde yok
# ve belkide hedefe giden yol sadece oydu. bu kareyi sonsuza kadar kaybederiz
# peki neden queueda değil exploredda tutar ve exploredda kontrol ederiz
# çünkü bir dictionaryda eleman aramak O(1)'dir, queueda ise ne kadar eleman varsa o kadardır
# diğer bir sebep queue sadece sırasını bekleyenleri tutar, bir kare ziyaret edilince onu kuyruktan çıkarır.
# explored ise hem bekleyenleri (aynı kareyi tekrar almamak için) hem ziyaret edilenleri tutar