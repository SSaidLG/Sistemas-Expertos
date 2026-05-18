"""
SISTEMA EXPERTO DIFUSO DE RECOMENDACIÓN DE VINOS — CDMX 2026
===========================================================
Representación del conocimiento avanzada:
  - Marcos (Frames): Vinos con slots técnicos y comerciales.
  - Múltiples Bases de Conocimiento: Separación de Vinos, Platillos y Reglas.
  - Motor de Inferencia con Lógica Difusa: Funciones de pertenencia híbridas
    (trapezoidales/lineales) para Presupuesto, Picor, Grasa y Complejidad.
  - Interfaz extendida: Cuestionario analítico de 10 variables.

Standalone — Sin dependencias externas.
"""

import os

# ─────────────────────────────────────────────────────────
# 1. BASES DE CONOCIMIENTO (BC)
# ─────────────────────────────────────────────────────────

# BC 1: MARCOS DE VINOS (Slots con descriptores difusos y numéricos)
BC_VINOS = [
    {"nombre": "L.A. Cetto Cabernet", "bodega": "L.A. Cetto", "tipo": "Tinto", "uva": "Cabernet Sauvignon", "popularidad": 95, "precio": 210, "cuerpo": 0.8, "taninos": 0.9, "acidez": 0.5, "dulzor": 0.1, "maridajes": ["carne asada", "pasta", "mole", "carnitas", "pizza", "hamburguesa"]},
    {"nombre": "L.A. Cetto Petite Sirah", "bodega": "L.A. Cetto", "tipo": "Tinto", "uva": "Petite Sirah", "popularidad": 90, "precio": 190, "cuerpo": 0.9, "taninos": 0.8, "acidez": 0.4, "dulzor": 0.2, "maridajes": ["birria", "carnitas", "carne asada", "tacos al pastor", "chorizo"]},
    {"nombre": "Casa Madero 3V", "bodega": "Casa Madero", "tipo": "Tinto", "uva": "Blend (C-M-S)", "popularidad": 98, "precio": 550, "cuerpo": 0.7, "taninos": 0.7, "acidez": 0.6, "dulzor": 0.1, "maridajes": ["mole", "pato", "cordero", "cortes finos", "quesos maduros"]},
    {"nombre": "Riunite Lambrusco", "bodega": "Riunite", "tipo": "Tinto Dulce", "uva": "Lambrusco", "popularidad": 99, "precio": 195, "cuerpo": 0.3, "taninos": 0.1, "acidez": 0.6, "dulzor": 0.9, "maridajes": ["pizza", "sushi", "pasta", "postres", "picante", "alitas"]},
    {"nombre": "Monte Xanic V. Kristel", "bodega": "Monte Xanic", "tipo": "Blanco", "uva": "Sauvignon Blanc", "popularidad": 94, "precio": 480, "cuerpo": 0.4, "taninos": 0.0, "acidez": 0.9, "dulzor": 0.1, "maridajes": ["mariscos", "ensaladas", "ceviche", "pescado blanco"]},
    {"nombre": "Casillero del Diablo", "bodega": "Concha y Toro", "tipo": "Tinto", "uva": "Cabernet Sauvignon", "popularidad": 96, "precio": 260, "cuerpo": 0.7, "taninos": 0.7, "acidez": 0.5, "dulzor": 0.2, "maridajes": ["hamburguesas", "quesos", "pizza", "carne asada"]},
    {"nombre": "Santo Tomás Barbera", "bodega": "Santo Tomás", "tipo": "Tinto", "uva": "Barbera", "popularidad": 88, "precio": 490, "cuerpo": 0.6, "taninos": 0.6, "acidez": 0.8, "dulzor": 0.2, "maridajes": ["pastas", "lasagna", "ensalada", "pizza"]},
    {"nombre": "Balero Tinto", "bodega": "Baja Wine", "tipo": "Tinto", "uva": "Blend", "popularidad": 91, "precio": 460, "cuerpo": 0.6, "taninos": 0.5, "acidez": 0.6, "dulzor": 0.2, "maridajes": ["tacos de guisado", "carnitas", "tacos al pastor"]},
    {"nombre": "Mariatinto", "bodega": "Mariatinto", "tipo": "Tinto", "uva": "Blend", "popularidad": 89, "precio": 950, "cuerpo": 0.8, "taninos": 0.7, "acidez": 0.5, "dulzor": 0.1, "maridajes": ["alta cocina mexicana", "mole negro", "pato"]},
    {"nombre": "Sala Vivé Brut", "bodega": "Freixenet Qro.", "tipo": "Espumoso", "uva": "Macabeo", "popularidad": 90, "precio": 360, "cuerpo": 0.4, "taninos": 0.0, "acidez": 0.8, "dulzor": 0.2, "maridajes": ["chiles en nogada", "postres", "mariscos", "sushi"]},
    {"nombre": "Corona del Valle Rosé", "bodega": "Corona del V.", "tipo": "Rosado", "uva": "Grenache", "popularidad": 82, "precio": 610, "cuerpo": 0.4, "taninos": 0.1, "acidez": 0.7, "dulzor": 0.3, "maridajes": ["sushi", "paella", "mariscos", "ensaladas"]},
    {"nombre": "Sangre de Toro", "bodega": "Torres", "tipo": "Tinto", "uva": "Garnacha-Cariñena", "popularidad": 92, "precio": 290, "cuerpo": 0.6, "taninos": 0.5, "acidez": 0.5, "dulzor": 0.2, "maridajes": ["tapas", "embutidos", "carnitas", "cordero"]},
    {"nombre": "Pedro Domecq XA", "bodega": "Domecq", "tipo": "Tinto", "uva": "Cabernet-Grenache", "popularidad": 93, "precio": 185, "cuerpo": 0.4, "taninos": 0.4, "acidez": 0.5, "dulzor": 0.3, "maridajes": ["tacos de canasta", "comida diaria", "quesadillas"]},
    {"nombre": "Gran Ricardo", "bodega": "Monte Xanic", "tipo": "Tinto", "uva": "Blend Bordelés", "popularidad": 81, "precio": 1850, "cuerpo": 0.9, "taninos": 0.9, "acidez": 0.6, "dulzor": 0.1, "maridajes": ["cena de gala", "cortes wagyu", "quesos premium", "cortes finos"]},
    {"nombre": "Vinaltura Rosado", "bodega": "Vinaltura", "tipo": "Rosado", "uva": "Syrah", "popularidad": 85, "precio": 420, "cuerpo": 0.5, "taninos": 0.2, "acidez": 0.7, "dulzor": 0.2, "maridajes": ["cochinita pibil", "pozole", "sushi", "chiles en nogada"]},
    {"nombre": "Sutter Home White Zin", "bodega": "Sutter Home", "tipo": "Rosado", "uva": "Zinfandel", "popularidad": 96, "precio": 220, "cuerpo": 0.3, "taninos": 0.0, "acidez": 0.5, "dulzor": 0.8, "maridajes": ["comida picante", "postres", "fruta", "alitas"]}
]

