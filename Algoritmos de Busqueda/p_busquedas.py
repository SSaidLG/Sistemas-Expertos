import heapq
import csv 

class BusquedaGrafo:
    
    def __init__(self, ruta_csv_heuristica):
        # Definimos el grafo, dirección, arcos 
        self.grafo = {
            1: {6: 117, 4: 701, 13: 699},
            2: {9: 245, 12: 137, 22: 171},
            3: {14: 317, 23: 235, 19:638, 18:291},
            4: {13: 98, 9: 202},
            5: {11: 705, 15: 220},
            6: {1: 117, 16: 288},
            7: {8: 662, 11:696, 27:475},
            8: {7: 662, 27:268, 15:309 },
            9: {4: 202, 24:214, 28: 320, 2:245, 17:321},
            10: {16: 381, 12:54},
            11: {7: 696, 5: 705},
            12: {2: 137, 10: 54},
            13: {24: 446, 4: 98, 1: 699},
            14: {3: 317, 23: 499},
            15: {5: 220, 8: 309, 24: 286},
            16: {6: 288, 26: 66, 10: 381, 19: 95, 25: 118, 20: 123},
            17: {9: 321, 26: 259},
            18: {3: 291, 21: 89, 14: 328},
            19: {3: 638, 23: 391, 16: 95},
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

    #Funcion para cargar y ajustar el csv para poder tratarlo
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
        if nodo not in self.grafo:
            return []
        vecinos = list(self.grafo[nodo].keys())
        reverso = True if sentido.lower() == 'antihorario' else False
        vecinos.sort(reverse=reverso)
        return vecinos

    def amplitud(self, inicio, meta, sentido):
        frontera = [(inicio, [inicio])]
        visitados = set()
        while frontera:
            nodo_actual, camino = frontera.pop(0)
            if nodo_actual == meta:
                return camino
            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                for vecino in self.obtener_vecinos(nodo_actual, sentido):
                    if vecino not in visitados:
                        frontera.append((vecino, camino + [vecino]))
        return None

    def profundidad(self, inicio, meta, sentido):
        frontera = [(inicio, [inicio])]
        visitados = set()
        while frontera:
            nodo_actual, camino = frontera.pop()
            if nodo_actual == meta:
                return camino
            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                vecinos = self.obtener_vecinos(nodo_actual, sentido)
                for vecino in reversed(vecinos):
                    if vecino not in visitados:
                        frontera.append((vecino, camino + [vecino]))
        return None

    def escalada_simple(self, inicio, meta, sentido):
        nodo_actual = inicio
        camino = [inicio]
        while nodo_actual != meta:
            vecinos = self.obtener_vecinos(nodo_actual, sentido)
            mejor_vecino = None
            for vecino in vecinos:
                if vecino not in camino:
                    mejor_vecino = vecino
                    break
            if mejor_vecino is None:
                break 
            camino.append(mejor_vecino)
            nodo_actual = mejor_vecino
        return camino if nodo_actual == meta else None

    
    def escalada_maxima_pendiente(self, inicio, meta, sentido):
        nodo_actual = inicio
        camino = [inicio]
        while nodo_actual != meta:
            vecinos = self.obtener_vecinos(nodo_actual, sentido)
            mejor_vecino = None
            
            mejor_h = self.tabla_h[nodo_actual][meta] 

            for vecino in vecinos:
                if vecino not in camino:
                    h_vecino = self.tabla_h[vecino][meta] 
                    if h_vecino < mejor_h:
                        mejor_h = h_vecino
                        mejor_vecino = vecino

            if mejor_vecino is None:
                break 
                
            camino.append(mejor_vecino)
            nodo_actual = mejor_vecino

        return camino if nodo_actual == meta else None

    
    def primero_mejor(self, inicio, meta, sentido):
        h_inicial = self.tabla_h[inicio][meta]
        frontera = [(h_inicial, 0, inicio, [inicio])] 
        visitados = set()

        while frontera:
            f_prima, g_acumulado, nodo_actual, camino = heapq.heappop(frontera)

            if nodo_actual == meta:
                return camino

            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                
                for vecino in self.obtener_vecinos(nodo_actual, sentido):
                    if vecino not in visitados:
                        costo_arco = self.grafo[nodo_actual][vecino]
                        nuevo_g = g_acumulado + costo_arco
                        h_estimada = self.tabla_h[vecino][meta]
                        nuevo_f = nuevo_g + h_estimada
                        
                        heapq.heappush(frontera, (nuevo_f, nuevo_g, vecino, camino + [vecino]))
        return None

def ejecutar_programa():
    
    grafo_app = BusquedaGrafo("tabla_datos.csv")
    
    if not grafo_app.tabla_h:
        print("Deteniendo ejecución por error en la carga de la heurística.")
        return
    
    try:
        inicio = int(input("Introduce el nodo inicial (1-28): "))
        meta = int(input("Introduce el nodo final (1-28): "))
    except ValueError:
        print("Por favor, introduce números enteros válidos.")
        return

    sentidos = ['horario', 'antihorario']
    algoritmos = [
        ("Amplitud ", grafo_app.amplitud),
        ("Profundidad ", grafo_app.profundidad),
        ("Escalada Simple", grafo_app.escalada_simple),
        ("Escalada Máxima Pendiente", grafo_app.escalada_maxima_pendiente),
        ("Primero Mejor", grafo_app.primero_mejor)
    ]

    print(f"\n--- INICIANDO BÚSQUEDAS DEL NODO {inicio} AL NODO {meta} ---\n")

    for sentido in sentidos:
        print(f"================ SENTIDO: {sentido.upper()} ================")
        for nombre, funcion in algoritmos:
            try:
                ruta = funcion(inicio, meta, sentido)
                if ruta:
                    print(f"{nombre}: {' -> '.join(map(str, ruta))}")
                else:
                    print(f"{nombre}: No se encontró ruta o se atoró.")
            except Exception as e:
                print(f"{nombre}: Error al calcular ({e}).")
        print("\n")

if __name__ == "__main__":
    ejecutar_programa()