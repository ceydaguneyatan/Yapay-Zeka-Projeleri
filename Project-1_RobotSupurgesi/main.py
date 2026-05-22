from robot_ai_agent import *

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