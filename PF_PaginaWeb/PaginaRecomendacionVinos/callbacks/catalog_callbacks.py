"""
Callback del catálogo: filtra las tarjetas por tipo y precio máximo.
"""
from dash import Input, Output, callback

from models.knowledge_base import KnowledgeBase
from views.components.wine_card import build_wine_card


_kb = KnowledgeBase()


@callback(
    Output("catalogo-grid", "children"),
    Output("catalog-count", "children"),
    Input("cat-filter-tipo", "value"),
    Input("cat-filter-precio", "value"),
)
def filtrar_catalogo(tipo, precio_max):
    filtrados = []
    for v in _kb.vinos:
        if tipo and tipo != "Todos" and v.tipo != tipo:
            continue
        if precio_max and v.precio > precio_max:
            continue
        filtrados.append(v)

    cards = [build_wine_card(v.to_dict()) for v in filtrados]
    contador = (
        f"Mostrando {len(filtrados)} de {len(_kb.vinos)} vinos."
        if filtrados
        else "Ningún vino cumple con los filtros. Ajusta los controles."
    )
    return cards, contador
