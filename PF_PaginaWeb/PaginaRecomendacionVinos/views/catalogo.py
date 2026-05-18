"""
Catálogo navegable de la base de conocimiento.
Permite filtrar por tipo y rango de precio.
"""
from dash import html, dcc, register_page

from models.knowledge_base import KnowledgeBase
from views.components.navbar import build_navbar
from views.components.wine_card import build_wine_card


_kb = KnowledgeBase()


def _filter_bar():
    tipos = ["Todos"] + _kb.tipos_disponibles()
    return html.Div(
        className="filter-bar",
        children=[
            html.Div(
                className="filter-group",
                children=[
                    html.Label("Tipo", className="filter-label"),
                    dcc.Dropdown(
                        id="cat-filter-tipo",
                        options=[{"label": t, "value": t} for t in tipos],
                        value="Todos",
                        clearable=False,
                        className="dropdown",
                    ),
                ],
            ),
            html.Div(
                className="filter-group filter-group-wide",
                children=[
                    html.Label("Precio máximo", className="filter-label"),
                    dcc.Slider(
                        id="cat-filter-precio",
                        min=150,
                        max=2000,
                        step=50,
                        value=2000,
                        marks={
                            150: "$150",
                            500: "$500",
                            1000: "$1000",
                            1500: "$1500",
                            2000: "$2000+",
                        },
                        tooltip={"placement": "top"},
                    ),
                ],
            ),
        ],
    )


def _initial_grid():
    """Renderiza todas las tarjetas; el callback filtrará vía display:none."""
    return html.Div(
        id="catalogo-grid",
        className="card-grid",
        children=[
            build_wine_card(v.to_dict()) for v in _kb.vinos
        ],
    )


layout = html.Div(
    className="page",
    children=[
        build_navbar("catalogo"),
        html.Section(
            className="page-intro",
            children=[
                html.Span("Base de conocimiento", className="eyebrow"),
                html.H1("Catálogo de vinos", className="page-title"),
                html.P(
                    "Explora los marcos (frames) que alimentan al motor de "
                    "inferencia. Cada vino está descrito por sus slots "
                    "técnicos y comerciales.",
                    className="page-subtitle",
                ),
            ],
        ),
        html.Main(
            className="catalog-container",
            children=[
                _filter_bar(),
                _initial_grid(),
                html.P(id="catalog-count", className="catalog-count"),
            ],
        ),
    ],
)


register_page(__name__, path="/catalogo", name="Catálogo", layout=layout)
