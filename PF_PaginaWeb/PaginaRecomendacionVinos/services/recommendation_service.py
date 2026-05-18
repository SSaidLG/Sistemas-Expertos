"""
Servicio orquestador (Motor de Búsqueda).
Aplica el motor de inferencia difusa a la base de hechos (KnowledgeBase)
y produce un ranking ponderado de recomendaciones.
"""
from typing import Dict, List

from models.knowledge_base import KnowledgeBase
from services.fuzzy_engine import FuzzyEngine


class RecommendationService:
    """Combina la base de conocimiento con el motor difuso."""

    def __init__(self, kb: KnowledgeBase = None):
        self.kb = kb or KnowledgeBase()
        self.engine = FuzzyEngine(self.kb.reglas)

    # ───── Pipeline principal de Evaluación ─────
    def recomendar(self, perfil_platillo: Dict, contexto: Dict) -> List[Dict]:
        """
        Ejecuta el Forward Chaining (Encadenamiento hacia adelante).
        Evalúa toda la base de vinos contra el perfil ideal y retorna el arreglo ordenado.
        """
        # 1. Deduce el perfil químico que necesita el vino para este platillo
        ideal = self.engine.perfil_ideal(perfil_platillo)
        pesos = self.kb.pesos()
        resultados = []

        for vino in self.kb.vinos:
            # Filtro booleano estricto (Poda del espacio de búsqueda)
            tipo_pref = (contexto.get("tipo_pref") or "").strip()
            if tipo_pref and vino.tipo.lower() != tipo_pref.lower():
                continue

            # Inferencia difusa al presupuesto
            mu_precio = self.engine.pertenencia_presupuesto(
                vino.precio, contexto["presupuesto"]
            )
            # Descrate temprano si el precio está totalmente fueran del rango
            if mu_precio == 0.0:
                continue

            # Bono por maridaje literal con el nombre del platillo
            nombre = (contexto.get("nombre_platillo") or "").lower()
            bono_maridaje = (
                pesos.get("maridaje_directo", 0.25)
                if any(m in nombre or nombre in m for m in vino.maridajes)
                else 0.0
            )

            # Afinidad sensorial
            mu_sensorial = self.engine.afinidad_sensorial(vino, ideal)

            # Bonos de contexto (Ocasión y Clima)
            bono_ocasion = self._bono_ocasion(vino, contexto.get("ocasion"))
            bono_clima = self._bono_clima(vino, contexto.get("clima"))

            # Score combinado, suma ponderada de todas las variables
            score = (
                mu_sensorial * pesos.get("sensorial", 0.5)
                + mu_precio * pesos.get("presupuesto", 0.2)
                + bono_maridaje
                + bono_ocasion
                + bono_clima
            )

            # Normalización del score final al 100%
            score = min(score * 100, 100.0)

            # Empaquetado del resultado con desglose de variables para la explicabilidad
            resultados.append(
                {
                    "vino": vino.to_dict(),
                    "score": round(score, 2),
                    "mu_sensorial": round(mu_sensorial, 3),
                    "mu_precio": round(mu_precio, 3),
                    "bono_maridaje": round(bono_maridaje, 3),
                    "bono_ocasion": round(bono_ocasion, 3),
                    "bono_clima": round(bono_clima, 3),
                    "perfil_ideal": ideal,
                }
            )
        # Ordenamiento descendente basado en el score final
        return sorted(resultados, key=lambda x: x["score"], reverse=True)

    # ───── Bonificaciones contextuales ─────
    def _bono_ocasion(self, vino, ocasion: str) -> float:
        """Asigna un puntaje extra basado en si el precio del vino se ajusta a la formalidad del evento."""
        if not ocasion:
            return 0.0
        for o in self.kb.ocasiones():
            if o["id"] != ocasion:
                continue
            if ocasion == "formal" and vino.precio >= o["umbral_precio"]:
                return o["bono"]
            if ocasion == "casual" and vino.precio < o["umbral_precio"]:
                return o["bono"]
            if ocasion == "moderada" and 300 <= vino.precio <= o["umbral_precio"]:
                return o["bono"]
        return 0.0

    def _bono_clima(self, vino, clima: str) -> float:
        """Asigna un puntaje extra si la temperatura de servicio del vino empata con el clima exterior."""
        if not clima:
            return 0.0
        for c in self.kb.climas():
            if c["id"] != clima:
                continue
            if vino.tipo in c.get("bono_tipos", []):
                return c.get("bono_valor", 0.0)
        return 0.0
