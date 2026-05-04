# =============================================================================

# Integrantes del equipo:
# 1. Cruz Hernandez Tristan Javier
# 2. Lopez Garcia Said Eduardo
#
# =============================================================================
import heapq
import csv 
import sys
import os

def ruta_recurso(rel_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)

# La clase BusquedaGrafo agrupa la definicion del mapa de nodos y todos los algoritmos de busqueda
class BusquedaGrafo:
    # La funcion de inicializacion se encarga de definir el grafo base y cargar los datos de la heuristica
    # La variable ruta_csv_heuristica es un texto con el nombre del archivo csv a leer
    def __init__(self, ruta_csv_heuristica):
        # La variable self.grafo es un diccionario que representa las conexiones entre nodos
        # La llave principal es el nodo de origen, y su valor es otro diccionario con los nodos destino y el costo real del viaje
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
        # Carga de la tabla heurística ('h')
        self.tabla_h = self.cargar_heuristica_desde_csv(ruta_csv_heuristica)


    # Esta funcion lee el archivo csv y convierte sus datos en un formato utilizable por Python
    # La variable ruta_archivo almacena el nombre o ubicacion de la tabla de datos
    def cargar_heuristica_desde_csv(self, ruta_archivo):
        tabla = {}
        ruta_archivo = ruta_recurso(ruta_archivo)

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

    # Esta funcion recupera los nodos sucesores respetando el sentido solicitado
    # La variable nodo es el lugar actual, y la variable sentido dicta el orden de los vecinos
    def obtener_vecinos(self, nodo, sentido):
            if nodo not in self.grafo: return []
            # La variable vecinos extrae todas las llaves asociadas al nodo actual (sus conexiones)
            vecinos = list(self.grafo[nodo].keys())
            # Si el usuario solicita el sentido antihorario, se invierte el orden de la lista
            if sentido.lower() == 'antihorario':
                vecinos.reverse()
            return vecinos
    
    # Algoritmo de busqueda a lo ancho
    def amplitud(self, inicio, meta, sentido):
        # La variable frontera actua como una cola, se ingresa el nodo inicial y el recorrido para llegar a el
        frontera = [(inicio, [inicio])]
        # La variable visitados es un conjunto que lleva un registro de los lugares ya evaluados
        visitados = set()
        # La variable paso lleva el conteo de las iteraciones para mostrarlas en la ejecucion
        paso = 1
        
        while frontera:
            # pop(0) extrae el primer elemento en entrar a la cola, priorizando lo ancho
            nodo_actual, camino = frontera.pop(0)
            # Muestra en consola los nombres de los nodos restantes por evaluar
            nodos_en_frontera = [n for n, c in frontera]
            print(f"  [Paso {paso}] Evaluando: {nodo_actual} | Frontera pendiente: {nodos_en_frontera}")
            paso += 1
            # Condicion de victoria: si el nodo actual es igual a lo que buscamos, regresa el camino recorrido
            if nodo_actual == meta:
                print(f"    -> ¡Meta encontrada en el nodo {meta}!")
                return camino
            # Si el nodo no se ha visitado anteriormente, se evalua   
            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                vecinos = self.obtener_vecinos(nodo_actual, sentido)
                # Filtra aquellos vecinos que no han sido analizados
                vecinos_validos = [v for v in vecinos if v not in visitados]
                
                if vecinos_validos:
                    print(f"    -> Expandiendo a lo ancho. Agregando a la cola: {vecinos_validos}")
                # Introduce a la cola los vecinos junto con la ruta de como llegar a ellos
                for vecino in vecinos:
                    if vecino not in visitados:
                        frontera.append((vecino, camino + [vecino]))
        return None
    # Algoritmo de busqueda por profundidad
    def profundidad(self, inicio, meta, sentido):
        # La variable frontera ahora actua como una pila
        frontera = [(inicio, [inicio])]
        visitados = set()
        paso = 1

        while frontera:
            # pop() sin parametros extrae el ultimo elemento ingresado
            nodo_actual, camino = frontera.pop()
            nodos_en_pila = [n for n, c in frontera]
            print(f"  [Paso {paso}] Evaluando: {nodo_actual} | Pila pendiente: {nodos_en_pila}")
            paso += 1
            # Comprueba si llegamos a la meta
            if nodo_actual == meta:
                print(f"    -> ¡Meta encontrada en el nodo {meta}!")
                return camino
            # Evalua unicamente nodos no visitados
            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                vecinos = self.obtener_vecinos(nodo_actual, sentido)
                vecinos_validos = [v for v in vecinos if v not in visitados]
                # Si no hay hacia donde moverse, notifica que se hara un retroceso
                if not vecinos_validos:
                    print("    -> Callejón sin salida. Retrocediendo (Backtracking)...")
                else:
                    print(f"    -> Profundizando. Añadiendo a la pila: {vecinos_validos}")
                #Al recorrer la lista de vecinos al reves, garantizamos que el primer elemento natural se quede hasta arriba en la pila
                for vecino in reversed(vecinos):
                    if vecino not in visitados:
                        frontera.append((vecino, camino + [vecino]))
            else:
                # Este caso indica que el nodo se extrajo de la pila pero en pasos anteriores ya habia sido visitado
                print(f"    -> El nodo {nodo_actual} ya fue explorado. Ignorando.")

        return None
    # Algoritmo heuristico de escalada simple
    def escalada_simple(self, inicio, meta, sentido):
        # A diferencia de amplitud y profundidad, no usamos arreglos para los sucesores, solo almacenamos el nodo en curso
        nodo_actual = inicio
        # Mantenemos el registro del camino con esta variable
        camino = [inicio]
        paso = 1
        
        # Iteramos hasta llegar a la meta
        while nodo_actual != meta:
            # Extraemos el valor de la heuristica entre el punto en el que estamos y la meta
            mejor_h = self.tabla_h[nodo_actual][meta]
            print(f"  [Paso {paso}] Evaluando: {nodo_actual} (h={mejor_h})")
            paso += 1
            
            vecinos = self.obtener_vecinos(nodo_actual, sentido)
            mejor_vecino = None
            
            # Recorremos cada vecino y verificamos su valor heuristico
            for vecino in vecinos:
                # Evita bucles infinitos no revisando nodos ya caminados
                if vecino not in camino:
                    h_vecino = self.tabla_h[vecino][meta]
                    print(f"    - Revisando vecino {vecino} (h={h_vecino})...", end=" ")
                    
                    # El algoritmo elige la primera opcion que mejore al estado actual y descarta evaluar al resto
                    if h_vecino < mejor_h:
                        mejor_vecino = vecino
                        print("¡Es mejor! Tomando este primer buen camino.")
                        break # Se detiene en el primero que mejora la situación
                    else:
                        print("No mejora.")

            # Si no se encontro ningun vecino con mejor estimacion que el nodo actual, el algoritmo se estanca            
            if mejor_vecino is None:
                print("    -> ¡Atrapado en máximo local! Ningún vecino analizado mejoró la heurística.")
                break 
            # Agrega la mejor opcion elegida a la ruta de viaje    
            camino.append(mejor_vecino)
            # Actualiza el nuevo punto de partida
            nodo_actual = mejor_vecino

        # Al salir del while, evaluamos la razon de su salida
        # Si la meta coincide con la posicion final, se termino exitosamente  
        if nodo_actual == meta:
            print(f"    -> ¡Meta encontrada en el nodo {meta}!")
        # En caso contrario, se imprime la ruta parcial recorrida hasta el momento del atasco
        else:
            print(f"    -> [!] Búsqueda detenida. Mostrando RUTA PARCIAL hasta el nodo {nodo_actual}.")
        return camino

    # Algoritmo heuristico de escalada por maxima pendiente
    def escalada_maxima_pendiente(self, inicio, meta, sentido):
        nodo_actual = inicio
        camino = [inicio]
        paso = 1
        
        # Iteramos hasta llegar a la meta
        while nodo_actual != meta:
            # Establece un punto de comparacion heuristico basado en el nodo actual
            mejor_h = self.tabla_h[nodo_actual][meta] 
            print(f"  [Paso {paso}] Evaluando: {nodo_actual} (h={mejor_h})")
            paso += 1
            
            vecinos = self.obtener_vecinos(nodo_actual, sentido)
            mejor_vecino = None
            
            # En maxima pendiente obligatoriamente revisamos todos los sucesores disponibles
            for vecino in vecinos:
                if vecino not in camino:
                    h_vecino = self.tabla_h[vecino][meta] 
                    print(f"    - Vecino {vecino} tiene (h={h_vecino})")
                    
                    # En vez de detenerse en el primero que sea mejor, guarda su valor y sigue iterando para buscar uno aun mas eficiente
                    if h_vecino < mejor_h:
                        mejor_h = h_vecino
                        mejor_vecino = vecino
            # Si despues de revisar todos, ninguno fue mas pequeño que el actual, nos estancamos
            if mejor_vecino is None:
                print("    -> ¡Atrapado en máximo local! Ningún vecino tiene un valor 'h' mejor.")
                break 
                
            print(f"    -> Se elige a {mejor_vecino} por tener la MÁXIMA pendiente (menor h={mejor_h}).")
            camino.append(mejor_vecino)
            nodo_actual = mejor_vecino
        # Verifica el motivo de terminacion y muestra la raazón
        if nodo_actual == meta:
            print(f"    -> ¡Meta encontrada en el nodo {meta}!")
        else:
            print(f"    -> [!] Búsqueda detenida. Mostrando RUTA PARCIAL hasta el nodo {nodo_actual}.")
        return camino

    # Algoritmo de busqueda de primero mejor utilizando costo acumulado sumado a heuristica
    def primero_mejor(self, inicio, meta, sentido):
        h_inicial = self.tabla_h[inicio][meta]
        # La frontera es una fila de prioridad, el primer valor de la tupla define la prioridad de extraccion
        # La tupla contiene (f_prima, g_acumulado, nodo, ruta_hasta_ahora)
        frontera = [(h_inicial, 0, inicio, [inicio])] 
        visitados = set()
        paso = 1

        while frontera:
            # heapq extrae automaticamente el nodo con el valor f_prima mas bajo de toda la frontera
            f_prima, g_acumulado, nodo_actual, camino = heapq.heappop(frontera)
            # Extrae la informacion visual de la frontera descartando caminos y datos extras para no ensuciar la terminal
            nodos_en_frontera = [(f, n) for f, g, n, c in frontera]
            
            print(f"  [Paso {paso}] Evaluando: {nodo_actual} (f'={f_prima}) | Frontera: {nodos_en_frontera}")
            paso += 1

            # Al igual que todos los metodos, verifica la condicion de exito antes de seguir
            if nodo_actual == meta:
                print(f"    -> ¡Meta encontrada! Costo real final (g) = {g_acumulado}")
                return camino
            # Si el nodo es nuevo, se procesa
            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                vecinos = self.obtener_vecinos(nodo_actual, sentido)
                
                for vecino in vecinos:
                    if vecino not in visitados:
                        # costo_arco es el costo de moverse del punto actual al vecino, definido en el diccionario principal
                        costo_arco = self.grafo[nodo_actual][vecino]
                        # nuevo_g es la suma del historial de costos mas este nuevo paso
                        nuevo_g = g_acumulado + costo_arco
                        # h_estimada representa la distancia recta estimada desde el nuevo lugar hacia el objetivo
                        h_estimada = self.tabla_h[vecino][meta]
                        # nuevo_f es el resultado de sumar el costo real con la estimacion hacia el final
                        nuevo_f = nuevo_g + h_estimada
                        
                        print(f"    - Sucesor {vecino}: g({nuevo_g}) + h({h_estimada}) = f'({nuevo_f})")
                        # Se introduce a la pila prioritaria, la libreria ordena en automático el objeto segun la variable nuevo_f
                        heapq.heappush(frontera, (nuevo_f, nuevo_g, vecino, camino + [vecino]))
        return None

