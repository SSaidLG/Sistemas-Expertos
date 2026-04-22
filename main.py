#!/usr/bin/env python3
# =============================================================================
# SISTEMA DE BÚSQUEDA EN GRAFO - Sistemas Expertos 2020-2
# =============================================================================
# Ejecuta 5 tipos de búsqueda sobre el grafo dirigido del profesor.
# El usuario indica: nodo_inicio, nodo_fin y sentido (horario/antihorario).
# El programa ejecuta TODAS las búsquedas automáticamente.
#
# Búsquedas:
#   1. A lo Ancho (BFS)
#   2. En Profundidad (DFS)
#   3. Escalada Simple
#   4. Escalada Máxima Pendiente
#   5. El Primero Mejor (A*)
# =============================================================================

import sys
from grafo import construir_grafo, construir_heuristica, NODOS
from busquedas import (
    busqueda_ancho,
    busqueda_profundidad,
    escalada_simple,
    escalada_maxima_pendiente,
    primero_mejor,
)

# ─────────────────────────────────────────────────────────────────────────────
# UTILIDADES DE PRESENTACIÓN
# ─────────────────────────────────────────────────────────────────────────────

ANCHO_LINEA = 70

def separador(caracter='═', ancho=ANCHO_LINEA):
    print(caracter * ancho)

def titulo(texto, caracter='═'):
    separador(caracter)
    print(f"  {texto}")
    separador(caracter)

def subtitulo(texto):
    print()
    print('─' * ANCHO_LINEA)
    print(f"  {texto}")
    print('─' * ANCHO_LINEA)


def formatear_camino(camino):
    if camino is None:
        return "No se encontró camino"
    return " → ".join(str(n) for n in camino)


def calcular_costo_camino(grafo, camino):
    """Recalcula el costo real del camino recorrido."""
    if camino is None or len(camino) < 2:
        return 0
    costo = 0
    tabla_arcos = {}
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos:
            tabla_arcos[(nodo, vecino)] = peso
    for i in range(len(camino) - 1):
        arco = (camino[i], camino[i + 1])
        if arco in tabla_arcos:
            costo += tabla_arcos[arco]
        else:
            costo += 0  # arco no encontrado
    return costo


def imprimir_resultado(nombre, camino, costo, visitados, pasos, verbose):
    """Imprime el resultado de una búsqueda de forma clara."""
    subtitulo(nombre)

    if camino:
        print(f"  Camino encontrado : {formatear_camino(camino)}")
        print(f"  Nodos en el camino: {len(camino)}")
        print(f"  Costo total       : {costo}")
        print(f"  Nodos explorados  : {len(visitados)}")
    else:
        print(f"  ✗ No se encontró un camino.")
        print(f"  Nodos explorados  : {len(visitados)}")

    if verbose:
        print()
        print("  [ Detalle del proceso ]")
        for paso in pasos:
            print(f"  {paso}")


def imprimir_resumen_comparativo(resultados, inicio, fin, sentido_texto):
    """Imprime tabla comparativa de todas las búsquedas."""
    print()
    separador('═')
    print(f"  RESUMEN COMPARATIVO")
    print(f"  Nodo inicio: {inicio}  →  Nodo fin: {fin}  |  Sentido: {sentido_texto}")
    separador('═')
    print(f"  {'Algoritmo':<35} {'Camino':<6} {'Costo':>8} {'Explorados':>12}")
    print(f"  {'─'*35} {'─'*6} {'─'*8} {'─'*12}")

    for nombre, camino, costo, visitados, _ in resultados:
        if camino:
            camino_str = f"{len(camino)} nodos"
            costo_str = str(costo)
        else:
            camino_str = "No halló"
            costo_str = "─"
        print(f"  {nombre:<35} {camino_str:<6} {costo_str:>8} {len(visitados):>12}")

    separador('═')


# ─────────────────────────────────────────────────────────────────────────────
# VALIDACIÓN DE ENTRADA
# ─────────────────────────────────────────────────────────────────────────────

def pedir_nodo(mensaje):
    """Solicita un nodo válido al usuario."""
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor in NODOS:
                return valor
            else:
                print(f"  ✗ Nodo inválido. Ingresa un número entre 1 y 28.")
        except ValueError:
            print(f"  ✗ Entrada inválida. Ingresa un número entero.")


def pedir_sentido():
    """Solicita el sentido de búsqueda al usuario."""
    while True:
        valor = input("  Sentido de búsqueda [H=Horario / A=Antihorario]: ").strip().upper()
        if valor in ('H', 'A'):
            return valor
        else:
            print("  ✗ Sentido inválido. Ingresa H (horario) o A (antihorario).")


def pedir_verbose():
    """Pregunta si se desea ver el detalle paso a paso."""
    valor = input("  ¿Mostrar detalle paso a paso? [S/N]: ").strip().upper()
    return valor == 'S'


