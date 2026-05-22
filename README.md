## Yapay Zeka Algoritmaları ve Simülasyonları

Fatih Sultan Mehmet Vakıf Üniversitesi Yapay Zeka dersi kapsamında geliştirilen temel arama algoritmaları, yerel optimizasyon yöntemleri ve ajan tabanlı simülasyonları içeren proje setidir. Bu depo, kör arama algoritmalarından sezgisel yöntemlere kadar çeşitli yapay zeka konseptlerinin uygulanmasını barındırmaktadır.

---

### Proje 1: Robot Süpürgesi Simülasyonu

Bu proje, çevre ile eş zamanlı etkileşime giren reaktif bir ajan (reactive agent) simülasyonudur. Ortam kendi kendine rastgele kirlenirken, robot süpürge odaları gezer, kirliliği algılar ve temizler.

- **Kullanılan Yapılar:** Ortamın ve robotun aynı anda çalışabilmesi için `threading` (çoklu iş parçacığı) kütüphanesi kullanılmıştır. Veri çakışmalarını önlemek adına odalar ve robot pozisyonu `Lock` mekanizmaları ile güvence altına alınmıştır.

---

### Proje 2: Pacman Ajanı

Klasik Pac-Man oyununun, yapay zeka tarafından oynanması üzerine kurulu bir problem çözme projesidir. Amaç, Pac-Man'in bulunduğu labirentte hedefe ulaşması için kendi kararlarını verebilmesidir.

- **Kullanılan Yapılar:** Oyun tahtası ve hareketler birer durum (state) ve düğüm (node) olarak modellenmiştir. Ajan, bu durumlar arasında graf tabanlı gezinme mantığı ile yolunu bulur.

---

### Proje 3: Kör Arama Yöntemleri (Uninformed Search)

Bu proje, hedefin nerede olduğuna dair hiçbir bilgisi olmayan, sadece deneme yanılma ve maliyet hesaplaması ile yolu bulan algoritmaları içerir.

- **Uniform Cost Search (UCS):** Her adımda en düşük maliyetli yolu seçerek ilerler. Hızlı maliyet sıralaması yapabilmek için `heapq` (öncelikli kuyruk) veri yapısı kullanılmıştır.

- **Depth Limited Search (DLS):** Sonsuz döngülere girmemek için aramayı sadece kendisine verilen belirli bir derinlik (adım sayısı) limitine kadar yapar. Özyinelemeli (recursive) bir yapı üzerine kuruludur.

- **Iterative Deepening Search (IDS):** Aramaya önce 0 derinlikle başlar, bulamazsa derinliği 1 artırıp baştan başlar. Hedefi bulana kadar bu işlemi kademeli olarak artırır. İçerisinde DLS fonksiyonunu çağırarak çalışır.

- **Bidirectional Search:** Hem başlangıç noktasından ileriye hem de hedef noktasından geriye doğru aynı anda arama yapar. Ortada buluştuklarında arama biter. Uçlardan hızlı veri çekebilmek için çift yönlü kuyruk olan `deque` ve geçilen yolları hatırlamak için sözlük (dictionary) yapıları kullanılmıştır.

---

### Proje 4: Bilgili Arama Yöntemleri (Informed Search)

Bu proje, sezgisel bir tahmin (heuristic) kullanarak hedefe daha akıllıca ve kısa yoldan ulaşmaya çalışan algoritmaları içerir.

- **Recursive Best-First Search (RBFS):** En iyi yolu denerken, her zaman ikinci en iyi yolun maliyetini aklında tutar. Eğer gittiği yolun maliyeti ikinci en iyi seçeneği geçerse, geri dönüp diğer yoldan devam eder. Bellekte çok az yer kaplayan özyinelemeli bir ağaç yapısı kullanır.

- **Simplified Memory-Bounded A\* (SMA\*):** Klasik A* algoritmasının bellek dostu versiyonudur. Kendisine verilen maksimum bellek limitine (kuyruk kapasitesine) ulaştığında, en kötü ihtimale sahip olan düğümleri silerek yer açar. Verileri sıralı tutmak için listeler ve silinen yolların kaybolmaması için bir hafıza sözlüğü (explored) kullanır.

---

### Proje 5: Tepe Tırmanma Optimizasyonu (Hill Climbing)

Bu proje, karmaşık arama uzaylarında en iyi çözümü (minimum hata/maksimum başarı) bulmaya çalışan yerel arama yöntemlerini içerir.

- **Steepest Ascent:** Bulunduğu noktadaki tüm komşularına bakar ve mevcut durumundan daha iyi olanlar arasından "en iyisini" seçerek ilerler.

- **Stochastic:** Sadece en iyiye odaklanmak yerine, mevcut durumdan daha iyi olan komşular arasından rastgele birini seçerek ilerler. Bu sayede tahmin edilebilirliği kırar.

- **Random Restart:** Algoritma çevresindeki her yerin daha kötü olduğu ama aslında hedefe ulaşmadığı "yerel optimum" tuzaklarına düştüğünde, pes etmek yerine tahtayı tamamen sıfırlayarak rastgele yeni bir noktadan aramaya baştan başlar.