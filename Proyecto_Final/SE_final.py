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
    {"nombre": "L.A. Cetto Cabernet", "bodega": "L.A. Cetto", "tipo": "Tinto", "uva": "Cabernet Sauvignon", "popularidad": 95, "precio_aprox": 210, "perfil": "tánico y robusto", "maridaje_target": "Carne asada, Pasta, Mole, Carnitas, Pizza, Hamburguesa"},
    {"nombre": "L.A. Cetto Petite Sirah", "bodega": "L.A. Cetto", "tipo": "Tinto", "uva": "Petite Sirah", "popularidad": 90, "precio_aprox": 190, "perfil": "intenso y especiado", "maridaje_target": "Birria, Carnitas, Carne asada, Tacos al pastor, Chorizo"},
    {"nombre": "Casa Madero 3V", "bodega": "Casa Madero", "tipo": "Tinto", "uva": "Blend (C-M-S)", "popularidad": 98, "precio_aprox": 550, "perfil": "elegante y equilibrado", "maridaje_target": "Mole, Pato, Cordero, Cortes finos, Quesos maduros"},
    {"nombre": "Riunite Lambrusco", "bodega": "Riunite", "tipo": "Tinto Dulce", "uva": "Lambrusco", "popularidad": 99, "precio_aprox": 195, "perfil": "dulce y efervescente", "maridaje_target": "Pizza, Sushi, Pasta, Postres, Picante"},
    {"nombre": "Monte Xanic V. Kristel", "bodega": "Monte Xanic", "tipo": "Blanco", "uva": "Sauvignon Blanc", "popularidad": 94, "precio_aprox": 480, "perfil": "cítrico y fresco", "maridaje_target": "Mariscos, Ensaladas, Ceviche, Pescado blanco"},
    {"nombre": "Casillero del Diablo", "bodega": "Concha y Toro", "tipo": "Tinto", "uva": "Cabernet Sauvignon", "popularidad": 96, "precio_aprox": 260, "perfil": "frutos rojos y vainilla", "maridaje_target": "Hamburguesas, Quesos, Pizza, Carne asada"},
    {"nombre": "Santo Tomás Barbera", "bodega": "Santo Tomás", "tipo": "Tinto", "uva": "Barbera", "popularidad": 88, "precio_aprox": 490, "perfil": "ácido y frutal", "maridaje_target": "Pastas, Lasagna, Ensalada, Pizza"},
    {"nombre": "Balero Tinto", "bodega": "Baja Wine", "tipo": "Tinto", "uva": "Blend", "popularidad": 91, "precio_aprox": 460, "perfil": "equilibrado y amigable", "maridaje_target": "Tacos de guisado, Carnitas, Tacos al pastor"},
    {"nombre": "Las Nubes Selección T.", "bodega": "Las Nubes", "tipo": "Tinto", "uva": "Blend", "popularidad": 85, "precio_aprox": 720, "perfil": "robusto y complejo", "maridaje_target": "Cordero, Borrego, Cortes de carne, Estofados"},
    {"nombre": "Mariatinto", "bodega": "Mariatinto", "tipo": "Tinto", "uva": "Blend", "popularidad": 89, "precio_aprox": 950, "perfil": "sofisticado y sedoso", "maridaje_target": "Alta cocina mexicana, Mole negro, Pato"},
    {"nombre": "Sala Vivé Brut", "bodega": "Freixenet Qro.", "tipo": "Espumoso", "uva": "Macabeo", "popularidad": 90, "precio_aprox": 360, "perfil": "burbuja fina y seco", "maridaje_target": "Chiles en nogada, Postres, Mariscos, Sushi"},
    {"nombre": "Don Leo Shiraz", "bodega": "Don Leo", "tipo": "Tinto", "uva": "Shiraz", "popularidad": 84, "precio_aprox": 680, "perfil": "especiado y potente", "maridaje_target": "Carne de caza, Estofados, Barbacoa"},
    {"nombre": "Corona del Valle Rosé", "bodega": "Corona del V.", "tipo": "Rosado", "uva": "Grenache", "popularidad": 82, "precio_aprox": 610, "perfil": "frutal y elegante", "maridaje_target": "Sushi, Paella, Mariscos, Ensaladas"},
    {"nombre": "Laberinto Mezcla T.", "bodega": "Cava Quintanilla", "tipo": "Tinto", "uva": "Blend", "popularidad": 80, "precio_aprox": 580, "perfil": "estructurado y mineral", "maridaje_target": "Enchiladas potosinas, Carne asada, Quesos maduros"},
    {"nombre": "Sangre de Toro", "bodega": "Torres", "tipo": "Tinto", "uva": "Garnacha-Cariñena", "popularidad": 92, "precio_aprox": 290, "perfil": "cálido y especiado", "maridaje_target": "Tapas, Embutidos, Carnitas, Cordero"},
    {"nombre": "Yellow Tail Shiraz", "bodega": "Casella Family", "tipo": "Tinto", "uva": "Shiraz", "popularidad": 87, "precio_aprox": 240, "perfil": "suave y frutal", "maridaje_target": "Barbacoa, Pizza, Comida rápida, Alitas"},
    {"nombre": "Adobe Guadalupe Kerubiel", "bodega": "Adobe Guad.", "tipo": "Tinto", "uva": "Blend G-S-M", "popularidad": 83, "precio_aprox": 1200, "perfil": "complejo y tánico", "maridaje_target": "Cortes premium, Venado, Estofados intensos"},
    {"nombre": "Pedro Domecq XA", "bodega": "Domecq", "tipo": "Tinto", "uva": "Cabernet-Grenache", "popularidad": 93, "precio_aprox": 185, "perfil": "ligero y directo", "maridaje_target": "Tacos de canasta, Comida diaria, Quesadillas"},
    {"nombre": "Ramón Bilbao Crianza", "bodega": "R. Bilbao", "tipo": "Tinto", "uva": "Tempranillo", "popularidad": 95, "precio_aprox": 460, "perfil": "clásico y equilibrado", "maridaje_target": "Jamón Ibérico, Quesos maduros, Cordero, Paella"},
    {"nombre": "19 Crimes Cali Red", "bodega": "19 Crimes", "tipo": "Tinto", "uva": "Blend", "popularidad": 91, "precio_aprox": 380, "perfil": "denso y dulce", "maridaje_target": "Alitas, Costillas BBQ, Pizza, Hamburguesas"},
    {"nombre": "Meinklang Prosa", "bodega": "Meinklang", "tipo": "Rosado E.", "uva": "Pinot Noir", "popularidad": 78, "precio_aprox": 550, "perfil": "natural y refrescante", "maridaje_target": "Brunch, Ensaladas frutales, Sushi, Mariscos"},
    {"nombre": "Roganto Nebbiolo", "bodega": "Roganto", "tipo": "Tinto", "uva": "Nebbiolo", "popularidad": 86, "precio_aprox": 1100, "perfil": "potente y seco", "maridaje_target": "Queso de cabra, Carnes rojas, Guisados"},
    {"nombre": "Santo Domingo Nebbiolo", "bodega": "Santo Domingo", "tipo": "Tinto", "uva": "Nebbiolo", "popularidad": 84, "precio_aprox": 640, "perfil": "intenso y persistente", "maridaje_target": "Cortes, Guisados intensos, Venado"},
    {"nombre": "Gran Ricardo", "bodega": "Monte Xanic", "tipo": "Tinto", "uva": "Blend Bordelés", "popularidad": 81, "precio_aprox": 1850, "perfil": "ícono y elegante", "maridaje_target": "Cena de gala, Cortes Wagyu, Quesos premium"},
    {"nombre": "Vinaltura Rosado", "bodega": "Vinaltura", "tipo": "Rosado", "uva": "Syrah", "popularidad": 85, "precio_aprox": 420, "perfil": "vibrante y floral", "maridaje_target": "Cochinita pibil, Pozole, Sushi, Chiles en nogada"},
    {"nombre": "Tres Raíces Blanco", "bodega": "Tres Raíces", "tipo": "Blanco", "uva": "Sauvignon Blanc", "popularidad": 83, "precio_aprox": 510, "perfil": "mineral y fresco", "maridaje_target": "Pescado a la talla, Ceviche, Mariscos, Ensaladas"},
    {"nombre": "Cava Maciel Venus", "bodega": "Cava Maciel", "tipo": "Tinto", "uva": "Petite Sirah", "popularidad": 79, "precio_aprox": 690, "perfil": "profundo y oscuro", "maridaje_target": "Birria, Cortes grasos, Carne asada"},
    {"nombre": "El Cielo Selene", "bodega": "El Cielo", "tipo": "Rosado", "uva": "Grenache-Syrah", "popularidad": 90, "precio_aprox": 590, "perfil": "delicado y frutal", "maridaje_target": "Chiles en nogada, Sushi, Mariscos, Ensalada"},
    {"nombre": "Faustino VII", "bodega": "Faustino", "tipo": "Tinto", "uva": "Tempranillo", "popularidad": 92, "precio_aprox": 320, "perfil": "sedoso y frutal", "maridaje_target": "Pollo asado, Tortilla española, Tapas"},
    {"nombre": "Barefoot Merlot", "bodega": "Barefoot", "tipo": "Tinto", "uva": "Merlot", "popularidad": 94, "precio_aprox": 215, "perfil": "suave y versátil", "maridaje_target": "Botanas, Pasta suave, Pollo, Quesos"},
    {"nombre": "Kim Crawford", "bodega": "Constellation", "tipo": "Blanco", "uva": "Sauvignon Blanc", "popularidad": 88, "precio_aprox": 750, "perfil": "tropical y ácido", "maridaje_target": "Comida asiática, Ensalada César, Mariscos"},
    {"nombre": "Espumante Puerta del Lobo", "bodega": "P. del Lobo", "tipo": "Espumoso", "uva": "Brut Nature", "popularidad": 82, "precio_aprox": 780, "perfil": "elegante y seco", "maridaje_target": "Ostras, Mariscos, Celebración, Sushi"},
    {"nombre": "Rutini Malbec", "bodega": "Rutini", "tipo": "Tinto", "uva": "Malbec", "popularidad": 87, "precio_aprox": 850, "perfil": "estructurado y distinguido", "maridaje_target": "Bife de chorizo, Empanadas, Carne asada"},
    {"nombre": "Luigi Bosca", "bodega": "L. Bosca", "tipo": "Tinto", "uva": "Malbec", "popularidad": 91, "precio_aprox": 620, "perfil": "clásico malbec argentino", "maridaje_target": "Carne asada, Choripán, Cortes, Quesos"},
    {"nombre": "Alamos Malbec", "bodega": "Alamos", "tipo": "Tinto", "uva": "Malbec", "popularidad": 93, "precio_aprox": 340, "perfil": "frutal y jugoso", "maridaje_target": "Hamburguesas, Tacos de bistec, Pasta"},
    {"nombre": "J.P. Chenet", "bodega": "J.P. Chenet", "tipo": "Tinto", "uva": "Cabernet-Syrah", "popularidad": 95, "precio_aprox": 235, "perfil": "fácil de beber", "maridaje_target": "Quesos suaves, Pizza, Pollo, Picnic"},
    {"nombre": "Sutter Home White Zin", "bodega": "Sutter Home", "tipo": "Rosado", "uva": "Zinfandel", "popularidad": 96, "precio_aprox": 220, "perfil": "dulce y ligero", "maridaje_target": "Comida picante, Postres, Fruta, Social"},
    {"nombre": "Chateau Camou Flor de L.", "bodega": "Ch. Camou", "tipo": "Blanco", "uva": "Chardonnay", "popularidad": 81, "precio_aprox": 520, "perfil": "untuoso y floral", "maridaje_target": "Pescado al horno, Risotto, Pollo con crema"},
    {"nombre": "Único Luis Miguel", "bodega": "Ventisquero", "tipo": "Tinto", "uva": "Cabernet Sauvignon", "popularidad": 85, "precio_aprox": 795, "perfil": "intenso y apasionado", "maridaje_target": "Cena romántica, Cortes, Regalos"},
    {"nombre": "Megacero", "bodega": "Encinillas", "tipo": "Tinto", "uva": "Blend", "popularidad": 88, "precio_aprox": 1150, "perfil": "poderoso y persistente", "maridaje_target": "Rib eye, Cortes añejados, Carne roja"},
    {"nombre": "Piedra Negra Alta Colecc.", "bodega": "Lurton", "tipo": "Tinto", "uva": "Malbec", "popularidad": 86, "precio_aprox": 430, "perfil": "fresco y frutal", "maridaje_target": "Tacos de tuétano, Carne asada, Empanadas"},
    {"nombre": "Evolución Chardonnay", "bodega": "Casa Madero", "tipo": "Blanco", "uva": "Chardonnay", "popularidad": 89, "precio_aprox": 415, "perfil": "fresco con madera", "maridaje_target": "Pollo con crema, Salmón, Pasta blanca"},
    {"nombre": "Mogor Badán", "bodega": "Mogor Badán", "tipo": "Tinto", "uva": "Blend Burdeos", "popularidad": 80, "precio_aprox": 1250, "perfil": "tradicional y complejo", "maridaje_target": "Gastronomía de autor, Cortes, Cordero"},
    {"nombre": "Bruma Plan B Tinto", "bodega": "Bruma", "tipo": "Tinto", "uva": "Blend", "popularidad": 84, "precio_aprox": 590, "perfil": "moderno y directo", "maridaje_target": "Tacos al pastor, Pizza, Hamburguesas, Pasta"},
    {"nombre": "Henri Lurton Chenin", "bodega": "Bodegas HL", "tipo": "Blanco", "uva": "Chenin Blanc", "popularidad": 82, "precio_aprox": 670, "perfil": "aromático y vivaz", "maridaje_target": "Comida tailandesa, Mariscos, Ceviche"},
    {"nombre": "Solar Fortún Syrah", "bodega": "Solar Fortún", "tipo": "Tinto", "uva": "Syrah", "popularidad": 81, "precio_aprox": 745, "perfil": "especiado y ahumado", "maridaje_target": "Carne de cerdo, Adobos, Barbacoa"},
    {"nombre": "Cuatro Soles", "bodega": "Valle Redondo", "tipo": "Tinto", "uva": "Cabernet Sauvignon", "popularidad": 97, "precio_aprox": 125, "perfil": "ligero y afrutado", "maridaje_target": "Tacos de canasta, Quesadillas, Uso diario"},
    {"nombre": "Reservado Concha y Toro", "bodega": "Concha y Toro", "tipo": "Tinto", "uva": "Merlot", "popularidad": 98, "precio_aprox": 165, "perfil": "suave y confiable", "maridaje_target": "Comida casera, Pasta con tomate, Pollo"},
    {"nombre": "Veuve Clicquot", "bodega": "LVMH", "tipo": "Espumoso", "uva": "Champagne", "popularidad": 89, "precio_aprox": 1950, "perfil": "lujo y estructura", "maridaje_target": "Mariscos, Canapés, Celebración, Ostras"},
    {"nombre": "Moët & Chandon", "bodega": "LVMH", "tipo": "Espumoso", "uva": "Champagne", "popularidad": 92, "precio_aprox": 1780, "perfil": "clásico y brillante", "maridaje_target": "Celebraciones, Fresas, Postres, Sushi"},
    {"nombre": "Prosecco Zonin", "bodega": "Zonin", "tipo": "Espumoso", "uva": "Glera", "popularidad": 94, "precio_aprox": 390, "perfil": "fresco y amigable", "maridaje_target": "Aperitivo, Brunch, Mimosas, Ensaladas"},
    {"nombre": "Apothic Red", "bodega": "Apothic", "tipo": "Tinto", "uva": "Blend", "popularidad": 91, "precio_aprox": 450, "perfil": "intenso y chocolate", "maridaje_target": "Costillas, Comida especiada, Pizza, Hamburguesa"},
    {"nombre": "Menade Nosso", "bodega": "Menade", "tipo": "Blanco", "uva": "Verdejo", "popularidad": 77, "precio_aprox": 680, "perfil": "ecológico y puro", "maridaje_target": "Comida vegana, Ensaladas, Pescado al vapor"},
    {"nombre": "Flor de Pingus", "bodega": "Dominio de Pingus", "tipo": "Tinto", "uva": "Tempranillo", "popularidad": 75, "precio_aprox": 2900, "perfil": "exclusivo y potente", "maridaje_target": "Coleccionista, Cortes premium, Cena especial"},
    {"nombre": "Pruno", "bodega": "Finca Villacreces", "tipo": "Tinto", "uva": "Tempranillo", "popularidad": 88, "precio_aprox": 655, "perfil": "fruta negra y roble", "maridaje_target": "Carne asada, Guisados, Embutidos"},
    {"nombre": "Montes Alpha", "bodega": "Montes", "tipo": "Tinto", "uva": "Cabernet Sauvignon", "popularidad": 86, "precio_aprox": 695, "perfil": "robusto y clásico", "maridaje_target": "Cordero, Cortes rojos, Estofados"},
    {"nombre": "Errázuriz Max", "bodega": "Errázuriz", "tipo": "Tinto", "uva": "Carmenere", "popularidad": 83, "precio_aprox": 585, "perfil": "terroso y especiado", "maridaje_target": "Comida chilena, Empanadas, Carne de cerdo"},
    {"nombre": "Kaiken Ultra", "bodega": "Kaiken", "tipo": "Tinto", "uva": "Malbec", "popularidad": 85, "precio_aprox": 595, "perfil": "elegante y floral", "maridaje_target": "Parrillada argentina, Cortes, Quesos"},
    {"nombre": "Beringer Founders Est.", "bodega": "Beringer", "tipo": "Tinto", "uva": "Cabernet Sauvignon", "popularidad": 84, "precio_aprox": 485, "perfil": "clásico americano", "maridaje_target": "Estofado de res, Quesos, Carne asada"},
    {"nombre": "Oyster Bay", "bodega": "Oyster Bay", "tipo": "Blanco", "uva": "Sauvignon Blanc", "popularidad": 82, "precio_aprox": 650, "perfil": "refrescante y tropical", "maridaje_target": "Pescados blancos, Espárragos, Ensaladas"},
    {"nombre": "Whispering Angel", "bodega": "Ch. d'Esclans", "tipo": "Rosado", "uva": "Blend Provenza", "popularidad": 87, "precio_aprox": 1100, "perfil": "fresco y seco", "maridaje_target": "Terrazas, Comida mediterránea, Mariscos"}
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