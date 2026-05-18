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
import streamlit as st

# ─────────────────────────────────────────────────────────
# BASE DE CONOCIMIENTO (Marcos / Frames)
# Cada entrada es un frame con slots: nombre, bodega, tipo,
# uva, popularidad, precio_aprox, perfil, maridaje_target
# ─────────────────────────────────────────────────────────

BASE_VINOS = [
    {"nombre": "L.A. Cetto Cabernet", "bodega": "L.A. Cetto", "tipo": "Tinto", "uva": "Cabernet Sauvignon", "popularidad": 95, "precio_aprox": 210, "perfil": "tánico y robusto", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "L.A. Cetto Petite Sirah", "bodega": "L.A. Cetto", "tipo": "Tinto", "uva": "Petite Sirah", "popularidad": 90, "precio_aprox": 190, "perfil": "intenso y especiado", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Casa Madero 3V", "bodega": "Casa Madero", "tipo": "Tinto", "uva": "Blend (C-M-S)", "popularidad": 98, "precio_aprox": 550, "perfil": "elegante y equilibrado", "cuerpo": "medio", "acidez": "media", "taninos": "medios", "dulzor": "seco"},
    {"nombre": "Riunite Lambrusco", "bodega": "Riunite", "tipo": "Tinto Dulce", "uva": "Lambrusco", "popularidad": 99, "precio_aprox": 195, "perfil": "dulce y efervescente", "cuerpo": "ligero", "acidez": "media", "taninos": "bajos", "dulzor": "dulce"},
    {"nombre": "Monte Xanic V. Kristel", "bodega": "Monte Xanic", "tipo": "Blanco", "uva": "Sauvignon Blanc", "popularidad": 94, "precio_aprox": 480, "perfil": "cítrico y fresco", "cuerpo": "ligero", "acidez": "alta", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Casillero del Diablo", "bodega": "Concha y Toro", "tipo": "Tinto", "uva": "Cabernet Sauvignon", "popularidad": 96, "precio_aprox": 260, "perfil": "frutos rojos y vainilla", "cuerpo": "medio", "acidez": "media", "taninos": "medios", "dulzor": "seco"},
    {"nombre": "Santo Tomás Barbera", "bodega": "Santo Tomás", "tipo": "Tinto", "uva": "Barbera", "popularidad": 88, "precio_aprox": 490, "perfil": "ácido y frutal", "cuerpo": "medio", "acidez": "alta", "taninos": "bajos", "dulzor": "seco"},
    {"nombre": "Balero Tinto", "bodega": "Baja Wine", "tipo": "Tinto", "uva": "Blend", "popularidad": 91, "precio_aprox": 460, "perfil": "equilibrado y amigable", "cuerpo": "medio", "acidez": "media", "taninos": "medios", "dulzor": "seco"},
    {"nombre": "Las Nubes Selección T.", "bodega": "Las Nubes", "tipo": "Tinto", "uva": "Blend", "popularidad": 85, "precio_aprox": 720, "perfil": "robusto y complejo", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Mariatinto", "bodega": "Mariatinto", "tipo": "Tinto", "uva": "Blend", "popularidad": 89, "precio_aprox": 950, "perfil": "sofisticado y sedoso", "cuerpo": "medio", "acidez": "media", "taninos": "medios", "dulzor": "seco"},
    {"nombre": "Sala Vivé Brut", "bodega": "Freixenet Qro.", "tipo": "Espumoso", "uva": "Macabeo", "popularidad": 90, "precio_aprox": 360, "perfil": "burbuja fina y seco", "cuerpo": "ligero", "acidez": "alta", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Don Leo Shiraz", "bodega": "Don Leo", "tipo": "Tinto", "uva": "Shiraz", "popularidad": 84, "precio_aprox": 680, "perfil": "especiado y potente", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Corona del Valle Rosé", "bodega": "Corona del V.", "tipo": "Rosado", "uva": "Grenache", "popularidad": 82, "precio_aprox": 610, "perfil": "frutal y elegante", "cuerpo": "ligero", "acidez": "media", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Laberinto Mezcla T.", "bodega": "Cava Quintanilla", "tipo": "Tinto", "uva": "Blend", "popularidad": 80, "precio_aprox": 580, "perfil": "estructurado y mineral", "cuerpo": "medio", "acidez": "media", "taninos": "medios", "dulzor": "seco"},
    {"nombre": "Sangre de Toro", "bodega": "Torres", "tipo": "Tinto", "uva": "Garnacha-Cariñena", "popularidad": 92, "precio_aprox": 290, "perfil": "cálido y especiado", "cuerpo": "medio", "acidez": "media", "taninos": "medios", "dulzor": "seco"},
    {"nombre": "Yellow Tail Shiraz", "bodega": "Casella Family", "tipo": "Tinto", "uva": "Shiraz", "popularidad": 87, "precio_aprox": 240, "perfil": "suave y frutal", "cuerpo": "medio", "acidez": "baja", "taninos": "bajos", "dulzor": "semi-seco"},
    {"nombre": "Adobe Guadalupe Kerubiel", "bodega": "Adobe Guad.", "tipo": "Tinto", "uva": "Blend G-S-M", "popularidad": 83, "precio_aprox": 1200, "perfil": "complejo y tánico", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Pedro Domecq XA", "bodega": "Domecq", "tipo": "Tinto", "uva": "Cabernet-Grenache", "popularidad": 93, "precio_aprox": 185, "perfil": "ligero y directo", "cuerpo": "ligero", "acidez": "media", "taninos": "bajos", "dulzor": "seco"},
    {"nombre": "Ramón Bilbao Crianza", "bodega": "R. Bilbao", "tipo": "Tinto", "uva": "Tempranillo", "popularidad": 95, "precio_aprox": 460, "perfil": "clásico y equilibrado", "cuerpo": "medio", "acidez": "media", "taninos": "medios", "dulzor": "seco"},
    {"nombre": "19 Crimes Cali Red", "bodega": "19 Crimes", "tipo": "Tinto", "uva": "Blend", "popularidad": 91, "precio_aprox": 380, "perfil": "denso y dulce", "cuerpo": "robusto", "acidez": "baja", "taninos": "medios", "dulzor": "semi-seco"},
    {"nombre": "Meinklang Prosa", "bodega": "Meinklang", "tipo": "Rosado E.", "uva": "Pinot Noir", "popularidad": 78, "precio_aprox": 550, "perfil": "natural y refrescante", "cuerpo": "ligero", "acidez": "alta", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Roganto Nebbiolo", "bodega": "Roganto", "tipo": "Tinto", "uva": "Nebbiolo", "popularidad": 86, "precio_aprox": 1100, "perfil": "potente y seco", "cuerpo": "robusto", "acidez": "alta", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Santo Domingo Nebbiolo", "bodega": "Santo Domingo", "tipo": "Tinto", "uva": "Nebbiolo", "popularidad": 84, "precio_aprox": 640, "perfil": "intenso y persistente", "cuerpo": "robusto", "acidez": "alta", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Gran Ricardo", "bodega": "Monte Xanic", "tipo": "Tinto", "uva": "Blend Bordelés", "popularidad": 81, "precio_aprox": 1850, "perfil": "ícono y elegante", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Vinaltura Rosado", "bodega": "Vinaltura", "tipo": "Rosado", "uva": "Syrah", "popularidad": 85, "precio_aprox": 420, "perfil": "vibrante y floral", "cuerpo": "medio", "acidez": "media", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Tres Raíces Blanco", "bodega": "Tres Raíces", "tipo": "Blanco", "uva": "Sauvignon Blanc", "popularidad": 83, "precio_aprox": 510, "perfil": "mineral y fresco", "cuerpo": "ligero", "acidez": "alta", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Cava Maciel Venus", "bodega": "Cava Maciel", "tipo": "Tinto", "uva": "Petite Sirah", "popularidad": 79, "precio_aprox": 690, "perfil": "profundo y oscuro", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "El Cielo Selene", "bodega": "El Cielo", "tipo": "Rosado", "uva": "Grenache-Syrah", "popularidad": 90, "precio_aprox": 590, "perfil": "delicado y frutal", "cuerpo": "ligero", "acidez": "media", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Faustino VII", "bodega": "Faustino", "tipo": "Tinto", "uva": "Tempranillo", "popularidad": 92, "precio_aprox": 320, "perfil": "sedoso y frutal", "cuerpo": "medio", "acidez": "media", "taninos": "medios", "dulzor": "seco"},
    {"nombre": "Barefoot Merlot", "bodega": "Barefoot", "tipo": "Tinto", "uva": "Merlot", "popularidad": 94, "precio_aprox": 215, "perfil": "suave y versátil", "cuerpo": "medio", "acidez": "baja", "taninos": "bajos", "dulzor": "semi-seco"},
    {"nombre": "Kim Crawford", "bodega": "Constellation", "tipo": "Blanco", "uva": "Sauvignon Blanc", "popularidad": 88, "precio_aprox": 750, "perfil": "tropical y ácido", "cuerpo": "ligero", "acidez": "alta", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Espumante Puerta del Lobo", "bodega": "P. del Lobo", "tipo": "Espumoso", "uva": "Brut Nature", "popularidad": 82, "precio_aprox": 780, "perfil": "elegante y seco", "cuerpo": "medio", "acidez": "alta", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Rutini Malbec", "bodega": "Rutini", "tipo": "Tinto", "uva": "Malbec", "popularidad": 87, "precio_aprox": 850, "perfil": "estructurado y distinguido", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Luigi Bosca", "bodega": "L. Bosca", "tipo": "Tinto", "uva": "Malbec", "popularidad": 91, "precio_aprox": 620, "perfil": "clásico malbec argentino", "cuerpo": "robusto", "acidez": "media", "taninos": "medios", "dulzor": "seco"},
    {"nombre": "Alamos Malbec", "bodega": "Alamos", "tipo": "Tinto", "uva": "Malbec", "popularidad": 93, "precio_aprox": 340, "perfil": "frutal y jugoso", "cuerpo": "medio", "acidez": "media", "taninos": "medios", "dulzor": "seco"},
    {"nombre": "J.P. Chenet", "bodega": "J.P. Chenet", "tipo": "Tinto", "uva": "Cabernet-Syrah", "popularidad": 95, "precio_aprox": 235, "perfil": "fácil de beber", "cuerpo": "medio", "acidez": "media", "taninos": "medios", "dulzor": "semi-seco"},
    {"nombre": "Sutter Home White Zin", "bodega": "Sutter Home", "tipo": "Rosado", "uva": "Zinfandel", "popularidad": 96, "precio_aprox": 220, "perfil": "dulce y ligero", "cuerpo": "ligero", "acidez": "media", "taninos": "nulos", "dulzor": "dulce"},
    {"nombre": "Chateau Camou Flor de L.", "bodega": "Ch. Camou", "tipo": "Blanco", "uva": "Chardonnay", "popularidad": 81, "precio_aprox": 520, "perfil": "untuoso y floral", "cuerpo": "medio", "acidez": "media", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Único Luis Miguel", "bodega": "Ventisquero", "tipo": "Tinto", "uva": "Cabernet Sauvignon", "popularidad": 85, "precio_aprox": 795, "perfil": "intenso y apasionado", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Megacero", "bodega": "Encinillas", "tipo": "Tinto", "uva": "Blend", "popularidad": 88, "precio_aprox": 1150, "perfil": "poderoso y persistente", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Piedra Negra Alta Colecc.", "bodega": "Lurton", "tipo": "Tinto", "uva": "Malbec", "popularidad": 86, "precio_aprox": 430, "perfil": "fresco y frutal", "cuerpo": "medio", "acidez": "alta", "taninos": "medios", "dulzor": "seco"},
    {"nombre": "Evolución Chardonnay", "bodega": "Casa Madero", "tipo": "Blanco", "uva": "Chardonnay", "popularidad": 89, "precio_aprox": 415, "perfil": "fresco con madera", "cuerpo": "medio", "acidez": "media", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Mogor Badán", "bodega": "Mogor Badán", "tipo": "Tinto", "uva": "Blend Burdeos", "popularidad": 80, "precio_aprox": 1250, "perfil": "tradicional y complejo", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Bruma Plan B Tinto", "bodega": "Bruma", "tipo": "Tinto", "uva": "Blend", "popularidad": 84, "precio_aprox": 590, "perfil": "moderno y directo", "cuerpo": "medio", "acidez": "media", "taninos": "medios", "dulzor": "seco"},
    {"nombre": "Henri Lurton Chenin", "bodega": "Bodegas HL", "tipo": "Blanco", "uva": "Chenin Blanc", "popularidad": 82, "precio_aprox": 670, "perfil": "aromático y vivaz", "cuerpo": "ligero", "acidez": "alta", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Solar Fortún Syrah", "bodega": "Solar Fortún", "tipo": "Tinto", "uva": "Syrah", "popularidad": 81, "precio_aprox": 745, "perfil": "especiado y ahumado", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Cuatro Soles", "bodega": "Valle Redondo", "tipo": "Tinto", "uva": "Cabernet Sauvignon", "popularidad": 97, "precio_aprox": 125, "perfil": "ligero y afrutado", "cuerpo": "ligero", "acidez": "baja", "taninos": "bajos", "dulzor": "semi-seco"},
    {"nombre": "Reservado Concha y Toro", "bodega": "Concha y Toro", "tipo": "Tinto", "uva": "Merlot", "popularidad": 98, "precio_aprox": 165, "perfil": "suave y confiable", "cuerpo": "medio", "acidez": "baja", "taninos": "bajos", "dulzor": "seco"},
    {"nombre": "Veuve Clicquot", "bodega": "LVMH", "tipo": "Espumoso", "uva": "Champagne", "popularidad": 89, "precio_aprox": 1950, "perfil": "lujo y estructura", "cuerpo": "medio", "acidez": "alta", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Moët & Chandon", "bodega": "LVMH", "tipo": "Espumoso", "uva": "Champagne", "popularidad": 92, "precio_aprox": 1780, "perfil": "clásico y brillante", "cuerpo": "ligero", "acidez": "alta", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Prosecco Zonin", "bodega": "Zonin", "tipo": "Espumoso", "uva": "Glera", "popularidad": 94, "precio_aprox": 390, "perfil": "fresco y amigable", "cuerpo": "ligero", "acidez": "alta", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Apothic Red", "bodega": "Apothic", "tipo": "Tinto", "uva": "Blend", "popularidad": 91, "precio_aprox": 450, "perfil": "intenso y chocolate", "cuerpo": "robusto", "acidez": "baja", "taninos": "medios", "dulzor": "semi-seco"},
    {"nombre": "Menade Nosso", "bodega": "Menade", "tipo": "Blanco", "uva": "Verdejo", "popularidad": 77, "precio_aprox": 680, "perfil": "ecológico y puro", "cuerpo": "medio", "acidez": "alta", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Flor de Pingus", "bodega": "Dominio de Pingus", "tipo": "Tinto", "uva": "Tempranillo", "popularidad": 75, "precio_aprox": 2900, "perfil": "exclusivo y potente", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Pruno", "bodega": "Finca Villacreces", "tipo": "Tinto", "uva": "Tempranillo", "popularidad": 88, "precio_aprox": 655, "perfil": "fruta negra y roble", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Montes Alpha", "bodega": "Montes", "tipo": "Tinto", "uva": "Cabernet Sauvignon", "popularidad": 86, "precio_aprox": 695, "perfil": "robusto y clásico", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Errázuriz Max", "bodega": "Errázuriz", "tipo": "Tinto", "uva": "Carmenere", "popularidad": 83, "precio_aprox": 585, "perfil": "terroso y especiado", "cuerpo": "medio", "acidez": "baja", "taninos": "medios", "dulzor": "seco"},
    {"nombre": "Kaiken Ultra", "bodega": "Kaiken", "tipo": "Tinto", "uva": "Malbec", "popularidad": 85, "precio_aprox": 595, "perfil": "elegante y floral", "cuerpo": "robusto", "acidez": "media", "taninos": "altos", "dulzor": "seco"},
    {"nombre": "Beringer Founders Est.", "bodega": "Beringer", "tipo": "Tinto", "uva": "Cabernet Sauvignon", "popularidad": 84, "precio_aprox": 485, "perfil": "clásico americano", "cuerpo": "medio", "acidez": "media", "taninos": "medios", "dulzor": "seco"},
    {"nombre": "Oyster Bay", "bodega": "Oyster Bay", "tipo": "Blanco", "uva": "Sauvignon Blanc", "popularidad": 82, "precio_aprox": 650, "perfil": "refrescante y tropical", "cuerpo": "ligero", "acidez": "alta", "taninos": "nulos", "dulzor": "seco"},
    {"nombre": "Whispering Angel", "bodega": "Ch. d'Esclans", "tipo": "Rosado", "uva": "Blend Provenza", "popularidad": 87, "precio_aprox": 1100, "perfil": "fresco y seco", "cuerpo": "ligero", "acidez": "alta", "taninos": "nulos", "dulzor": "seco"}
]


# ─────────────────────────────────────────────────────────
# 2. MOTOR DE INFERENCIA (Scoring y Lógica Difusa)
# ─────────────────────────────────────────────────────────
def evaluar_vinos(proteina, preparacion, clima, presupuesto):
    resultados = []
    
    for vino in BASE_VINOS:
        score = 0
        justificacion = []
        alerta_difusa = False
        
        # --- REGLA 1: Match de Proteína (Taninos y Cuerpo) ---
        if proteina == "Carnes Rojas (Res, Borrego)":
            if vino["taninos"] in ["altos", "medios"]: score += 30; justificacion.append("Sus taninos limpian la proteína de la carne.")
            if vino["cuerpo"] == "robusto": score += 20; justificacion.append("Tiene el cuerpo suficiente para soportar el peso del platillo.")
        
        elif proteina == "Carnes Blancas (Pollo, Cerdo)":
            if vino["cuerpo"] == "medio": score += 20; justificacion.append("Cuerpo medio ideal para no opacar la carne blanca.")
            if vino["acidez"] in ["media", "alta"]: score += 15
            
        elif proteina == "Pescados y Mariscos":
            if vino["taninos"] == "nulos": score += 30; justificacion.append("No tiene taninos, evitando el sabor metálico con los mariscos.")
            if vino["acidez"] == "alta": score += 20; justificacion.append("Su alta acidez aporta frescura, actuando como un 'limón' en el platillo.")
            
        elif proteina == "Vegetariano / Pastas":
            if vino["cuerpo"] in ["ligero", "medio"]: score += 20; justificacion.append("Cuerpo amigable que respeta los sabores vegetales.")

        # --- REGLA 2: Match de Preparación (Grasa, Especias y Dulzor) ---
        if preparacion == "A la parrilla / Asado":
            if vino["cuerpo"] == "robusto": score += 15; justificacion.append("Hace sinergia con los tonos ahumados del asado.")
        elif preparacion == "Picante / Especiado":
            if vino["dulzor"] in ["dulce", "semi-seco"]: score += 25; justificacion.append("Su ligero dulzor ayuda a apagar el fuego del picante.")
            if vino["tipo"] in ["Rosado", "Blanco"]: score += 10
        elif preparacion == "Salsas cremosas / Quesos":
            if vino["acidez"] == "alta": score += 25; justificacion.append("La acidez corta perfectamente la grasa de la crema/queso.")
        elif preparacion == "Fresco / Crudo (Ceviches)":
            if vino["tipo"] in ["Blanco", "Espumoso"]: score += 20; justificacion.append("Estilo refrescante perfecto para platillos crudos.")

        # --- REGLA 3: Contexto / Clima ---
        if clima == "Día caluroso / Terraza":
            if vino["tipo"] in ["Blanco", "Rosado", "Espumoso"]: score += 15; justificacion.append("Temperatura de servicio fría, ideal para el clima.")
        elif clima == "Noche fría / Lluvia":
            if vino["tipo"] == "Tinto": score += 15; justificacion.append("Vino tinto cálido, perfecto para una noche fría.")
            
        # --- REGLA 4: Presupuesto y Lógica Difusa ---
        diferencia_precio = vino["precio_aprox"] - presupuesto
        
        if diferencia_precio <= 0:
            score += 20 # Bonificación por estar en presupuesto
            justificacion.append("Se ajusta perfectamente a tu presupuesto.")
        elif 0 < diferencia_precio <= 100:
            score -= 10 # Penalización leve (Lógica Difusa)
            alerta_difusa = True
            justificacion.append(f"Excede tu presupuesto por ${diferencia_precio} MXN, pero la compatibilidad lo vale.")
        else:
            score -= 500 # Descarte técnico por pasarse demasiado
            
        # --- REGLA 5: Desempate por Popularidad ---
        score += (vino["popularidad"] / 10) # Suma de 7 a 9.9 puntos
        
        # Guardar si tiene un score aceptable
        if score > 0:
            resultados.append({
                "vino": vino,
                "score": round(score, 1),
                "justificacion": list(set(justificacion)), # Eliminar duplicados
                "alerta_difusa": alerta_difusa
            })
            
    # Ordenar de mayor a menor score
    resultados_ordenados = sorted(resultados, key=lambda x: x["score"], reverse=True)
    return resultados_ordenados[:3] # Retornar el Top 3

# ─────────────────────────────────────────────────────────
# 3. INTERFAZ GRÁFICA (Frontend Minimalista)
# ─────────────────────────────────────────────────────────
st.set_page_config(page_title="Sommelier Virtual CDMX", page_icon="🍷", layout="centered")

st.title("🍷 Sommelier Virtual CDMX")
st.markdown("Sistema Experto de recomendaciones enológicas mediante inferencia heurística.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Tu Platillo")
    proteina = st.selectbox("Ingrediente Principal:", [
        "Carnes Rojas (Res, Borrego)", 
        "Carnes Blancas (Pollo, Cerdo)", 
        "Pescados y Mariscos", 
        "Vegetariano / Pastas"
    ])
    
    preparacion = st.selectbox("Tipo de Preparación:", [
        "A la parrilla / Asado", 
        "Salsas cremosas / Quesos", 
        "Picante / Especiado", 
        "Fresco / Crudo (Ceviches)",
        "Guisos / Estofados"
    ])

with col2:
    st.subheader("2. Tu Contexto")
    clima = st.selectbox("Momento o Clima:", [
        "Día caluroso / Terraza", 
        "Noche fría / Lluvia", 
        "Cena interior casual"
    ])
    
    presupuesto = st.slider("Presupuesto Máximo (MXN):", min_value=150, max_value=2500, value=500, step=50)

st.divider()
submit = st.button("Recomendar Vinos 🍇", type="primary", use_container_width=True)

# ─────────────────────────────────────────────────────────
# 4. EJECUCIÓN Y RESULTADOS
# ─────────────────────────────────────────────────────────
if submit:
    top_3 = evaluar_vinos(proteina, preparacion, clima, presupuesto)
    
    if not top_3:
        st.error("No encontré vinos que se ajusten a ese nivel de presupuesto y exigencia. ¡Intenta subir el presupuesto!")
    else:
        st.success("¡He analizado la base de conocimiento! Aquí tienes mi Top 3:")
        
        for i, recomendacion in enumerate(top_3, 1):
            vino = recomendacion["vino"]
            
            with st.container(border=True):
                st.subheader(f"#{i} - {vino['nombre']}")
                
                # Alerta si se aplicó lógica difusa
                if recomendacion["alerta_difusa"]:
                    st.warning(f"⚠️ **Sobre Presupuesto:** Este vino cuesta **${vino['precio_aprox']} MXN**, superando tu límite por poco, pero su perfil es ideal para tu platillo.")
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Precio", f"${vino['precio_aprox']} MXN")
                c2.metric("Tipo", f"{vino['tipo']} ({vino['uva']})")
                c3.metric("Match", f"{min(recomendacion['score'], 100)}%")
                
                st.markdown("**¿Por qué lo recomiendo? (Traza de Inferencia):**")
                for just in recomendacion["justificacion"]:
                    st.markdown(f"- *{just}*")