# ─────────────────────────────────────────────────────────────────────────────
# PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def ejecutar_busquedas(grafo, heuristica, inicio, fin, sentido, verbose):
    """Ejecuta los 5 algoritmos y retorna los resultados."""
    sentido_texto = "Horario (menor → mayor)" if sentido == 'H' else "Antihorario (mayor → menor)"

    print()
    titulo(f"BÚSQUEDAS: {inicio} → {fin}  |  {sentido_texto}")

    resultados = []

    # ── 1. Búsqueda a lo Ancho ──────────────────────────────────────────────
    print("\n  Ejecutando búsquedas a ciegas...")
    camino, costo, visitados, pasos = busqueda_ancho(grafo, inicio, fin, sentido)
    imprimir_resultado("1. Búsqueda a lo Ancho (BFS)", camino, costo, visitados, pasos, verbose)
    resultados.append(("1. A lo Ancho (BFS)", camino, costo, visitados, pasos))

    # ── 2. Búsqueda en Profundidad ──────────────────────────────────────────
    camino, costo, visitados, pasos = busqueda_profundidad(grafo, inicio, fin, sentido)
    imprimir_resultado("2. Búsqueda en Profundidad (DFS)", camino, costo, visitados, pasos, verbose)
    resultados.append(("2. En Profundidad (DFS)", camino, costo, visitados, pasos))

    # ── 3. Escalada Simple ──────────────────────────────────────────────────
    print("\n  Ejecutando búsquedas heurísticas...")
    camino, costo, visitados, pasos = escalada_simple(grafo, inicio, fin, sentido, heuristica)
    imprimir_resultado("3. Escalada Simple", camino, costo, visitados, pasos, verbose)
    resultados.append(("3. Escalada Simple", camino, costo, visitados, pasos))

    # ── 4. Escalada Máxima Pendiente ────────────────────────────────────────
    camino, costo, visitados, pasos = escalada_maxima_pendiente(grafo, inicio, fin, sentido, heuristica)
    imprimir_resultado("4. Escalada Máxima Pendiente", camino, costo, visitados, pasos, verbose)
    resultados.append(("4. Escalada Máx. Pendiente", camino, costo, visitados, pasos))

    # ── 5. El Primero Mejor (A*) ─────────────────────────────────────────────
    camino, costo, visitados, pasos = primero_mejor(grafo, inicio, fin, sentido, heuristica)
    imprimir_resultado("5. El Primero Mejor (A*)", camino, costo, visitados, pasos, verbose)
    resultados.append(("5. El Primero Mejor (A*)", camino, costo, visitados, pasos))

    # ── Resumen comparativo ─────────────────────────────────────────────────
    imprimir_resumen_comparativo(resultados, inicio, fin, sentido_texto)

    return resultados


def mostrar_grafo_info(grafo):
    """Muestra información básica del grafo cargado."""
    total_arcos = sum(len(v) for v in grafo.values())
    print(f"  Nodos en el grafo : {len(grafo)}")
    print(f"  Total de arcos    : {total_arcos}")
    print(f"  Nodos disponibles : {sorted(grafo.keys())}")


def menu_principal():
    """Bucle principal del programa."""
    separador('═')
    print("  SISTEMA DE BÚSQUEDA EN GRAFO")
    print("  Sistemas Expertos - Grafo 2020-2")
    separador('═')

    # Cargar datos
    print("\n  Cargando grafo y tabla heurística...")
    grafo = construir_grafo()
    heuristica = construir_heuristica()
    print("  ✓ Grafo cargado correctamente.")
    mostrar_grafo_info(grafo)

    while True:
        print()
        separador('─')
        print("  NUEVA BÚSQUEDA")
        separador('─')
        print(f"  Nodos disponibles: 1 al 28")
        print()

        inicio = pedir_nodo("  Nodo de inicio  : ")
        fin    = pedir_nodo("  Nodo de destino : ")
        sentido = pedir_sentido()
        verbose = pedir_verbose()

        ejecutar_busquedas(grafo, heuristica, inicio, fin, sentido, verbose)

        print()
        continuar = input("  ¿Realizar otra búsqueda? [S/N]: ").strip().upper()
        if continuar != 'S':
            break

    print()
    separador('═')
    print("  Programa terminado.")
    separador('═')


# ─────────────────────────────────────────────────────────────────────────────
# MODO NO INTERACTIVO (para pruebas automáticas)
# ─────────────────────────────────────────────────────────────────────────────

def ejecutar_prueba(inicio, fin, sentido, verbose=False):
    """Función de prueba para ejecutar directamente sin interacción."""
    grafo = construir_grafo()
    heuristica = construir_heuristica()
    ejecutar_busquedas(grafo, heuristica, inicio, fin, sentido, verbose)


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Si se pasan argumentos por línea de comandos: inicio fin sentido [v]
    if len(sys.argv) >= 4:
        try:
            arg_inicio  = int(sys.argv[1])
            arg_fin     = int(sys.argv[2])
            arg_sentido = sys.argv[3].upper()
            arg_verbose = len(sys.argv) >= 5 and sys.argv[4].lower() in ('v', 'verbose', 's', 'si')

            if arg_inicio not in NODOS or arg_fin not in NODOS:
                print(f"Error: los nodos deben estar entre 1 y 28.")
                sys.exit(1)
            if arg_sentido not in ('H', 'A'):
                print("Error: sentido debe ser H (horario) o A (antihorario).")
                sys.exit(1)

            grafo = construir_grafo()
            heuristica = construir_heuristica()
            ejecutar_busquedas(grafo, heuristica, arg_inicio, arg_fin, arg_sentido, arg_verbose)

        except ValueError:
            print("Uso: python main.py <inicio> <fin> <H|A> [v]")
            sys.exit(1)
    else:
        # Modo interactivo
        try:
            menu_principal()
        except KeyboardInterrupt:
            print("\n\n  Programa interrumpido por el usuario.")
