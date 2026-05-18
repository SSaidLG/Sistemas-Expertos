"""
Callback principal del cuestionario.
Recoge las respuestas pattern-matching, invoca el servicio de recomendación
y construye la sección de resultados con tarjetas y radar charts.
"""
from dash import Input, Output, State, ALL, callback, html, no_update

from models.knowledge_base import KnowledgeBase
from services.recommendation_service import RecommendationService
from views.components.wine_card import build_wine_card
from views.components.radar_chart import build_radar_chart


_service = RecommendationService()
_kb = KnowledgeBase()


def _empaquetar_respuestas(ids, values):
    """Convierte las listas pattern-matching en un dict {qid: valor}."""
    paquete = {}
    for id_obj, val in zip(ids, values):
        paquete[id_obj["qid"]] = val
    return paquete


def _construir_perfil(respuestas: dict):
    """Separa las respuestas en (perfil_platillo, contexto)."""
    perfil = {
        "picor": int(respuestas.get("picor", 3) or 3),
        "grasa": int(respuestas.get("grasa", 3) or 3),
        "dulce": int(respuestas.get("dulce", 1) or 1),
        "intensidad": int(respuestas.get("intensidad", 3) or 3),
        "proteina": int(respuestas.get("proteina", 1) or 1),
    }
    contexto = {
        "nombre_platillo": (respuestas.get("nombre_platillo") or "").strip(),
        "presupuesto": float(respuestas.get("presupuesto") or 500),
        "tipo_pref": (respuestas.get("tipo_pref") or "").strip(),
        "ocasion": respuestas.get("ocasion") or "casual",
        "clima": respuestas.get("clima") or "fresco",
    }
    return perfil, contexto


def _render_resultados(ranking, contexto):
    if not ranking:
        return html.Div(
            className="empty-state",
            children=[
                html.H3("Sin coincidencias", className="empty-title"),
                html.P(
                    "Ningún vino entra dentro de tus filtros de tipo y "
                    "presupuesto. Prueba a relajar alguno y vuelve a calcular.",
                    className="empty-text",
                ),
            ],
        )

    top = ranking[:3]
    perfil_ideal = top[0]["perfil_ideal"]

    cards = []
    for idx, item in enumerate(top, start=1):
        v = item["vino"]
        cards.append(
            html.Div(
                className="result-row",
                **{"data-aos": "fade-up"},
                children=[
                    html.Div(
                        className="result-card-col",
                        children=[build_wine_card(v, score=item["score"], ranking=idx)],
                    ),
                    html.Div(
                        className="result-chart-col",
                        children=[
                            html.H4("Perfil sensorial vs. ideal",
                                    className="result-section-title"),
                            build_radar_chart(v, perfil_ideal),
                            html.Div(
                                className="result-breakdown",
                                children=[
                                    html.Div(className="bd-item", children=[
                                        html.Span("Afinidad sensorial",
                                                  className="bd-label"),
                                        html.Span(f"{item['mu_sensorial']:.2f}",
                                                  className="bd-value"),
                                    ]),
                                    html.Div(className="bd-item", children=[
                                        html.Span("Ajuste de precio",
                                                  className="bd-label"),
                                        html.Span(f"{item['mu_precio']:.2f}",
                                                  className="bd-value"),
                                    ]),
                                    html.Div(className="bd-item", children=[
                                        html.Span("Bono maridaje",
                                                  className="bd-label"),
                                        html.Span(f"+{item['bono_maridaje']:.2f}",
                                                  className="bd-value"),
                                    ]),
                                    html.Div(className="bd-item", children=[
                                        html.Span("Bono ocasión",
                                                  className="bd-label"),
                                        html.Span(f"+{item['bono_ocasion']:.2f}",
                                                  className="bd-value"),
                                    ]),
                                    html.Div(className="bd-item", children=[
                                        html.Span("Bono clima",
                                                  className="bd-label"),
                                        html.Span(f"+{item['bono_clima']:.2f}",
                                                  className="bd-value"),
                                    ]),
                                ],
                            ),
                        ],
                    ),
                ],
            )
        )

    nombre = contexto["nombre_platillo"].title() or "tu platillo"
    return html.Section(
        className="resultados-section",
        children=[
            html.Div(
                className="resultados-head",
                children=[
                    html.Span("Resultado del motor difuso", className="eyebrow"),
                    html.H2(f"Top 3 maridajes para {nombre}",
                            className="section-title"),
                    html.P(
                        f"Evaluamos {len(_kb.vinos)} vinos contra tu perfil. "
                        f"De ellos, {len(ranking)} entraron en presupuesto y "
                        f"estilo. Estos son los más afines:",
                        className="section-sub",
                    ),
                ],
            ),
            html.Div(className="results-stack", children=cards),
        ],
    )


@callback(
    Output("resultados-container", "children"),
    Input("btn-calcular", "n_clicks"),
    State({"type": "ans", "qid": ALL}, "value"),
    State({"type": "ans", "qid": ALL}, "id"),
    prevent_initial_call=True,
)
def calcular_recomendaciones(n_clicks, values, ids):
    if not n_clicks:
        return no_update
    respuestas = _empaquetar_respuestas(ids, values)
    perfil, contexto = _construir_perfil(respuestas)
    ranking = _service.recomendar(perfil, contexto)
    return _render_resultados(ranking, contexto)
