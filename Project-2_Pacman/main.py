import pygame as pg
import sys
from settings import *
from game import Game

if __name__ == "__main__":
    pg.init()

    # Skor veritabanı
    results = {
        "human": {"score": 0, "time": 0, "perf": 0},
        "ai": {"score": 0, "time": 0, "perf": 0}
    }

    next_mode = None

    while True:
        game = Game()

        # 1. Başlangıç Ekranı (Sadece ilk açılışta veya ana menüye dönüldüyse)
        if next_mode is None:
            choice = game.start_screen()
            if choice == "quit":
                break
            next_mode = choice

        # 2. Oyunu Oynat
        game.player.control_type = next_mode
        game.run()

        # 3. İstatistikleri Hesapla
        final_time = (pg.time.get_ticks() - game.start_time) / 1000
        metric = game.score / final_time if final_time > 0 else 0

        results[next_mode]["score"] = game.score
        results[next_mode]["time"] = final_time
        results[next_mode]["perf"] = metric

        # 4. TEK SONUÇ EKRANI (Burada kullanıcı tekrar seçim yapar)
        next_mode = game.show_unified_results(results, next_mode)

        if next_mode == "quit":
            break

        # Oyun yeniden başlarken sesleri temizle
        game.quit_for_restart()

    pg.quit()
    sys.exit()