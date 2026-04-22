# =============================================================================
# ALGORITMOS DE BÚSQUEDA
# Búsquedas a ciegas:
#   1. Búsqueda a lo Ancho (BFS)
#   2. Búsqueda en Profundidad (DFS)
#
# Búsquedas heurísticas:
#   3. Escalada Simple
#   4. Escalada Máxima Pendiente
#   5. El Primero Mejor (Best-First / A*)
# =============================================================================

from collections import deque
import heapq


def obtener_vecinos(grafo, nodo, sentido):
    """
    Retorna los vecinos de un nodo ordenados según el sentido de búsqueda.
    sentido='H'  → horario      → orden ascendente  (menor nodo primero)
    sentido='A'  → antihorario  → orden descendente (mayor nodo primero)
    """
    vecinos = grafo.get(nodo, [])
    if sentido == 'H':
        return sorted(vecinos, key=lambda x: x[0])
    else:
        return sorted(vecinos, key=lambda x: x[0], reverse=True)


def reconstruir_camino(padres, inicio, fin):
    """Reconstruye el camino desde inicio hasta fin usando el diccionario de padres."""
    camino = []
    nodo = fin
    while nodo is not None:
        camino.append(nodo)
        nodo = padres.get(nodo)
    camino.reverse()
    if camino[0] == inicio:
        return camino
    return None


# =============================================================================
# 1. BÚSQUEDA A LO ANCHO (BFS - Breadth First Search)
# =============================================================================

def busqueda_ancho(grafo, inicio, fin, sentido):
    """
    Búsqueda primero a lo ancho.
    Explora todos los nodos nivel por nivel.
    Garantiza encontrar el camino con menos arcos (no necesariamente el de menor costo).

    Retorna: (camino, costo_total, nodos_visitados, pasos_log)
    """
    if inicio == fin:
        return [inicio], 0, [inicio], ["Estado inicial = Estado final"]

    lista_nodos = deque()
    lista_nodos.append(inicio)
    visitados = {inicio: None}   # nodo -> padre
    costos = {inicio: 0}
    pasos = []
    nodos_visitados = []

    pasos.append(f"  INICIO: LISTA-NODOS = [{inicio}]")

    while lista_nodos:
        actual = lista_nodos.popleft()
        nodos_visitados.append(actual)
        pasos.append(f"  Expandiendo nodo: {actual}  (costo acumulado hasta aquí: {costos[actual]})")

        if actual == fin:
            camino = reconstruir_camino(visitados, inicio, fin)
            costo = costos[fin]
            pasos.append(f"  ✓ META ENCONTRADA: nodo {fin}")
            return camino, costo, nodos_visitados, pasos

        vecinos = obtener_vecinos(grafo, actual, sentido)
        for vecino, peso in vecinos:
            if vecino not in visitados:
                visitados[vecino] = actual
                costos[vecino] = costos[actual] + peso
                lista_nodos.append(vecino)
                pasos.append(f"    → Añadiendo nodo {vecino} (costo: {costos[vecino]}) al final de LISTA-NODOS")

    pasos.append("  ✗ No se encontró camino (LISTA-NODOS vacía)")
    return None, float('inf'), nodos_visitados, pasos


# =============================================================================
# 2. BÚSQUEDA EN PROFUNDIDAD (DFS - Depth First Search)
# =============================================================================

def busqueda_profundidad(grafo, inicio, fin, sentido):
    """
    Búsqueda primero en profundidad.
    Explora tan profundo como sea posible antes de retroceder.
    Usa una pila (LIFO). No garantiza camino óptimo.

    Retorna: (camino, costo_total, nodos_visitados, pasos_log)
    """
    if inicio == fin:
        return [inicio], 0, [inicio], ["Estado inicial = Estado final"]

    # Pila: (nodo_actual, camino_hasta_aqui, costo_acumulado)
    pila = [(inicio, [inicio], 0)]
    visitados = set()
    pasos = []
    nodos_visitados = []

    pasos.append(f"  INICIO: LISTA-NODOS = [{inicio}]")

    while pila:
        actual, camino, costo = pila.pop()

        if actual in visitados:
            continue
        visitados.add(actual)
        nodos_visitados.append(actual)
        pasos.append(f"  Expandiendo nodo: {actual}  (costo acumulado: {costo})")

        if actual == fin:
            pasos.append(f"  ✓ META ENCONTRADA: nodo {fin}")
            return camino, costo, nodos_visitados, pasos

        vecinos = obtener_vecinos(grafo, actual, sentido)
        # En DFS con pila, añadimos en orden inverso para que el primero
        # (según sentido) sea el que se procese primero al hacer pop
        for vecino, peso in reversed(vecinos):
            if vecino not in visitados:
                nueva_pila_entrada = (vecino, camino + [vecino], costo + peso)
                pila.append(nueva_pila_entrada)
                pasos.append(f"    → Añadiendo nodo {vecino} al inicio de LISTA-NODOS")

    pasos.append("  ✗ No se encontró camino")
    return None, float('inf'), nodos_visitados, pasos


