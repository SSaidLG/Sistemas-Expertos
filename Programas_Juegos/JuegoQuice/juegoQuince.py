import tkinter as tk
import heapq

class Puzzle15:
    def __init__(self, master):
        self.master = master
        self.master.title("15-Puzzle - A*")
        self.inicial = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 15)
        self.estado = self.inicial
        self.crear_tablero()

    def crear_tablero(self):
        for widget in self.master.winfo_children(): widget.destroy()
        frame = tk.Frame(self.master)
        frame.pack()
        for i in range(4):
            for j in range(4):
                val = self.estado[i*4+j]
                tk.Button(frame, text=str(val) if val!=0 else "", width=5, height=2, font=('Arial', 20),
                          command=lambda p=(i*4+j): self.mover(p)).grid(row=i, column=j, padx=2, pady=2)
        
        btn_f = tk.Frame(self.master)
        btn_f.pack(pady=10)
        tk.Button(btn_f, text="Resolver (A*)", command=self.resolver).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_f, text="Reiniciar", command=self.reset).pack(side=tk.LEFT, padx=5)

    def reset(self):
        self.estado = self.inicial
        self.crear_tablero()

    def mover(self, pos):
        v = self.estado.index(0)
        if pos in [v-1, v+1, v-4, v+4]:
            if (pos==v-1 and v%4==0) or (pos==v+1 and v%4==3): return
            l = list(self.estado); l[v], l[pos] = l[pos], l[v]
            self.estado = tuple(l); self.crear_tablero()

    def resolver(self):
        obj = tuple(list(range(1, 16)) + [0])
        def h(est): return sum(abs(i%4-obj.index(v)%4)+abs(i//4-obj.index(v)//4) for i,v in enumerate(est) if v!=0)
        
        cola = [(h(self.estado), self.estado, [])]
        vis = {self.estado}
        while cola:
            _, act, cam = heapq.heappop(cola)
            if act == obj: self.animar(cam); return
            v = act.index(0)
            for m in [-1, 1, -4, 4]:
                if (m==-1 and v%4==0) or (m==1 and v%4==3) or (v+m<0) or (v+m>15): continue
                n = list(act); n[v], n[v+m] = n[v+m], n[v]; nt = tuple(n)
                if nt not in vis:
                    vis.add(nt)
                    heapq.heappush(cola, (len(cam)+1+h(nt), nt, cam+[v+m]))

    def animar(self, cam):
        if cam: self.mover(cam.pop(0)); self.master.after(200, lambda: self.animar(cam))

if __name__ == "__main__":
    root = tk.Tk()
    app = Puzzle15(root)
    root.mainloop()