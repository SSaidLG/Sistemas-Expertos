import heapq
import csv 

class BusquedaGrafo:
    
    def __init__(self, ruta_csv_heuristica):
        self.grafo = {
            1: {6: 117, 13: 699, 4: 701},
            2: {22: 171, 12: 137, 9: 245},
            3: {14: 317, 23: 235, 19:638, 18:291},
            4: {9: 202, 1:701 , 13: 98},
            5: {15: 220, 11: 705},
            6: {16: 288, 1: 117},
            7: {27:475, 8:662 , 11:696},
            8: {27:268,15:309, 7: 662 },
            9: {28: 320, 2:245, 17:321, 4: 202, 24:214},
            10: {16: 381, 12:54},
            11: {7: 696, 5: 705},
            12: {10: 54, 2: 137},
            13: { 4: 98, 1: 699, 24: 446},
            14: {23: 499, 3: 317},
            15: { 8: 309, 24: 286 ,5: 220},
            16: {19: 95, 25: 118, 20: 123, 6: 288, 26: 66, 10: 381},
            17: {26: 259, 9: 321},
            18: {14: 328, 3: 291, 21: 89},
            19: { 23: 391, 16: 95, 3: 638},
            20: {25:33, 16:123},
            21: {18:89, 22:449, 28:380, 27:262},
            22: {21:449, 23:401, 2:171, 28:190},
            23: {14:499, 19:391, 22:401, 3:235},
            24: {9:214, 13:446, 15:286},
            25: {},
            26: {16:66, 17:259},
            27: {21:262, 28:390, 8:268, 7:475},
            28: {27:390, 21:380, 22:190, 2:131, 9:320, 8:310}
        }
        # 2. Carga de la tabla heurística ('h')
        self.tabla_h = self.cargar_heuristica_desde_csv(ruta_csv_heuristica)

    # Funcion para cargar y ajustar el csv para poder tratarlo
    def cargar_heuristica_desde_csv(self, ruta_archivo):
        tabla = {}
        try:
            with open(ruta_archivo, mode='r', encoding='utf-8-sig') as archivo:
                lector = csv.reader(archivo)
                next(lector) 
                for fila in lector:
                    if not fila or not fila[0].strip():
                        continue
                    nodo_origen = int(fila[0])
                    tabla[nodo_origen] = {}
                    for i in range(1, len(fila)):
                        valor_celda = fila[i].strip()
                        if valor_celda != "":
                            nodo_destino = i 
                            tabla[nodo_origen][nodo_destino] = int(valor_celda)
                            
            for origen in list(tabla.keys()):
                for destino, costo in tabla[origen].items():
                    if destino not in tabla:
                        tabla[destino] = {}
                    tabla[destino][origen] = costo
            return tabla
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{ruta_archivo}'.")
            return {}
        except Exception as e:
            print(f"Error al procesar el CSV: {e}")
            return {}

    def obtener_vecinos(self, nodo, sentido):
            if nodo not in self.grafo: return []
            vecinos = list(self.grafo[nodo].keys())
            if sentido.lower() == 'antihorario':
                vecinos.reverse()
            return vecinos

    def amplitud(self, inicio, meta, sentido):
        frontera = [(inicio, [inicio])]
        visitados = set()
        paso = 1
        
        while frontera:
            nodo_actual, camino = frontera.pop(0)
            nodos_en_frontera = [n for n, c in frontera]
            print(f"  [Paso {paso}] Evaluando: {nodo_actual} | Frontera pendiente: {nodos_en_frontera}")
            paso += 1
            
            if nodo_actual == meta:
                print(f"    -> ¡Meta encontrada en el nodo {meta}!")
                return camino
                
            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                vecinos = self.obtener_vecinos(nodo_actual, sentido)
                vecinos_validos = [v for v in vecinos if v not in visitados]
                
                if vecinos_validos:
                    print(f"    -> Expandiendo a lo ancho. Agregando a la cola: {vecinos_validos}")
                
                for vecino in vecinos:
                    if vecino not in visitados:
                        frontera.append((vecino, camino + [vecino]))
        return None

    def profundidad(self, inicio, meta, sentido):
        frontera = [(inicio, [inicio])]
        visitados = set()
        paso = 1

        while frontera:
            nodo_actual, camino = frontera.pop()
            nodos_en_pila = [n for n, c in frontera]
            print(f"  [Paso {paso}] Evaluando: {nodo_actual} | Pila pendiente: {nodos_en_pila}")
            paso += 1

            if nodo_actual == meta:
                print(f"    -> ¡Meta encontrada en el nodo {meta}!")
                return camino

            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                vecinos = self.obtener_vecinos(nodo_actual, sentido)
                vecinos_validos = [v for v in vecinos if v not in visitados]
                
                if not vecinos_validos:
                    print("    -> Callejón sin salida. Retrocediendo (Backtracking)...")
                else:
                    print(f"    -> Profundizando. Añadiendo a la pila: {vecinos_validos}")

                for vecino in reversed(vecinos):
                    if vecino not in visitados:
                        frontera.append((vecino, camino + [vecino]))
            else:
                print(f"    -> El nodo {nodo_actual} ya fue explorado. Ignorando.")

        return None

    def escalada_simple(self, inicio, meta, sentido):
        nodo_actual = inicio
        camino = [inicio]
        paso = 1
        
        while nodo_actual != meta:
            mejor_h = self.tabla_h[nodo_actual][meta]
            print(f"  [Paso {paso}] Evaluando: {nodo_actual} (h={mejor_h})")
            paso += 1
            
            vecinos = self.obtener_vecinos(nodo_actual, sentido)
            mejor_vecino = None
            
            for vecino in vecinos:
                if vecino not in camino:
                    h_vecino = self.tabla_h[vecino][meta]
                    print(f"    - Revisando vecino {vecino} (h={h_vecino})...", end=" ")
                    
                    # Cambio Importante: Ahora evalúa que sea MEJOR que el actual (h_vecino < mejor_h)
                    if h_vecino < mejor_h:
                        mejor_vecino = vecino
                        print("¡Es mejor! Tomando este primer buen camino.")
                        break # Se detiene en el primero que mejora la situación
                    else:
                        print("No mejora.")
                        
            if mejor_vecino is None:
                print("    -> ¡Atrapado en máximo local! Ningún vecino analizado mejoró la heurística.")
                break 
                
            camino.append(mejor_vecino)
            nodo_actual = mejor_vecino
            
        if nodo_actual == meta:
            print(f"    -> ¡Meta encontrada en el nodo {meta}!")
        return camino if nodo_actual == meta else None

    
    def escalada_maxima_pendiente(self, inicio, meta, sentido):
        nodo_actual = inicio
        camino = [inicio]
        paso = 1
        
        while nodo_actual != meta:
            mejor_h = self.tabla_h[nodo_actual][meta] 
            print(f"  [Paso {paso}] Evaluando: {nodo_actual} (h={mejor_h})")
            paso += 1
            
            vecinos = self.obtener_vecinos(nodo_actual, sentido)
            mejor_vecino = None

            for vecino in vecinos:
                if vecino not in camino:
                    h_vecino = self.tabla_h[vecino][meta] 
                    print(f"    - Vecino {vecino} tiene (h={h_vecino})")
                    
                    if h_vecino < mejor_h:
                        mejor_h = h_vecino
                        mejor_vecino = vecino

            if mejor_vecino is None:
                print("    -> ¡Atrapado en máximo local! Ningún vecino tiene un valor 'h' mejor.")
                break 
                
            print(f"    -> Se elige a {mejor_vecino} por tener la MÁXIMA pendiente (menor h={mejor_h}).")
            camino.append(mejor_vecino)
            nodo_actual = mejor_vecino

        if nodo_actual == meta:
            print(f"    -> ¡Meta encontrada en el nodo {meta}!")
        return camino if nodo_actual == meta else None

    
    def primero_mejor(self, inicio, meta, sentido):
        h_inicial = self.tabla_h[inicio][meta]
        frontera = [(h_inicial, 0, inicio, [inicio])] 
        visitados = set()
        paso = 1

        while frontera:
            f_prima, g_acumulado, nodo_actual, camino = heapq.heappop(frontera)
            nodos_en_frontera = [(f, n) for f, g, n, c in frontera]
            
            print(f"  [Paso {paso}] Evaluando: {nodo_actual} (f'={f_prima}) | Frontera: {nodos_en_frontera}")
            paso += 1

            if nodo_actual == meta:
                print(f"    -> ¡Meta encontrada! Costo real final (g) = {g_acumulado}")
                return camino

            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                vecinos = self.obtener_vecinos(nodo_actual, sentido)
                
                for vecino in vecinos:
                    if vecino not in visitados:
                        costo_arco = self.grafo[nodo_actual][vecino]
                        nuevo_g = g_acumulado + costo_arco
                        h_estimada = self.tabla_h[vecino][meta]
                        nuevo_f = nuevo_g + h_estimada
                        
                        print(f"    - Sucesor {vecino}: g({nuevo_g}) + h({h_estimada}) = f'({nuevo_f})")
                        heapq.heappush(frontera, (nuevo_f, nuevo_g, vecino, camino + [vecino]))
        return None

