"""
SISTEMA EXPERTO DE RECOMENDACIÓN DE VINOS — CDMX 2026
=====================================================
Representación del conocimiento:
  - Marcos (Frames): cada vino es un diccionario con slots
  - Tripletas OAV: (Objeto=vino, Atributo=maridaje, Valor=comida)
  - Motor de inferencia basado en reglas (lógica proposicional)

Standalone — no requiere MySQL ni dependencias externas.
"""

import os

# ─────────────────────────────────────────────────────────
# BASE DE CONOCIMIENTO (Marcos / Frames)
# Cada entrada es un frame con slots: nombre, bodega, tipo,
# uva, popularidad, precio_aprox, perfil, maridaje_target
# ─────────────────────────────────────────────────────────
BASE_CONOCIMIENTO = [
    {
        "nombre": "L.A. Cetto Cabernet",
        "bodega": "L.A. Cetto",
        "tipo": "Tinto",
        "uva": "Cabernet Sauvignon",
        "popularidad": 95,
        "precio_aprox": 200,
        "perfil": "tánico y robusto",
        "maridaje_target": "Carne asada, Pasta, Mole, Carnitas, Pizza, Hamburguesa",
    },
    {
        "nombre": "L.A. Cetto Petite Sirah",
        "bodega": "L.A. Cetto",
        "tipo": "Tinto",
        "uva": "Petite Sirah",
        "popularidad": 90,
        "precio_aprox": 190,
        "perfil": "intenso y especiado",
        "maridaje_target": "Birria, Carnitas, Carne asada, Tacos al pastor, Chorizo",
    },
    {
        "nombre": "Casa Madero 3V",
        "bodega": "Casa Madero",
        "tipo": "Tinto",
        "uva": "Blend Cabernet-Merlot-Shiraz",
        "popularidad": 98,
        "precio_aprox": 520,
        "perfil": "elegante y equilibrado",
        "maridaje_target": "Mole, Pato, Cordero, Carne asada, Quesos",
    },
    {
        "nombre": "Casa Madero V Rosado",
        "bodega": "Casa Madero",
        "tipo": "Rosado",
        "uva": "Tempranillo",
        "popularidad": 92,
        "precio_aprox": 400,
        "perfil": "frutal y fresco",
        "maridaje_target": "Sushi, Mariscos, Ensalada, Champiñones, Pasta",
    },
    {
        "nombre": "Monte Xanic Viña Kristel",
        "bodega": "Monte Xanic",
        "tipo": "Blanco",
        "uva": "Sauvignon Blanc",
        "popularidad": 94,
        "precio_aprox": 450,
        "perfil": "cítrico y mineral",
        "maridaje_target": "Mariscos, Sushi, Pescado, Champiñones, Ensalada",
    },
    {
        "nombre": "Riunite Lambrusco",
        "bodega": "Riunite",
        "tipo": "Tinto Dulce",
        "uva": "Lambrusco",
        "popularidad": 99,
        "precio_aprox": 180,
        "perfil": "dulce y afrutado",
        "maridaje_target": "Pizza, Pasta, Quesos, Embutidos, Sushi",
    },
    {
        "nombre": "Ramón Bilbao Crianza",
        "bodega": "Ramón Bilbao",
        "tipo": "Tinto",
        "uva": "Tempranillo",
        "popularidad": 91,
        "precio_aprox": 450,
        "perfil": "suave y afrutado",
        "maridaje_target": "Pasta, Tacos al pastor, Quesos, Pizza, Carnitas",
    },
    {
        "nombre": "Casillero del Diablo Malbec",
        "bodega": "Casillero del Diablo",
        "tipo": "Tinto",
        "uva": "Malbec",
        "popularidad": 88,
        "precio_aprox": 250,
        "perfil": "frutal con taninos suaves",
        "maridaje_target": "Carne asada, Hamburguesa, Pizza, Tacos al pastor, Champiñones",
    },
    {
        "nombre": "Sala Vivé Brut",
        "bodega": "Sala Vivé",
        "tipo": "Espumoso",
        "uva": "Macabeo",
        "popularidad": 86,
        "precio_aprox": 350,
        "perfil": "burbujas finas y cítrico",
        "maridaje_target": "Mariscos, Sushi, Quesos, Ensalada, Champiñones",
    },
    {
        "nombre": "Balero Tinto",
        "bodega": "Baja Wine",
        "tipo": "Tinto",
        "uva": "Blend",
        "popularidad": 84,
        "precio_aprox": 420,
        "perfil": "moderno y jugoso",
        "maridaje_target": "Tacos al pastor, Carnitas, Quesadillas, Mole, Birria",
    },
    {
        "nombre": "Santo Tomás Barbera",
        "bodega": "Santo Tomás",
        "tipo": "Tinto",
        "uva": "Barbera",
        "popularidad": 80,
        "precio_aprox": 470,
        "perfil": "ácido y ligero",
        "maridaje_target": "Pasta, Pizza, Quesos, Mariscos, Ensalada",
    },
    {
        "nombre": "Don Leo Cabernet",
        "bodega": "Don Leo",
        "tipo": "Tinto",
        "uva": "Cabernet Sauvignon",
        "popularidad": 82,
        "precio_aprox": 580,
        "perfil": "robusto y especiado",
        "maridaje_target": "Carne asada, Mole, Pato, Cordero, Quesos",
    },
]


