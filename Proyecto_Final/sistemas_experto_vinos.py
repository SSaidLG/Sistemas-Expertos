import mysql.connector
import pandas as pd
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def sistema_experto():
    # Credenciales proporcionadas
    config = {
        'user': 'root',
        'password': '75891100',
        'host': '127.0.0.1',
        'database': 'SRvinos'
    }

    while True:
        limpiar_pantalla()
        print("==============================================")
        print("   SISTEMA EXPERTO DE VINOS (CDMX 2026)      ")
        print("==============================================")
        
        try:
            db = mysql.connector.connect(**config)
            query = "SELECT * FROM conocimiento_vinos"
            df = pd.read_sql(query, db)
            db.close()

            # Captura de datos del usuario
            comida = input("\n¿Qué vas a comer hoy? (ej. Pasta, Pastor, Mole): ").strip()
            while True:
                try:
                    presupuesto = float(input("¿Cuál es tu presupuesto máximo? (MXN): "))
                    break
                except ValueError:
                    print("Por favor, ingresa un número válido.")

            # Motor de Inferencia: Regla 1 (Match Directo)
            mask = (df['maridaje_target'].str.contains(comida, case=False)) & \
                   (df['precio_aprox'] <= presupuesto)
            
            candidatos = df[mask]

            print("\n----------------------------------------------")
            if not candidatos.empty:
                # Resolución de Conflictos: El más popular
                ganador = candidatos.sort_values(by='popularidad', ascending=False).iloc[0]
                print(f"¡RECOMENDACIÓN ENCONTRADA!")
                print(f"Vino: {ganador['nombre']} de la bodega {ganador['bodega']}")
                print(f"Tipo: {ganador['tipo']} ({ganador['uva']})")
                print(f"Popularidad en CDMX: {ganador['popularidad']}%")
                print(f"Precio: ${ganador['precio_aprox']} MXN")
                print(f"¿Por qué?: Porque su perfil {ganador['perfil']} va excelente con {comida}.")
            else:
                # Regla 2: Fallback (Recomendación General por presupuesto)
                print(f"No encontré un maridaje exacto para '{comida}' bajo ese precio.")
                print("Buscando el vino más popular disponible en tu rango de precio...")
                
                comodines = df[df['precio_aprox'] <= presupuesto]
                if not comodines.empty:
                    ganador = comodines.sort_values(by='popularidad', ascending=False).iloc[0]
                    print(f"\nSUGERENCIA VERSÁTIL: {ganador['nombre']} ({ganador['bodega']})")
                    print(f"Es un vino muy aceptado ({ganador['popularidad']}%) y cuesta ${ganador['precio_aprox']}.")
                else:
                    print("Lo sentimos, no hay vinos registrados con un precio tan bajo.")

            print("----------------------------------------------")
            
        except mysql.connector.Error as err:
            print(f"Error de conexión a la base de datos: {err}")
            break

        # Preguntar si desea continuar (Bucle de control)
        respuesta = input("\n¿Te gustaría otra recomendación? (s/n): ").lower().strip()
        if respuesta != 's':
            print("\n¡Gracias por usar el Sistema Experto de Vinos. Salud!")
            break

if __name__ == "__main__":
    sistema_experto()