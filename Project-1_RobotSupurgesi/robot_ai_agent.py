import threading  # aynı anda birden fazla iş yapabilmek için
import time
import random

ROOM_NAMES = ["A", "B"]
POSSIBLE_STATES = ["clean", "dirty"]

room_states = {room: random.choice(POSSIBLE_STATES) for room in ROOM_NAMES}
robot_position = random.choice(ROOM_NAMES)
# kilitlenmesi gerektiğinde kullanılacak anahtarlar:
room_locks = {room: threading.Lock() for room in ROOM_NAMES}
position_lock = threading.Lock()
print_lock = threading.Lock()


def log(log_type, action, message):
    print(f"{log_type:<13}\t{action:<12}\t{message}")


def dirty_rooms():
    while True:
        time.sleep(random.randint(3, 6))
        room_to_dirty = random.choice(list(room_states.keys()))

        # Hangi odayı kirleteceksek, sadece o odanın kilidini alıyoruz.
        with room_locks[room_to_dirty]:
            if room_states[room_to_dirty] == "clean":
                room_states[room_to_dirty] = "dirty"
                log("ENVIRONMENT", "Dirtied", f"Room {room_to_dirty} became dirty")


def robot_agent():
    global robot_position
    while True:
        with position_lock:
            current_room = robot_position

        # Şu anki odanın kilidini alarak durumu kontrol et
        with room_locks[current_room]:
            algılama = room_states[current_room]
            log("ROBOT", "Detection", f"Room {current_room} is {algılama}")

            if algılama == "dirty":  # Temizleme işlemi
                log("ROBOT", "Cleaning", f"Cleaning room {current_room}...")
                time.sleep(5)
                room_states[current_room] = "clean"
                log("ROBOT", "Done", f"Room {current_room} cleaned")

        # Harekete devam etmek için
        if algılama == "clean":
            with position_lock:
                current_room_for_move = robot_position
                new_room = "B" if current_room_for_move == "A" else "A"
                log("ROBOT", "Move", f"{robot_position} -> {new_room}")
                robot_position = new_room

            time.sleep(1)

if __name__ == "__main__":
    print(f"{'TYPE':<13}\t{'ACTION':<12}\tMESSAGE")
    print("-------------\t------------\t------------------------------")
    log("INFO", "Start", f"Initial states: {room_states}, robot at {robot_position}\n")
    time.sleep(1)  # Başlangıcı görmek için küçük bir bekleme

    # Paralel olarak çalışsın diye thread kullandık
    t1 = threading.Thread(target=dirty_rooms, daemon=True)
    t2 = threading.Thread(target=robot_agent, daemon=True)
    t1.start()
    t2.start()

    time.sleep(30)
    print("\n-------------\t------------\t------------------------------")
    log("INFO", "End", "Simulation finished.")
    print("\n--- Summary ---")