# Esta es la funcion de inicio que coordina las interacciones del usuario y ejecuta los metodos
def ejecutar_programa():
    
    # Se instancia el objeto principal pasandole el nombre del archivo de la tabla de datos
    grafo_app = BusquedaGrafo("tabla_datos.csv")
    
    # Valida tempranamente que el archivo fue encontrado, si no, termina el flujo
    if not grafo_app.tabla_h:
        print("\n[!] Deteniendo ejecución por error en la carga de la heurística.")
        return
    
    print("\n" + "="*60)
    print("           SISTEMA DE BÚSQUEDAS HEURÍSTICAS")
    print("="*60)
    # El bloque try se utiliza para prever que el usuario introduzca texto en vez de los numeros requeridos
    try:
        # Se piden explicitamente los tres datos obligatorios
        inicio = int(input("Introduce el nodo inicial (1-28): "))
        meta = int(input("Introduce el nodo final (1-28): "))
        # Se pide el sentido y se normaliza para evitar errores de validación
        sentido = input("Introduce el sentido de búsqueda (horario / antihorario): ").strip().lower()
        
        # Validación de seguridad
        if sentido not in ['horario', 'antihorario']:
            print("\n[!] Error: El sentido debe ser exactamente 'horario' o 'antihorario'.")
            return
        
    except ValueError:
        print("Por favor, introduce números enteros válidos para los nodos.")
        return

    sentidos = ['horario', 'antihorario']

    # Arreglo que relaciona con texto las referencias reales a las funciones de clase
    algoritmos = [
        ("Amplitud", grafo_app.amplitud),
        ("Profundidad", grafo_app.profundidad),
        ("Escalada Simple", grafo_app.escalada_simple),
        ("Escalada Máxima Pendiente", grafo_app.escalada_maxima_pendiente),
        ("Primero Mejor", grafo_app.primero_mejor)
    ]

    print("\n\n" + "█"*60)
    print(f"██         SENTIDO SELECCIONADO: {sentido.upper().ljust(17)} ██")
    print("█"*60)

    # Itera sobre el arreglo de algoritmos ejecutando cada uno con los mismos parametros 
    for nombre, funcion in algoritmos:
        print(f"\n" + "-"*60)
        print(f"  ALGORITMO: {nombre.upper()}")
        print("-"*60)
        
        try:
            # Invoca a la funcion en turno y recibe la coleccion de nodos visitados
            ruta = funcion(inicio, meta, sentido)
            
            # Impresión clara de la RUTA (Final o Parcial)
            print("\n  >> RUTA GENERADA:")
            # Si el valor de la ruta es un arreglo y no un valor nulo, lo imprime concatenando flechas
            if ruta:
                print(f"     {' -> '.join(map(str, ruta))}")
            # Si se devolvio un valor nulo es porque los metodos tradicionales de amplitud o profundidad no hallaron camino posible
            else:
                print(f"     [!] No se encontró ruta o el algoritmo se atoró.")
        except Exception as e:
            print(f"     [!] Error de cálculo ({e}).")
                
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    ejecutar_programa()