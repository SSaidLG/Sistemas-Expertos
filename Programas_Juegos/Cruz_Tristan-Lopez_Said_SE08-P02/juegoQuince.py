# =============================================================================
# Integrantes :
# 1. Cruz Hernandez Tristan Javier
# 2. Lopez Garcia Said Eduardo
#
# Descripción breve del código:
# Implementación del clásico Juego del Quince (15-Puzzle) con interfaz gráfica
# en Tkinter. Incluye una función para resolver el rompecabezas de manera 
# automática utilizando el algoritmo de búsqueda A* (A-estrella). Se utiliza la 
# heurística de la Distancia de Manhattan para calcular el costo desde el estado
# actual hasta el estado objetivo, encontrando así el camino más eficiente.
# =============================================================================

import tkinter as tk
import heapq

class Puzzle15:
    def __init__(self, master):
        # Inicializa la ventana y define el estado inicial del rompecabezas.
        # El número 0 representa la casilla vacía.
        self.master = master
        self.master.title("15-Puzzle - A*")
        self.inicial = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 15)
        self.estado = self.inicial
        self.crear_tablero()

    def crear_tablero(self):
        # Limpia la interfaz actual y genera una cuadrícula de 4x4.
        for widget in self.master.winfo_children(): 
            widget.destroy()
            
        frame = tk.Frame(self.master)
        frame.pack()
        
        # Crea los 16 botones iterando sobre el estado actual
        for i in range(4):
            for j in range(4):
                val = self.estado[i*4+j]
                # Si el valor es 0 (espacio vacío), no muestra texto.
                tk.Button(frame, text=str(val) if val!=0 else "", width=5, height=2, font=('Arial', 20),
                          command=lambda p=(i*4+j): self.mover(p)).grid(row=i, column=j, padx=2, pady=2)
        
        # Agrega los botones de control en la parte inferior
        btn_f = tk.Frame(self.master)
        btn_f.pack(pady=10)
        tk.Button(btn_f, text="Resolver (A*)", command=self.resolver).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_f, text="Reiniciar", command=self.reset).pack(side=tk.LEFT, padx=5)

    def reset(self):
        # Devuelve el rompecabezas a su estado desordenado inicial
        self.estado = self.inicial
        self.crear_tablero()

    def mover(self, pos):
        # Lógica para mover una ficha manualmente o durante la animación.
        v = self.estado.index(0) # Encuentra la posición actual del espacio vacío (0)
        
        # Verifica si la posición clicada es adyacente (arriba, abajo, izquierda, derecha)
        if pos in [v-1, v+1, v-4, v+4]:
            # Evita movimientos inválidos que "crucen" los bordes laterales del tablero
            if (pos==v-1 and v%4==0) or (pos==v+1 and v%4==3): 
                return
                
            # Intercambia la ficha seleccionada con el espacio vacío
            l = list(self.estado)
            l[v], l[pos] = l[pos], l[v]
            self.estado = tuple(l)
            self.crear_tablero() # Refresca el tablero visualmente

    def resolver(self):
        # Define el estado objetivo o meta: los números del 1 al 15 ordenados, con el 0 al final.
        obj = tuple(list(range(1, 16)) + [0])
        
        # Función Heurística (Distancia de Manhattan): Calcula cuántos pasos le faltan a 
        # cada ficha para llegar a su posición final correcta (ignorando obstáculos).
        def h(est): 
            return sum(abs(i%4-obj.index(v)%4)+abs(i//4-obj.index(v)//4) for i,v in enumerate(est) if v!=0)
        
        # Cola de prioridad para el algoritmo A*. Guarda tuplas: (Costo Total, Estado Actual, Camino Recorrido)
        cola = [(h(self.estado), self.estado, [])]
        vis = {self.estado} # Set de estados visitados para no entrar en bucles infinitos
        
        while cola:
            # Extrae el nodo con el menor costo estimado (f = g + h)
            _, act, cam = heapq.heappop(cola)
            
            # Si el estado actual es igual al objetivo, encontramos la solución
            if act == obj: 
                self.animar(cam)
                return
                
            v = act.index(0) # Posición del hueco vacío
            
            # Explora los 4 movimientos posibles (izquierda, derecha, arriba, abajo)
            for m in [-1, 1, -4, 4]:
                # Descarta movimientos que salen del tablero o cruzan bordes
                if (m==-1 and v%4==0) or (m==1 and v%4==3) or (v+m<0) or (v+m>15): 
                    continue
                    
                # Genera un nuevo estado hipotético
                n = list(act); n[v], n[v+m] = n[v+m], n[v]; nt = tuple(n)
                
                # Si el estado no ha sido visitado, se evalúa y se mete a la cola de prioridad
                if nt not in vis:
                    vis.add(nt)
                    # El costo total es: pasos dados (len(cam) + 1) + distancia estimada (h(nt))
                    heapq.heappush(cola, (len(cam)+1+h(nt), nt, cam+[v+m]))

    def animar(self, cam):
        # Reproduce la lista de movimientos ('cam') encontrada por A* de forma visual
        # y recursiva con un retraso de 200 milisegundos entre cada paso.
        if cam: 
            self.mover(cam.pop(0))
            self.master.after(200, lambda: self.animar(cam))

if __name__ == "__main__":
    # Inicializa la ventana de Tkinter
    root = tk.Tk()
    app = Puzzle15(root)
    root.mainloop()