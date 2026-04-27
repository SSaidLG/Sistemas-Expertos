import tkinter as tk
import math

class NimGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("NIM - Minimax")
        self.estado_inicial = [1, 2, 3]
        self.estado = list(self.estado_inicial)
        self.crear_interfaz()

    def crear_interfaz(self):
        for widget in self.master.winfo_children(): widget.destroy()
        
        for i, cant in enumerate(self.estado):
            frame = tk.Frame(self.master)
            frame.pack(pady=5)
            for _ in range(cant):
                tk.Button(frame, text="O", width=4, bg="skyblue", command=lambda f=i: self.jugada_humano(f)).pack(side=tk.LEFT, padx=2)
        
        tk.Button(self.master, text="Reiniciar Juego", command=self.reset).pack(pady=10)

    def reset(self):
        self.estado = list(self.estado_inicial)
        self.crear_interfaz()

    def jugada_humano(self, fila):
        self.estado[fila] -= 1
        self.crear_interfaz()
        if sum(self.estado) > 0: self.master.after(500, self.turno_ia)

    def turno_ia(self):
        def minimax(est, t_max, a, b):
            if sum(est) == 0: return 1 if t_max else -1
            m = -math.inf if t_max else math.inf
            for i in range(len(est)):
                for j in range(1, est[i] + 1):
                    n = list(est); n[i] -= j
                    v = minimax(n, not t_max, a, b)
                    if t_max: m, a = max(m, v), max(a, m)
                    else: m, b = min(m, v), min(b, m)
                    if b <= a: break
            return m

        mejor_val, mejor_mov = -math.inf, None
        for i in range(len(self.estado)):
            for j in range(1, self.estado[i] + 1):
                n = list(self.estado); n[i] -= j
                val = minimax(n, False, -math.inf, math.inf)
                if val > mejor_val: mejor_val, mejor_mov = val, (i, j)
        
        if mejor_mov: self.estado[mejor_mov[0]] -= mejor_mov[1]
        self.crear_interfaz()

if __name__ == "__main__":
    root = tk.Tk()
    app = NimGUI(root)
    root.mainloop()