# Juego del Gato con IA (Minimax + Poda Alfa-Beta)
# Autor: Tristan Javier Cruz Hernandez

import tkinter as tk
from tkinter import messagebox

# ── Lógica del juego ──────────────────────────────────────────────────────────

def verificarGanador(tablero, jugador):
    for fila in tablero:
        if all(c == jugador for c in fila):
            return True
    for col in range(3):
        if all(tablero[f][col] == jugador for f in range(3)):
            return True
    if all(tablero[i][i] == jugador for i in range(3)):
        return True
    if all(tablero[i][2-i] == jugador for i in range(3)):
        return True
    return False

def movimientosDisponibles(tablero):
    return [(f, c) for f in range(3) for c in range(3) if tablero[f][c] == " "]

def minimax(tablero, esMaximizando, alfa, beta):
    if verificarGanador(tablero, "O"):
        return 10
    if verificarGanador(tablero, "X"):
        return -10
    if not movimientosDisponibles(tablero):
        return 0

    if esMaximizando:
        mejor = -1000
        for f, c in movimientosDisponibles(tablero):
            tablero[f][c] = "O"
            mejor = max(mejor, minimax(tablero, False, alfa, beta))
            tablero[f][c] = " "
            alfa = max(alfa, mejor)
            if beta <= alfa:
                break
        return mejor
    else:
        mejor = 1000
        for f, c in movimientosDisponibles(tablero):
            tablero[f][c] = "X"
            mejor = min(mejor, minimax(tablero, True, alfa, beta))
            tablero[f][c] = " "
            beta = min(beta, mejor)
            if beta <= alfa:
                break
        return mejor

def mejorMovimientoIA(tablero):
    mejorPuntaje = -1000
    movimiento = None
    for f, c in movimientosDisponibles(tablero):
        tablero[f][c] = "O"
        puntaje = minimax(tablero, False, -1000, 1000)
        tablero[f][c] = " "
        if puntaje > mejorPuntaje:
            mejorPuntaje = puntaje
            movimiento = (f, c)
    return movimiento

# ── Interfaz Gráfica ──────────────────────────────────────────────────────────

