import tkinter as tk

class CuadroMagico:
    def __init__(self, root):
        self.root = root
        self.root.title("Cuadro Mágico - Backtracking")
        self.celdas = []
        self.crear_interfaz()

    def crear_interfaz(self):
        for i in range(3):
            for j in range(3):
                e = tk.Entry(self.root, width=3, font=('Arial', 30), justify='center')
                e.grid(row=i, column=j, padx=5, pady=5)
                self.celdas.append(e)
                
        tk.Button(self.root, text="Resolver", command=self.resolver).grid(row=3, column=0, pady=10)
        tk.Button(self.root, text="Reiniciar", command=self.reset).grid(row=3, column=2, pady=10)

    def reset(self):
        for c in self.celdas:
            c.delete(0, tk.END)

    def resolver(self):
        def es_valido(c):
            if len(c) == 9:
                s = sum(c[0:3])
                return all([sum(c[3:6])==s, sum(c[6:9])==s, sum(c[0::3])==s, sum(c[1::3])==s, sum(c[2::3])==s, c[0]+c[4]+c[8]==s, c[2]+c[4]+c[6]==s])
            return True

        def backtrack(c, disp):
            if len(c) == 9: return c if es_valido(c) else None
            for n in list(disp):
                disp.remove(n)
                res = backtrack(c + [n], disp)
                if res: return res
                disp.add(n)
            return None

        self.reset()
        solucion = backtrack([], set(range(1, 10)))
        if solucion:
            for i, val in enumerate(solucion):
                self.celdas[i].insert(0, str(val))

if __name__ == "__main__":
    root = tk.Tk()
    app = CuadroMagico(root)
    root.mainloop()