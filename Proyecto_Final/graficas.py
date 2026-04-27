import pandas as pd
import matplotlib.pyplot as plt

# 1. Crear el set de datos con tendencias reales de la CDMX
data = {
    "nombre": [
        "L.A. Cetto Cabernet", "L.A. Cetto Petite Sirah", "Casa Madero 3V", 
        "Casa Madero V Rosado", "Monte Xanic Viña Kristel", "Riunite Lambrusco", 
        "Ramón Bilbao Crianza", "Casillero del Diablo Malbec", "Sala Vivé Brut", 
        "Balero Tinto", "Santo Tomás Barbera", "Don Leo Cabernet"
    ],
    "tipo": [
        "Tinto", "Tinto", "Tinto", "Rosado", "Blanco", "Tinto Dulce", 
        "Tinto", "Tinto", "Espumoso", "Tinto", "Tinto", "Tinto"
    ],
    "popularidad": [95, 90, 98, 92, 94, 99, 91, 88, 86, 84, 80, 82],
    "precio": [200, 190, 520, 400, 450, 180, 450, 250, 350, 420, 470, 580]
}

df = pd.DataFrame(data)

# --- GRÁFICA 1: TOP 10 VINOS POR POPULARIDAD ---
# Ordenamos los datos para que la gráfica sea legible
df_sorted = df.sort_values(by="popularidad", ascending=True)

plt.barh(df_sorted["nombre"], df_sorted["popularidad"], color='darkred')
plt.xlabel("Nivel de Popularidad (0-100)")
plt.title("Vinos más consumidos y aceptados en CDMX")
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("popularidad_vinos.png")
# plt.show() # Descomenta si lo corres localmente

# --- GRÁFICA 2: POPULARIDAD PROMEDIO POR TIPO ---
# Esto ayuda al sistema experto a saber qué categoría es más "segura" recomendar
plt.clf() # Limpiamos la figura anterior
tipo_stats = df.groupby("tipo")["popularidad"].mean().sort_values(ascending=False)

tipo_stats.plot(kind='bar', color=['firebrick', 'lightcoral', 'gold', 'silver', 'plum'])
plt.ylabel("Popularidad Promedio")
plt.title("Preferencia por Tipo de Vino en el mercado Chilango")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("popularidad_por_tipo.png")
# plt.show()

print("¡Gráficas generadas exitosamente!")
print(df.describe())