# ─────────────────────────────────────────────────────────
# MOTOR DE INFERENCIA
# Reglas basadas en lógica proposicional:
#   Regla 1: maridaje ∋ comida ∧ precio ≤ presupuesto → recomendar
#   Regla 1b: + filtro por tipo preferido si aplica
#   Regla 2: fallback → vino más popular en presupuesto
#   Regla 3: sin resultado → notificar
# ─────────────────────────────────────────────────────────
def motor_inferencia(comida: str, presupuesto: float, tipo_pref: str = "") -> dict:
    """
    Aplica las reglas de inferencia y retorna un dict con:
      - ganador: frame del vino recomendado (o None)
      - regla_aplicada: número de regla usada
      - es_fallback: True si se usó Regla 2
    """
    # Regla 1 — Match directo
    candidatos = [
        v for v in BASE_CONOCIMIENTO
        if comida.lower() in v["maridaje_target"].lower()
        and v["precio_aprox"] <= presupuesto
    ]

    regla = 1
    es_fallback = False

    # Regla 1b — Filtro por tipo
    if candidatos and tipo_pref:
        con_tipo = [v for v in candidatos if v["tipo"].lower() == tipo_pref.lower()]
        if con_tipo:
            candidatos = con_tipo
            regla = "1b"

    if candidatos:
        ganador = max(candidatos, key=lambda v: v["popularidad"])
        return {"ganador": ganador, "regla_aplicada": regla, "es_fallback": False}

    # Regla 2 — Fallback
    comodines = [v for v in BASE_CONOCIMIENTO if v["precio_aprox"] <= presupuesto]
    if comodines:
        ganador = max(comodines, key=lambda v: v["popularidad"])
        return {"ganador": ganador, "regla_aplicada": 2, "es_fallback": True}

    # Regla 3 — Sin resultado
    return {"ganador": None, "regla_aplicada": 3, "es_fallback": False}


# ─────────────────────────────────────────────────────────
# INTERFAZ DE USUARIO (terminal)
# ─────────────────────────────────────────────────────────
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_barra(valor: int, maximo: int = 100, largo: int = 20) -> str:
    llenos = int((valor / maximo) * largo)
    return "█" * llenos + "░" * (largo - llenos)


def mostrar_resultado(resultado: dict, comida: str):
    print("\n" + "─" * 50)
    ganador = resultado["ganador"]

    if ganador is None:
        print("  Sin resultado: no hay vinos en ese rango de precio.")
        print("  Intenta con un presupuesto mayor.")
        return

    if resultado["es_fallback"]:
        print(f"  No encontré maridaje exacto para '{comida}'.")
        print("  Buscando el vino más popular en tu presupuesto...\n")

    print(f"  🍷  {ganador['nombre']}")
    print(f"      {ganador['bodega']}  ·  {ganador['tipo']}  ·  {ganador['uva']}")
    print()
    print(f"  Popularidad CDMX:  {mostrar_barra(ganador['popularidad'])} {ganador['popularidad']}%")
    print(f"  Precio aprox.:     ${ganador['precio_aprox']} MXN")
    print(f"  Perfil:            {ganador['perfil']}")
    print()
    print(f"  ¿Por qué? Su perfil combina excelente con {comida}.")
    print(f"  Maridajes: {ganador['maridaje_target']}")
    print(f"\n  [Regla aplicada: {resultado['regla_aplicada']}]")
    print("─" * 50)


def listar_vinos():
    print("\n  Base de conocimiento — vinos disponibles:\n")
    for i, v in enumerate(BASE_CONOCIMIENTO, 1):
        print(f"  {i:2}. {v['nombre']:<35} {v['tipo']:<12} ${v['precio_aprox']:>4}  pop:{v['popularidad']}%")
    print()


def sistema_experto():
    while True:
        limpiar()
        print("=" * 52)
        print("   SISTEMA EXPERTO DE VINOS  —  CDMX 2026")
        print("=" * 52)
        print("\n  [1] Obtener recomendación")
        print("  [2] Ver todos los vinos")
        print("  [3] Salir")

        opcion = input("\n  Elige una opción: ").strip()

        if opcion == "3":
            print("\n  ¡Salud! 🍷\n")
            break

        if opcion == "2":
            listar_vinos()
            input("  Presiona Enter para continuar...")
            continue

        if opcion != "1":
            continue

        # Captura de datos
        comida = input("\n  ¿Qué vas a comer? (ej. Pasta, Mole, Tacos): ").strip()
        if not comida:
            continue

        while True:
            try:
                presupuesto = float(input("  Presupuesto máximo (MXN): "))
                break
            except ValueError:
                print("  Ingresa un número válido.")

        tipo_pref = input(
            "  Tipo preferido (Tinto/Blanco/Rosado/Espumoso o Enter para cualquiera): "
        ).strip()

        resultado = motor_inferencia(comida, presupuesto, tipo_pref)
        mostrar_resultado(resultado, comida)

        otra = input("\n  ¿Otra recomendación? (s/n): ").strip().lower()
        if otra != "s":
            print("\n  ¡Salud! 🍷\n")
            break


if __name__ == "__main__":
    sistema_experto()