def ejecutar_programa():
    
    grafo_app = BusquedaGrafo("tabla_datos.csv")
    
    if not grafo_app.tabla_h:
        print("\n[!] Deteniendo ejecución por error en la carga de la heurística.")
        return
    
    print("\n" + "="*60)
    print("           SISTEMA DE BÚSQUEDAS HEURÍSTICAS")
    print("="*60)
    try:
        inicio = int(input("Introduce el nodo inicial (1-28): "))
        meta = int(input("Introduce el nodo final (1-28): "))
    except ValueError:
        print("Por favor, introduce números enteros válidos.")
        return

    sentidos = ['horario', 'antihorario']
    algoritmos = [
        ("Amplitud", grafo_app.amplitud),
        ("Profundidad", grafo_app.profundidad),
        ("Escalada Simple", grafo_app.escalada_simple),
        ("Escalada Máxima Pendiente", grafo_app.escalada_maxima_pendiente),
        ("Primero Mejor", grafo_app.primero_mejor)
    ]

    for sentido in sentidos:
        print("\n\n" + "█"*60)
        print(f"██                SENTIDO: {sentido.upper().ljust(25)} ██")
        print("█"*60)
        
        for nombre, funcion in algoritmos:
            print(f"\n" + "-"*60)
            print(f"  ALGORITMO: {nombre.upper()}")
            print("-"*60)
            
            try:
                # Ejecución de la traza visual
                ruta = funcion(inicio, meta, sentido)
                
                # Impresión clara de la RUTA FINAL
                print("\n  >> RUTA FINAL OBTENIDA:")
                if ruta:
                    print(f"     {' -> '.join(map(str, ruta))}")
                else:
                    print(f"     [!] No se encontró ruta o el algoritmo se atoró.")
            except Exception as e:
                print(f"     [!] Error de cálculo ({e}).")
                
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    ejecutar_programa()