# =============================================================================
# 3. ESCALADA SIMPLE (Simple Hill Climbing)
# =============================================================================

def escalada_simple(grafo, inicio, fin, sentido, heuristica):
    """
    Búsqueda por escalada simple.
    En cada paso, selecciona el PRIMER vecino que sea mejor que el estado actual
    (menor valor heurístico = más cercano al objetivo).
    Puede quedar atrapada en máximos locales.

    h'(nodo) = distancia directa de nodo a fin (heurística del dominio)

    Retorna: (camino, costo_total, nodos_visitados, pasos_log)
    """
    if inicio == fin:
        return [inicio], 0, [inicio], ["Estado inicial = Estado final"]

    actual = inicio
    camino = [inicio]
    costo_total = 0
    visitados = {inicio}
    pasos = []
    nodos_visitados = [inicio]

    h_actual = heuristica[actual][fin]
    pasos.append(f"  Estado inicial: nodo {actual}  h'={h_actual}")

    while actual != fin:
        vecinos = obtener_vecinos(grafo, actual, sentido)
        mejora_encontrada = False

        pasos.append(f"  Evaluando vecinos de nodo {actual}:")
        for vecino, peso in vecinos:
            if vecino in visitados:
                continue
            h_vecino = heuristica[vecino][fin]
            pasos.append(f"    Vecino {vecino}: costo_arco={peso}, h'={h_vecino}  (actual h'={h_actual})")

            if h_vecino < h_actual:
                # Primer vecino mejor → lo tomamos
                visitados.add(vecino)
                camino.append(vecino)
                costo_total += peso
                nodos_visitados.append(vecino)
                pasos.append(f"    ✓ Mejor estado encontrado: nodo {vecino} (h'={h_vecino} < {h_actual}). Moviéndose.")
                actual = vecino
                h_actual = h_vecino
                mejora_encontrada = True
                break

        if not mejora_encontrada:
            pasos.append(f"  ✗ No se encontró estado mejor desde nodo {actual}. Escalada detenida (posible máximo local).")
            if actual == fin:
                pasos.append(f"  ✓ META ENCONTRADA: nodo {fin}")
                return camino, costo_total, nodos_visitados, pasos
            return None, float('inf'), nodos_visitados, pasos

    pasos.append(f"  ✓ META ENCONTRADA: nodo {fin}")
    return camino, costo_total, nodos_visitados, pasos


# =============================================================================
# 4. ESCALADA MÁXIMA PENDIENTE (Steepest-Ascent Hill Climbing)
# =============================================================================

def escalada_maxima_pendiente(grafo, inicio, fin, sentido, heuristica):
    """
    Escalada por la máxima pendiente.
    Evalúa TODOS los vecinos del estado actual y elige el MEJOR (menor h').
    Más sistemática que la escalada simple, pero también puede quedar
    atrapada en máximos locales.

    Retorna: (camino, costo_total, nodos_visitados, pasos_log)
    """
    if inicio == fin:
        return [inicio], 0, [inicio], ["Estado inicial = Estado final"]

    actual = inicio
    camino = [inicio]
    costo_total = 0
    visitados = {inicio}
    pasos = []
    nodos_visitados = [inicio]

    h_actual = heuristica[actual][fin]
    pasos.append(f"  Estado inicial: nodo {actual}  h'={h_actual}")

    while actual != fin:
        vecinos = obtener_vecinos(grafo, actual, sentido)
        pasos.append(f"  Evaluando TODOS los vecinos de nodo {actual}:")

        mejor_vecino = None
        mejor_h = h_actual
        mejor_costo_arco = 0
        succ_info = []

        for vecino, peso in vecinos:
            if vecino in visitados:
                continue
            h_vecino = heuristica[vecino][fin]
            succ_info.append((vecino, peso, h_vecino))
            pasos.append(f"    Vecino {vecino}: costo_arco={peso}, h'={h_vecino}")
            if h_vecino < mejor_h:
                mejor_h = h_vecino
                mejor_vecino = vecino
                mejor_costo_arco = peso

        if mejor_vecino is None:
            pasos.append(f"  ✗ Ningún vecino mejora el estado actual (h'={h_actual}). Escalada detenida.")
            if actual == fin:
                return camino, costo_total, nodos_visitados, pasos
            return None, float('inf'), nodos_visitados, pasos

        pasos.append(f"  ✓ Mejor sucesor: nodo {mejor_vecino} (h'={mejor_h}). Moviéndose.")
        visitados.add(mejor_vecino)
        camino.append(mejor_vecino)
        costo_total += mejor_costo_arco
        nodos_visitados.append(mejor_vecino)
        actual = mejor_vecino
        h_actual = mejor_h

    pasos.append(f"  ✓ META ENCONTRADA: nodo {fin}")
    return camino, costo_total, nodos_visitados, pasos


