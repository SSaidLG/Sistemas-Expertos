# =============================================================================
# Integrantes :
# 1. Cruz Hernandez Tristan Javier
# 2. Lopez Garcia Said Eduardo
#
# Descripción breve del código:
# Este programa resuelve un Cuadro Mágico de 3x3 mediante el método de 
# Backtracking (búsqueda con retroceso). La interfaz en Tkinter muestra el cuadro.
# El algoritmo prueba de forma recursiva combinaciones de números del 1 al 9, 
# retrocediendo inmediatamente cuando detecta que la suma de filas, columnas o 
# diagonales no cumple la condición de un cuadro mágico válido.
# =============================================================================

import tkinter as tk

class CuadroMagico:
    def __init__(self, root):
        # Inicializa la ventana principal y configura el título
        self.root = root
        self.root.title("Cuadro Mágico - Backtracking")
        # Lista para almacenar las referencias a las celdas de la interfaz
        self.celdas = []
        self.crear_interfaz()

    def crear_interfaz(self):
        # Genera una cuadrícula de 3x3 con widgets Entry para mostrar los números
        for i in range(3):
            for j in range(3):
                e = tk.Entry(self.root, width=3, font=('Arial', 30), justify='center')
                e.grid(row=i, column=j, padx=5, pady=5)
                self.celdas.append(e)
                
        # Agrega los botones para iniciar la resolución o limpiar el tablero
        tk.Button(self.root, text="Resolver", command=self.resolver).grid(row=3, column=0, pady=10)
        tk.Button(self.root, text="Reiniciar", command=self.reset).grid(row=3, column=2, pady=10)

    def reset(self):
        # Recorre todas las celdas de la cuadrícula y borra su contenido
        for c in self.celdas:
            c.delete(0, tk.END)

    def resolver(self):
        def es_valido(c):
            # Verifica si una combinación de 9 números cumple las reglas del cuadro mágico.
            # Comprueba que la suma de filas, columnas y diagonales sea exactamente la misma.
            if len(c) == 9:
                s = sum(c[0:3]) # Toma la suma de la primera fila como referencia
                return all([sum(c[3:6])==s, sum(c[6:9])==s, sum(c[0::3])==s, sum(c[1::3])==s, sum(c[2::3])==s, c[0]+c[4]+c[8]==s, c[2]+c[4]+c[6]==s])
            return True

        def backtrack(c, disp):
            # Algoritmo principal de backtracking para encontrar la combinación.
            # 'c' es la lista actual de números colocados, 'disp' son los números disponibles.
            if len(c) == 9: 
                return c if es_valido(c) else None
            
            for n in list(disp):
                disp.remove(n) # Toma un número de los disponibles
                res = backtrack(c + [n], disp) # Llamada recursiva con el nuevo número
                if res: 
                    return res # Si la rama encuentra la solución, la devuelve
                disp.add(n) # Si falla, retrocede (backtrack) y devuelve el número al conjunto
            return None

        # Limpia el tablero visualmente antes de comenzar a calcular
        self.reset()
        
        # Inicia la búsqueda con una lista vacía y los números del 1 al 9
        solucion = backtrack([], set(range(1, 10)))
        
        # Si el algoritmo encuentra una solución válida, la inserta en las celdas
        if solucion:
            for i, val in enumerate(solucion):
                self.celdas[i].insert(0, str(val))

if __name__ == "__main__":
    # Arranca la aplicación creando la ventana raíz y el bucle de eventos de Tkinter
    root = tk.Tk()
    app = CuadroMagico(root)
    root.mainloop()