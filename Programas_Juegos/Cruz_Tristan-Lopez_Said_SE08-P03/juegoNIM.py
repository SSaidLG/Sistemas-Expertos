# =============================================================================
# Integrantes :
# 1. Cruz Hernandez Tristan Javier
# 2. Lopez Garcia Said Eduardo
#
# Descripción breve del código:
# Interfaz gráfica para el juego NIM desarrollada con Tkinter. El estado inicial
# consta de filas con 1, 2 y 3 objetos. Un jugador humano se enfrenta a una IA 
# que toma decisiones utilizando el algoritmo Minimax con poda Alfa-Beta. El 
# algoritmo simula todas las posibles reducciones de objetos para maximizar las 
# posibilidades de victoria de la máquina y predecir los movimientos del rival.
# =============================================================================

import tkinter as tk
import math

class NimGUI:
    def __init__(self, master):
        # Inicializa la ventana principal y define el estado inicial del juego.
        # En este caso clásico de NIM, usamos 3 filas con 1, 2 y 3 objetos respectivamente.
        self.master = master
        self.master.title("NIM - Minimax")
        self.estado_inicial = [1, 2, 3]
        self.estado = list(self.estado_inicial)
        self.crear_interfaz()

    def crear_interfaz(self):
        # Limpia los widgets anteriores de la ventana para evitar duplicados al actualizar.
        for widget in self.master.winfo_children(): 
            widget.destroy()
        
        # Recorre el estado actual y dibuja un botón ("O") por cada objeto disponible en cada fila.
        for i, cant in enumerate(self.estado):
            frame = tk.Frame(self.master)
            frame.pack(pady=5)
            for _ in range(cant):
                tk.Button(frame, text="O", width=4, bg="skyblue", command=lambda f=i: self.jugada_humano(f)).pack(side=tk.LEFT, padx=2)
        
        # Botón general para reiniciar la partida en cualquier momento.
        tk.Button(self.master, text="Reiniciar Juego", command=self.reset).pack(pady=10)

    def reset(self):
        # Restaura la lista de objetos al estado original [1, 2, 3] y redibuja la interfaz.
        self.estado = list(self.estado_inicial)
        self.crear_interfaz()

    def jugada_humano(self, fila):
        # Procesa la jugada del humano: al hacer clic en un objeto, se resta 1 a esa fila.
        self.estado[fila] -= 1
        self.crear_interfaz() # Actualiza la pantalla para reflejar que el objeto desapareció.
        
        # Si aún quedan objetos en el tablero, pasa el turno a la Inteligencia Artificial
        # después de una pausa de 500 milisegundos.
        if sum(self.estado) > 0: 
            self.master.after(500, self.turno_ia)

    def turno_ia(self):
        def minimax(est, t_max, a, b):
            # Algoritmo recursivo que simula los futuros movimientos posibles de ambos jugadores.
            # 't_max' indica si es el turno de maximizar (IA) o minimizar (Humano).
            # 'a' y 'b' (alfa y beta) sirven para "podar" ramas inútiles y calcular más rápido.
            
            if sum(est) == 0: 
                return 1 if t_max else -1 # Retorna 1 si gana la IA, -1 si gana el humano.
            
            m = -math.inf if t_max else math.inf
            
            # Explora todas las jugadas posibles: quitar de 1 a N objetos en cada fila disponible.
            for i in range(len(est)):
                for j in range(1, est[i] + 1):
                    n = list(est); n[i] -= j
                    v = minimax(n, not t_max, a, b) # Llamada recursiva alternando el turno
                    
                    if t_max: 
                        m, a = max(m, v), max(a, m)
                    else: 
                        m, b = min(m, v), min(b, m)
                        
                    if b <= a: 
                        break # Aplica la Poda Alfa-Beta para detener la búsqueda en esta rama.
            return m

        # La IA evalúa todos sus movimientos posibles desde el estado actual para elegir el mejor.
        mejor_val, mejor_mov = -math.inf, None
        for i in range(len(self.estado)):
            for j in range(1, self.estado[i] + 1):
                n = list(self.estado); n[i] -= j
                val = minimax(n, False, -math.inf, math.inf)
                if val > mejor_val: 
                    mejor_val, mejor_mov = val, (i, j)
        
        # Aplica el mejor movimiento encontrado (quitar 'j' objetos de la fila 'i').
        if mejor_mov: 
            self.estado[mejor_mov[0]] -= mejor_mov[1]
        
        # Actualiza visualmente el tablero tras el movimiento de la máquina.
        self.crear_interfaz()

if __name__ == "__main__":
    # Inicializa y lanza el bucle principal de la interfaz gráfica Tkinter.
    root = tk.Tk()
    app = NimGUI(root)
    root.mainloop()