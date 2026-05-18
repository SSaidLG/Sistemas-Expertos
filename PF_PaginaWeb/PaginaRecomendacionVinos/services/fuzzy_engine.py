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
        self.reglas = reglas["reglas"]
        self.pesos = reglas.get("pesos_score", {})

    # ───── Funciones de pertenencia ─────
    @staticmethod
    def pertenencia_presupuesto(precio: float, presupuesto: float) -> float:
        """μ_presupuesto(precio) — trapezoidal decreciente.

        1.0 cuando el precio es ≤ 80% del presupuesto, decae linealmente
        hasta 0 al alcanzar el presupuesto y se anula por encima.
        """
        if presupuesto <= 0:
            return 0.0
        if precio <= presupuesto * 0.8:
            return 1.0
        if precio <= presupuesto:
            return (presupuesto - precio) / (presupuesto * 0.2)
        return 0.0

    def perfil_ideal(self, platillo: Dict) -> Dict[str, float]:
        """Compone el perfil ideal del vino combinando los rasgos del platillo.

        Cada rasgo (picor, grasa, dulce, intensidad) aporta un grado [0,1].
        Las reglas heurísticas del JSON proporcionan el ideal por sabor.
        """
        g_pic = platillo["picor"] / 5.0
        g_gra = platillo["grasa"] / 5.0
        g_dul = platillo["dulce"] / 5.0
        g_int = platillo["intensidad"] / 5.0

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

        return {
            "acidez": min(max(id_acidez, 0.0), 1.0),
            "dulzor": min(max(id_dulzor, 0.0), 1.0),
            "taninos": min(max(id_tanino, 0.0), 1.0),
            "cuerpo": min(max(id_cuerpo, 0.0), 1.0),
        }

    def afinidad_sensorial(self, vino: WineFrame, ideal: Dict[str, float]) -> float:
        """Similitud difusa = 1 - distancia euclidiana normalizada."""
        distancia = (
            (vino.acidez - ideal["acidez"]) ** 2
            + (vino.dulzor - ideal["dulzor"]) ** 2
            + (vino.taninos - ideal["taninos"]) ** 2
            + (vino.cuerpo - ideal["cuerpo"]) ** 2
        ) ** 0.5
        return max(1.0 - (distancia / 2.0), 0.0)
