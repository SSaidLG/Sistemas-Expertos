"""
Cargador de la Base de Conocimiento.
Implementa el patrón Singleton para garantizar una sola lectura por proceso.
"""
import json
import os
from typing import Dict, List

from .wine_frame import WineFrame


class KnowledgeBase:
    """Carga, valida y expone la base de conocimiento del sistema experto.

    Está fraccionada en cuatro archivos JSON:
      - vinos.json         → Marcos de vinos
      - reglas_sabor.json  → Reglas heurísticas y pesos
      - meta.json          → Metadatos (tipos, ocasiones, climas, proteínas)
      - preguntas.json     → Esquema dinámico del cuestionario
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def __init__(self, data_dir: str = None):
        if self._loaded:
            return
        if data_dir is None:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base, "data")
        self.data_dir = data_dir
        self.vinos: List[WineFrame] = []
        self.reglas: Dict = {}
        self.meta: Dict = {}
        self.preguntas: List[Dict] = []
        self._cargar_todo()
        self._loaded = True

    # ───── Lectura de archivos JSON ─────
    def _leer_json(self, nombre: str) -> dict:
        ruta = os.path.join(self.data_dir, nombre)
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)

    def _cargar_todo(self) -> None:
        vinos_raw = self._leer_json("vinos.json")
        self.vinos = [WineFrame.from_dict(v) for v in vinos_raw]
        self.reglas = self._leer_json("reglas_sabor.json")
        self.meta = self._leer_json("meta.json")
        self.preguntas = self._leer_json("preguntas.json")["preguntas"]

    # ───── Accesores de alto nivel ─────
    def listar_vinos(self) -> List[Dict]:
        return [v.to_dict() for v in self.vinos]

    def obtener_vino(self, vino_id: str) -> WineFrame:
        for v in self.vinos:
            if v.id == vino_id:
                return v
        raise KeyError(f"Vino '{vino_id}' no encontrado en la base.")

    def regla(self, atributo: str) -> Dict:
        return self.reglas["reglas"].get(atributo, {})

    def pesos(self) -> Dict:
        return self.reglas.get("pesos_score", {})

    def tipos_disponibles(self) -> List[str]:
        return self.meta.get("tipos_vino", [])

    def ocasiones(self) -> List[Dict]:
        return self.meta.get("ocasiones", [])

    def climas(self) -> List[Dict]:
        return self.meta.get("climas", [])