# BC 2: MATRIZ DE AFINIDAD DE SABORES ELEMENTALES (Reglas heurísticas implícitas)
BC_REGLAS_SABOR = {
    "picante":   {"acidez_ideal": 0.7, "dulzor_ideal": 0.8, "tanino_ideal": 0.1, "cuerpo_ideal": 0.4},
    "grasoso":   {"acidez_ideal": 0.8, "dulzor_ideal": 0.2, "tanino_ideal": 0.8, "cuerpo_ideal": 0.8},
    "dulce":     {"acidez_ideal": 0.5, "dulzor_ideal": 0.9, "tanino_ideal": 0.1, "cuerpo_ideal": 0.5},
    "acido":     {"acidez_ideal": 0.4, "dulzor_ideal": 0.4, "tanino_ideal": 0.3, "cuerpo_ideal": 0.5},
    "ligero":    {"acidez_ideal": 0.7, "dulzor_ideal": 0.3, "tanino_ideal": 0.2, "cuerpo_ideal": 0.3},
    "pesado":    {"acidez_ideal": 0.5, "dulzor_ideal": 0.1, "tanino_ideal": 0.8, "cuerpo_ideal": 0.9}
}


# ─────────────────────────────────────────────────────────
# 2. MOTOR DE INFERENCIA DIFUSO (Fuzzy Inference Engine)
# ─────────────────────────────────────────────────────────