# =============================================================================
# 5. EL PRIMERO MEJOR / BEST-FIRST (A*)
# =============================================================================

def primero_mejor(grafo, inicio, fin, sentido, heuristica):
    """
    Búsqueda El Primero Mejor (Best-First Search / A*).
    Combina las ventajas de BFS y DFS.
    Usa f'(n) = g(n) + h'(n) donde:
      g(n) = costo real desde el inicio hasta n
      h'(n) = estimación heurística del costo de n hasta el fin

    Mantiene listas ABIERTOS y CERRADOS.
    Garantiza el camino óptimo si h' es admisible (no sobreestima).

    Retorna: (camino, costo_total, nodos_visitados, pasos_log)
    """
    if inicio == fin:
        return [inicio], 0, [inicio], ["Estado inicial = Estado final"]

    # ABIERTOS: cola de prioridad (f', nodo, g, camino)
    # Para desempate por sentido, usamos el nodo como segundo criterio
    h_inicio = heuristica[inicio][fin]
    abiertos = [(h_inicio, inicio, 0, [inicio])]
    heapq.heapify(abiertos)

    cerrados = set()
    mejor_g = {inicio: 0}   # mejor g conocido para cada nodo
    pasos = []
    nodos_visitados = []

    pasos.append(f"  INICIO: ABIERTOS = [({inicio}, f'={h_inicio})]")
    pasos.append(f"  CERRADOS = []")

    while abiertos:
        f_actual, actual, g_actual, camino = heapq.heappop(abiertos)

        if actual in cerrados:
            continue

        cerrados.add(actual)
        nodos_visitados.append(actual)
        h_actual = heuristica[actual][fin]
        pasos.append(f"  Tomando mejor nodo de ABIERTOS: {actual}  g={g_actual}, h'={h_actual}, f'={f_actual}")
        pasos.append(f"  → Moviendo nodo {actual} a CERRADOS")

        if actual == fin:
            pasos.append(f"  ✓ META ENCONTRADA: nodo {fin}  Costo total: {g_actual}")
            return camino, g_actual, nodos_visitados, pasos

        vecinos = obtener_vecinos(grafo, actual, sentido)
        pasos.append(f"  Generando sucesores de nodo {actual}:")

        for vecino, peso in vecinos:
            if vecino in cerrados:
                pasos.append(f"    Vecino {vecino}: ya en CERRADOS, ignorado")
                continue

            nuevo_g = g_actual + peso
            h_vecino = heuristica[vecino][fin]
            nuevo_f = nuevo_g + h_vecino

            if vecino not in mejor_g or nuevo_g < mejor_g[vecino]:
                mejor_g[vecino] = nuevo_g
                heapq.heappush(abiertos, (nuevo_f, vecino, nuevo_g, camino + [vecino]))
                pasos.append(f"    → Añadiendo/actualizando nodo {vecino} en ABIERTOS: g={nuevo_g}, h'={h_vecino}, f'={nuevo_f}")
            else:
                pasos.append(f"    Vecino {vecino}: ya existe con mejor camino (g={mejor_g[vecino]} ≤ {nuevo_g}), ignorado")

    pasos.append("  ✗ No se encontró camino (ABIERTOS vacío)")
    return None, float('inf'), nodos_visitados, pasos
