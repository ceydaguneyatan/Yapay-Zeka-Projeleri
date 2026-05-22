import tkinter as tk
from visualization import NQueensGUI

if __name__ == "__main__":
    root = tk.Tk()

    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    app = NQueensGUI(root)
    root.mainloop()