def pertenencia_presupuesto(precio_vino: float, presupuesto_max: float) -> float:
    """Función de pertenencia difusa: evalúa qué tan aceptable es el precio."""
    if precio_vino <= presupuesto_max * 0.8:
        return 1.0  # Plenamente económico/adecuado
    elif precio_vino <= presupuesto_max:
        # Decremento lineal conforme se acerca al límite
        return (presupuesto_max - precio_vino) / (presupuesto_max * 0.2)
    else:
        return 0.0  # Fuera de presupuesto totalmente


def evaluar_afinidad_difusa(vino: dict, perfil_platillo: dict) -> float:
    """
    Calcula el grado de idoneidad empleando distancias difusas normadas.
    Retorna un valor en el intervalo [0, 1].
    """
    # Determinar el perfil ideal combinando los rasgos del platillo
    g_picante = perfil_platillo["picor"] / 5.0
    g_grasa = perfil_platillo["grasa"] / 5.0
    g_intensidad = perfil_platillo["intensidad"] / 5.0
    
    # Pesos por defecto basados en las respuestas dominantes
    id_acidez = (BC_REGLAS_SABOR["picante"]["acidez_ideal"] * g_picante + 
                 BC_REGLAS_SABOR["grasoso"]["acidez_ideal"] * g_grasa +
                 0.5 * (1 - g_picante - g_grasa))
                 
    id_dulzor = (BC_REGLAS_SABOR["picante"]["dulzor_ideal"] * g_picante + 
                 BC_REGLAS_SABOR["dulce"]["dulzor_ideal"] * (perfil_platillo["dulce"]/5.0))
                 
    id_tanino = (BC_REGLAS_SABOR["grasoso"]["tanino_ideal"] * g_grasa + 
                 BC_REGLAS_SABOR["pesado"]["tanino_ideal"] * g_intensidad)

    id_cuerpo = (BC_REGLAS_SABOR["pesado"]["cuerpo_ideal"] * g_intensidad + 
                 BC_REGLAS_SABOR["ligero"]["cuerpo_ideal"] * (1 - g_intensidad))

    # Limitar los ideales entre [0, 1]
    id_acidez = min(max(id_acidez, 0.0), 1.0)
    id_dulzor = min(max(id_dulzor, 0.0), 1.0)
    id_tanino = min(max(id_tanino, 0.0), 1.0)
    id_cuerpo = min(max(id_cuerpo, 0.0), 1.0)

    # Distancia Euclidiana ponderada invertida para obtener la pertenencia
    distancia = (
        (vino["acidez"] - id_acidez) ** 2 +
        (vino["dulzor"] - id_dulzor) ** 2 +
        (vino["taninos"] - id_tanino) ** 2 +
        (vino["cuerpo"] - id_cuerpo) ** 2
    ) ** 0.5

    # Retornamos la similitud (1 - distancia normalizada)
    similitud = max(1.0 - (distancia / 2.0), 0.0)
    return similitud


