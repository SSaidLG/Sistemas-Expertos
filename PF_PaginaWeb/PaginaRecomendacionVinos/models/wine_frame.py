"""
Representación de un Vino como Marco (Frame).
Cada slot del marco corresponde a un atributo técnico o comercial del vino.
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class WineFrame:
    """Marco de conocimiento (frame) para un vino individual.

    Mantiene los slots como atributos tipados, lo que permite usar
    autocompletado, validación y serialización limpia.
    """

    id: str
    nombre: str
    bodega: str
    region: str
    pais: str
    tipo: str
    uva: str
    popularidad: int
    precio: float
    cuerpo: float
    taninos: float
    acidez: float
    dulzor: float
    alcohol: float
    maridajes: List[str] = field(default_factory=list)
    descripcion: str = ""
    imagen: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "WineFrame":
        """Crea una instancia a partir de un diccionario (JSON)."""
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            bodega=data["bodega"],
            region=data.get("region", ""),
            pais=data.get("pais", ""),
            tipo=data["tipo"],
            uva=data["uva"],
            popularidad=int(data.get("popularidad", 0)),
            precio=float(data["precio"]),
            cuerpo=float(data["cuerpo"]),
            taninos=float(data["taninos"]),
            acidez=float(data["acidez"]),
            dulzor=float(data["dulzor"]),
            alcohol=float(data.get("alcohol", 13.0)),
            maridajes=list(data.get("maridajes", [])),
            descripcion=data.get("descripcion", ""),
            imagen=data.get("imagen", ""),
        )

    def to_dict(self) -> dict:
        """Serializa el marco a diccionario plano."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "bodega": self.bodega,
            "region": self.region,
            "pais": self.pais,
            "tipo": self.tipo,
            "uva": self.uva,
            "popularidad": self.popularidad,
            "precio": self.precio,
            "cuerpo": self.cuerpo,
            "taninos": self.taninos,
            "acidez": self.acidez,
            "dulzor": self.dulzor,
            "alcohol": self.alcohol,
            "maridajes": self.maridajes,
            "descripcion": self.descripcion,
            "imagen": self.imagen,
        }
