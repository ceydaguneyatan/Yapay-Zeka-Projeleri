import tkinter as tk
from tkinter import messagebox
import time
from board import Board
from hill_climbing_solver import HillClimbingSolver

class NQueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Vezir Problemi: Hill Climbing Çözücü")
        self.size = 8
        self.cell_size = 60
        self.solver = HillClimbingSolver(self.size)

        self.current_board = Board(self.size)

        self.setup_ui()
        self.draw_board(self.current_board)

        # PENCEREYİ ÖNE GETİRME
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.root.focus_force()

    def setup_ui(self):
        self.canvas_area = tk.Frame(self.root)
        self.canvas_area.pack(side=tk.LEFT, padx=10, pady=10)

        self.canvas = tk.Canvas(self.canvas_area,
                                width=self.size * self.cell_size,
                                height=self.size * self.cell_size)
        self.canvas.pack()

        # Sağ Panel: Kontroller
        self.controls = tk.Frame(self.root)
        self.controls.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Bilgi Alanı
        self.lbl_status = tk.Label(self.controls, text="Hazır", font=("Arial", 12, "bold"))
        self.lbl_status.pack(pady=10)

        self.lbl_conflicts = tk.Label(self.controls, text=f"Çatışma: {self.current_board.conflicts}", fg="red",
                                      font=("Arial", 12))
        self.lbl_conflicts.pack(pady=5)

        # Butonlar
        btn_config = {"width": 25, "pady": 5}

        tk.Button(self.controls, text="🔄 Yeni Rastgele Tahta", bg="#ddd",
                  command=self.reset_board, **btn_config).pack(pady=20)

        tk.Label(self.controls, text="--- Algoritmalar ---").pack(pady=5)

        tk.Button(self.controls, text="1. Steepest Ascent (En Dik)", bg="lightblue",
                  command=lambda: self.run_algorithm("steepest"), **btn_config).pack(pady=5)

        tk.Button(self.controls, text="2. Stochastic (Rastgele Seçim)", bg="lightgreen",
                  command=lambda: self.run_algorithm("stochastic"), **btn_config).pack(pady=5)

        tk.Button(self.controls, text="3. Random Restart (Yeniden)", bg="orange",
                  command=lambda: self.run_algorithm("restart"), **btn_config).pack(pady=5)

    def draw_board(self, board):
        self.canvas.delete("all")
        colors = ["#F0D9B5", "#B58863"]  # Satranç renkleri

        for col in range(self.size):
            for row in range(self.size):
                color = colors[(col + row) % 2]
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                # Vezir çizimi
                if board.state[col] == row:
                    self.canvas.create_text(x1 + self.cell_size / 2, y1 + self.cell_size / 2,
                                            text="♛", font=("Arial", 36),
                                            fill="black" if color == "#F0D9B5" else "white")

        self.lbl_conflicts.config(text=f"Çatışma (H): {board.conflicts}",
                                  fg="green" if board.conflicts == 0 else "red")
        self.root.update()

    def reset_board(self):
        self.current_board = Board(self.size)
        self.draw_board(self.current_board)
        self.lbl_status.config(text="Tahta Sıfırlandı", fg="black")

    def run_algorithm(self, algo_type):
        self.lbl_status.config(text="Hesaplanıyor...", fg="blue")
        self.root.update()  # UI güncellensin diye

        # Algoritmayı çalıştır
        if algo_type == "steepest":
            final_board, path = self.solver.steepesst_ascent(self.current_board)
            info = f"Adım: {len(path)}"

        elif algo_type == "stochastic":
            final_board, path = self.solver.stochastic(self.current_board)
            info = f"Adım: {len(path)}"

        elif algo_type == "restart":
            final_board, path, restarts = self.solver.random_restart(self.current_board)
            info = f"Adım: {len(path)} | Restart: {restarts}"

        self.animate_solution(path)

        if final_board.is_goal():
            self.lbl_status.config(text=f"ÇÖZÜM BULUNDU!\n{info}", fg="green")
            messagebox.showinfo("Başarılı", f"Çözüm Bulundu!\n{info}")
        else:
            self.lbl_status.config(text=f"YEREL OPTİMUM!\n{info}", fg="red")
            messagebox.showwarning("Başarısız", f"Yerel Optimuma Takıldı.\nÇözüm Bulunamadı.\n{info}")

        self.current_board = final_board

    def animate_solution(self, path):
        delay = 150 if len(path) < 20 else 50

        for i, board in enumerate(path):
            self.draw_board(board)
            self.lbl_status.config(text=f"Oynatılıyor: {i + 1}/{len(path)}")
            self.root.after(delay)
            self.root.update()