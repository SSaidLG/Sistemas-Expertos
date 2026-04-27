import tkinter as tk
from tkinter import messagebox
import random

#Cruz Hernandez Tristan Javier 
#SISTEMAS EXPERTOS

#BASE DE CONOCIMIENTOS (Reglas lógicas del sistema)

def motor_inferencia_computadora(tablero, marca_comp, marca_humano):
    """
    MOTOR DE INFERENCIA: Selecciona la mejor acción basada en una 
    jerarquía de reglas predefinidas (Base de Conocimientos).
    """
    
    def obtener_lineas():
        filas = [[(f, c) for c in range(3)] for f in range(3)]
        cols = [[(r, c) for r in range(3)] for c in range(3)]
        diags = [[(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]]
        return filas + cols + diags

    lineas = obtener_lineas()

    # REGLA 1: Prioridad de Victoria (Si puede ganar en este turno, lo hace)
    for linea in lineas:
        valores = [tablero[f][c] for f, c in linea]
        if valores.count(marca_comp) == 2 and valores.count(" ") == 1:
            return linea[valores.index(" ")]

    # REGLA 2: Prioridad de Defensa (Si el usuario va a ganar, bloquea)
    for linea in lineas:
        valores = [tablero[f][c] for f, c in linea]
        if valores.count(marca_humano) == 2 and valores.count(" ") == 1:
            return linea[valores.index(" ")]

    # REGLA 3: Control del Centro (Posición estratégica clave en Sistemas Expertos)
    if tablero[1][1] == " ":
        return (1, 1)

    # REGLA 4: Contraataque en Esquinas (Neutraliza estrategias del humano)
    esquinas = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for e in esquinas:
        opuesta = (2 - e[0], 2 - e[1])
        if tablero[e[0]][e[1]] == marca_humano and tablero[opuesta[0]][opuesta[1]] == " ":
            return opuesta

    # REGLA 5: Ocupar Esquinas Libres
    vacias = [e for e in esquinas if tablero[e[0]][e[1]] == " "]
    if vacias:
        return random.choice(vacias)

    # REGLA 6: Movimiento por Defecto (Cualquier espacio restante)
    lados = [(0, 1), (1, 0), (1, 2), (2, 1)]
    vacias = [l for l in lados if tablero[l[0]][l[1]] == " "]
    return random.choice(vacias) if vacias else None

# ── INTERFAZ Y CONTROL DE PROCESOS ──────────────────────────────────────────

class GatoSistemaExperto:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Gato: Computadora vs Jugador")
        self.tablero = [[" "]*3 for _ in range(3)]
        self.botones = [[None]*3 for _ in range(3)]
        self.juego_activo = True
        
        # Construcción de la interfaz
        for f in range(3):
            for c in range(3):
                self.botones[f][c] = tk.Button(root, text=" ", font=('Helvetica', 20, 'bold'), 
                                              width=6, height=3, bg="#f0f0f0",
                                              command=lambda r=f, col=c: self.turno_humano(r, col))
                self.botones[f][c].grid(row=f, column=c, padx=5, pady=5)

    def turno_humano(self, f, c):
        if self.tablero[f][c] == " " and self.juego_activo:
            self.ejecutar_movimiento(f, c, "X")
            if not self.revisar_estado_juego("X"):
                self.root.after(400, self.turno_computadora)

    def turno_computadora(self):
        # La computadora consulta al Motor de Inferencia para decidir
        mov = motor_inferencia_computadora(self.tablero, "O", "X")
        if mov:
            self.ejecutar_movimiento(mov[0], mov[1], "O")
            self.revisar_estado_juego("O")

    def ejecutar_movimiento(self, f, c, marca):
        self.tablero[f][c] = marca
        color = "#e74c3c" if marca == "X" else "#3498db"
        self.botones[f][c].config(text=marca, state="disabled", disabledforeground=color)

    def revisar_estado_juego(self, jugador):
        lineas = [self.tablero[i] for i in range(3)] + \
                 [[self.tablero[i][j] for i in range(3)] for j in range(3)] + \
                 [[self.tablero[i][i] for i in range(3)], [self.tablero[i][2-i] for i in range(3)]]
        
        if [jugador]*3 in lineas:
            msg = "¡Ganaste!" if jugador == "X" else "La Computadora ha ganado"
            messagebox.showinfo("Fin del Juego", msg)
            self.juego_activo = False
            return True
        
        if all(celda != " " for fila in self.tablero for celda in fila):
            messagebox.showinfo("Fin del Juego", "Empate técnico")
            self.juego_activo = False
            return True
        return False

if __name__ == "__main__":
    ventana = tk.Tk()
    app = GatoSistemaExperto(ventana)
    ventana.mainloop()