def motor_inferencia_difuso(perfil_platillo: dict, contextuales: dict) -> list:
    """
    Cruza la información recolectada aplicando fusificación del presupuesto y
    del perfil gustativo, retornando los vinos ordenados por Score Difuso.
    """
    resultados = []
    
    for vino in BC_VINOS:
        # 1. Validación estricta / filtro preliminar por tipo si el usuario lo forzó
        if contextuales["tipo_pref"] and vino["tipo"].lower() != contextuales["tipo_pref"].lower():
            continue
            
        # 2. Pertenencia Difusa de Presupuesto
        mu_presupuesto = pertenencia_presupuesto(vino["precio"], contextuales["presupuesto"])
        if mu_presupuesto == 0.0:
            continue  # Completamente inaccesible
            
        # 3. Pertenencia Difusa por Maridaje de String (Bono de compatibilidad directa)
        bono_maridaje = 0.25 if contextuales["nombre_platillo"].lower() in vino["maridajes"] else 0.0
        
        # 4. Idoneidad Química / Sensorial
        mu_sensorial = evaluar_afinidad_difusa(vino, perfil_platillo)
        
        # 5. Modificadores Contextuales (Ocasión y Temperatura)
        bono_ocasion = 0.0
        if contextuales["ocasion"] == "formal" and vino["precio"] >= 500:
            bono_ocasion = 0.15
        elif contextuales["ocasion"] == "casual" and vino["precio"] < 400:
            bono_ocasion = 0.10
            
        bono_clima = 0.0
        if contextuales["clima"] == "calor" and vino["tipo"] in ["Blanco", "Rosado", "Espumoso"]:
            bono_clima = 0.15

        # Cálculo del Score Difuso Integrado
        score_final = (mu_sensorial * 0.5) + (mu_presupuesto * 0.2) + bono_maridaje + bono_ocasion + bono_clima
        score_final = min(score_final * 100, 100.0) # Escala a 100%

        resultados.append({
            "vino": vino,
            "score": round(score_final, 2),
            "mu_sensorial": round(mu_sensorial, 2),
            "mu_precio": round(mu_presupuesto, 2)
        })

    # Ordenar de mayor a menor puntuación
    return sorted(resultados, key=lambda x: x["score"], reverse=True)


# ─────────────────────────────────────────────────────────
# 3. INTERFAZ DE USUARIO Y CUESTIONARIO (10 PREGUNTAS)
# ─────────────────────────────────────────────────────────

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def pedir_escala(pregunta: str, min_val: int = 1, max_val: int = 5) -> int:
    while True:
        try:
            res = int(input(f"  {pregunta} ({min_val}-{max_val}): "))
            if min_val <= res <= max_val:
                return res
            print(f"   Por favor introduce un número entre {min_val} y {max_val}.")
        except ValueError:
            print("   Entrada inválida. Digita un número entero.")


def ejecutar_cuestionario():
    limpiar()
    print("=" * 60)
    print("   FORMULARIO DE CARACTERIZACIÓN DEL PLATILLO (10 Preguntas)")
    print("=" * 60)
    
    # 1. Identificación básica
    nombre_platillo = input("\n  1. ¿Qué platillo vas a consumir? (ej. Tacos al Pastor, Mole): ").strip()
    
    # 2. Presupuesto
    while True:
        try:
            presupuesto = float(input("  2. ¿Cuál es tu presupuesto máximo en MXN?: $"))
            break
        except ValueError:
            print("   Introduce un monto numérico válido.")

    # 3. Tipo Preferido
    tipo_pref = input("  3. ¿Deseas algún tipo en específico? (Tinto/Blanco/Rosado/Espumoso o Enter): ").strip()
    
    print("\n  --- Perfil de Sabores del Platillo ---")
    # 4. Picor
    picor = pedir_escala("4. ¿Qué tan picante es el platillo? (1: Nada - 5: Extremo)")
    # 5. Grasa
    grasa = pedir_escala("5. ¿Qué tanta grasa/aceite/densidad tiene? (1: Muy ligero - 5: Muy grasoso/pesado)")
    # 6. Dulzor
    dulce = pedir_escala("6. ¿Tiene matices dulces o agridulces? (1: Nada dulce - 5: Muy dulce)")
    # 7. Intensidad general
    intensidad = pedir_escala("7. Complejidad/Intensidad de las especias (1: Suave/Plano - 5: Muy condimentado)")
    
    print("\n  --- Factores Contextuales ---")
    # 8. Proteína principal
    print("  8. Proteína predominante:")
    print("     [1] Carnes Rojas/Caza  [2] Cerdo/Aves  [3] Pescados/Mariscos  [4] Vegetales/Ninguna")
    prot_opc = pedir_escala("Selecciona una opción", 1, 4)
    
    # 9. Ocasión
    print("  9. Tipo de evento u ocasión:")
    print("     [1] Casual/Uso diario  [2] Reunión/Cena especial  [3] Gala/Celebración premium")
    oc_opc = pedir_escala("Selecciona una opción", 1, 3)
    map_ocasion = {1: "casual", 2: "moderada", 3: "formal"}

    # 10. Clima / Entorno
    print("  10. Sensación térmica del entorno:")
    print("     [1] Templado/Fresco  [2] Mucho Calor (ideal para vinos refrescantes)")
    clima_opc = pedir_escala("Selecciona una opción", 1, 2)
    map_clima = {1: "fresco", 2: "calor"}

    # Empaquetado de estructuras de conocimiento temporal
    perfil_platillo = {
        "picor": picor,
        "grasa": grasa,
        "dulce": dulce,
        "intensidad": intensidad,
        "proteina": prot_opc
    }
    
    contextuales = {
        "nombre_platillo": nombre_platillo,
        "presupuesto": presupuesto,
        "tipo_pref": tipo_pref,
        "ocasion": map_ocasion[oc_opc],
        "clima": map_clima[clima_opc]
    }
    
    return perfil_platillo, contextuales


