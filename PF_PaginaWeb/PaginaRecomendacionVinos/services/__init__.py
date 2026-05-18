"""Capa de servicios: lógica de negocio y motor de inferencia."""
from .fuzzy_engine import FuzzyEngine
from .recommendation_service import RecommendationService

__all__ = ["FuzzyEngine", "RecommendationService"]
