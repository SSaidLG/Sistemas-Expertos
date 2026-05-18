"""
Motor de Inferencia Difuso.
Implementa funciones de pertenencia y cálculo de similitud entre el
perfil del platillo y cada marco de vino.
"""
from typing import Dict

from models.wine_frame import WineFrame


class FuzzyEngine:
    """Encapsula las funciones de pertenencia y la regla de combinación."""

    def __init__(self, reglas: Dict):
        # Carga las heurísticas de cruce de sabores desde el JSON
        self.reglas = reglas["reglas"]
        self.pesos = reglas.get("pesos_score", {})

    # ───── Funciones de pertenencia ─────
    @staticmethod
    def pertenencia_presupuesto(precio: float, presupuesto: float) -> float:
    
        """
        Calcula el grado de pertenencia μ_presupuesto(precio) usando una función trapezoidal decreciente.
        
        Lógica Matemática:
        - Si el precio es <= 80% del presupuesto: μ = 1.0 (Aceptación total)
        - Si el precio está entre el 80% y el 100%: Decae linealmente de 1.0 a 0.0
        - Si supera el presupuesto: μ = 0.0 (Rechazo total)
        """
        
        if presupuesto <= 0:
            return 0.0
        if precio <= presupuesto * 0.8:
            return 1.0
        if precio <= presupuesto:
            # Ecuación de la pendiente decreciente
            return (presupuesto - precio) / (presupuesto * 0.2)
        return 0.0

    def perfil_ideal(self, platillo: Dict) -> Dict[str, float]:
        """
        Infiere el perfil enológico ideal (acidez, dulzor, taninos, cuerpo) 
        ponderando los rasgos gastronómicos del platillo de entrada.
        
        Normaliza las variables del platillo (0 a 5) a una escala difusa [0, 1]
        y aplica una suma ponderada basada en las reglas heurísticas.
        """
        # Normalizacion a rango [0,1]
        g_pic = platillo["picor"] / 5.0
        g_gra = platillo["grasa"] / 5.0
        g_dul = platillo["dulce"] / 5.0
        g_int = platillo["intensidad"] / 5.0

        # Cálculo de los atributos enológicos ideales mediante superposición de reglas
        id_acidez = (
            self.reglas["picante"]["acidez_ideal"] * g_pic
            + self.reglas["grasoso"]["acidez_ideal"] * g_gra
            + 0.5 * (1 - g_pic - g_gra)
        )
        id_dulzor = (
            self.reglas["picante"]["dulzor_ideal"] * g_pic
            + self.reglas["dulce"]["dulzor_ideal"] * g_dul
        )
        id_tanino = (
            self.reglas["grasoso"]["tanino_ideal"] * g_gra
            + self.reglas["pesado"]["tanino_ideal"] * g_int
        )
        id_cuerpo = (
            self.reglas["pesado"]["cuerpo_ideal"] * g_int
            + self.reglas["ligero"]["cuerpo_ideal"] * (1 - g_int)
        )

        # Clamping: Asegura que los valores se mantengan estrictamente en [0.0, 1.0]
        return {
            "acidez": min(max(id_acidez, 0.0), 1.0),
            "dulzor": min(max(id_dulzor, 0.0), 1.0),
            "taninos": min(max(id_tanino, 0.0), 1.0),
            "cuerpo": min(max(id_cuerpo, 0.0), 1.0),
        }

    def afinidad_sensorial(self, vino: WineFrame, ideal: Dict[str, float]) -> float:
        """
        Calcula la similitud entre el vino evaluado y el perfil ideal.
        Utiliza el complemento de la distancia euclidiana normalizada en 4D.
        Fórmula: Similitud = 1 - (Distancia_Euclidiana / Distancia_Máxima_Posible)
        """
        # Distancia euclidiana en 4 dimensiones (acidez, dulzor, taninos, cuerpo)
        distancia = (
            (vino.acidez - ideal["acidez"]) ** 2
            + (vino.dulzor - ideal["dulzor"]) ** 2
            + (vino.taninos - ideal["taninos"]) ** 2
            + (vino.cuerpo - ideal["cuerpo"]) ** 2
        ) ** 0.5
        # El divisor 2.0 asume la máxima distancia teórica en este espacio normalizado
        return max(1.0 - (distancia / 2.0), 0.0)
