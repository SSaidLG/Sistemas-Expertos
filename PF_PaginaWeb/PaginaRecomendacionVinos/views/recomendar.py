"""
Página del cuestionario interactivo.
Construye dinámicamente el formulario a partir de preguntas.json.
La lógica de cálculo vive en callbacks/questionnaire_callbacks.py.
"""
from dash import html, dcc, register_page

from models.knowledge_base import KnowledgeBase
from views.components.navbar import build_navbar


_kb = KnowledgeBase()


def _build_input(pregunta: dict):
    """Genera el componente de entrada adecuado para cada tipo de pregunta."""
    tipo = pregunta["tipo"]
    qid = pregunta["id"]

    if tipo == "texto":
        return dcc.Input(
            id={"type": "ans", "qid": qid},
            type="text",
            placeholder=pregunta.get("placeholder", ""),
            className="form-input",
            debounce=True,
        )
    if tipo == "numero":
        return dcc.Input(
            id={"type": "ans", "qid": qid},
            type="number",
            min=pregunta.get("min", 0),
            max=pregunta.get("max", 10000),
            step=pregunta.get("step", 1),
            value=pregunta.get("default", 500),
            className="form-input",
            debounce=True,
        )
    if tipo == "escala":
        return html.Div(
            className="scale-wrapper",
            children=[
                dcc.Slider(
                    id={"type": "ans", "qid": qid},
                    min=pregunta["min"],
                    max=pregunta["max"],
                    step=1,
                    value=pregunta.get("default", 3),
                    marks={i: str(i) for i in range(pregunta["min"], pregunta["max"] + 1)},
                    tooltip={"placement": "top", "always_visible": False},
                ),
            ],
        )
    if tipo == "opcion":
        return dcc.RadioItems(
            id={"type": "ans", "qid": qid},
            options=[{"label": o["label"], "value": o["value"]} for o in pregunta["opciones"]],
            value=pregunta["opciones"][0]["value"],
            className="radio-group",
            labelClassName="radio-item",
        )
    return html.Div()


def _build_question(idx: int, pregunta: dict):
    return html.Section(
        className="question-card",
        **{"data-step": idx + 1, "data-aos": "fade-up"},
        children=[
            html.Span(
                f"Pregunta {idx + 1} de {len(_kb.preguntas)}",
                className="question-number",
            ),
            html.H2(pregunta["titulo"], className="question-title"),
            html.P(pregunta.get("subtitulo", ""), className="question-sub"),
            html.Div(_build_input(pregunta), className="question-input"),
        ],
    )


def _build_form():
    return html.Div(
        className="form-stack",
        children=[_build_question(i, q) for i, q in enumerate(_kb.preguntas)],
    )


layout = html.Div(
    className="page page-form",
    children=[
        build_navbar("recomendar"),
        html.Section(
            className="page-intro",
            children=[
                html.Span("Cuestionario · 10 preguntas", className="eyebrow"),
                html.H1("Cuéntanos sobre tu platillo", className="page-title"),
                html.P(
                    "Cada pregunta alimenta una variable del motor difuso. "
                    "Tómate tu tiempo — entre más preciso, mejor el maridaje.",
                    className="page-subtitle",
                ),
            ],
        ),
        html.Main(
            className="form-container",
            children=[
                _build_form(),
                html.Div(
                    className="form-actions",
                    children=[
                        html.Button(
                            "Calcular maridaje difuso →",
                            id="btn-calcular",
                            className="btn btn-primary btn-large",
                            n_clicks=0,
                        ),
                    ],
                ),
                html.Div(id="resultados-container", className="resultados"),
            ],
        ),
    ],
)


register_page(__name__, path="/recomendar", name="Recomendar", layout=layout)