class GatoApp:
    COLORES = {
        "fondo":    "#1e1e2e",
        "panel":    "#2a2a3e",
        "boton":    "#313145",
        "hover":    "#3d3d5c",
        "X":        "#f38ba8",
        "O":        "#89b4fa",
        "empate":   "#a6e3a1",
        "texto":    "#cdd6f4",
        "subtexto": "#6c7086",
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Gato — IA Experta")
        self.root.configure(bg=self.COLORES["fondo"])
        self.root.resizable(False, False)

        self.tablero = []
        self.botones = []
        self.juegoActivo = False
        self.marcaJugador = "X"
        self.puntajes = {"Jugador": 0, "IA": 0, "Empates": 0}

        self._construirUI()
        self.nuevaPartida()

    def _construirUI(self):
        # Título
        tk.Label(self.root, text="GATO", font=("Helvetica", 28, "bold"),
                 bg=self.COLORES["fondo"], fg=self.COLORES["texto"]).pack(pady=(20, 2))
        tk.Label(self.root, text="Sistema Experto — Minimax + Poda Alfa-Beta",
                 font=("Helvetica", 9), bg=self.COLORES["fondo"],
                 fg=self.COLORES["subtexto"]).pack()

        # Marcador
        self.framePuntaje = tk.Frame(self.root, bg=self.COLORES["panel"], padx=20, pady=8)
        self.framePuntaje.pack(pady=12, padx=30, fill="x")
        self.labelPuntaje = tk.Label(self.framePuntaje, text="",
                                     font=("Helvetica", 11),
                                     bg=self.COLORES["panel"], fg=self.COLORES["texto"])
        self.labelPuntaje.pack()

        # Estado del turno
        self.labelEstado = tk.Label(self.root, text="", font=("Helvetica", 13, "bold"),
                                    bg=self.COLORES["fondo"], fg=self.COLORES["texto"])
        self.labelEstado.pack(pady=(0, 10))

        # Tablero
        frameTablero = tk.Frame(self.root, bg=self.COLORES["fondo"])
        frameTablero.pack(padx=30)

        for f in range(3):
            fila_botones = []
            for c in range(3):
                btn = tk.Button(frameTablero, text="", font=("Helvetica", 36, "bold"),
                                width=3, height=1,
                                bg=self.COLORES["boton"], fg=self.COLORES["texto"],
                                activebackground=self.COLORES["hover"],
                                relief="flat", bd=0,
                                command=lambda fila=f, col=c: self.jugadaHumano(fila, col))
                btn.grid(row=f, column=c, padx=4, pady=4, ipadx=10, ipady=10)
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.COLORES["hover"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.COLORES["boton"]))
                fila_botones.append(btn)
            self.botones.append(fila_botones)

        # Selector de turno
        frameOpciones = tk.Frame(self.root, bg=self.COLORES["fondo"])
        frameOpciones.pack(pady=14)

        tk.Label(frameOpciones, text="Jugar como:", font=("Helvetica", 10),
                 bg=self.COLORES["fondo"], fg=self.COLORES["subtexto"]).pack(side="left", padx=(0, 8))

        self.varMarca = tk.StringVar(value="X")
        for marca in ("X", "O"):
            color = self.COLORES[marca]
            tk.Radiobutton(frameOpciones, text=f"  {marca}  ", variable=self.varMarca,
                           value=marca, font=("Helvetica", 10, "bold"),
                           bg=self.COLORES["fondo"], fg=color,
                           selectcolor=self.COLORES["panel"],
                           activebackground=self.COLORES["fondo"],
                           command=self.nuevaPartida).pack(side="left", padx=4)

        # Botón nueva partida
        tk.Button(self.root, text="Nueva Partida", font=("Helvetica", 11),
                  bg=self.COLORES["panel"], fg=self.COLORES["texto"],
                  activebackground=self.COLORES["hover"],
                  relief="flat", padx=16, pady=6,
                  command=self.nuevaPartida).pack(pady=(0, 20))

    def nuevaPartida(self):
        self.tablero = [[" "] * 3 for _ in range(3)]
        self.juegoActivo = True
        self.marcaJugador = self.varMarca.get()
        self.marcaIA = "O" if self.marcaJugador == "X" else "X"

        for f in range(3):
            for c in range(3):
                self.botones[f][c].config(text="", bg=self.COLORES["boton"],
                                          fg=self.COLORES["texto"], state="normal")

        self._actualizarPuntaje()

        # Si el jugador eligió O, la IA empieza
        if self.marcaJugador == "O":
            self.labelEstado.config(text="IA está pensando...", fg=self.COLORES["O"])
            self.root.after(400, self.jugadaIA)
        else:
            self.labelEstado.config(text="Tu turno  ✏️", fg=self.COLORES["X"])

    def jugadaHumano(self, fila, col):
        if not self.juegoActivo or self.tablero[fila][col] != " ":
            return

        self._colocarMarca(fila, col, self.marcaJugador)

        if verificarGanador(self.tablero, self.marcaJugador):
            self._finJuego("jugador")
            return
        if not movimientosDisponibles(self.tablero):
            self._finJuego("empate")
            return

        self.labelEstado.config(text="IA está pensando...", fg=self.COLORES[self.marcaIA])
        self.root.after(300, self.jugadaIA)

    def jugadaIA(self):
        mov = mejorMovimientoIA(self.tablero) if self.marcaIA == "O" else self._mejorMovIA_X()
        if mov:
            self._colocarMarca(mov[0], mov[1], self.marcaIA)

        if verificarGanador(self.tablero, self.marcaIA):
            self._finJuego("ia")
            return
        if not movimientosDisponibles(self.tablero):
            self._finJuego("empate")
            return

        self.labelEstado.config(text="Tu turno  ✏️", fg=self.COLORES[self.marcaJugador])

    def _mejorMovIA_X(self):
        """Minimax cuando la IA juega con X (minimiza para O, maximiza para X)."""
        mejorPuntaje = 1000
        movimiento = None
        for f, c in movimientosDisponibles(self.tablero):
            self.tablero[f][c] = "X"
            puntaje = minimax(self.tablero, True, -1000, 1000)
            self.tablero[f][c] = " "
            if puntaje < mejorPuntaje:
                mejorPuntaje = puntaje
                movimiento = (f, c)
        return movimiento

    def _colocarMarca(self, fila, col, marca):
        self.tablero[fila][col] = marca
        self.botones[fila][col].config(text=marca, fg=self.COLORES[marca],
                                       state="disabled", disabledforeground=self.COLORES[marca])

    def _resaltarGanador(self, jugador):
        # Resaltar la línea ganadora
        lineas = (
            [(f, c) for c in range(3) for f in range(3) if all(self.tablero[f][c2] == jugador for c2 in range(3))],
        )
        for f in range(3):
            if all(self.tablero[f][c] == jugador for c in range(3)):
                for c in range(3):
                    self.botones[f][c].config(bg="#45475a")
        for c in range(3):
            if all(self.tablero[f][c] == jugador for f in range(3)):
                for f in range(3):
                    self.botones[f][c].config(bg="#45475a")
        if all(self.tablero[i][i] == jugador for i in range(3)):
            for i in range(3):
                self.botones[i][i].config(bg="#45475a")
        if all(self.tablero[i][2-i] == jugador for i in range(3)):
            for i in range(3):
                self.botones[i][2-i].config(bg="#45475a")

    def _finJuego(self, resultado):
        self.juegoActivo = False
        if resultado == "jugador":
            self.puntajes["Jugador"] += 1
            self._resaltarGanador(self.marcaJugador)
            self.labelEstado.config(text="🎉 ¡Ganaste! ¡Increíble!", fg=self.COLORES["X"])
        elif resultado == "ia":
            self.puntajes["IA"] += 1
            self._resaltarGanador(self.marcaIA)
            self.labelEstado.config(text="🤖 La IA ganó. ¡Inténtalo de nuevo!", fg=self.COLORES["O"])
        else:
            self.puntajes["Empates"] += 1
            self.labelEstado.config(text="🤝 ¡Empate!", fg=self.COLORES["empate"])
        self._actualizarPuntaje()

    def _actualizarPuntaje(self):
        self.labelPuntaje.config(
            text=f"Jugador: {self.puntajes['Jugador']}   |   "
                 f"IA: {self.puntajes['IA']}   |   "
                 f"Empates: {self.puntajes['Empates']}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = GatoApp(root)
    root.mainloop()

# Comando para correr el programa : python3 GatoGUI.py