def mostrar_barra(porcentaje: float, largo: int = 20) -> str:
    llenos = int((porcentaje / 100) * largo)
    return "█" * llenos + "░" * (largo - llenos)


def desplegar_menu():
    while True:
        limpiar()
        print("=" * 60)
        print("   SISTEMA EXPERTO DE MARIDAJE CON LÓGICA DIFUSA — CDMX")
        print("=" * 60)
        print("\n  [1] Ejecutar test de maridaje difuso (10 preguntas)")
        print("  [2] Auditar Base de Conocimiento (Ver Vinos)")
        print("  [3] Salir")
        
        opc = input("\n  Selecciona una opción: ").strip()
        
        if opc == "3":
            print("\n  ¡Salud! Que disfrutes tu maridaje. 🍷\n")
            break
            
        elif opc == "2":
            limpiar()
            print("\n  --- BASE DE CONOCIMIENTO (Frames de Vinos Disponibles) ---\n")
            for i, v in enumerate(BC_VINOS, 1):
                print(f"  {i:2}. {v['nombre']:<28} | {v['tipo']:<10} | ${v['precio']:>4} MXN | Pop: {v['popularidad']}%")
            input("\n  Presiona Enter para regresar al menú...")
            
        elif opc == "1":
            perfil, contexto = ejecutar_cuestionario()
            vinos_recomendados = motor_inferencia_difuso(perfil, contexto)
            
            limpiar()
            print("=" * 60)
            print(f"  RESULTADOS DEL MARIDAJE DIFUSO PARA: {contexto['nombre_platillo'].upper()}")
            print("=" * 60)
            
            if not vinos_recomendados:
                print("\n   El motor de inferencia determinó conjunto vacío.")
                print("     Ningún vino cumple el criterio de presupuesto o tipo seleccionado.")
            else:
                print("\n  Top de recomendaciones óptimas encontradas:")
                # Desplegar los 3 mejores resultados si existen
                for idx, item in enumerate(vinos_recomendados[:3], 1):
                    v = item["vino"]
                    print(f"\n   [{idx}] {v['nombre']} ({v['bodega']})")
                    print(f"      Tipo: {v['tipo']} | Uva: {v['uva']} | Precio: ${v['precio']} MXN")
                    print(f"      Compatibilidad General: {mostrar_barra(item['score'])} {item['score']}%")
                    print(f"      [Grado de Verdad Sensorial: {item['mu_sensorial']} | Ajuste de Precio: {item['mu_precio']}]")
                    print(f"      Perfil del vino: Cuerpo: {v['cuerpo']}, Taninos: {v['taninos']}, Acidez: {v['acidez']}, Dulzor: {v['dulzor']}")
            
            input("\n  Presiona Enter para volver al menú principal...")


if __name__ == "__main__":
    desplegar_menu()